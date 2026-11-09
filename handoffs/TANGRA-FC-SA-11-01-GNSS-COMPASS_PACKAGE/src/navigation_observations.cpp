#include "tangra_fc/navigation_observations.hpp"
#include <cmath>
namespace tangra::fc {
namespace {constexpr double kEarth=6378137.0;constexpr double kPi=3.14159265358979323846;double rad(double d){return d*kPi/180.0;}bool fresh(std::uint64_t ts,std::uint64_t now,std::uint64_t max){return now>=ts&&now-ts<=max;}}
bool NavigationObservationIntegrator::establish_origin(const GnssObservation&o){if(!o.valid||!std::isfinite(o.lat_deg)||!std::isfinite(o.lon_deg)||!std::isfinite(o.alt_m)||std::fabs(o.lat_deg)>90||std::fabs(o.lon_deg)>180)return false;origin_=o;return true;}
LocalNavUpdate NavigationObservationIntegrator::update(const GnssObservation*g,const HeadingObservation*h,std::uint64_t now)const{LocalNavUpdate u{};bool anyfresh=false;if(g&&origin_&&g->valid&&fresh(g->timestamp_ms,now,max_age_ms_)&&std::isfinite(g->lat_deg)&&std::isfinite(g->lon_deg)&&std::isfinite(g->alt_m)){double dlat=rad(g->lat_deg-origin_->lat_deg);double dlon=rad(g->lon_deg-origin_->lon_deg);double lat0=rad(origin_->lat_deg);u.x=kEarth*dlon*std::cos(lat0);u.y=kEarth*dlat;u.z=g->alt_m-origin_->alt_m;u.position_valid=true;anyfresh=true;}if(h&&h->valid&&fresh(h->timestamp_ms,now,max_age_ms_)&&std::isfinite(h->heading_rad)){u.heading_rad=h->heading_rad;u.heading_valid=true;anyfresh=true;}u.fresh=anyfresh;return u;}
}
