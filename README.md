# myclang

standalone libclang code with some modifications

[![Build Status](https://github.com/FindDefinition/myclang/workflows/build/badge.svg)](https://github.com/FindDefinition/myclang/actions?query=workflow%3Abuild)

Only support Clang 11.

## Usage

1. Download llvm 11, If you are using Linux, just download from official website. If windows, download from this [page](https://github.com/ziglang/zig/wiki/Building-Zig-on-Windows).

2. Add llvm bin to your PATH. if your system already have clang, you need to use ```CLANG_LIBRARY_PATH``` to indicate correct llvm.

3. ```from myclang import cindex```
