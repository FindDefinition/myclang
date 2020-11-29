#include "DeclKindToCXCursor.h"
#include "IndexCustom.h"

namespace clang {

CXCursorKind getCursorKindForDeclCustom(const Decl *D) {
  if (!D)
    return CXCursor_UnexposedDecl;

  switch (D->getKind()) {
  case Decl::Enum:
    return CXCursor_EnumDecl;
  case Decl::EnumConstant:
    return CXCursor_EnumConstantDecl;
  case Decl::Field:
    return CXCursor_FieldDecl;
  case Decl::Function:
    return CXCursor_FunctionDecl;
  case Decl::ObjCCategory:
    return CXCursor_ObjCCategoryDecl;
  case Decl::ObjCCategoryImpl:
    return CXCursor_ObjCCategoryImplDecl;
  case Decl::ObjCImplementation:
    return CXCursor_ObjCImplementationDecl;

  case Decl::ObjCInterface:
    return CXCursor_ObjCInterfaceDecl;
  case Decl::ObjCIvar:
    return CXCursor_ObjCIvarDecl;
  case Decl::ObjCMethod:
    return cast<ObjCMethodDecl>(D)->isInstanceMethod()
               ? CXCursor_ObjCInstanceMethodDecl
               : CXCursor_ObjCClassMethodDecl;
  case Decl::CXXMethod:
    return CXCursor_CXXMethod;
  case Decl::CXXConstructor:
    return CXCursor_Constructor;
  case Decl::CXXDestructor:
    return CXCursor_Destructor;
  case Decl::CXXConversion:
    return CXCursor_ConversionFunction;
  case Decl::ObjCProperty:
    return CXCursor_ObjCPropertyDecl;
  case Decl::ObjCProtocol:
    return CXCursor_ObjCProtocolDecl;
  case Decl::ParmVar:
    return CXCursor_ParmDecl;
  case Decl::Typedef:
    return CXCursor_TypedefDecl;
  case Decl::TypeAlias:
    return CXCursor_TypeAliasDecl;
  case Decl::TypeAliasTemplate:
    return CXCursor_TypeAliasTemplateDecl;
  case Decl::Var:
    return CXCursor_VarDecl;
  case Decl::Namespace:
    return CXCursor_Namespace;
  case Decl::NamespaceAlias:
    return CXCursor_NamespaceAlias;
  case Decl::TemplateTypeParm:
    return CXCursor_TemplateTypeParameter;
  case Decl::NonTypeTemplateParm:
    return CXCursor_NonTypeTemplateParameter;
  case Decl::TemplateTemplateParm:
    return CXCursor_TemplateTemplateParameter;
  case Decl::FunctionTemplate:
    return CXCursor_FunctionTemplate;
  case Decl::ClassTemplate:
    return CXCursor_ClassTemplate;
  case Decl::AccessSpec:
    return CXCursor_CXXAccessSpecifier;
  case Decl::ClassTemplatePartialSpecialization:
    return CXCursor_ClassTemplatePartialSpecialization;
  case Decl::ClassTemplateSpecialization:
    return CXCursorKind(CXCursorEx_ClassTemplateSpecialization);
  case Decl::UsingDirective:
    return CXCursor_UsingDirective;
  case Decl::StaticAssert:
    return CXCursor_StaticAssert;
  case Decl::Friend:
    return CXCursor_FriendDecl;
  case Decl::TranslationUnit:
    return CXCursor_TranslationUnit;
  case Decl::Binding:
    return CXCursorKind(CXCursorEx_BindingDecl);
  case Decl::Decomposition:
    return CXCursorKind(CXCursorEx_DecompositionDecl);

  case Decl::Using:
  case Decl::UnresolvedUsingValue:
  case Decl::UnresolvedUsingTypename:
    return CXCursor_UsingDeclaration;

  case Decl::ObjCPropertyImpl:
    switch (cast<ObjCPropertyImplDecl>(D)->getPropertyImplementation()) {
    case ObjCPropertyImplDecl::Dynamic:
      return CXCursor_ObjCDynamicDecl;

    case ObjCPropertyImplDecl::Synthesize:
      return CXCursor_ObjCSynthesizeDecl;
    }
    llvm_unreachable("Unexpected Kind!");

  case Decl::Import:
    return CXCursor_ModuleImportDecl;

  case Decl::ObjCTypeParam:
    return CXCursor_TemplateTypeParameter;

  default:
    if (const auto *TD = dyn_cast<TagDecl>(D)) {
      switch (TD->getTagKind()) {
      case TTK_Interface: // fall through
      case TTK_Struct:
        return CXCursor_StructDecl;
      case TTK_Class:
        return CXCursor_ClassDecl;
      case TTK_Union:
        return CXCursor_UnionDecl;
      case TTK_Enum:
        return CXCursor_EnumDecl;
      }
    }
  }

  return CXCursor_UnexposedDecl;
}
}
