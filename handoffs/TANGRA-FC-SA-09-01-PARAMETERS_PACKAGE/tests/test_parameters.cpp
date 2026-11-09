#include "tangra_fc/parameters.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
struct Mem:IParameterStorage{std::optional<std::string>x;bool save(const std::string&s)override{x=s;return true;}std::optional<std::string>load()override{return x;}};
int main(){ParameterStore p(1,{{"kp",1,0,10},{"limit",2,0,5}});assert(p.set("kp",3));assert(!p.set("kp",30));Mem m;assert(p.persist(m,"step9-test"));ParameterStore q(1,{{"kp",1,0,10},{"limit",2,0,5}});assert(q.restore(m));assert(q.get("kp")==3);assert(q.set("kp",4));assert(q.rollback());assert(q.get("kp")==3);auto bad=*m.x;bad[0]='X';m.x=bad;ParameterStore r(1,{{"kp",1,0,10},{"limit",2,0,5}});assert(!r.restore(m));std::cout<<"PASS: versioned parameters persistence\n";}
