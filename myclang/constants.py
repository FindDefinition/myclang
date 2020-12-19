from pathlib import Path

CODEAI_SAVE_ROOT = Path.home() / ".codeai"
CODEAI_SAVE_ROOT.mkdir(exist_ok=True)

MYCLANG_ROOT = CODEAI_SAVE_ROOT / "myclang"
MYCLANG_ROOT.mkdir(exist_ok=True)

MYCLANG_CEXT_ROOT = Path(__file__).parent / "cext"

MYCLANG_FAKE_CLANG_ROOT = Path(__file__).parent / "clang_fake_root"
MYCLANG_RESOURCE_INCLUDE = MYCLANG_FAKE_CLANG_ROOT / "lib" / "clang" / "11.0.0" / "include"

CXCURSOR_FIRST_DECL = 1
CXCURSOR_LAST_DECL = 39

CXCURSOR_FIRST_EXTRA_DECL = 600
CXCURSOR_LAST_EXTRA_DECL = 603

CXCURSOREX_FIRST_DECL = 1001
CXCURSOREX_LAST_DECL = 1003