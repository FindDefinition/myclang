from myclang import astgen 
from pathlib import Path 

def test_pch_gen():
    path = Path(__file__).parent.resolve() / "pch.h"
    astgen.create_pch(str(path), [], [])

def test_from_ast_file():
    path = Path(__file__).parent.resolve() / "code.cc"
    astgen.from_ast_file([str(path)], [], [])

