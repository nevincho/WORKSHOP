#pragma once
#include <cstdint>
namespace tangra::fc {
struct HorizontalState { double x=0,y=0,vx=0,vy=0; bool valid=false; bool fresh=false; };
struct LocalObjective { double x=0,y=0; bool valid=false; };
struct GuidanceLimits { double max_speed_mps=5.0; double max_tilt_norm=0.5; double kp_position=0.8; double kp_velocity=0.25; };
struct GuidanceSetpoint { double vx_mps=0,vy_mps=0,roll_norm=0,pitch_norm=0; bool valid=false; bool safe_reject=true; };
class HorizontalGuidance { public: explicit HorizontalGuidance(GuidanceLimits l={}):limits_(l){} GuidanceSetpoint update(const HorizontalState&,const LocalObjective&) const; private:GuidanceLimits limits_;};
}
