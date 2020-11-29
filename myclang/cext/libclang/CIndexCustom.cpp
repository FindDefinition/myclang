#include "CIndexDiagnostic.h"
#include "CIndexer.h"
#include "CLog.h"
#include "CXCursor.h"
#include "CXSourceLocation.h"
#include "CXString.h"
#include "CXTranslationUnit.h"
#include "CXType.h"
#include "CursorVisitor.h"
#include "IndexCustom.h"
#include "clang-c/FatalErrorHandler.h"
#include "clang/AST/Attr.h"
#include "clang/AST/DeclObjCCommon.h"
#include "clang/AST/Mangle.h"
#include "clang/AST/OpenMPClause.h"
#include "clang/AST/StmtVisitor.h"
#include "clang/Basic/Diagnostic.h"
#include "clang/Basic/DiagnosticCategories.h"
#include "clang/Basic/DiagnosticIDs.h"
#include "clang/Basic/Stack.h"
#include "clang/Basic/TargetInfo.h"
#include "clang/Basic/Version.h"
#include "clang/Frontend/ASTUnit.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Index/CommentToXML.h"
#include "clang/Lex/HeaderSearch.h"
#include "clang/Lex/Lexer.h"
#include "clang/Lex/PreprocessingRecord.h"
#include "clang/Lex/Preprocessor.h"
#include "llvm/ADT/Optional.h"
#include "llvm/ADT/STLExtras.h"
#include "llvm/ADT/StringSwitch.h"
#include "llvm/Config/llvm-config.h"
#include "llvm/Support/Compiler.h"
#include "llvm/Support/CrashRecoveryContext.h"
#include "llvm/Support/Format.h"
#include "llvm/Support/ManagedStatic.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/Program.h"
#include "llvm/Support/SaveAndRestore.h"
#include "llvm/Support/Signals.h"
#include "llvm/Support/TargetSelect.h"
#include "llvm/Support/Threading.h"
#include "llvm/Support/Timer.h"
#include "llvm/Support/raw_ostream.h"
#include <mutex>

#include "DeclKindToCXCursor.h"

using namespace clang;
using namespace clang::cxcursor;
using namespace clang::cxtu;
using namespace clang::cxindex;


bool clang_cursorDevelop(CXCursor cursor) {
  fprintf(stdout, "myclang: hello world\n");
  if (const Decl *D = getCursorDecl(cursor)) {
    const DeclContext *DC = D->getDeclContext();
    if (DC){
      
      for (auto p = DC->decls_begin(); p != DC->decls_end(); ++p){
          CXCursorKind K = getCursorKindForDeclCustom(D);
          fprintf(stdout, "myclang: CursorKind %d\n", K);
      }
      return true;
    }else{
        fprintf(stdout, "myclang: wtf 1\n");

    }
  }else{
    fprintf(stdout, "myclang: wtf 0\n");

  }
  return  false;
}
