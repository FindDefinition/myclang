from myclang import astgen 
from pathlib import Path 
import pytest 
from ccimport import compat

_MSG = "vs 16.8 in github CI have a bug that cause this test fail, we need to wait for vs 16.9"
@pytest.mark.skipif(compat.InWindows, reason=_MSG)
def test_pch_gen():
    path = Path(__file__).parent.resolve() / "pch.h"
    astgen.create_pch(str(path), [], [])

@pytest.mark.skipif(compat.InWindows, reason=_MSG)
def test_from_ast_file():
    path = Path(__file__).parent.resolve() / "code.cc"
    astgen.from_ast_file([str(path)], [], [])

