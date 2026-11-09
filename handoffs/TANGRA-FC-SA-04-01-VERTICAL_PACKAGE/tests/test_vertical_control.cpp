#include "tangra_fc/vertical_control.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
#include <limits>
using namespace tangra::fc;
int main(){
    VerticalStateProducer p(100,1,1000);
    auto first=p.update({10.0,1000,true},1000);assert(first.valid&&first.fresh&&!first.velocity_valid);
    auto climb=p.update({11.0,1500,true},1500);assert(climb.valid&&climb.velocity_valid&&std::fabs(climb.vz_mps-2.0)<1e-12);
    auto descent=p.update({10.5,2000,true},2000);assert(descent.valid&&descent.velocity_valid&&std::fabs(descent.vz_mps+1.0)<1e-12);
    auto duplicate=p.update({10.6,2000,true},2000);assert(!duplicate.valid&&!duplicate.velocity_valid);
    auto stale=p.update({10.7,2100,true},2301);assert(!stale.valid&&!stale.fresh);
    auto invalid=p.update({std::numeric_limits<double>::quiet_NaN(),2200,true},2200);assert(!invalid.valid);
    p.reset();assert(!p.initialized());
    auto after_reset=p.update({20.0,5000,true},5000);assert(after_reset.valid&&!after_reset.velocity_valid);
    auto usable=p.update({20.1,5100,true},5100);VerticalController c;auto control=c.update(usable,{21.0,0.0,true,true});assert(control.valid&&!control.safe_fallback);
    std::cout<<"PASS: stateful vertical producer/control\n";
}
