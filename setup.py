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
from typing import Optional

from ccimport import compat
from ccimport.extension import (AutoImportExtension, CCImportBuild,
                                CCImportExtension)
from setuptools import Command, find_packages, setup

# Package meta-data.
NAME = 'myclang'
DESCRIPTION = 'standalone libclang code with some modifications'
URL = 'https://github.com/FindDefinition/myclang'
EMAIL = 'yanyan.sub@outlook.com'
AUTHOR = 'Yan Yan'
REQUIRES_PYTHON = '>=3.6'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "ccimport>=0.1.2",
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
    path = get_executable_path("clang")
    clang_folder = os.getenv("CLANG_LIBRARY_PATH", None)
    if clang_folder:
        return Path(clang_folder)
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

    CLANG_ROOT = get_clang_root()
    assert CLANG_ROOT is not None, "can't find clang, install clang first."
    cmdclass = {
        'upload': UploadCommand,
        'build_ext': CCImportBuild,
    }
    LIBCLANG_SOURCES = list((LIBCLANG_MODULE_PATH / "libclang").glob("*.cpp"))
    print(len(LIBCLANG_SOURCES))
    libclang_ext = CCImportExtension(
        "myclang",
        LIBCLANG_SOURCES,
        "myclang/cext/myclang",
        includes=[CLANG_ROOT / "include"],
        libpaths=[CLANG_ROOT / "lib"],
        libraries=LIBCLANG_BUILD_META["libraries"],
        compile_options=LIBCLANG_BUILD_META["cflags"],
        link_options=LIBCLANG_BUILD_META["ldflags"],
        build_ctype=True,
        std="c++14",
    )
    flags = []
    if not compat.InWindows:
        flags.append("-Wl,-rpath,{}".format("."))

    clangutils_ext = AutoImportExtension(
        "clangutils",
        [LIBCLANG_MODULE_PATH / "clangutils.cc"],
        "myclang/cext/clangutils",
        includes=[CLANG_ROOT / "include"],
        libpaths=["{extdir}/myclang/cext"],
        libraries=["myclang"],
        link_options=flags,
        std="c++14",
    )
    ext_modules = [libclang_ext, clangutils_ext]

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
