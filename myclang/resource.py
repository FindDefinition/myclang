from myclang.constants import MYCLANG_FAKE_CLANG_ROOT
from pathlib import Path 
import subprocess
from typing import List, Union 
import contextlib
from ccimport import compat

def get_executable_path(executable: str) -> str:
    if compat.InWindows:
        cmd = ["powershell.exe", "(Get-Command {}).Path".format(executable)]
    elif compat.InLinux:
        cmd = ["which", executable]
    else:
        raise NotImplementedError
    try:
        out = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        return ""
    return out.decode("utf-8").strip()

def get_system_include(compiler: str="clang++") -> List[Path]:
    # TODO find a way to use clang headers instead of gcc/cl
    return compat.get_system_include_paths(compiler)


def get_fake_clang_root() -> Union[None, Path]:
    if MYCLANG_FAKE_CLANG_ROOT.exists():
        return MYCLANG_FAKE_CLANG_ROOT
    clang_exec = get_executable_path("clang++")
    if clang_exec is None:
        return None 
    return Path(clang_exec).parent.parent


def get_clang_compiler_path() -> Union[None, Path]:
    root = get_fake_clang_root()
    if not root:
        return None 
    return root / "bin" / "clang++"

