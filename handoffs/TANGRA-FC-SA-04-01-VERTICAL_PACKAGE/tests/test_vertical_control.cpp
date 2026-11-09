#include "tangra_fc/vertical_control.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
using namespace tangra::fc;
int main(){ VerticalController c; VerticalState s{10,0,100,true,true}; AltitudeTarget t{12,0,true,true}; auto o=c.update(s,t); assert(o.valid&&!o.safe_fallback); assert(o.vertical_speed_target_mps>0&&o.vertical_speed_target_mps<=2.0); assert(o.collective_delta>0&&o.collective_delta<=0.35); s.fresh=false; o=c.update(s,t); assert(!o.valid&&o.safe_fallback); s={10,0,100,true,true}; t={100,5,true,true}; o=c.update(s,t); assert(std::fabs(o.vertical_speed_target_mps-2.0)<1e-12); assert(o.collective_delta<=0.35); std::cout<<"PASS: vertical control contract\n"; }
