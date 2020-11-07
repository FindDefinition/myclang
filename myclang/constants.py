from pathlib import Path

CODEAI_SAVE_ROOT = Path.home() / ".codeai"
CODEAI_SAVE_ROOT.mkdir(exist_ok=True)

MYCLANG_ROOT = CODEAI_SAVE_ROOT / "myclang"
MYCLANG_ROOT.mkdir(exist_ok=True)