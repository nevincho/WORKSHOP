#include <iostream>
#include <string>
int main(int argc,char**argv){
 if(argc!=2) return 3;
 std::string k=argv[1];
 if(k=="bytes"||k=="set"||k=="implementation_object"){std::cout<<"INVALID_TYPE\n";return 2;}
 std::cout<<"SUPPORTED\n";return 0;
}
