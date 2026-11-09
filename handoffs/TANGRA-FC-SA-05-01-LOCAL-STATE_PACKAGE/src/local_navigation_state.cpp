#include "tangra_fc/local_navigation_state.hpp"
#include <cmath>
namespace tangra::fc {
namespace {constexpr double kEarthRadiusM=6378137.0;constexpr double kPi=3.14159265358979323846;double rad(double d){return d*kPi/180.0;}bool finite_geo(const GeodeticObservation&o){return std::isfinite(o.lat_deg)&&std::isfinite(o.lon_deg)&&std::isfinite(o.alt_m)&&std::fabs(o.lat_deg)<=90.0&&std::fabs(o.lon_deg)<=180.0;}}
bool LocalStateProducer::set_origin(const LocalOrigin&o){if(!o.valid||!std::isfinite(o.lat_deg)||!std::isfinite(o.lon_deg)||!std::isfinite(o.alt_m)||std::fabs(o.lat_deg)>90.0||std::fabs(o.lon_deg)>180.0)return false;origin_=o;have_previous_=false;return true;}
bool LocalStateProducer::establish_origin(const GeodeticObservation&o){if(!o.valid||!finite_geo(o))return false;origin_={o.lat_deg,o.lon_deg,o.alt_m,true,o.timestamp_ms};have_previous_=false;return true;}
bool LocalStateProducer::to_local(const GeodeticObservation&o,double&x,double&y,double&z)const{if(!origin_.valid||!finite_geo(o))return false;double dlat=rad(o.lat_deg-origin_.lat_deg),dlon=rad(o.lon_deg-origin_.lon_deg);x=kEarthRadiusM*dlon*std::cos(rad(origin_.lat_deg));y=kEarthRadiusM*dlat;z=o.alt_m-origin_.alt_m;return std::isfinite(x)&&std::isfinite(y)&&std::isfinite(z);}
LocalNavigationState LocalStateProducer::update(const GeodeticObservation&o,const StateUncertainty&u,std::uint64_t now){
 LocalNavigationState s{};s.origin=origin_;s.uncertainty=u;s.timestamp_ms=o.timestamp_ms;if(!o.valid||now<o.timestamp_ms||!origin_.valid)return s;s.fresh=(now-o.timestamp_ms)<=max_age_ms_;if(!s.fresh||!to_local(o,s.x,s.y,s.z))return s;
 if(!have_previous_){prev_x_=s.x;prev_y_=s.y;prev_z_=s.z;prev_timestamp_ms_=o.timestamp_ms;have_previous_=true;s.valid=true;s.velocity_valid=false;s.health=NavHealth::Degraded;return s;}
 if(o.timestamp_ms<=prev_timestamp_ms_)return s;auto dt_ms=o.timestamp_ms-prev_timestamp_ms_;double dx=s.x-prev_x_,dy=s.y-prev_y_,dz=s.z-prev_z_;double step=std::sqrt(dx*dx+dy*dy+dz*dz);if(!std::isfinite(step)||step>max_step_m_)return s;
 if(dt_ms<min_dt_ms_||dt_ms>max_dt_ms_){prev_x_=s.x;prev_y_=s.y;prev_z_=s.z;prev_timestamp_ms_=o.timestamp_ms;s.valid=true;s.velocity_valid=false;s.health=NavHealth::Degraded;return s;}
 double dt=static_cast<double>(dt_ms)/1000.0;s.vx=dx/dt;s.vy=dy/dt;s.vz=dz/dt;if(!std::isfinite(s.vx)||!std::isfinite(s.vy)||!std::isfinite(s.vz))return LocalNavigationState{};prev_x_=s.x;prev_y_=s.y;prev_z_=s.z;prev_timestamp_ms_=o.timestamp_ms;s.valid=true;s.velocity_valid=true;s.health=u.valid?NavHealth::Healthy:NavHealth::Degraded;return s;
}
void LocalStateProducer::reset(){origin_={};have_previous_=false;prev_x_=prev_y_=prev_z_=0;prev_timestamp_ms_=0;}
LocalNavigationState LocalStateValidator::evaluate(LocalNavigationState s,std::uint64_t now)const{bool finite=std::isfinite(s.x)&&std::isfinite(s.y)&&std::isfinite(s.z)&&std::isfinite(s.vx)&&std::isfinite(s.vy)&&std::isfinite(s.vz);s.fresh=now>=s.timestamp_ms&&(now-s.timestamp_ms)<=max_age_ms_;s.valid=s.valid&&finite&&s.origin.valid;if(!s.valid)s.health=NavHealth::Invalid;else if(!s.fresh||!s.uncertainty.valid||!s.velocity_valid)s.health=NavHealth::Degraded;else s.health=NavHealth::Healthy;return s;}
}
