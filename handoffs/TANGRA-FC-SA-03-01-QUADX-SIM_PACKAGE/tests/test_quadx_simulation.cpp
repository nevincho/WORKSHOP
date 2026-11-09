#include "tangra_fc/quadx_simulation.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
using namespace tangra::fc::sim;

struct HoldController final: IControllerAdapter { AxisDemand update(const AttitudeState& s,double) override { return {-0.4*s.roll,-0.4*s.pitch,-0.2*s.yaw,0.5}; } };
struct QuadMixer final: IMixerAdapter { MotorMix mix(const AxisDemand& d) override { MotorMix m; double c=d.collective; m.motor={c-d.roll-d.pitch+d.yaw,c+d.roll-d.pitch-d.yaw,c+d.roll+d.pitch+d.yaw,c-d.roll+d.pitch-d.yaw}; return m; } };
struct PerfectEstimator final: IEstimatorAdapter { AttitudeState last{}; AttitudeState update(const SensorSample& s,double) override { if(s.valid) last=s.attitude; return last; } };

int main(){
 HoldController c1,c2; QuadMixer m1,m2; PerfectEstimator e1,e2;
 VehicleState init; init.attitude.roll=0.2; init.attitude.pitch=-0.15;
 ClosedLoopHarness h1(c1,m1,e1,init), h2(c2,m2,e2,init);
 auto r1=h1.run_steps(500,4000); auto r2=h2.run_steps(500,4000);
 assert(std::fabs(r1.truth.attitude.roll-r2.truth.attitude.roll)<1e-12);
 assert(std::fabs(r1.truth.attitude.pitch-r2.truth.attitude.pitch)<1e-12);
 assert(r1.attitude_error_norm<1e-12);
 assert(std::fabs(r1.truth.attitude.roll)<0.2);
 Disturbance d; d.roll_torque=0.05;
 HoldController c3; QuadMixer m3; PerfectEstimator e3; ClosedLoopHarness h3(c3,m3,e3,{});
 auto disturbed=h3.run_steps(250,4000,d);
 assert(std::isfinite(disturbed.truth.attitude.roll));
 FaultInjection f; f.sensor_invalid=true;
 HoldController c4; QuadMixer m4; PerfectEstimator e4; ClosedLoopHarness h4(c4,m4,e4,{});
 auto faulted=h4.run_steps(10,4000,{},f);
 assert(std::isfinite(faulted.truth.z));
 std::cout<<"PASS: deterministic closed-loop Quad-X plant\n";
}
