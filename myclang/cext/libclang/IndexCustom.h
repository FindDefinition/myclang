#pragma once
#include <clang-c/Index.h>

enum CXCursorKindEx {
  CXCursorEx_UnexposedDecl = 1000,
  /** An access specifier. */
  CXCursorEx_ClassTemplateSpecialization = 1001,
  CXCursorEx_DecompositionDecl = 1002,
  CXCursorEx_BindingDecl = 1003,
  CXCursorEx_FirstDecl = CXCursorEx_ClassTemplateSpecialization,
  CXCursorEx_LastDecl = CXCursorEx_BindingDecl
};

enum CXTemplateSpecializationKind {

  /// This template specialization was formed from a template-id but
  /// has not yet been declared, defined, or instantiated.
  CXTSK_Undeclared = 0,
  /// This template specialization was implicitly instantiated from a
  /// template. (C++ [temp.inst]).
  CXTSK_ImplicitInstantiation,
  /// This template specialization was declared or defined by an
  /// explicit specialization (C++ [temp.expl.spec]) or partial
  /// specialization (C++ [temp.class.spec]).
  CXTSK_ExplicitSpecialization,
  /// This template specialization was instantiated from a template
  /// due to an explicit instantiation declaration request
  /// (C++11 [temp.explicit]).
  CXTSK_ExplicitInstantiationDeclaration,
  /// This template specialization was instantiated from a template
  /// due to an explicit instantiation definition request
  /// (C++ [temp.explicit]).
  CXTSK_ExplicitInstantiationDefinition
};

LLVM_CLANG_C_EXTERN_C_BEGIN

CINDEX_LINKAGE enum CXTemplateSpecializationKind
clang_getTemplateSpecializationKind(CXCursor C);

CINDEX_LINKAGE bool clang_cursorDevelop(CXCursor C);

LLVM_CLANG_C_EXTERN_C_END