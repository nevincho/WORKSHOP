#include "tangra_fc/real_fc_contracts.hpp"
#include "tangra_fc/mission_protocol.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;using namespace tangra::fc::sim;using namespace tangra::fc::integration;
struct ControllerContract final:ITangraFcControllerContract{AxisDemand controller_update(const AttitudeState&s,double dt)override{return{s.roll+dt,0,0,.5};}};
struct MixerContract final:ITangraFcVirtualQuadXMixerContract{MotorMix mixer_mix(const AxisDemand&d)override{MotorMix m;m.motor={d.collective,d.collective,d.collective,d.collective};return m;}};
struct EstimatorContract final:ITangraFcEstimatorContract{AttitudeState estimator_update(const SensorSample&s,double)override{return s.attitude;}};
struct TransportContract final:ITangraMavlinkTransportAdapter{bool called=false;std::uint32_t id=0;std::uint8_t crc=0;bool send_payload(std::uint32_t i,const std::vector<std::uint8_t>&,std::uint8_t c)override{called=true;id=i;crc=c;return true;}};
int main(){ControllerContract c;MixerContract m;EstimatorContract e;RealControllerAdapter ca(c);RealVirtualQuadXMixerAdapter ma(m);RealEstimatorAdapter ea(e);AttitudeState a{};a.roll=.1;auto d=ca.update(a,.01);auto motors=ma.mix(d);SensorSample s{};s.attitude.roll=.2;auto est=ea.update(s,.01);assert(d.roll>.1&&motors.motor[0]==.5&&est.roll==.2);MavlinkMissionDialectContract fixture{{42000,(std::uint8_t)MissionPayloadCodec::kGoalPayloadLength,17},{42001,(std::uint8_t)MissionPayloadCodec::kAckPayloadLength,91},{42002,(std::uint8_t)MissionPayloadCodec::kTelemetryPayloadLength,203}};MavlinkMissionPayloadAdapter adapter(fixture);MissionGoalCommand g;g.ttl_ms=100;auto env=adapter.encode_goal(g);assert(env&&adapter.crc_extra_for(env->message_id).value()==17);TransportContract t;assert(t.send_payload(env->message_id,env->payload,*adapter.crc_extra_for(env->message_id)));assert(t.called&&t.id==42000&&t.crc==17);std::cout<<"ADAPTER_CONTRACT_PASS\nREAL_FC_INTEGRATION_NOT_TESTED\nTRANSPORT_ADAPTER_REQUIRED\n";}
