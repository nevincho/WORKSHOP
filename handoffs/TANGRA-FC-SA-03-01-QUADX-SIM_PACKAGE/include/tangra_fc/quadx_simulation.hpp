#pragma once
#include <array>
#include <cstdint>

namespace tangra::fc::sim {

struct AttitudeState { double roll=0, pitch=0, yaw=0; double p=0, q=0, r=0; };
struct VehicleState { double x=0,y=0,z=0; double vx=0,vy=0,vz=0; AttitudeState attitude{}; };
struct SensorSample { std::uint64_t timestamp_us=0; AttitudeState attitude{}; bool valid=true; };
struct AxisDemand { double roll=0,pitch=0,yaw=0,collective=0; };
struct MotorMix { std::array<double,4> motor{0,0,0,0}; };

class IControllerAdapter { public: virtual ~IControllerAdapter()=default; virtual AxisDemand update(const AttitudeState&, double dt_s)=0; };
class IMixerAdapter { public: virtual ~IMixerAdapter()=default; virtual MotorMix mix(const AxisDemand&)=0; };
class IEstimatorAdapter { public: virtual ~IEstimatorAdapter()=default; virtual AttitudeState update(const SensorSample&, double dt_s)=0; };

struct Disturbance { double roll_torque=0,pitch_torque=0,yaw_torque=0,vertical_force=0; };
struct FaultInjection { bool sensor_invalid=false; bool freeze_sensor=false; };

class DeterministicClock {
public:
    explicit DeterministicClock(std::uint64_t start_us=0): now_us_(start_us) {}
    std::uint64_t now_us() const { return now_us_; }
    void advance(std::uint64_t dt_us) { now_us_ += dt_us; }
private: std::uint64_t now_us_;
};

class QuadXPlant {
public:
    explicit QuadXPlant(VehicleState initial = {}): state_(initial) {}
    void step(const MotorMix& motors, double dt_s, const Disturbance& d = {});
    const VehicleState& truth() const { return state_; }
    SensorSample sense(std::uint64_t timestamp_us, const FaultInjection& fault = {});
private:
    VehicleState state_{};
    SensorSample last_sample_{};
};

struct ClosedLoopResult { VehicleState truth{}; AttitudeState estimate{}; double attitude_error_norm=0; };

class ClosedLoopHarness {
public:
    ClosedLoopHarness(IControllerAdapter& c, IMixerAdapter& m, IEstimatorAdapter& e, VehicleState initial={});
    ClosedLoopResult run_steps(std::size_t steps, std::uint64_t dt_us, const Disturbance& disturbance={}, const FaultInjection& fault={});
private:
    IControllerAdapter& controller_; IMixerAdapter& mixer_; IEstimatorAdapter& estimator_;
    DeterministicClock clock_{}; QuadXPlant plant_; AttitudeState estimate_{};
};

} // namespace tangra::fc::sim
