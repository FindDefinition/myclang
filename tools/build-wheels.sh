#!/bin/bash
set -e -u -x

function repair_wheel {
    wheel="$1"
    outpath="$2"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT" -w "$outpath"
    fi
}

mkdir -p /io/myclang/clang_fake_root/lib/clang/11.0.0
cp -r $LLVM_ROOT/lib/clang/11.0.0/include /io/myclang/clang_fake_root/lib/clang/11.0.0
export MYCLANG_ENABLE_JIT=0
export MYCLANG_STATIC_ZLIB=libz.a
# Compile wheels, we only support 35-39.
"/opt/python/cp35-cp35m/bin/pip" wheel /io/ --no-deps -w /io/wheelhouse_tmp
"/opt/python/cp36-cp36m/bin/pip" wheel /io/ --no-deps -w /io/wheelhouse_tmp
"/opt/python/cp37-cp37m/bin/pip" wheel /io/ --no-deps -w /io/wheelhouse_tmp
"/opt/python/cp38-cp38/bin/pip" wheel /io/ --no-deps -v -w /io/wheelhouse_tmp
"/opt/python/cp39-cp39/bin/pip" wheel /io/ --no-deps -w /io/wheelhouse_tmp

# Bundle external shared libraries into the wheels
for whl in /io/wheelhouse_tmp/*.whl; do
    repair_wheel "$whl" /io/dist
done

rm -rf /io/myclang/clang_fake_root
rm -rf /io/wheelhouse_tmp