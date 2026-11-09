#include "tangra_fc/command_arbitration.hpp"
#include <algorithm>
#include <cmath>
#include <stdexcept>
namespace tangra::fc {
namespace {
bool finite_setpoint(const ControlSetpoint&s){return std::isfinite(s.roll)&&std::isfinite(s.pitch)&&std::isfinite(s.yaw_rate)&&std::isfinite(s.collective);}
ControlSetpoint clamp_setpoint(ControlSetpoint s){auto clamp=[](float v){return std::max(-1.0f,std::min(1.0f,v));};s.roll=clamp(s.roll);s.pitch=clamp(s.pitch);s.yaw_rate=clamp(s.yaw_rate);s.collective=clamp(s.collective);return s;}
}
std::size_t CommandArbitrator::index(CommandSource s){switch(s){case CommandSource::SimulatedAutonomy:return 0;case CommandSource::PiSupervisor:return 1;case CommandSource::BenchTest:return 2;case CommandSource::SafetyOverride:return 3;default:throw std::invalid_argument("CommandSource::None has no slot");}}
int CommandArbitrator::priority(CommandSource s){switch(s){case CommandSource::SafetyOverride:return 400;case CommandSource::BenchTest:return 300;case CommandSource::PiSupervisor:return 200;case CommandSource::SimulatedAutonomy:return 100;case CommandSource::None:return 0;}return 0;}
bool CommandArbitrator::eligible(const SourceCommand&c,std::uint64_t now){if(!c.valid||c.source==CommandSource::None||!finite_setpoint(c.setpoint)||c.ttl_ms==0||now<c.timestamp_ms)return false;return(now-c.timestamp_ms)<=c.ttl_ms;}
ControlSetpoint CommandArbitrator::safe_setpoint(){return{};}
SubmitStatus CommandArbitrator::submit(const SourceCommand&c){if(c.source==CommandSource::None)return SubmitStatus::InvalidSource;auto&slot=slots_[index(c.source)];if(slot.source==c.source){if(c.sequence==slot.sequence)return SubmitStatus::DuplicateSequence;if(c.sequence<slot.sequence)return SubmitStatus::OutOfOrderSequence;}slot=c;return SubmitStatus::Accepted;}
ArbitrationDecision CommandArbitrator::select(std::uint64_t now)const{ArbitrationDecision d{};const SourceCommand*best=nullptr;for(const auto&c:slots_){if(c.source==CommandSource::None)continue;if(!eligible(c,now)){d.had_rejected_input=true;continue;}if(c.source==CommandSource::SafetyOverride&&c.force_safe){d.selected_source=CommandSource::SafetyOverride;d.reason=ArbitrationReason::SafetyOverride;d.safe_fallback=true;d.setpoint=safe_setpoint();return d;}if(!best||priority(c.source)>priority(best->source))best=&c;}if(!best){d.selected_source=CommandSource::None;d.reason=ArbitrationReason::NoEligibleSource;d.safe_fallback=true;d.setpoint=safe_setpoint();return d;}d.selected_source=best->source;d.reason=ArbitrationReason::Selected;d.safe_fallback=false;d.setpoint=clamp_setpoint(best->setpoint);return d;}
void CommandArbitrator::clear(CommandSource s){if(s!=CommandSource::None)slots_[index(s)]={};}
void CommandArbitrator::clear_all(){for(auto&slot:slots_)slot={};}
}
