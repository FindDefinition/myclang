from myclang import astgen 
from pathlib import Path 

def test_pch_gen():
    path = Path(__file__).parent / "pch.h"
    astgen.create_pch(str(path), [], [])

    path = Path(__file__).parent / "pch.cu.h"
    astgen.create_pch(str(path), [], [], cuda=True)


def test_from_ast_file():
    path = Path(__file__).parent / "code.cu"
    astgen.from_ast_file([str(path)], [], [])
    path = Path(__file__).parent / "code.cc"
    astgen.from_ast_file([str(path)], [], [])

