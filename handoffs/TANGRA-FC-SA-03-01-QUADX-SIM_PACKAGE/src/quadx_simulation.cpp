#include "tangra_fc/quadx_simulation.hpp"
#include <algorithm>
#include <cmath>

namespace tangra::fc::sim {
namespace {
double clamp01(double v){ return std::max(0.0,std::min(1.0,v)); }
}

void QuadXPlant::step(const MotorMix& motors, double dt, const Disturbance& d) {
    std::array<double,4> m{}; for(size_t i=0;i<4;i++) m[i]=clamp01(motors.motor[i]);
    const double roll_t = (m[1]+m[2]-m[0]-m[3])*2.0 + d.roll_torque;
    const double pitch_t = (m[2]+m[3]-m[0]-m[1])*2.0 + d.pitch_torque;
    const double yaw_t = (m[0]+m[2]-m[1]-m[3])*1.0 + d.yaw_torque;
    const double damp=0.8;
    state_.attitude.p += (roll_t - damp*state_.attitude.p)*dt;
    state_.attitude.q += (pitch_t - damp*state_.attitude.q)*dt;
    state_.attitude.r += (yaw_t - damp*state_.attitude.r)*dt;
    state_.attitude.roll += state_.attitude.p*dt;
    state_.attitude.pitch += state_.attitude.q*dt;
    state_.attitude.yaw += state_.attitude.r*dt;
    const double collective=(m[0]+m[1]+m[2]+m[3])/4.0;
    const double az=(collective-0.5)*4.0 + d.vertical_force - 0.2*state_.vz;
    state_.vz += az*dt; state_.z += state_.vz*dt;
}

SensorSample QuadXPlant::sense(std::uint64_t ts, const FaultInjection& f) {
    if (f.freeze_sensor) return last_sample_;
    SensorSample s{}; s.timestamp_us=ts; s.attitude=state_.attitude; s.valid=!f.sensor_invalid; last_sample_=s; return s;
}

ClosedLoopHarness::ClosedLoopHarness(IControllerAdapter& c, IMixerAdapter& m, IEstimatorAdapter& e, VehicleState initial)
: controller_(c),mixer_(m),estimator_(e),plant_(initial),estimate_(initial.attitude) {}

ClosedLoopResult ClosedLoopHarness::run_steps(std::size_t steps, std::uint64_t dt_us, const Disturbance& d, const FaultInjection& f) {
    const double dt=static_cast<double>(dt_us)/1e6;
    for(std::size_t i=0;i<steps;i++){
        auto demand=controller_.update(estimate_,dt);
        auto motors=mixer_.mix(demand);
        plant_.step(motors,dt,d);
        clock_.advance(dt_us);
        auto sample=plant_.sense(clock_.now_us(),f);
        estimate_=estimator_.update(sample,dt);
    }
    const auto& t=plant_.truth().attitude;
    const double dr=t.roll-estimate_.roll, dp=t.pitch-estimate_.pitch, dy=t.yaw-estimate_.yaw;
    return {plant_.truth(),estimate_,std::sqrt(dr*dr+dp*dp+dy*dy)};
}
}
