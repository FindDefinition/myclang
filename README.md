# myclang

standalone libclang/clang++ code with some modifications

[![Build Status](https://github.com/FindDefinition/myclang/workflows/build/badge.svg)](https://github.com/FindDefinition/myclang/actions?query=workflow%3Abuild)

Only support Clang 11.

```pip install myclang```

## Usage

```from myclang import cindex```


## TODO
* try to expose compile API to remove llvm toolchain dependency
* try to solve CUDA problem
* add standard headers to python package
* find a way to get msvc c++ include