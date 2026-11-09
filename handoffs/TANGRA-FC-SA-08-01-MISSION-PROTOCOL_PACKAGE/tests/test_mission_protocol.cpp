#include "tangra_fc/mission_protocol.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
struct Sink:IMissionCommandSink{int n=0;bool accept_goal(const MissionGoalCommand&)override{++n;return true;}};
int main(){
 MavlinkMissionDialectContract d{{42000,(std::uint8_t)MissionPayloadCodec::kGoalPayloadLength,17},{42001,(std::uint8_t)MissionPayloadCodec::kAckPayloadLength,91},{42002,(std::uint8_t)MissionPayloadCodec::kTelemetryPayloadLength,203}};
 MavlinkMissionPayloadAdapter a(d);assert(a.configured());MissionGoalCommand c;c.sequence=1;c.timestamp_ms=100;c.ttl_ms=50;c.x=1;c.z=2;
 auto env=a.encode_goal(c);assert(env&&env->payload.size()==MissionPayloadCodec::kGoalPayloadLength);auto goal=a.decode_goal(*env);assert(goal.status==MavlinkAdapterStatus::Ok&&goal.value&&goal.value->z==2);assert(a.crc_extra_for(42000).value()==17);
 auto truncated=*env;truncated.payload.pop_back();assert(a.decode_goal(truncated).status==MavlinkAdapterStatus::MalformedLength);
 auto extended=*env;extended.payload.push_back(0);assert(a.decode_goal(extended).status==MavlinkAdapterStatus::MalformedLength);
 auto unknown=*env;unknown.message_id=999;assert(a.decode_goal(unknown).status==MavlinkAdapterStatus::UnknownMessageId);
 Sink s;MissionProtocolEndpoint endpoint(s);auto ack=endpoint.receive(*goal.value,120,MissionStateWire::READY);assert(ack.status==ProtocolStatus::Accepted&&s.n==1);
 auto ack_env=a.encode_ack(ack);assert(ack_env);auto ack_round=a.decode_ack(*ack_env);assert(ack_round.status==MavlinkAdapterStatus::Ok&&ack_round.value->status==ProtocolStatus::Accepted);
 auto bad_enum=*ack_env;bad_enum.payload[8]=255;assert(a.decode_ack(bad_enum).status==MavlinkAdapterStatus::InvalidPayload);
 auto telem=endpoint.telemetry(MissionStateWire::ACTIVE,.5,MissionFault::None);auto telem_env=a.encode_telemetry(telem);assert(telem_env);auto telem_round=a.decode_telemetry(*telem_env);assert(telem_round.status==MavlinkAdapterStatus::Ok&&telem_round.value->progress==.5);
 auto telem_trunc=*telem_env;telem_trunc.payload.resize(5);assert(a.decode_telemetry(telem_trunc).status==MavlinkAdapterStatus::MalformedLength);
 MavlinkMissionPayloadAdapter unavailable({});assert(!unavailable.configured());assert(unavailable.decode_goal(*env).status==MavlinkAdapterStatus::DialectUnavailable);
 std::cout<<"PASS: payload codec + MAVLink dialect/transport boundary; TRANSPORT_ADAPTER_REQUIRED\n";
}
