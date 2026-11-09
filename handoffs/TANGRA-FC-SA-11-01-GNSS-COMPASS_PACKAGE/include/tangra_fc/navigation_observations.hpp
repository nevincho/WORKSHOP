#pragma once
#include <cstdint>
#include <optional>
namespace tangra::fc {
struct GnssObservation{double lat_deg=0,lon_deg=0,alt_m=0;double horizontal_sigma_m=0,vertical_sigma_m=0;std::uint64_t timestamp_ms=0;bool valid=false;};
struct HeadingObservation{double heading_rad=0;double sigma_rad=0;std::uint64_t timestamp_ms=0;bool valid=false;};
struct LocalNavUpdate{double x=0,y=0,z=0;double heading_rad=0;bool position_valid=false;bool heading_valid=false;bool fresh=false;};
class NavigationObservationIntegrator{
public: explicit NavigationObservationIntegrator(std::uint64_t max_age_ms=1000):max_age_ms_(max_age_ms){}
 bool establish_origin(const GnssObservation&); LocalNavUpdate update(const GnssObservation*,const HeadingObservation*,std::uint64_t now_ms)const;
private:std::uint64_t max_age_ms_;std::optional<GnssObservation> origin_;
};
}
