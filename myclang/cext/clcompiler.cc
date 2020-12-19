#include <compiler.h>
#include <string>
#define CODEAI_EXPORT

int CODEAI_EXPORT compiler_main_bind(std::vector<std::string> args){
    std::vector<const char *> args_ptrs;
    for (auto &s : args){
        args_ptrs.push_back(s.c_str());
    }
    return compiler_main(args_ptrs);
}