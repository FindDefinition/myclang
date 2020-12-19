import subprocess
import time
from pathlib import Path
from typing import Deque, Dict, Iterator, List, Optional, Tuple, Union

import myclang.cindex as cindex
from myclang.cindex import Cursor, CursorKind, TranslationUnit

from ccimport import compat
from myclang.global_cfg import GLOBAL_CONFIG
from myclang.constants import MYCLANG_RESOURCE_INCLUDE, MYCLANG_CEXT_ROOT
from myclang.utils import tempdir
from myclang.resource import get_executable_path
import myclang
import os 
import sys


def create_pch(include: str,
               includes: List[str],
               options: List[str],
               cuda=False,
               compiler=None):
    """use pch can greatly increase ast gen speed for 
    header-only libraries.
    """
    # TODO: g++/msvc support (dont support cuda)
    cuda_flags: List[str] = []
    includes = includes.copy()
    includes.extend(GLOBAL_CONFIG.includes)
    includes = ["-I" + p for p in includes]
    if cuda:
        # see https://reviews.llvm.org/D87325 for '-S'
        cuda_flags = ["-x", "cuda", "-S", "--cuda-host-only"]
    pch_out_path = Path(include).parent / (Path(include).stem + ".pch")
    if compiler is None:
        compiler = myclang.get_clang_compiler_path()
        if compiler is None:
            raise ValueError("you need to provide clang compiler by download llvm or install myclang prebuilt")
    
    cmds = [
        str(compiler), *includes, *options, *cuda_flags, "-Xclang", "-emit-pch",
        include, "-o",
        str(pch_out_path)
    ]
    if compat.InWindows:
        # no way to add rpath-like to executable, so we need to append myclang.dll dir 
        env = os.environ.copy()
        paths = env["PATH"].split(";")
        paths.append(str(MYCLANG_CEXT_ROOT))
        env["PATH"] = ";".join(paths)
        return subprocess.check_call(cmds, env=env)

    return subprocess.check_call(cmds)


def from_ast_file(sources: List[Union[Path, str]],
                  includes: List[str],
                  options: List[str],
                  clang_path=None,
                  index: Optional[cindex.Index] = None
                  ) -> List[TranslationUnit]:
    """this function generate ast by subprocess ```clang++ -emit-ast```, 
    then read it by TranslationUnit.from_ast_file. 
    """
    # from myclang.cext import clcompiler

    source_paths: List[Path] = []
    includes = includes.copy()
    includes.extend(GLOBAL_CONFIG.includes)
    if compat.InWindows:
        assert get_executable_path("cl") is not None, "you must run inside vs develop prompt"
        # includes.extend(compat.get_system_include_paths("cl")), "you need to install vs in windows"
    elif compat.InLinux:
        assert get_executable_path("g++") is not None, "you need to install gcc in linux"
        includes.extend(compat.get_system_include_paths("g++"))
    else:
        raise NotImplementedError
    includes = ["-I" + str(p) for p in includes]
    for source_path in sources:
        source_path = Path(source_path)
        source_paths.extend(source_path.parent.glob(source_path.name))
    res: List[TranslationUnit] = []
    delete = True
    if clang_path is None:
        clang_path = myclang.get_clang_compiler_path()
        if clang_path is None:
            raise ValueError("you need to provide clang compiler by download llvm or install myclang prebuilt")

    if compat.InWindows:
        # you need to delete generated ast files by yourself.
        # because clang from_ast_file do something on ast file
        # and make it can't be deleted in current process.
        delete = False
    with tempdir(delete) as temp:
        cuda_flags = []
        for p in source_paths:
            if p.suffix == ".cu":
                # for cuda code, we only need host ast.
                # this can reduce compile time.
                cuda_flags.append("--cuda-host-only")
                break
        cmds = [
            str(clang_path), *includes, *options, *cuda_flags, "-emit-ast",
            *[str(p) for p in source_paths]
        ]
        # python_root = Path(sys.executable).parent.parent # xxx/bin/python -> xxx
        # correct_clang_root = myclang.get_fake_clang_root()
        # assert correct_clang_root is not None 
        # we replace MYCLANG_WRONG_PREFIX with MYCLANG_FIXED_ROOT
        # os.environ["MYCLANG_FIXED_ROOT"] = str(correct_clang_root)
        # os.environ["MYCLANG_WRONG_PREFIX"] = str(python_root)
        # TODO run clcompiler.compiler_main_bind(cmds) in subprocess to control .ast file
        # clcompiler.compiler_main_bind(cmds)
        if compat.InWindows:
            # no way to add rpath-like to executable, so we need to append myclang.dll dir 
            env = os.environ.copy()
            paths = env["PATH"].split(";")
            paths.append(str(MYCLANG_CEXT_ROOT))
            env["PATH"] = ";".join(paths)
            subprocess.check_call(cmds, cwd=str(temp), env=env, stderr=subprocess.STDOUT)
        else:
            subprocess.check_call(cmds, cwd=str(temp), stderr=subprocess.STDOUT)
        for source_path in source_paths:
            out_path: Path = temp / (source_path.stem + ".ast")
            res.append(TranslationUnit.from_ast_file(str(out_path), index))
    return res


def direct_gen(sources: List[Union[Path, str]],
               includes: List[str],
               options: List[str],
               parse_option=TranslationUnit.PARSE_NONE,
               index: Optional[cindex.Index] = None,
               unsaved_files: Optional[Tuple[Union[Path, str], str]] = None
               ) -> List[TranslationUnit]:
    """this function generate ast by TranslationUnit.from_source. 
    currently not working with cuda source. 
    """
    includes = includes.copy()
    includes.extend(GLOBAL_CONFIG.includes)
    includes.append(str(MYCLANG_RESOURCE_INCLUDE))
    if compat.InWindows:
        assert get_executable_path("cl") is not None, "you must run inside vs develop prompt"
        # includes.extend(compat.get_system_include_paths("cl")), "you need to install vs in windows"
    elif compat.InLinux:
        assert get_executable_path("g++") is not None, "you need to install gcc in linux"
        includes.extend(compat.get_system_include_paths("g++"))
    else:
        raise NotImplementedError
    source_paths: List[Path] = []
    includes = ["-I" + str(p) for p in includes]
    for source_path in sources:
        source_path = Path(source_path)
        source_paths.extend(source_path.parent.glob(source_path.name))
    res: List[TranslationUnit] = []

    for source_path in source_paths:
        if source_path.suffix == ".cu":
            raise NotImplementedError(
                "don't support cuda directly ast for now.")
        res.append(
            TranslationUnit.from_source(str(source_path),
                                        [*includes, *options],
                                        options=parse_option,
                                        index=index,
                                        unsaved_files=unsaved_files))
        for diag in res[-1].diagnostics:
            print(diag)

    return res