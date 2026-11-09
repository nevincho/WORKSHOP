#include "tangra_fc/parameters.hpp"
#include <cassert>
#include <iostream>
using namespace tangra::fc;
struct Mem:IParameterStorage{std::optional<std::string>x;bool save(const std::string&s)override{x=s;return true;}std::optional<std::string>load()override{return x;}};
struct V1toV2:IParameterMigration{bool migrate(std::uint32_t from,std::uint32_t to,const std::map<std::string,double>&src,std::map<std::string,double>&dst)override{if(from!=1||to!=2)return false;auto it=src.find("kp");if(it==src.end())return false;dst["kp"]=it->second;dst["limit"]=2.0;return true;}};
int main(){ParameterStore p(1,{{"kp",1,0,10}});assert(p.set("kp",3));Mem m;assert(p.persist(m,"v1-source"));ParameterStore same(1,{{"kp",1,0,10}});assert(same.restore(m));assert(same.get("kp")==3&&same.last_provenance()=="v1-source");ParameterStore v2(2,{{"kp",1,0,10},{"limit",2,0,5}});assert(!v2.restore(m));V1toV2 mig;assert(v2.restore(m,&mig));assert(v2.get("kp")==3&&v2.get("limit")==2);assert(v2.last_provenance()=="migrated:v1-source");assert(v2.set("kp",4));assert(v2.rollback());assert(v2.get("kp")==3);auto bad=*m.x;bad[0]='X';m.x=bad;ParameterStore r(1,{{"kp",1,0,10}});assert(!r.restore(m));std::cout<<"PASS: versioned parameters persistence migration rollback\n";}
