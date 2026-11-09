#include "tangra_fc/navigation_observations.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
using namespace tangra::fc;
int main(){NavigationObservationIntegrator n(100);GnssObservation o{51.0,-1.0,100,1,2,100,true};assert(n.establish_origin(o));GnssObservation g=o;g.lat_deg+=0.0001;g.lon_deg+=0.0001;g.alt_m=105;g.timestamp_ms=120;HeadingObservation h{1.2,0.1,120,true};auto u=n.update(&g,&h,150);assert(u.position_valid&&u.heading_valid&&u.fresh);assert(std::fabs(u.z-5)<1e-9);assert(std::fabs(u.x)>1&&std::fabs(u.y)>1);auto stale=n.update(&g,&h,500);assert(!stale.position_valid&&!stale.heading_valid&&!stale.fresh);std::cout<<"PASS: GNSS/heading observation integration\n";}
