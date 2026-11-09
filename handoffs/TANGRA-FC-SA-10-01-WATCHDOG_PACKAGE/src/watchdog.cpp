#include "tangra_fc/watchdog.hpp"
namespace tangra::fc {
void WatchdogSupervisor::initialize(std::uint64_t now,IWatchdogHardware&hw){last_ms_=now;reason_=hw.reset_reason();initialized_=true;if(reason_==ResetReason::Watchdog)recovery_=RecoveryState::SafeHold;}
void WatchdogSupervisor::heartbeat(std::uint64_t now,IWatchdogHardware&hw){if(!initialized_)initialize(now,hw);last_ms_=now;hw.feed();}
WatchdogStatus WatchdogSupervisor::evaluate(std::uint64_t now)const{WatchdogStatus s;s.last_heartbeat_ms=last_ms_;s.deadline_ms=deadline_ms_;s.reset_reason=reason_;s.recovery=recovery_;s.expired=!initialized_||now<last_ms_||(now-last_ms_)>deadline_ms_;if(s.expired&&s.recovery==RecoveryState::Normal)s.recovery=RecoveryState::SafeHold;return s;}
void WatchdogSupervisor::acknowledge_recovery(){if(recovery_==RecoveryState::SafeHold)recovery_=RecoveryState::Normal;}
}
