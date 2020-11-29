# https://ziglang.org/deps/llvm%2bclang%2blld-11.0.0-x86_64-windows-msvc-release-mt.tar.xz
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

import ccimport
from ccimport import compat, loader
from ccimport.core import get_full_file_name

from myclang.build_meta import ENABLE_JIT
from myclang.constants import MYCLANG_ROOT

with (Path(__file__).parent / "libclang.json").open("r") as f:
    LIBCLANG_BUILD_META_ALL = json.load(f)
LIBCLANG_BUILD_META = LIBCLANG_BUILD_META_ALL[compat.OS.value]
with (Path(__file__).parent / "clang++.json").open("r") as f:
    CLANG_COMPILER_BUILD_META_ALL = json.load(f)
CLANG_COMPILER_BUILD_META = CLANG_COMPILER_BUILD_META_ALL[compat.OS.value]

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
    clang_folder = os.getenv("LLVM_ROOT", None)
    if clang_folder:
        return Path(clang_folder)
    path = get_executable_path("clang")
    if path:
        clang_folder = Path(path).parent.parent / "lib"
    if clang_folder is None:
        return None
    return clang_folder.parent

print(os.getenv("LLVM_ROOT", None))
CLANG_ROOT = get_clang_root()
assert CLANG_ROOT is not None
LIBCLANG_NAME = "myclang"
CLANG_COMPILER_NAME = "clangmain"
CLANG_LIBPATH = CLANG_ROOT / "lib"

if compat.InWindows:
    LIBCLANG_PATH = CLANG_ROOT / "bin" / "libclang.dll"
LIBCLANG_SOURCES = list((Path(__file__).parent / "libclang").glob("*.cpp"))
CLANG_COMPILER_SOURCES = list((Path(__file__).parent / "clangcompiler").glob("*.cpp"))

if ENABLE_JIT:
    LIBCLANG_PATH = ccimport.ccimport(
        LIBCLANG_SOURCES,
        MYCLANG_ROOT / "myclang",
        includes=[CLANG_ROOT / "include"],
        libpaths=[CLANG_ROOT / "lib"],
        libraries=LIBCLANG_BUILD_META["libraries"],
        compile_options=LIBCLANG_BUILD_META["cflags"],
        link_options=LIBCLANG_BUILD_META["ldflags"],
        build_ctype=True,
        load_library=False,
        disable_hash=True)
else:
    LIBCLANG_PATH = Path(__file__).parent / get_full_file_name("myclang", True)

if ENABLE_JIT:
    CLANG_COMPILER_PATH = ccimport.ccimport(
        CLANG_COMPILER_SOURCES,
        MYCLANG_ROOT / "clangmain",
        includes=[CLANG_ROOT / "include"],
        libpaths=[CLANG_ROOT / "lib"],
        libraries=CLANG_COMPILER_BUILD_META["libraries"],
        compile_options=CLANG_COMPILER_BUILD_META["cflags"],
        link_options=CLANG_COMPILER_BUILD_META["ldflags"],
        build_ctype=True,
        load_library=False,
        disable_hash=True)
else:
    CLANG_COMPILER_PATH = Path(__file__).parent / get_full_file_name("clangmain", True)

flags = []
if not compat.InWindows:
    flags.append("-Wl,-rpath,{}".format(str(MYCLANG_ROOT)))
if ENABLE_JIT:
    # FIXME find out SIGSEGV error when exit if import clang libraries
    clangutils = ccimport.autoimport([Path(__file__).parent / "clangutils.cc"],
                                     MYCLANG_ROOT / "clangutils",
                                     includes=[CLANG_ROOT / "include"],
                                     libpaths=[MYCLANG_ROOT],
                                     libraries=[LIBCLANG_NAME],
                                     link_options=flags)
    clcompiler = ccimport.autoimport([Path(__file__).parent / "clcompiler.cc"],
                                     MYCLANG_ROOT / "clcompiler",
                                     includes=[CLANG_ROOT / "include", Path(__file__).parent / "clangcompiler"],
                                     libpaths=[MYCLANG_ROOT],
                                     libraries=[CLANG_COMPILER_NAME],
                                     link_options=flags)

else:
    clangutils = loader.try_import_from_path(
        Path(__file__).parent / get_full_file_name("clangutils", False))
    clcompiler = loader.try_import_from_path(
        Path(__file__).parent / get_full_file_name("clcompiler", False))
