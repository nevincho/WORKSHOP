#include "tangra_fc/waypoint_executor.hpp"
#include <cmath>
namespace tangra::fc {

bool WaypointExecutor::load(std::vector<Waypoint> goals){
    for(const auto& g:goals){ if(!g.valid||g.acceptance_radius_m<=0||g.timeout_ms==0) { reason_=MissionReason::INVALID_GOAL; return false; } }
    goals_=std::move(goals); index_=0; reason_=MissionReason::NONE; return !goals_.empty();
}

void WaypointExecutor::start(std::uint64_t now){
    if(goals_.empty()){reason_=MissionReason::INVALID_GOAL; lifecycle_.request(MissionLifecycleState::ABORT,reason_); return;}
    if(lifecycle_.request(MissionLifecycleState::ACTIVE,MissionReason::NONE)){goal_start_ms_=now;}
}

ExecutorStatus WaypointExecutor::update(const ExecutorObservation& o){
    if(lifecycle_.state()!=MissionLifecycleState::ACTIVE) return status();
    if(index_>=goals_.size()){ lifecycle_.request(MissionLifecycleState::COMPLETE,MissionReason::SEQUENCE_COMPLETE); reason_=MissionReason::SEQUENCE_COMPLETE; return status(); }
    if(!o.valid||!o.fresh) return status();
    const auto& g=goals_[index_];
    if(o.now_ms<goal_start_ms_ || o.now_ms-goal_start_ms_>g.timeout_ms){ reason_=MissionReason::TIMEOUT; lifecycle_.request(MissionLifecycleState::ABORT,reason_); return status(); }
    const double dx=g.x-o.x,dy=g.y-o.y,dz=g.z-o.z; const double dist=std::sqrt(dx*dx+dy*dy+dz*dz);
    if(dist<=g.acceptance_radius_m){ reason_=MissionReason::ARRIVED; ++index_; if(index_>=goals_.size()){reason_=MissionReason::SEQUENCE_COMPLETE;lifecycle_.request(MissionLifecycleState::COMPLETE,reason_);} else goal_start_ms_=o.now_ms; }
    return status();
}
void WaypointExecutor::hold(){reason_=MissionReason::HOLD_REQUESTED;lifecycle_.request(MissionLifecycleState::HOLD,reason_);}
void WaypointExecutor::abort(){reason_=MissionReason::ABORT_REQUESTED;lifecycle_.request(MissionLifecycleState::ABORT,reason_);}
ExecutorStatus WaypointExecutor::status() const{ ExecutorStatus s; s.active_index=index_;s.count=goals_.size();s.progress=goals_.empty()?0.0:static_cast<double>(index_)/goals_.size();s.reason=reason_;s.has_active_goal=index_<goals_.size();return s; }
}
