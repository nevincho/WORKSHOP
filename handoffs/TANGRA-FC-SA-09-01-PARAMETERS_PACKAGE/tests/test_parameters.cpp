#include "tangra_fc/parameters.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
struct Mem:IParameterStorage{std::optional<std::string>x;bool save(const std::string&s)override{x=s;return true;}std::optional<std::string>load()override{return x;}};
struct V1toV2:IParameterMigration{bool migrate(std::uint32_t from,std::uint32_t to,const std::map<std::string,double>&src,std::map<std::string,double>&dst)override{if(from!=1||to!=2)return false;auto it=src.find("kp");if(it==src.end())return false;dst["kp"]=it->second;dst["limit"]=2.0;return true;}};
int main(){ParameterStore p(1,{{"kp",1,0,10}});assert(p.set("kp",3));Mem m;assert(p.persist(m,"v1"));ParameterStore q(1,{{"kp",1,0,10}});assert(q.restore(m));for(const auto&bad:{std::string("version=X\nprovenance=x\nkp=1\nchecksum=0\n"),std::string("version=1\nprovenance=x\nkp=abc\nchecksum=0\n"),std::string("version=999999999999999999999\nprovenance=x\nkp=1\nchecksum=0\n")}){Mem b;b.x=bad;ParameterStore x(1,{{"kp",1,0,10}});bool ok=false;try{ok=x.restore(b);}catch(...){assert(false&&"malformed input threw");}assert(!ok);}ParameterStore v2(2,{{"kp",1,0,10},{"limit",2,0,5}});V1toV2 mig;assert(v2.restore(m,&mig));std::cout<<"PASS: fail-safe parameter parsing/migration\n";}
