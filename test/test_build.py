from pathlib import Path

from ccimport import compat


def test_build():
    from myclang import cext, cindex


def test_parse():
    from myclang import cindex
    from myclang.cindex import TranslationUnit
    path = Path(__file__).parent / "code.cc"
    index = cindex.Index.create()
    cxxflags = [
        "-std=c++17",
    ]
    tu = index.parse(path,
                     args=[*cxxflags],
                     options=TranslationUnit.PARSE_NONE)


if __name__ == "__main__":
    test_parse()
