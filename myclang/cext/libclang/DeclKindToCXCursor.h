
#pragma once
#include <clang-c/Index.h>
#include "IndexCustom.h"
#include <clang/AST/Decl.h>
#include <clang/AST/DeclObjC.h>
#include <llvm/Support/Casting.h>

namespace clang {

CXCursorKind getCursorKindForDeclCustom(const Decl *D);

}