#pragma once
#include <cstdint>
#include <map>
#include <optional>
#include <string>
#include <vector>
namespace tangra::fc {
struct ParameterDef{std::string name;double default_value=0,min_value=0,max_value=0;};
struct ParameterSnapshot{std::uint32_t schema_version=1;std::map<std::string,double> values;std::string provenance;};
class IParameterStorage{public:virtual ~IParameterStorage()=default;virtual bool save(const std::string&)=0;virtual std::optional<std::string> load()=0;};
class IParameterMigration{public:virtual ~IParameterMigration()=default;virtual bool migrate(std::uint32_t,std::uint32_t,const std::map<std::string,double>&,std::map<std::string,double>&)=0;};
class ParameterStore{
public:
 explicit ParameterStore(std::uint32_t,std::vector<ParameterDef>);
 bool set(const std::string&,double);
 bool apply(const std::map<std::string,double>&);
 bool reset_defaults();
 double get(const std::string&) const;
 bool validate(const ParameterSnapshot&) const;
 std::string serialize(const std::string&) const;
 bool deserialize(const std::string&,IParameterMigration* = nullptr);
 bool persist(IParameterStorage&,const std::string&);
 bool restore(IParameterStorage&,IParameterMigration* = nullptr);
 bool rollback();
 std::uint32_t schema_version()const{return version_;}
 const std::string& last_provenance()const{return provenance_;}
 const std::map<std::string,ParameterDef>& definitions()const{return defs_;}
private:
 std::uint32_t version_;
 std::map<std::string,ParameterDef> defs_;
 std::map<std::string,double> values_;
 std::map<std::string,double> previous_;
 std::string provenance_;
 static std::uint32_t checksum(const std::string&);
};
}
