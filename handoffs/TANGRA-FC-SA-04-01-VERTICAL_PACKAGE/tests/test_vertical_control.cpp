#include "tangra_fc/vertical_control.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
using namespace tangra::fc;
int main(){VerticalStateProducer p(50);auto s=p.produce({10,0,100,true},120);assert(s.valid&&s.fresh);auto stale=p.produce({10,0,100,true},200);assert(stale.valid&&!stale.fresh);VerticalController c;AltitudeTarget t{12,0,true,true};auto o=c.update(s,t);assert(o.valid&&!o.safe_fallback&&o.vertical_speed_target_mps>0);std::cout<<"PASS: vertical producer/control\n";}
