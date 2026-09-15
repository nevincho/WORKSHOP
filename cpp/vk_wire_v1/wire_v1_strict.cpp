#define main vk_wire_internal_cli
#include "wire_v1.cpp"
#undef main
int main(int argc,char**argv){try{
 if(argc<3)throw std::runtime_error("usage: mode json");
 std::string mode=argv[1],s=argv[2]; P p(s); V v=p.parse(); std::string c=canon(v);
 if(c!=s) throw Err("INVALID_ENCODING","received bytes are not canonical Wire v1");
 if(mode=="canonical"){std::cout<<c<<"\n"<<sha(c)<<"\n";return 0;}
 O&o=obj(v);
 if(mode=="durable"){durable(o,true);std::cout<<"ACCEPTED\n"<<c<<"\n";return 0;}
 if(mode=="frontier"){frontier(o);std::cout<<"ACCEPTED\n"<<c<<"\n"<<sha(c)<<"\n";return 0;}
 if(mode=="checkpoint"){
  closed(o,{"wire_profile_version","checkpoint_id","vk_identity_id","frontier","canonical_state_digest","manifest_digest","schema_version"});ver(o);ident(ss(o,"checkpoint_id"));ident(ss(o,"vk_identity_id"));frontier(obj(o.at("frontier")));
  for(auto k:{"canonical_state_digest","manifest_digest"}){auto d=ss(o,k);if(d.size()!=64||!std::all_of(d.begin(),d.end(),[](char x){return isdigit((unsigned char)x)||(x>='a'&&x<='f');}))throw Err("INVALID_SCHEMA");}
  std::cout<<"ACCEPTED\n"<<c<<"\n"<<sha(c)<<"\n";return 0;
 }
 if(mode=="recon"){
  closed(o,{"wire_profile_version","reconciliation_id","vk_identity_id","input_record_ids","result","provenance","policy","authority","schema_version"});ver(o);auto&a=std::get<A>(o.at("input_record_ids").x);if(a.size()<2)throw Err("INVALID_SCHEMA");std::string last;for(auto&x:a){if(!std::holds_alternative<std::string>(x.x))throw Err("INVALID_SCHEMA");auto z=std::get<std::string>(x.x);if(!last.empty()&&z<=last)throw Err("INVALID_SCHEMA");last=z;}std::cout<<"ACCEPTED\n"<<c<<"\n"<<sha(c)<<"\n";return 0;
 }
 if(mode=="relation"){auto&a=obj(o.at("a")),&b=obj(o.at("b"));frontier(a);frontier(b);std::cout<<relation(a,b)<<"\n";return 0;}
 throw std::runtime_error("mode");
 }catch(const Err&e){std::cout<<e.cat<<"\n";return 2;}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 3;}}
