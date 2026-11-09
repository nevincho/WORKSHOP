#include "tangra_fc/horizontal_guidance.hpp"
#include <algorithm>
#include <cmath>
namespace tangra::fc { namespace { double clamp(double v,double a,double b){return std::max(a,std::min(b,v));}}
GuidanceSetpoint HorizontalGuidance::update(const HorizontalState&s,const LocalObjective&o) const{
 GuidanceSetpoint g{}; if(!s.valid||!s.fresh||!o.valid) return g; if(!std::isfinite(s.x)||!std::isfinite(s.y)||!std::isfinite(s.vx)||!std::isfinite(s.vy)||!std::isfinite(o.x)||!std::isfinite(o.y)) return g;
 double vx=clamp(limits_.kp_position*(o.x-s.x),-limits_.max_speed_mps,limits_.max_speed_mps);
 double vy=clamp(limits_.kp_position*(o.y-s.y),-limits_.max_speed_mps,limits_.max_speed_mps);
 double pitch=clamp(limits_.kp_velocity*(vx-s.vx),-limits_.max_tilt_norm,limits_.max_tilt_norm);
 double roll=clamp(-limits_.kp_velocity*(vy-s.vy),-limits_.max_tilt_norm,limits_.max_tilt_norm);
 g.vx_mps=vx;g.vy_mps=vy;g.roll_norm=roll;g.pitch_norm=pitch;g.valid=true;g.safe_reject=false;return g;
}}
