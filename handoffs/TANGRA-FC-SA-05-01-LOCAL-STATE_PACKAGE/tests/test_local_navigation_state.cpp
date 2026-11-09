#include "tangra_fc/local_navigation_state.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
int main(){ LocalNavigationState s; s.valid=true;s.timestamp_ms=100;s.origin.valid=true;s.uncertainty.valid=true;s.uncertainty.position_sigma_m=0.5;s.uncertainty.velocity_sigma_mps=0.2; LocalStateValidator v(50); auto a=v.evaluate(s,120); assert(a.valid&&a.fresh&&a.health==NavHealth::Healthy); auto b=v.evaluate(s,200); assert(b.valid&&!b.fresh&&b.health==NavHealth::Degraded); s.origin.valid=false; auto c=v.evaluate(s,120); assert(!c.valid&&c.health==NavHealth::Invalid); std::cout<<"PASS: local navigation state\n";}
