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

flags = []
if not compat.InWindows:
    flags.append("-Wl,-rpath,{}".format(str(MYCLANG_ROOT)))

if ENABLE_JIT:
    with (Path(__file__).parent / "libclang.json").open("r") as f:
        LIBCLANG_BUILD_META_ALL = json.load(f)
    LIBCLANG_BUILD_META = LIBCLANG_BUILD_META_ALL[compat.OS.value]
    CLANG_ROOT = get_clang_root()
    msg = "you must provide clang root by either add clang++ to Path or export LLVM_ROOT"
    assert CLANG_ROOT is not None, msg
    LIBCLANG_NAME = "myclang"
    CLANG_COMPILER_NAME = "clangmain"
    CLANG_LIBPATH = CLANG_ROOT / "lib"

    if compat.InWindows:
        LIBCLANG_PATH = CLANG_ROOT / "bin" / "libclang.dll"
    LIBCLANG_INCLUDE = Path(__file__).parent.resolve() / "include"
    LIBCLANG_SOURCES = list((Path(__file__).parent / "libclang").glob("*.cpp"))
    CLANG_COMPILER_SOURCES = list((Path(__file__).parent / "clangcompiler").glob("*.cpp"))
    LIBCLANG_PATH = ccimport.ccimport(
        LIBCLANG_SOURCES,
        MYCLANG_ROOT / "myclang",
        includes=[CLANG_ROOT / "include", LIBCLANG_INCLUDE],
        libpaths=[CLANG_ROOT / "lib"],
        libraries=LIBCLANG_BUILD_META["libraries"],
        compile_options=LIBCLANG_BUILD_META["cflags"],
        link_options=LIBCLANG_BUILD_META["ldflags"],
        build_ctype=True,
        load_library=False,
        disable_hash=True)

    # FIXME find out SIGSEGV error when exit if import clang libraries
    clangutils = ccimport.autoimport([Path(__file__).parent / "clangutils.cc"],
                                     MYCLANG_ROOT / "clangutils",
                                     includes=[CLANG_ROOT / "include", LIBCLANG_INCLUDE],
                                     libpaths=[MYCLANG_ROOT],
                                     libraries=[LIBCLANG_NAME],
                                     link_options=flags)
    clcompiler = ccimport.autoimport([Path(__file__).parent / "clcompiler.cc"],
                                     MYCLANG_ROOT / "clcompiler",
                                     includes=[CLANG_ROOT / "include", LIBCLANG_INCLUDE],
                                     libpaths=[MYCLANG_ROOT],
                                     libraries=[LIBCLANG_NAME],
                                     link_options=flags)
else:
    LIBCLANG_PATH = Path(__file__).parent / get_full_file_name("myclang", True)
    clangutils = loader.try_import_from_path(
        Path(__file__).parent / get_full_file_name("clangutils", False))
    clcompiler = loader.try_import_from_path(
        Path(__file__).parent / get_full_file_name("clcompiler", False))
