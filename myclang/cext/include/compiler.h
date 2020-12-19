#include <vector>
#include <clang-c/Platform.h>

CINDEX_LINKAGE int compiler_main(std::vector<const char*> args);

CINDEX_LINKAGE int clang_main(int argc_, const char **argv_);