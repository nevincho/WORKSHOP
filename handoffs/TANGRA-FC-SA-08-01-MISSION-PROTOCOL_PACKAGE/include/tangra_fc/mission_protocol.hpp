#pragma once
#include <cstdint>
#include <optional>
#include <vector>
namespace tangra::fc {
static constexpr std::uint16_t kMissionProtocolVersion=1;
enum class ProtocolStatus:std::uint8_t{Accepted,Rejected,Stale,OutOfOrder,VersionMismatch,NotSynchronized};
enum class MissionStateWire:std::uint8_t{INIT,READY,ACTIVE,HOLD,ABORT,COMPLETE,FAULT};
enum class MissionFault:std::uint16_t{None=0,InvalidGoal=1,Timeout=2,LinkLoss=3,Protocol=4,NotReady=5};
struct MissionGoalCommand{std::uint16_t protocol_version=kMissionProtocolVersion;std::uint64_t sequence=0;std::uint64_t timestamp_ms=0;std::uint32_t ttl_ms=0;double x=0,y=0,z=0;bool valid=true;};
struct MissionAck{std::uint64_t sequence=0;ProtocolStatus status=ProtocolStatus::Rejected;MissionStateWire mission_state=MissionStateWire::INIT;MissionFault fault=MissionFault::None;};
struct MissionTelemetry{std::uint16_t capability_version=kMissionProtocolVersion;std::uint64_t last_accepted_sequence=0;MissionStateWire mission_state=MissionStateWire::INIT;double progress=0;MissionFault fault=MissionFault::None;bool synchronized=false;};
class IMissionCommandSink{public:virtual~IMissionCommandSink()=default;virtual bool accept_goal(const MissionGoalCommand&)=0;};
class MissionProtocolEndpoint{
public:
 explicit MissionProtocolEndpoint(IMissionCommandSink&sink):sink_(sink){}
 MissionAck receive(const MissionGoalCommand&,std::uint64_t now_ms,MissionStateWire current_state);
 void on_disconnect();void on_reconnect();void resynchronize(std::uint64_t peer_last_sequence);
 MissionTelemetry telemetry(MissionStateWire state,double progress,MissionFault fault)const;
private:IMissionCommandSink&sink_;std::uint64_t last_sequence_=0;bool has_sequence_=false;bool connected_=true;bool synchronized_=true;
};
struct MavlinkMessage { std::uint32_t message_id=0; std::vector<std::uint8_t> payload; };
struct MavlinkMissionIds {
    std::uint32_t goal_message_id=0; std::uint32_t ack_message_id=0; std::uint32_t telemetry_message_id=0;
    bool valid() const {return goal_message_id!=0&&ack_message_id!=0&&telemetry_message_id!=0&&goal_message_id!=ack_message_id&&goal_message_id!=telemetry_message_id&&ack_message_id!=telemetry_message_id;}
};
class MavlinkMissionBinding {
public:
 explicit MavlinkMissionBinding(MavlinkMissionIds ids):ids_(ids){}
 bool configured() const { return ids_.valid(); }
 std::optional<MavlinkMessage> encode_goal(const MissionGoalCommand&) const;
 std::optional<MissionGoalCommand> decode_goal(const MavlinkMessage&) const;
 std::optional<MavlinkMessage> encode_ack(const MissionAck&) const;
 std::optional<MissionAck> decode_ack(const MavlinkMessage&) const;
 std::optional<MavlinkMessage> encode_telemetry(const MissionTelemetry&) const;
 std::optional<MissionTelemetry> decode_telemetry(const MavlinkMessage&) const;
private:MavlinkMissionIds ids_;
};
}
