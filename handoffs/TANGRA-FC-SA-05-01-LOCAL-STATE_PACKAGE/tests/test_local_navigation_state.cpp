#include "tangra_fc/local_navigation_state.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
using namespace tangra::fc;
int main(){
 LocalStateProducer p(100,1,1000,50.0);StateUncertainty u{.5,.2,true};GeodeticObservation o0{51.0,-1.0,100.0,1000,true};assert(p.establish_origin(o0));
 auto s0=p.update(o0,u,1000);assert(s0.valid&&s0.fresh&&!s0.velocity_valid&&std::fabs(s0.x)<1e-9);
 GeodeticObservation o1{51.00001,-0.99999,101.0,2000,true};auto s1=p.update(o1,u,2000);assert(s1.valid&&s1.velocity_valid&&s1.health==NavHealth::Healthy&&s1.x>0&&s1.y>0&&s1.z==1.0&&std::fabs(s1.vz-1.0)<1e-12);
 auto stale=p.update({51.00002,-0.99998,102.0,2100,true},u,2301);assert(!stale.valid&&!stale.fresh);
 auto duplicate=p.update({51.00001,-0.99999,101.2,2000,true},u,2000);assert(!duplicate.valid);
 auto jump=p.update({52.0,0.0,101.0,2500,true},u,2500);assert(!jump.valid);
 LocalStateProducer invalid_origin;auto no_origin=invalid_origin.update(o1,u,2000);assert(!no_origin.valid&&no_origin.health==NavHealth::Invalid);LocalOrigin bad{};bad.valid=true;bad.lat_deg=999.0;assert(!invalid_origin.set_origin(bad));
 p.reset();assert(!p.origin().valid);auto after_reset=p.update(o1,u,2000);assert(!after_reset.valid);
 std::cout<<"PASS: stateful local-frame/velocity producer\n";
}
