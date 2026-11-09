#pragma once
#include "tangra_fc/parameters.hpp"
#include <cstddef>
#include <cstdint>
#include <optional>
#include <string>
#include <vector>
namespace tangra::fc {
enum class ConfigGroup:std::uint8_t{VehicleProfile,MotorEsc,Servos,Imu,GnssCompass,Pid,Navigation,FailsafeWatchdog,TelemetryMavlink};
enum class ConfigValueKind:std::uint8_t{Float,Integer,Boolean,Enum};
struct ConfigField{ParameterDef parameter;ConfigGroup group=ConfigGroup::VehicleProfile;ConfigValueKind kind=ConfigValueKind::Float;std::string units;std::string enum_labels;};
enum class VehicleProfileId:std::uint8_t{QuadX=0,FixedWing=1,TwinMotorPusher=2,VTOL=3};
struct VehicleProfileDef{VehicleProfileId id=VehicleProfileId::QuadX;std::string name;bool control_implemented=false;int required_motor_count=0;};
struct FirmwareIdentity{std::string product;std::string firmware_version;std::string build_id;std::uint16_t config_protocol_version=1;std::uint32_t parameter_schema_version=1;};
struct ConfigValidation{bool valid=true;std::vector<std::string> errors;};
std::vector<ConfigField> make_fc_configuration_schema();
std::vector<ParameterDef> configuration_parameter_defs(const std::vector<ConfigField>&);
std::vector<VehicleProfileDef> make_vehicle_profiles();
class FcConfigurationService{
public:
 FcConfigurationService(FirmwareIdentity,ParameterStore&,IParameterStorage&,std::vector<ConfigField> schema=make_fc_configuration_schema(),std::vector<VehicleProfileDef> profiles=make_vehicle_profiles());
 const FirmwareIdentity& identity()const{return identity_;}
 const std::vector<ConfigField>& schema()const{return schema_;}
 const std::vector<VehicleProfileDef>& profiles()const{return profiles_;}
 std::optional<double> get(const std::string&)const;
 bool set(const std::string&,double,std::string* error=nullptr);
 ConfigValidation validate()const;
 bool save(std::string* error=nullptr);
 bool defaults(std::string* error=nullptr);
 std::string export_parameters()const;
 bool import_parameters(const std::string&,std::string* error=nullptr);
private:
 const ConfigField* find_field(const std::string&)const;
 const VehicleProfileDef* current_profile()const;
 FirmwareIdentity identity_;ParameterStore& store_;IParameterStorage& storage_;std::vector<ConfigField> schema_;std::vector<VehicleProfileDef> profiles_;
};
class UsbConfigurationProtocol{
public:explicit UsbConfigurationProtocol(FcConfigurationService&s):service_(s){}std::string handle(const std::string&);
private:static std::string hex_encode(const std::string&);static std::optional<std::string> hex_decode(const std::string&);FcConfigurationService&service_;
};
class IUsbConfigurationTransport{public:virtual~IUsbConfigurationTransport()=default;virtual std::optional<std::string> read_request()=0;virtual void write_response(const std::string&)=0;};
class UsbConfigurationSession{
public:UsbConfigurationSession(UsbConfigurationProtocol&p,IUsbConfigurationTransport&t):protocol_(p),transport_(t){}bool poll_once();
private:UsbConfigurationProtocol&protocol_;IUsbConfigurationTransport&transport_;
};
}
