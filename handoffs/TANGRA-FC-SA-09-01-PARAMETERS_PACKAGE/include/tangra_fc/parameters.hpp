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
class ParameterStore{
public:
 explicit ParameterStore(std::uint32_t schema_version,std::vector<ParameterDef> defs);
 bool set(const std::string&,double); double get(const std::string&) const; bool validate(const ParameterSnapshot&) const;
 std::string serialize(const std::string& provenance) const; bool deserialize(const std::string& text);
 bool persist(IParameterStorage&,const std::string& provenance); bool restore(IParameterStorage&);
 bool rollback(); std::uint32_t schema_version()const{return version_;}
private:
 std::uint32_t version_;std::map<std::string,ParameterDef> defs_;std::map<std::string,double> values_;std::map<std::string,double> previous_;
 static std::uint32_t checksum(const std::string&);
};
}
