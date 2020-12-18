from .cext import LIBCLANG_PATH
from .constants import MYCLANG_SYSTEM_INCLUDES

from pathlib import Path 
from typing import List 

from ccimport import compat

def get_system_include(compiler: str="clang") -> List[Path]:
    standalone_headers = []
    for p in MYCLANG_SYSTEM_INCLUDES:
        if p.exists():
            standalone_headers.append(p)
    if len(standalone_headers) == len(MYCLANG_SYSTEM_INCLUDES):
        return standalone_headers
    # find system include by available compiler
    # for windows, you need to start terminal with visual studio dev environments
    return compat.get_system_include_paths(compiler)
