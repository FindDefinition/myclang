#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import json
import os
import subprocess
import sys
from pathlib import Path
from shutil import rmtree
import shutil
from typing import Optional, Union

from ccimport import compat
from ccimport.extension import (AutoImportExtension, CCImportBuild,
                                CCImportExtension, ExtCallback)
from setuptools import Command, find_packages, setup

# Package meta-data.
NAME = 'myclang'
DESCRIPTION = 'standalone libclang code with some modifications'
URL = 'https://github.com/FindDefinition/myclang'
EMAIL = 'yanyan.sub@outlook.com'
AUTHOR = 'Yan Yan'
REQUIRES_PYTHON = '>=3.5'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "ccimport>=0.1.11",
]
if sys.version_info[:2] == (3, 6):
    REQUIRED.append("dataclasses")

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open('version.txt', 'r') as f:
        version = f.read().strip()
else:
    version = VERSION
cwd = os.path.dirname(os.path.abspath(__file__))


def _convert_build_number(build_number):
    parts = build_number.split(".")
    if len(parts) == 2:
        return "{}{:03d}".format(int(parts[0]), int(parts[1]))
    elif len(parts) == 1:
        return build_number
    else:
        raise NotImplementedError


env_suffix = os.environ.get("CCIMPORT_VERSION_SUFFIX", "")
if env_suffix != "":
    version += ".dev{}".format(_convert_build_number(env_suffix))
version_path = os.path.join(cwd, NAME, '__version__.py')
about['__version__'] = version

with open(version_path, 'w') as f:
    f.write("__version__ = '{}'\n".format(version))
enable_jit = os.environ.get("MYCLANG_ENABLE_JIT", "1") == "1"
enable_jit_str = "True"
if not enable_jit:
    enable_jit_str = "False"
meta_path = os.path.join(cwd, NAME, 'build_meta.py')
with open(meta_path, 'w') as f:
    f.write("ENABLE_JIT = {}\n".format(enable_jit_str))

static_zlib_path = os.environ.get("MYCLANG_STATIC_ZLIB", None)
static_tinfo_path = os.environ.get("MYCLANG_STATIC_TINFO", None)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(
            sys.executable))

        self.status('Uploading the package to PyPI via Twine...')
        os.system('twine upload dist/*')

        self.status('Pushing git tags...')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()

class CreateLinkCallback(ExtCallback):
    def __call__(self, ext: Union["AutoImportExtension", "CCImportExtension"], extdir: Path, target_path: Path):
        clang_name = "clang"
        clangpp_name = "clang++"
        if compat.InWindows:
            clang_name = "clang.exe"
            clangpp_name = "clang++.exe"

        assert target_path.name == clang_name
        clangpp_p = extdir / "myclang" / "clang_fake_root" / "bin" / clangpp_name
        shutil.copy(str(target_path), str(clangpp_p))
        # permission denied when create symlink in windows. 
        # so we just copy them.

        # clangpp_p.symlink_to(target_path, False)


def get_executable_path(executable: str) -> str:
    if compat.InWindows:
        cmd = ["powershell.exe", "(Get-Command {}).Path".format(executable)]
    else:
        cmd = ["which", executable]
    try:
        out = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        return ""
    return out.decode("utf-8").strip()


def get_clang_root() -> Optional[Path]:
    clang_folder = os.getenv("LLVM_ROOT", None)
    if clang_folder:
        return Path(clang_folder)
    path = get_executable_path("clang")
    if path:
        clang_folder = Path(path).parent.parent / "lib"
    if clang_folder is None:
        return None
    return clang_folder.parent


if enable_jit:
    cmdclass = {
        'upload': UploadCommand,
    }
    ext_modules = []
