#include "tangra_fc/parameters.hpp"
#include <cassert>
#include <cstdint>
#include <iostream>
#include <sstream>
using namespace tangra::fc;
struct Mem:IParameterStorage{std::optional<std::string>x;bool save(const std::string&s)override{x=s;return true;}std::optional<std::string>load()override{return x;}};
struct V1toV2:IParameterMigration{bool migrate(std::uint32_t from,std::uint32_t to,const std::map<std::string,double>&src,std::map<std::string,double>&dst)override{if(from!=1||to!=2)return false;auto it=src.find("kp");if(it==src.end())return false;dst["kp"]=it->second;dst["limit"]=2.0;return true;}};
static std::uint32_t fnv(const std::string&s){std::uint32_t h=2166136261u;for(unsigned char c:s){h^=c;h*=16777619u;}return h;}
static std::string payload(const std::string&body){std::ostringstream o;o<<body<<"checksum="<<fnv(body)<<"\n";return o.str();}
int main(){
 ParameterStore p(1,{{"kp",1,0,10}});assert(p.set("kp",3));Mem m;assert(p.persist(m,"v1"));ParameterStore q(1,{{"kp",1,0,10}});assert(q.restore(m));
 const std::string bad_version=payload("version=X\nprovenance=x\nkp=1\n");
 const std::string bad_number=payload("version=1\nprovenance=x\nkp=abc\n");
 const std::string overflow_version=payload("version=999999999999999999999\nprovenance=x\nkp=1\n");
 for(const auto&bad:{bad_version,bad_number,overflow_version}){Mem b;b.x=bad;ParameterStore x(1,{{"kp",1,0,10}});bool ok=false;try{ok=x.restore(b);}catch(...){assert(false&&"malformed input threw");}assert(!ok);}
 ParameterStore v2(2,{{"kp",1,0,10},{"limit",2,0,5}});V1toV2 mig;assert(v2.restore(m,&mig));
 std::cout<<"PASS: fail-safe parameter parsing/migration\n";
}
