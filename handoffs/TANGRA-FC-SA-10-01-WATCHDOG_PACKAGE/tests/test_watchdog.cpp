#include "tangra_fc/watchdog.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
struct HW:IWatchdogHardware{int feeds=0;ResetReason r=ResetReason::PowerOn;void feed()override{feeds++;}ResetReason reset_reason()const override{return r;}};
int main(){HW h;WatchdogSupervisor w(100);w.initialize(1000,h);auto s=w.evaluate(1050);assert(!s.expired&&s.reset_reason==ResetReason::PowerOn);w.heartbeat(1060,h);assert(h.feeds==1);s=w.evaluate(1200);assert(s.expired&&s.recovery==RecoveryState::SafeHold);HW h2;h2.r=ResetReason::Watchdog;WatchdogSupervisor w2(100);w2.initialize(0,h2);s=w2.evaluate(0);assert(s.recovery==RecoveryState::SafeHold);w2.acknowledge_recovery();s=w2.evaluate(0);assert(s.recovery==RecoveryState::Normal);std::cout<<"PASS: watchdog contract\n";}
