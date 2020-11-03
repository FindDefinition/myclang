# https://ziglang.org/deps/llvm%2bclang%2blld-11.0.0-x86_64-windows-msvc-release-mt.tar.xz

import subprocess
import os
import sys
from pathlib import Path
from typing import Optional
import ccimport
from ccimport import compat

def get_executable_path(executable: str) -> str:
    if compat.InWindows:
        cmd = ["powershell.exe", "(Get-Command {}).Path".format(executable)]
    else:
        cmd = ["which", executable]
    try:
        out = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        return ""
    return out.decode("utf-8").strip()

def get_clang_root() -> Optional[Path]:
    path = get_executable_path("clang")
    clang_folder = os.getenv("CLANG_LIBRARY_PATH", None)
    if clang_folder:
        return clang_folder
    if path:
        clang_folder = Path(path).parent.parent / "lib"
    if clang_folder is None:
        return None
    return clang_folder.parent

CLANG_ROOT = get_clang_root()
assert CLANG_ROOT is not None
LIBCLANG_NAME = "clang"
CLANG_LIBPATH = CLANG_ROOT / "lib"
if compat.InWindows:
    LIBCLANG_NAME = "libclang"
    LIBCLANG_PATH = CLANG_ROOT / "bin" / "libclang.dll"
LIBCLANG_SOURCES = list((Path(__file__).parent / "libclang").glob("*.cpp"))
if not compat.InWindows:
    # generated by compile llvm source code.
    LIBCLANG_CFLAGS = "-O3 -fdiagnostics-color -Wall -Wextra -Wno-unused-parameter -Wno-comment -Wno-maybe-uninitialized -fno-strict-aliasing".split(
        " ")
    LIBCLANG_CFLAGS += "-std=c++14 -fvisibility-inlines-hidden -Wno-noexcept-type -Wno-class-memaccess -Wno-redundant-move -fno-exceptions -fno-rtti".split(
        " ")
    DEP_LIBS_CLANG = [
        'clangAST', 'clangBasic', 'clangDriver', 'clangFrontend', 'clangIndex',
        'clangLex', 'clangSema', 'clangSerialization', 'clangTooling',
        'clangARCMigrate', 'LLVMAArch64CodeGen', 'LLVMAArch64AsmParser',
        'LLVMAArch64Desc', 'LLVMAArch64Disassembler', 'LLVMAArch64Info',
        'LLVMAArch64Utils', 'LLVMAMDGPUCodeGen', 'LLVMAMDGPUAsmParser',
        'LLVMAMDGPUDesc', 'LLVMAMDGPUDisassembler', 'LLVMAMDGPUInfo',
        'LLVMAMDGPUUtils', 'LLVMARMCodeGen', 'LLVMARMAsmParser', 'LLVMARMDesc',
        'LLVMARMDisassembler', 'LLVMARMInfo', 'LLVMARMUtils', 'LLVMAVRCodeGen',
        'LLVMAVRAsmParser', 'LLVMAVRDesc', 'LLVMAVRDisassembler',
        'LLVMAVRInfo', 'LLVMBPFCodeGen', 'LLVMBPFAsmParser', 'LLVMBPFDesc',
        'LLVMBPFDisassembler', 'LLVMBPFInfo', 'LLVMHexagonCodeGen',
        'LLVMHexagonAsmParser', 'LLVMHexagonDesc', 'LLVMHexagonDisassembler',
        'LLVMHexagonInfo', 'LLVMLanaiCodeGen', 'LLVMLanaiAsmParser',
        'LLVMLanaiDesc', 'LLVMLanaiDisassembler', 'LLVMLanaiInfo',
        'LLVMMipsCodeGen', 'LLVMMipsAsmParser', 'LLVMMipsDesc',
        'LLVMMipsDisassembler', 'LLVMMipsInfo', 'LLVMMSP430CodeGen',
        'LLVMMSP430AsmParser', 'LLVMMSP430Desc', 'LLVMMSP430Disassembler',
        'LLVMMSP430Info', 'LLVMNVPTXCodeGen', 'LLVMNVPTXDesc', 'LLVMNVPTXInfo',
        'LLVMPowerPCCodeGen', 'LLVMPowerPCAsmParser', 'LLVMPowerPCDesc',
        'LLVMPowerPCDisassembler', 'LLVMPowerPCInfo', 'LLVMRISCVCodeGen',
        'LLVMRISCVAsmParser', 'LLVMRISCVDesc', 'LLVMRISCVDisassembler',
        'LLVMRISCVInfo', 'LLVMRISCVUtils', 'LLVMSparcCodeGen',
        'LLVMSparcAsmParser', 'LLVMSparcDesc', 'LLVMSparcDisassembler',
        'LLVMSparcInfo', 'LLVMSystemZCodeGen', 'LLVMSystemZAsmParser',
        'LLVMSystemZDesc', 'LLVMSystemZDisassembler', 'LLVMSystemZInfo',
        'LLVMWebAssemblyCodeGen', 'LLVMWebAssemblyAsmParser',
        'LLVMWebAssemblyDesc', 'LLVMWebAssemblyDisassembler',
        'LLVMWebAssemblyInfo', 'LLVMX86CodeGen', 'LLVMX86AsmParser',
        'LLVMX86Desc', 'LLVMX86Disassembler', 'LLVMX86Info',
        'LLVMXCoreCodeGen', 'LLVMXCoreDesc', 'LLVMXCoreDisassembler',
        'LLVMXCoreInfo', 'LLVMCore', 'LLVMSupport', 'clangFormat',
        'clangToolingInclusions', 'clangToolingCore', 'clangFrontend',
        'clangDriver', 'LLVMOption', 'clangParse', 'clangSerialization',
        'clangSema', 'clangEdit', 'clangRewrite', 'clangAnalysis',
        'clangASTMatchers', 'clangAST', 'clangLex', 'clangBasic',
        'LLVMAArch64Desc', 'LLVMAArch64Info', 'LLVMAArch64Utils',
        'LLVMMIRParser', 'LLVMAMDGPUDesc', 'LLVMAMDGPUInfo', 'LLVMAMDGPUUtils',
        'LLVMARMDesc', 'LLVMARMInfo', 'LLVMARMUtils', 'LLVMHexagonDesc',
        'LLVMHexagonInfo', 'LLVMLanaiDesc', 'LLVMLanaiInfo', 'LLVMipo',
        'LLVMFrontendOpenMP', 'LLVMVectorize', 'LLVMIRReader', 'LLVMAsmParser',
        'LLVMInstrumentation', 'LLVMLinker', 'LLVMSystemZDesc',
        'LLVMSystemZInfo', 'LLVMWebAssemblyDesc', 'LLVMWebAssemblyInfo',
        'LLVMCFGuard', 'LLVMGlobalISel', 'LLVMAsmPrinter',
        'LLVMDebugInfoDWARF', 'LLVMSelectionDAG', 'LLVMCodeGen',
        'LLVMScalarOpts', 'LLVMAggressiveInstCombine', 'LLVMInstCombine',
        'LLVMBitWriter', 'LLVMTarget', 'LLVMTransformUtils', 'LLVMAnalysis',
        'LLVMProfileData', 'LLVMObject', 'LLVMBitReader', 'LLVMCore',
        'LLVMRemarks', 'LLVMBitstreamReader', 'LLVMMCParser', 'LLVMTextAPI',
        'LLVMMCDisassembler', 'LLVMMC', 'LLVMBinaryFormat',
        'LLVMDebugInfoCodeView', 'LLVMDebugInfoMSF', 'LLVMSupport',
        'pthread', "dl", "tinfo", 'rt', 'm', 'z', 'LLVMDemangle',
    ]

    LIBCLANG_LDFLAGS = "-fvisibility-inlines-hidden -Werror=date-time -Wall -Wextra -Wno-unused-parameter -Wwrite-strings -Wcast-qual -Wno-missing-field-initializers -pedantic -Wno-long-long -Wimplicit-fallthrough -Wno-maybe-uninitialized -Wno-noexcept-type -Wdelete-non-virtual-dtor -Wno-comment -fdiagnostics-color -ffunction-sections -fdata-sections -fno-common -Woverloaded-virtual -fno-strict-aliasing -O3 -DNDEBUG  -Wl,-z,defs -Wl,-z,nodelete  -Wl,-O3 -Wl,--gc-sections".split(
        " ")
    LIBCLANG_PATH = ccimport.ccimport(LIBCLANG_SOURCES,
                                      Path(__file__).parent / "myclang",
                                      includes=[CLANG_ROOT / "include"],
                                      libpaths=[CLANG_ROOT / "lib"],
                                      libraries=DEP_LIBS_CLANG,
                                      compile_options=LIBCLANG_CFLAGS,
                                      link_options=LIBCLANG_LDFLAGS,
                                      build_ctype=True,
                                      load_library=False)
    LIBCLANG_NAME = "myclang"
    CLANG_LIBPATH = Path(__file__).parent
