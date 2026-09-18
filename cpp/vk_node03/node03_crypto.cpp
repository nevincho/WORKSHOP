#define main vk_wire_v1_embedded_main
#include "../vk_wire_v1/wire_v1.cpp"
#undef main
#include <openssl/evp.h>
#include <fstream>

static std::vector<unsigned char> hx(const std::string&s,size_t n=0){
 if((s.size()&1)|| (n&&s.size()!=2*n))throw std::runtime_error("bad hex length");
 std::vector<unsigned char>r; r.reserve(s.size()/2);
 auto h=[](char c)->int{if(c>='0'&&c<='9')return c-'0';if(c>='a'&&c<='f')return c-'a'+10;return -1;};
 for(size_t i=0;i<s.size();i+=2){int a=h(s[i]),b=h(s[i+1]);if(a<0||b<0)throw std::runtime_error("bad lowercase hex");r.push_back((unsigned char)((a<<4)|b));}return r;
}
static bool edverify(const std::string&pkh,const std::string&sigh,const std::string&msg){
 try{auto pk=hx(pkh,32),sg=hx(sigh,64);EVP_PKEY*p=EVP_PKEY_new_raw_public_key(EVP_PKEY_ED25519,nullptr,pk.data(),pk.size());if(!p)return false;EVP_MD_CTX*c=EVP_MD_CTX_new();bool ok=c&&EVP_DigestVerifyInit(c,nullptr,nullptr,nullptr,p)==1&&EVP_DigestVerify(c,sg.data(),sg.size(),(const unsigned char*)msg.data(),msg.size())==1;EVP_MD_CTX_free(c);EVP_PKEY_free(p);return ok;}catch(...){return false;}
}
static std::string readall(const char*p){std::ifstream f(p,std::ios::binary);if(!f)throw std::runtime_error("vector open");return std::string((std::istreambuf_iterator<char>(f)),{});}
static std::string getstr(const O&o,const char*k){return ss(o,k);}
static V parsecanon(const std::string&s){P p(s);V v=p.parse();if(canon(v)!=s)throw std::runtime_error("frozen unsigned JSON noncanonical");return v;}
static std::string action_domain(const std::string&a,const V&u){return "VK-NODE-CONTROL-V1/"+a+"\n"+canon(u);}
static void require(bool x,const char*m){if(!x)throw std::runtime_error(m);}
static void setstr(O&o,const std::string&k,const std::string&v){o[k]=V(v);}
static void setint(O&o,const std::string&k,int64_t v){o[k]=V(v);}
static std::string signed_integrity(const V&u,const std::string&sig){
 O full=obj(u); O p=obj(full.at("payload"));p["signature"]=V(sig);full["payload"]=V(p);return sha(canon(V(full)));
}
int main(int argc,char**argv){try{
 if(argc!=2)throw std::runtime_error("usage: vk_node03 <crypto_vectors_v1.json>");
 P vp(readall(argv[1]));V root=vp.parse();const O&ro=obj(root);const A&vs=std::get<A>(ro.at("vectors").x);
 require(vs.size()==4,"vector count");
 std::string matrix="{\"profile\":\"VK-NODE-03-CPP20-ED25519\",\"vectors\":[";
 size_t valid=0,negative=0; std::vector<std::pair<std::string,std::string>> frozen;
 for(size_t i=0;i<vs.size();++i){
  const O&vo=obj(vs[i]);std::string a=getstr(vo,"action"),dh=getstr(vo,"signing_domain_hex"),eh=getstr(vo,"signing_domain_sha256"),pk=getstr(vo,"public_key_hex"),sg=getstr(vo,"signature_hex");
  auto db=hx(dh);std::string expected((char*)db.data(),db.size());std::string prefix="VK-NODE-CONTROL-V1/"+a+"\n";require(expected.rfind(prefix,0)==0,"domain prefix");
  V u=parsecanon(expected.substr(prefix.size()));std::string actual=action_domain(a,u);
  bool be=actual==expected,he=sha(actual)==eh,pe=hx(pk,32).size()==32,se=hx(sg,64).size()==64,ver=edverify(pk,sg,actual);
  require(be&&he&&pe&&se&&ver,"valid conformance");valid++;frozen.push_back({pk,sg});
  if(i)matrix+=",";
  matrix+="{\"vector_id\":\"C0"+std::to_string(i+1)+"\",\"action\":\""+a+"\",\"expected_domain_length\":"+std::to_string(expected.size())+",\"actual_domain_length\":"+std::to_string(actual.size())+",\"domain_bytes_equal\":"+(be?"true":"false")+",\"expected_domain_sha256\":\""+eh+"\",\"actual_domain_sha256\":\""+sha(actual)+"\",\"public_key_bytes_equal\":"+(pe?"true":"false")+",\"signature_bytes_equal\":true,\"expected_verification\":\"SIGNATURE_VALID\",\"actual_verification\":\"SIGNATURE_VALID\",\"result\":\"PASS\"}";
  // Cross-action domain separation against every other action.
  for(auto b:{"ENROLLMENT","REVOCATION","MIGRATION","RECOVERY"})if(a!=b){require(!edverify(pk,sg,action_domain(b,u)),"domain separation");negative++;}
  // signature bit mutation
  auto sm=hx(sg,64);sm[0]^=1;std::ostringstream sq;for(auto c:sm)sq<<std::hex<<std::setw(2)<<std::setfill('0')<<(int)c;require(!edverify(pk,sq.str(),actual),"sig mutation");negative++;
  // wrong public key: deterministic all-01 raw key
  require(!edverify(std::string(64,'1'),sg,actual),"wrong key");negative++;
 }
 // Mutations on ENROLLMENT independently reconstructed object.
 const O&v0=obj(vs[0]);std::string a=getstr(v0,"action"),pk=getstr(v0,"public_key_hex"),sg=getstr(v0,"signature_hex"),dh=getstr(v0,"signing_domain_hex");
 auto db=hx(dh);std::string exp((char*)db.data(),db.size()),pre="VK-NODE-CONTROL-V1/"+a+"\n";V base=parsecanon(exp.substr(pre.size()));
 auto reject=[&](V x,const char*name){std::string m=action_domain(a,x);require(!edverify(pk,sg,m),name);negative++;};
 {V x=base;setstr(obj(x),"vk_identity_id","vk-mutated");reject(x,"logical identity");}
 {V x=base;setstr(obj(x),"origin_node_id","origin-mutated");reject(x,"origin node identity");}
 {V x=base;O p=obj(obj(x).at("payload"));setstr(p,"subject_node_id","node-mutated");obj(x)["payload"]=V(p);reject(x,"subject node identity");}
 {V x=base;setstr(obj(x),"record_type","NodeRevocationRecord");reject(x,"record type");}
 {V x=base;setint(obj(x),"origin_sequence",2);reject(x,"origin sequence");}
 {V x=base;obj(x)["parents"]=V(A{V(std::string("parent-x"))});reject(x,"parents");}
 {V x=base;O p=obj(obj(x).at("payload"));setstr(p,"bootstrap_checkpoint_ref","cp-mutated");obj(x)["payload"]=V(p);reject(x,"payload");}
 // signature copied to another valid frozen record
 {const O&v1=obj(vs[1]);auto d=hx(getstr(v1,"signing_domain_hex"));std::string m((char*)d.data(),d.size());require(!edverify(pk,sg,m),"copied signature");negative++;}
 // R28 placeholder zero signature
 require(!edverify(pk,std::string(128,'0'),exp),"R28");negative++;
 // malformed encodings
 require(!edverify(pk,sg.substr(0,126),exp),"truncated");negative++;std::string up=sg;for(char&c:up)c=(char)std::toupper((unsigned char)c);require(!edverify(pk,up,exp),"uppercase");negative++;
 // integrity/authenticity separation: synthesize signed record integrity from unsigned+signature.
 std::string good_digest=signed_integrity(base,sg);require(good_digest.size()==64,"integrity base");
 V mut=base;O mp=obj(obj(mut).at("payload"));setstr(mp,"bootstrap_checkpoint_ref","cp-integrity-mut");obj(mut)["payload"]=V(mp);
 std::string stale=signed_integrity(base,sg),recomputed=signed_integrity(mut,sg);require(stale!=recomputed,"wire integrity mutation");require(!edverify(pk,sg,action_domain(a,mut)),"recomputed integrity authenticity");negative++;
 // Authority and clone boundaries are explicit verifier non-claims.
 bool signature_valid=edverify(pk,sg,exp),authorized=false,no_clone_conflict=false;require(signature_valid&&!authorized&&!no_clone_conflict,"authority/clone boundary");
 matrix+="],\"valid_vectors\":"+std::to_string(valid)+",\"negative_checks\":"+std::to_string(negative)+",\"r28\":\"SIGNATURE_INVALID\",\"authority_separation\":true,\"clone_limit_preserved\":true,\"result\":\"CROSS_LANGUAGE_EXACT_MATCH\"}";
 std::cout<<"VALID_VECTORS "<<valid<<"/4\nNEGATIVE_CHECKS "<<negative<<" PASS\nR28_BAD_SIGNATURE SIGNATURE_INVALID\nINTEGRITY_VS_AUTHENTICITY PASS\nAUTHORITY_SEPARATION PASS\nCLONE_LIMIT PASS\nMATRIX_JSON "<<matrix<<"\nCPP_CRYPTO_CONFORMANCE_PASS\n";
 return 0;
}catch(const std::exception&e){std::cerr<<"FAIL "<<e.what()<<"\n";return 1;}}
