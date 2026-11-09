#include "tangra_fc/mission_protocol.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
struct Sink:IMissionCommandSink{int n=0;bool accept_goal(const MissionGoalCommand&)override{++n;return true;}};
int main(){MavlinkMissionBinding b({42000,42001,42002});assert(b.configured());MissionGoalCommand c;c.sequence=1;c.timestamp_ms=100;c.ttl_ms=50;c.x=1;c.z=2;auto frame=b.encode_goal(c);assert(frame);auto decoded=b.decode_goal(*frame);assert(decoded&&decoded->sequence==1&&decoded->z==2);Sink s;MissionProtocolEndpoint e(s);auto a=e.receive(*decoded,120,MissionStateWire::READY);assert(a.status==ProtocolStatus::Accepted&&s.n==1);auto af=b.encode_ack(a);assert(af&&b.decode_ack(*af)->status==ProtocolStatus::Accepted);auto t=e.telemetry(MissionStateWire::ACTIVE,.5,MissionFault::None);auto tf=b.encode_telemetry(t);assert(tf&&b.decode_telemetry(*tf)->progress==.5);MavlinkMessage bad=*frame;bad.payload.pop_back();assert(!b.decode_goal(bad));std::cout<<"PASS: mission protocol MAVLink binding\n";}
