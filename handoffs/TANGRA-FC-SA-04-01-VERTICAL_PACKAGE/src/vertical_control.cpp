#include "tangra_fc/vertical_control.hpp"
#include <algorithm>
#include <cmath>
namespace tangra::fc {
namespace { double clamp(double v,double lo,double hi){return std::max(lo,std::min(hi,v));} }
VerticalState VerticalStateProducer::update(const AltitudeSample& sample,std::uint64_t now_ms){
    VerticalState out{};out.timestamp_ms=sample.timestamp_ms;out.z_m=sample.altitude_m;
    if(!sample.valid||!std::isfinite(sample.altitude_m)||now_ms<sample.timestamp_ms)return out;
    out.fresh=(now_ms-sample.timestamp_ms)<=max_age_ms_;
    if(!out.fresh)return out;
    if(!initialized_){previous_=sample;initialized_=true;out.valid=true;out.velocity_valid=false;return out;}
    if(sample.timestamp_ms<=previous_.timestamp_ms)return out;
    const auto dt_ms=sample.timestamp_ms-previous_.timestamp_ms;
    if(dt_ms<min_dt_ms_||dt_ms>max_dt_ms_){previous_=sample;out.valid=true;out.velocity_valid=false;return out;}
    const double dt_s=static_cast<double>(dt_ms)/1000.0;
    const double vz=(sample.altitude_m-previous_.altitude_m)/dt_s;
    previous_=sample;
    if(!std::isfinite(vz))return VerticalState{};
    out.vz_mps=vz;out.valid=true;out.velocity_valid=true;return out;
}
void VerticalStateProducer::reset(){initialized_=false;previous_={};}
VerticalControlOutput VerticalController::update(const VerticalState&s,const AltitudeTarget&t)const{
    VerticalControlOutput o{};
    if(!s.valid||!s.fresh||!s.velocity_valid||!t.valid||!std::isfinite(s.z_m)||!std::isfinite(s.vz_mps)||!std::isfinite(t.altitude_m)||!std::isfinite(t.vertical_speed_mps))return o;
    double vz=t.vertical_speed_mps;if(t.use_altitude)vz+=limits_.kp_altitude*(t.altitude_m-s.z_m);
    vz=clamp(vz,-limits_.max_descent_mps,limits_.max_climb_mps);
    double delta=clamp(limits_.kp_velocity*(vz-s.vz_mps),-limits_.max_collective_delta,limits_.max_collective_delta);
    o.vertical_speed_target_mps=vz;o.collective_delta=delta;o.valid=true;o.safe_fallback=false;return o;
}
}
