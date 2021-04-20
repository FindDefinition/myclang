#include <vector>
#include <clang-c/Platform.h>
#include <vector>
#include <unordered_map>
#include <string>


CINDEX_LINKAGE int compiler_main(std::vector<const char*> args);

CINDEX_LINKAGE int clang_main(int argc_, const char **argv_);

std::tuple<int, std::unordered_map<std::string, std::string>> clangfmt_main(std::vector<std::string> args, std::string inp);
