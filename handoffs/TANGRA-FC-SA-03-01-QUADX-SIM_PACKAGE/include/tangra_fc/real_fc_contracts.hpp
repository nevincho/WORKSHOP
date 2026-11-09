#pragma once
#include "tangra_fc/quadx_simulation.hpp"

namespace tangra::fc::integration {

class ITangraFcControllerContract {
public:
    virtual ~ITangraFcControllerContract() = default;
    virtual sim::AxisDemand controller_update(const sim::AttitudeState& estimate, double dt_s) = 0;
};
class ITangraFcVirtualQuadXMixerContract {
public:
    virtual ~ITangraFcVirtualQuadXMixerContract() = default;
    virtual sim::MotorMix mixer_mix(const sim::AxisDemand& demand) = 0;
};
class ITangraFcEstimatorContract {
public:
    virtual ~ITangraFcEstimatorContract() = default;
    virtual sim::AttitudeState estimator_update(const sim::SensorSample& sample, double dt_s) = 0;
};

class RealControllerAdapter final : public sim::IControllerAdapter {
public:
    explicit RealControllerAdapter(ITangraFcControllerContract& target) : target_(target) {}
    sim::AxisDemand update(const sim::AttitudeState& estimate, double dt_s) override {
        return target_.controller_update(estimate, dt_s);
    }
private:
    ITangraFcControllerContract& target_;
};

class RealVirtualQuadXMixerAdapter final : public sim::IMixerAdapter {
public:
    explicit RealVirtualQuadXMixerAdapter(ITangraFcVirtualQuadXMixerContract& target) : target_(target) {}
    sim::MotorMix mix(const sim::AxisDemand& demand) override {
        return target_.mixer_mix(demand);
    }
private:
    ITangraFcVirtualQuadXMixerContract& target_;
};

class RealEstimatorAdapter final : public sim::IEstimatorAdapter {
public:
    explicit RealEstimatorAdapter(ITangraFcEstimatorContract& target) : target_(target) {}
    sim::AttitudeState update(const sim::SensorSample& sample, double dt_s) override {
        return target_.estimator_update(sample, dt_s);
    }
private:
    ITangraFcEstimatorContract& target_;
};

} // namespace tangra::fc::integration
