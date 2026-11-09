#include "tangra_fc/parameters.hpp"
#include <cerrno>
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <limits>
#include <sstream>
#include <stdexcept>
namespace tangra::fc {
namespace {
bool parse_u32(const std::string&s,std::uint32_t&out){if(s.empty())return false;char*end=nullptr;errno=0;unsigned long v=std::strtoul(s.c_str(),&end,10);if(errno!=0||end==s.c_str()||*end!='\0'||v>std::numeric_limits<std::uint32_t>::max())return false;out=static_cast<std::uint32_t>(v);return true;}
bool parse_double(const std::string&s,double&out){if(s.empty())return false;char*end=nullptr;errno=0;double v=std::strtod(s.c_str(),&end);if(errno!=0||end==s.c_str()||*end!='\0'||!std::isfinite(v))return false;out=v;return true;}
}
ParameterStore::ParameterStore(std::uint32_t v,std::vector<ParameterDef>d):version_(v){for(auto&x:d){defs_[x.name]=x;values_[x.name]=x.default_value;}}
bool ParameterStore::set(const std::string&n,double v){auto it=defs_.find(n);if(it==defs_.end()||!std::isfinite(v)||v<it->second.min_value||v>it->second.max_value)return false;previous_=values_;values_[n]=v;return true;}
double ParameterStore::get(const std::string&n)const{auto it=values_.find(n);if(it==values_.end())throw std::out_of_range(n);return it->second;}
bool ParameterStore::validate(const ParameterSnapshot&s)const{if(s.schema_version!=version_||s.values.size()!=defs_.size())return false;for(auto&[n,d]:defs_){auto it=s.values.find(n);if(it==s.values.end()||!std::isfinite(it->second)||it->second<d.min_value||it->second>d.max_value)return false;}return true;}
std::uint32_t ParameterStore::checksum(const std::string&s){std::uint32_t h=2166136261u;for(unsigned char c:s){h^=c;h*=16777619u;}return h;}
std::string ParameterStore::serialize(const std::string&p)const{std::ostringstream body;body<<"version="<<version_<<"\n"<<"provenance="<<p<<"\n";body<<std::setprecision(17);for(auto&[n,v]:values_)body<<n<<"="<<v<<"\n";auto b=body.str();std::ostringstream out;out<<b<<"checksum="<<checksum(b)<<"\n";return out.str();}
bool ParameterStore::deserialize(const std::string&t,IParameterMigration*migration){
 auto pos=t.rfind("checksum=");if(pos==std::string::npos)return false;std::string body=t.substr(0,pos);std::uint32_t expected=0;if(!parse_u32(t.substr(pos+9,t.find('\n',pos)-pos-9),expected)||checksum(body)!=expected)return false;
 std::istringstream in(body);std::string line;ParameterSnapshot s;if(!std::getline(in,line)||line.rfind("version=",0)!=0||!parse_u32(line.substr(8),s.schema_version))return false;
 if(!std::getline(in,line)||line.rfind("provenance=",0)!=0)return false;s.provenance=line.substr(11);
 while(std::getline(in,line)){if(line.empty())continue;auto e=line.find('=');if(e==std::string::npos||e==0||e+1>=line.size())return false;double v=0;if(!parse_double(line.substr(e+1),v))return false;if(!s.values.emplace(line.substr(0,e),v).second)return false;}
 if(s.schema_version!=version_){if(!migration)return false;std::map<std::string,double> migrated;if(!migration->migrate(s.schema_version,version_,s.values,migrated))return false;s.schema_version=version_;s.values=std::move(migrated);s.provenance="migrated:"+s.provenance;}
 if(!validate(s))return false;previous_=values_;values_=s.values;provenance_=s.provenance;return true;
}
bool ParameterStore::persist(IParameterStorage&s,const std::string&p){return s.save(serialize(p));}
bool ParameterStore::restore(IParameterStorage&s,IParameterMigration*migration){auto x=s.load();return x&&deserialize(*x,migration);}
bool ParameterStore::rollback(){if(previous_.empty())return false;values_.swap(previous_);return true;}
}
