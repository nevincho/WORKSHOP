#pragma once
#include <cstdint>
namespace tangra::fc {
enum class ResetReason:std::uint8_t{Unknown,PowerOn,Software,Watchdog,Brownout,External};
enum class RecoveryState:std::uint8_t{Normal,SafeHold,FaultLatched};
struct WatchdogStatus{std::uint64_t last_heartbeat_ms=0;std::uint32_t deadline_ms=0;bool expired=false;ResetReason reset_reason=ResetReason::Unknown;RecoveryState recovery=RecoveryState::Normal;};
class IWatchdogHardware{public:virtual ~IWatchdogHardware()=default;virtual void feed()=0;virtual ResetReason reset_reason()const=0;};
class WatchdogSupervisor{
public: explicit WatchdogSupervisor(std::uint32_t deadline_ms):deadline_ms_(deadline_ms){}
 void initialize(std::uint64_t now_ms,IWatchdogHardware& hw); void heartbeat(std::uint64_t now_ms,IWatchdogHardware& hw); WatchdogStatus evaluate(std::uint64_t now_ms)const; void acknowledge_recovery();
private:std::uint32_t deadline_ms_;std::uint64_t last_ms_=0;ResetReason reason_=ResetReason::Unknown;RecoveryState recovery_=RecoveryState::Normal;bool initialized_=false;};
}
