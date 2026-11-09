#pragma once
#include <cstdint>
namespace tangra::fc {
enum class NavHealth:std::uint8_t{Invalid,Degraded,Healthy};
struct LocalOrigin { double lat_deg=0,lon_deg=0,alt_m=0; bool valid=false; std::uint64_t established_ms=0; };
struct StateUncertainty { double position_sigma_m=0; double velocity_sigma_mps=0; bool valid=false; };
struct LocalKinematicObservation { double x=0,y=0,z=0,vx=0,vy=0,vz=0; std::uint64_t timestamp_ms=0; bool valid=false; };
struct LocalNavigationState { double x=0,y=0,z=0,vx=0,vy=0,vz=0; std::uint64_t timestamp_ms=0; bool valid=false; bool fresh=false; LocalOrigin origin{}; StateUncertainty uncertainty{}; NavHealth health=NavHealth::Invalid; };
class LocalStateProducer{
public: explicit LocalStateProducer(std::uint64_t max_age_ms=250):max_age_ms_(max_age_ms){}
 LocalNavigationState produce(const LocalKinematicObservation&,const LocalOrigin&,const StateUncertainty&,std::uint64_t now_ms)const;
private:std::uint64_t max_age_ms_;
};
class LocalStateValidator { public: explicit LocalStateValidator(std::uint64_t max_age_ms=250):max_age_ms_(max_age_ms){} LocalNavigationState evaluate(LocalNavigationState s,std::uint64_t now_ms) const; private:std::uint64_t max_age_ms_;};
}