else:
    DEP_LIBS_CLANG11 = [
        'clangAST', 'clangBasic', 'clangDriver', 'clangFrontend', 'clangIndex',
        'clangLex', 'clangSema', 'clangSerialization', 'clangTooling',
        'clangARCMigrate', 'LLVMAArch64CodeGen', 'LLVMAArch64AsmParser',
        'LLVMAArch64Desc', 'LLVMAArch64Disassembler', 'LLVMAArch64Info',
        'LLVMAArch64Utils', 'LLVMAMDGPUCodeGen', 'LLVMAMDGPUAsmParser',
        'LLVMAMDGPUDesc', 'LLVMAMDGPUDisassembler', 'LLVMAMDGPUInfo',
        'LLVMAMDGPUUtils', 'LLVMARMCodeGen', 'LLVMARMAsmParser', 'LLVMARMDesc',
        'LLVMARMDisassembler', 'LLVMARMInfo', 'LLVMARMUtils', 'LLVMAVRCodeGen',
        'LLVMAVRAsmParser', 'LLVMAVRDesc', 'LLVMAVRDisassembler',
        'LLVMAVRInfo', 'LLVMBPFCodeGen', 'LLVMBPFAsmParser', 'LLVMBPFDesc',
        'LLVMBPFDisassembler', 'LLVMBPFInfo', 'LLVMHexagonCodeGen',
        'LLVMHexagonAsmParser', 'LLVMHexagonDesc', 'LLVMHexagonDisassembler',
        'LLVMHexagonInfo', 'LLVMLanaiCodeGen', 'LLVMLanaiAsmParser',
        'LLVMLanaiDesc', 'LLVMLanaiDisassembler', 'LLVMLanaiInfo',
        'LLVMMipsCodeGen', 'LLVMMipsAsmParser', 'LLVMMipsDesc',
        'LLVMMipsDisassembler', 'LLVMMipsInfo', 'LLVMMSP430CodeGen',
        'LLVMMSP430AsmParser', 'LLVMMSP430Desc', 'LLVMMSP430Disassembler',
        'LLVMMSP430Info', 'LLVMNVPTXCodeGen', 'LLVMNVPTXDesc', 'LLVMNVPTXInfo',
        'LLVMPowerPCCodeGen', 'LLVMPowerPCAsmParser', 'LLVMPowerPCDesc',
        'LLVMPowerPCDisassembler', 'LLVMPowerPCInfo', 'LLVMRISCVCodeGen',
        'LLVMRISCVAsmParser', 'LLVMRISCVDesc', 'LLVMRISCVDisassembler',
        'LLVMRISCVInfo', 'LLVMRISCVUtils', 'LLVMSparcCodeGen',
        'LLVMSparcAsmParser', 'LLVMSparcDesc', 'LLVMSparcDisassembler',
        'LLVMSparcInfo', 'LLVMSystemZCodeGen', 'LLVMSystemZAsmParser',
        'LLVMSystemZDesc', 'LLVMSystemZDisassembler', 'LLVMSystemZInfo',
        'LLVMWebAssemblyCodeGen', 'LLVMWebAssemblyAsmParser',
        'LLVMWebAssemblyDesc', 'LLVMWebAssemblyDisassembler',
        'LLVMWebAssemblyInfo', 'LLVMX86CodeGen', 'LLVMX86AsmParser',
        'LLVMX86Desc', 'LLVMX86Disassembler', 'LLVMX86Info',
        'LLVMXCoreCodeGen', 'LLVMXCoreDesc', 'LLVMXCoreDisassembler',
        'LLVMXCoreInfo', 'LLVMCore', 'LLVMSupport', 'clangFormat',
        'clangToolingInclusions', 'clangToolingCore', 'clangFrontend',
        'clangDriver', 'LLVMOption', 'clangParse', 'clangSerialization',
        'clangSema', 'clangEdit', 'clangRewrite', 'clangAnalysis',
        'clangASTMatchers', 'clangAST', 'clangLex', 'clangBasic',
        'LLVMAArch64Desc', 'LLVMAArch64Info', 'LLVMAArch64Utils',
        'LLVMMIRParser', 'LLVMAMDGPUDesc', 'LLVMAMDGPUInfo', 'LLVMAMDGPUUtils',
        'LLVMARMDesc', 'LLVMARMInfo', 'LLVMARMUtils', 'LLVMHexagonDesc',
        'LLVMHexagonInfo', 'LLVMLanaiDesc', 'LLVMLanaiInfo', 'LLVMipo',
        'LLVMFrontendOpenMP', 'LLVMVectorize', 'LLVMIRReader', 'LLVMAsmParser',
        'LLVMInstrumentation', 'LLVMLinker', 'LLVMSystemZDesc',
        'LLVMSystemZInfo', 'LLVMWebAssemblyDesc', 'LLVMWebAssemblyInfo',
        'LLVMCFGuard', 'LLVMGlobalISel', 'LLVMAsmPrinter',
        'LLVMDebugInfoDWARF', 'LLVMSelectionDAG', 'LLVMCodeGen',
        'LLVMScalarOpts', 'LLVMAggressiveInstCombine', 'LLVMInstCombine',
        'LLVMBitWriter', 'LLVMTarget', 'LLVMTransformUtils', 'LLVMAnalysis',
        'LLVMProfileData', 'LLVMObject', 'LLVMBitReader', 'LLVMCore',
        'LLVMRemarks', 'LLVMBitstreamReader', 'LLVMMCParser', 'LLVMTextAPI',
        'LLVMMCDisassembler', 'LLVMMC', 'LLVMBinaryFormat',
        'LLVMDebugInfoCodeView', 'LLVMDebugInfoMSF', 'LLVMSupport',
        'LLVMDemangle', 'LLVMAVRCodeGen', 'LLVMAVRAsmParser',
        'LLVMAVRDisassembler', 'LLVMAVRDesc', 'LLVMAVRInfo'
    ]
    DEP_LIBS_CLANG11.append("Version")
    DEP_LIBS = DEP_LIBS_CLANG11
    LIBCLANG_CFLAGS = "/O2 /D_CINDEX_LIB_ /MT".split(" ")
    LIBCLANG_CFLAGS += "/std:c++latest".split(" ")
    LIBCLANG_LDFLAGS = "".split(" ")

    LIBCLANG_PATH = ccimport.ccimport(LIBCLANG_SOURCES,
                                      Path(__file__).parent / "myclang",
                                      includes=[CLANG_ROOT / "include"],
                                      libpaths=[CLANG_ROOT / "lib"],
                                      libraries=DEP_LIBS,
                                      compile_options=LIBCLANG_CFLAGS,
                                      link_options=LIBCLANG_LDFLAGS,
                                      build_ctype=True,
                                      load_library=False,
                                      disable_hash=False)
flags = []
if not compat.InWindows:
    flags.append("-Wl,-rpath,{}".format(str(Path(__file__).parent)))

clangutils = ccimport.autoimport([Path(__file__).parent / "clangutils.cc"],
                                 Path(__file__).parent / "clangutils",
                                 includes=[CLANG_ROOT / "include"],
                                 libpaths=[CLANG_LIBPATH],
                                 libraries=[LIBCLANG_NAME],
                                 link_options=flags)
