#!/usr/bin/python
# Copyright (C) 2009 Julian Andres Klode <jak@debian.org>
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.
"""Run all available unit tests."""
import os
import unittest
import sys

# workaround for py3.2 that apparently does not have this anymore
# it has "abiflags" 
if not hasattr(sys, "pydebug"):
    if sys.abiflags.startswith("d"):
        sys.pydebug = True
    else:
        sys.pydebug = False

def get_library_dir():
    # Find the path to the built apt_pkg and apt_inst extensions
    if not os.path.exists("../build"):
        return None
    from distutils.util import get_platform
    from distutils.sysconfig import get_python_version
    # Set the path to the build directory.
    plat_specifier = ".%s-%s" % (get_platform(), get_python_version())
    if sys.version_info[0] >= 3 or sys.version_info[1] >= 6:
        library_dir = "../build/lib%s%s" % (plat_specifier,
                                            (sys.pydebug and "-pydebug" or ""))
    else:
        library_dir = "../build/lib%s%s" % ((sys.pydebug and "_d" or ""),
                                            plat_specifier)
    return os.path.abspath(library_dir)

if __name__ == '__main__':
    if not os.access("/etc/apt/sources.list", os.R_OK):
        sys.stderr.write("[tests] Skipping because sources.list is not readable\n")
        sys.exit(0)

    sys.stderr.write("[tests] Running on %s\n" % sys.version.replace("\n", ""))
    dirname = os.path.dirname(__file__)
    if dirname:
        os.chdir(dirname)
    library_dir = get_library_dir()
    sys.stderr.write("Using library_dir: '%s'" % library_dir)
    if library_dir:
        sys.path.insert(0, os.path.abspath(library_dir))

    for path in os.listdir('.'):
        if path.endswith('.py') and os.path.isfile(path):
            exec('from %s import *' % path[:-3])

    unittest.main()
