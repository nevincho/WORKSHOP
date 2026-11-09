#pragma once
#include <cstddef>
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
class MissionProtocolEndpoint{public:explicit MissionProtocolEndpoint(IMissionCommandSink&sink):sink_(sink){}MissionAck receive(const MissionGoalCommand&,std::uint64_t now_ms,MissionStateWire current_state);void on_disconnect();void on_reconnect();void resynchronize(std::uint64_t peer_last_sequence);MissionTelemetry telemetry(MissionStateWire state,double progress,MissionFault fault)const;private:IMissionCommandSink&sink_;std::uint64_t last_sequence_=0;bool has_sequence_=false;bool connected_=true;bool synchronized_=true;};

class MissionPayloadCodec{
public:
 static constexpr std::size_t kGoalPayloadLength=47;
 static constexpr std::size_t kAckPayloadLength=12;
 static constexpr std::size_t kTelemetryPayloadLength=22;
 static std::vector<std::uint8_t> encode_goal(const MissionGoalCommand&);
 static std::optional<MissionGoalCommand> decode_goal(const std::vector<std::uint8_t>&);
 static std::vector<std::uint8_t> encode_ack(const MissionAck&);
 static std::optional<MissionAck> decode_ack(const std::vector<std::uint8_t>&);
 static std::vector<std::uint8_t> encode_telemetry(const MissionTelemetry&);
 static std::optional<MissionTelemetry> decode_telemetry(const std::vector<std::uint8_t>&);
};

struct MavlinkMessageContract{std::uint32_t message_id=0;std::uint8_t payload_length=0;std::uint8_t crc_extra=0;};
struct MavlinkMissionDialectContract{MavlinkMessageContract goal{},ack{},telemetry{};bool valid()const;};
struct MavlinkPayloadEnvelope{std::uint32_t message_id=0;std::vector<std::uint8_t>payload;};
enum class MavlinkAdapterStatus:std::uint8_t{Ok,DialectUnavailable,UnknownMessageId,MalformedLength,InvalidPayload};
template<class T>struct MavlinkDecodeResult{MavlinkAdapterStatus status=MavlinkAdapterStatus::DialectUnavailable;std::optional<T>value;};

class MavlinkMissionPayloadAdapter{
public:
 explicit MavlinkMissionPayloadAdapter(MavlinkMissionDialectContract c):contract_(c){}
 bool configured()const{return contract_.valid();}
 std::optional<MavlinkPayloadEnvelope> encode_goal(const MissionGoalCommand&)const;
 MavlinkDecodeResult<MissionGoalCommand> decode_goal(const MavlinkPayloadEnvelope&)const;
 std::optional<MavlinkPayloadEnvelope> encode_ack(const MissionAck&)const;
 MavlinkDecodeResult<MissionAck> decode_ack(const MavlinkPayloadEnvelope&)const;
 std::optional<MavlinkPayloadEnvelope> encode_telemetry(const MissionTelemetry&)const;
 MavlinkDecodeResult<MissionTelemetry> decode_telemetry(const MavlinkPayloadEnvelope&)const;
 std::optional<std::uint8_t> crc_extra_for(std::uint32_t message_id)const;
private:MavlinkMissionDialectContract contract_;
};

class ITangraMavlinkTransportAdapter{
public:
 virtual~ITangraMavlinkTransportAdapter()=default;
 virtual bool send_payload(std::uint32_t message_id,const std::vector<std::uint8_t>&payload,std::uint8_t crc_extra)=0;
};
}
