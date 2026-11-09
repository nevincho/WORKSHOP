#include "tangra_fc/mission_protocol.hpp"
#include <algorithm>
#include <cmath>
namespace tangra::fc {
MissionAck MissionProtocolEndpoint::receive(const MissionGoalCommand& c,std::uint64_t now,MissionStateWire state){
 MissionAck a{};a.sequence=c.sequence;a.mission_state=state;
 if(c.protocol_version!=kMissionProtocolVersion){a.status=ProtocolStatus::VersionMismatch;a.fault=MissionFault::Protocol;return a;}
 if(!connected_||!synchronized_){a.status=ProtocolStatus::NotSynchronized;a.fault=MissionFault::LinkLoss;return a;}
 if(!c.valid||c.ttl_ms==0||!std::isfinite(c.x)||!std::isfinite(c.y)||!std::isfinite(c.z)){a.status=ProtocolStatus::Rejected;a.fault=MissionFault::InvalidGoal;return a;}
 if(now<c.timestamp_ms||now-c.timestamp_ms>c.ttl_ms){a.status=ProtocolStatus::Stale;return a;}
 if(has_sequence_&&c.sequence<=last_sequence_){a.status=ProtocolStatus::OutOfOrder;return a;}
 if(!sink_.accept_goal(c)){a.status=ProtocolStatus::Rejected;a.fault=MissionFault::NotReady;return a;}
 last_sequence_=c.sequence;has_sequence_=true;a.status=ProtocolStatus::Accepted;return a;
}
void MissionProtocolEndpoint::on_disconnect(){connected_=false;synchronized_=false;}
void MissionProtocolEndpoint::on_reconnect(){connected_=true;synchronized_=false;}
void MissionProtocolEndpoint::resynchronize(std::uint64_t peer_last){ if(connected_){ if(!has_sequence_||peer_last>=last_sequence_) {last_sequence_=peer_last;has_sequence_=true;} synchronized_=true; } }
MissionTelemetry MissionProtocolEndpoint::telemetry(MissionStateWire s,double p,MissionFault f) const{MissionTelemetry t;t.last_accepted_sequence=last_sequence_;t.mission_state=s;t.progress=std::max(0.0,std::min(1.0,p));t.fault=f;t.synchronized=synchronized_&&connected_;return t;}
}
