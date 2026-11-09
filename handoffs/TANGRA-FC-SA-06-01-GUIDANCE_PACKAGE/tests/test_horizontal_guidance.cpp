#include "tangra_fc/horizontal_guidance.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
using namespace tangra::fc;
int main(){HorizontalGuidance g;HorizontalState s{0,0,0,0,true,true};LocalObjective o{10,-10,true};auto a=g.update(s,o);assert(a.valid&&!a.safe_reject);assert(std::fabs(a.vx_mps)<=5&&std::fabs(a.vy_mps)<=5);assert(std::fabs(a.roll_norm)<=0.5&&std::fabs(a.pitch_norm)<=0.5);s.fresh=false;auto b=g.update(s,o);assert(!b.valid&&b.safe_reject);std::cout<<"PASS: horizontal guidance\n";}