else:
    LIBCLANG_MODULE_PATH = Path(__file__).parent / "myclang" / "cext"
    with (LIBCLANG_MODULE_PATH / "libclang.json").open("r") as f:
        LIBCLANG_BUILD_META_ALL = json.load(f)
    LIBCLANG_BUILD_META = LIBCLANG_BUILD_META_ALL[compat.OS.value]
    if 'tinfo' in LIBCLANG_BUILD_META["libraries"]:
        # currently tinfo static build have bug in manylinux docker
        LIBCLANG_BUILD_META["libraries"].remove('tinfo')

    if static_zlib_path is not None and "z" in LIBCLANG_BUILD_META["libraries"]:
        idx = LIBCLANG_BUILD_META["libraries"].index("z")
        if Path(static_zlib_path).is_absolute():
            LIBCLANG_BUILD_META["libraries"][idx] = "path::" + static_zlib_path
        else:
            LIBCLANG_BUILD_META["libraries"][idx] = "file::" + static_zlib_path
    if static_tinfo_path is not None and "tinfo" in LIBCLANG_BUILD_META["libraries"]:
        idx = LIBCLANG_BUILD_META["libraries"].index("tinfo")
        if Path(static_tinfo_path).is_absolute():
            LIBCLANG_BUILD_META["libraries"][idx] = "path::" + static_tinfo_path
        else:
            LIBCLANG_BUILD_META["libraries"][idx] = "file::" + static_tinfo_path

    CLANG_ROOT = get_clang_root()
    assert CLANG_ROOT is not None, "can't find clang, install clang first."
    cmdclass = {
        'upload': UploadCommand,
        'build_ext': CCImportBuild,
    }
    LIBCLANG_INCLUDE = LIBCLANG_MODULE_PATH.resolve() / "include"

    LIBCLANG_SOURCES = list((LIBCLANG_MODULE_PATH / "libclang").glob("*.cpp"))
    libclang_ext = CCImportExtension(
        "myclang",
        LIBCLANG_SOURCES,
        "myclang/cext/myclang",
        includes=[CLANG_ROOT / "include", LIBCLANG_INCLUDE],
        libpaths=[CLANG_ROOT / "lib"],
        libraries=LIBCLANG_BUILD_META["libraries"],
        compile_options=LIBCLANG_BUILD_META["cflags"],
        link_options=LIBCLANG_BUILD_META["ldflags"],
        build_ctype=True,
        std="c++14",
    )
    flags = []
    clang_main_flags = []
    if not compat.InWindows:
        flags.append("-Wl,--enable-new-dtags")
        # ninja need to escape dollar sign
        flags.append("-Wl,-rpath='$$ORIGIN'")
        clang_main_flags.append("-Wl,--enable-new-dtags")
        clang_main_flags.append("-Wl,-rpath='$$ORIGIN/../../cext'")

    clangutils_ext = AutoImportExtension(
        "clangutils",
        [LIBCLANG_MODULE_PATH / "clangutils.cc"],
        "myclang/cext/clangutils",
        includes=[CLANG_ROOT / "include", LIBCLANG_INCLUDE],
        libpaths=["{extdir}/myclang/cext"],
        libraries=["myclang"],
        link_options=flags,
        std="c++14",
    )
    clcompiler_ext = AutoImportExtension(
        "clcompiler",
        [LIBCLANG_MODULE_PATH / "clcompiler.cc"],
        "myclang/cext/clcompiler",
        includes=[CLANG_ROOT / "include", LIBCLANG_INCLUDE],
        libpaths=["{extdir}/myclang/cext"],
        libraries=["myclang"],
        link_options=flags,
        std="c++14",
    )
    compiler_path = "myclang/clang_fake_root/bin/clang"
    clang_compiler_ext = CCImportExtension(
        "clang",
        [LIBCLANG_MODULE_PATH / "clangmain.cc"],
        compiler_path,
        includes=[CLANG_ROOT / "include", LIBCLANG_INCLUDE],
        libpaths=["{extdir}/myclang/cext"],
        libraries=["myclang"],
        link_options=clang_main_flags,
        std="c++14",
        shared=False, 
        extcallback=CreateLinkCallback(),
    )

    ext_modules = [libclang_ext, clangutils_ext, clcompiler_ext, clang_compiler_ext]

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests', )),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    entry_points={
        'console_scripts': [],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    # $ setup.py publish support.
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
