#include "tangra_fc/real_fc_contracts.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc::sim;
using namespace tangra::fc::integration;

struct ControllerContract final : ITangraFcControllerContract {
    int calls=0;
    AxisDemand controller_update(const AttitudeState& s,double dt) override { ++calls; return {s.roll+dt,s.pitch,0,0.5}; }
};
struct MixerContract final : ITangraFcVirtualQuadXMixerContract {
    int calls=0;
    MotorMix mixer_mix(const AxisDemand& d) override { ++calls; MotorMix m; m.motor={d.collective,d.collective,d.collective,d.collective}; return m; }
};
struct EstimatorContract final : ITangraFcEstimatorContract {
    int calls=0;
    AttitudeState estimator_update(const SensorSample& s,double) override { ++calls; return s.attitude; }
};
int main(){
    ControllerContract c; MixerContract m; EstimatorContract e;
    RealControllerAdapter ca(c); RealVirtualQuadXMixerAdapter ma(m); RealEstimatorAdapter ea(e);
    AttitudeState a{}; a.roll=.2; auto d=ca.update(a,.01);
    assert(c.calls==1&&d.roll>.2);
    auto motors=ma.mix(d); assert(m.calls==1&&motors.motor[0]==.5);
    SensorSample s{}; s.attitude.roll=.3; auto est=ea.update(s,.01);
    assert(e.calls==1&&est.roll==.3);
    std::cout<<"ADAPTER_CONTRACT_PASS\nREAL_FC_INTEGRATION_NOT_TESTED\n";
}
