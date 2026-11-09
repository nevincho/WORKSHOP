#pragma once
#include <cstdint>
namespace tangra::fc {
enum class NavHealth:std::uint8_t{Invalid,Degraded,Healthy};
struct LocalOrigin{double lat_deg=0,lon_deg=0,alt_m=0;bool valid=false;std::uint64_t established_ms=0;};
struct StateUncertainty{double position_sigma_m=0;double velocity_sigma_mps=0;bool valid=false;};
struct GeodeticObservation{double lat_deg=0,lon_deg=0,alt_m=0;std::uint64_t timestamp_ms=0;bool valid=false;};
struct LocalNavigationState{double x=0,y=0,z=0,vx=0,vy=0,vz=0;std::uint64_t timestamp_ms=0;bool valid=false;bool fresh=false;bool velocity_valid=false;LocalOrigin origin{};StateUncertainty uncertainty{};NavHealth health=NavHealth::Invalid;};
class LocalStateProducer{
public:
 LocalStateProducer(std::uint64_t max_age_ms=250,std::uint64_t min_dt_ms=1,std::uint64_t max_dt_ms=2000,double max_step_m=100.0):max_age_ms_(max_age_ms),min_dt_ms_(min_dt_ms),max_dt_ms_(max_dt_ms),max_step_m_(max_step_m){}
 bool set_origin(const LocalOrigin&);bool establish_origin(const GeodeticObservation&);
 LocalNavigationState update(const GeodeticObservation&,const StateUncertainty&,std::uint64_t now_ms);
 void reset();const LocalOrigin& origin()const{return origin_;}
private:
 bool to_local(const GeodeticObservation&,double&x,double&y,double&z)const;
 std::uint64_t max_age_ms_,min_dt_ms_,max_dt_ms_;double max_step_m_;LocalOrigin origin_{};bool have_previous_=false;double prev_x_=0,prev_y_=0,prev_z_=0;std::uint64_t prev_timestamp_ms_=0;
};
class LocalStateValidator{public:explicit LocalStateValidator(std::uint64_t max_age_ms=250):max_age_ms_(max_age_ms){}LocalNavigationState evaluate(LocalNavigationState s,std::uint64_t now_ms)const;private:std::uint64_t max_age_ms_;};
}
