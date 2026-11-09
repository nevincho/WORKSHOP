#include "tangra_fc/local_navigation_state.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
int main(){LocalStateProducer p(50);LocalOrigin o;o.valid=true;StateUncertainty u{.5,.2,true};auto s=p.produce({1,2,3,.1,.2,.3,100,true},o,u,120);assert(s.valid&&s.fresh&&s.health==NavHealth::Healthy);auto stale=p.produce({1,2,3,.1,.2,.3,100,true},o,u,200);assert(stale.valid&&!stale.fresh&&stale.health==NavHealth::Degraded);std::cout<<"PASS: local state producer\n";}
