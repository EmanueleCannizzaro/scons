#
# Copyright (c) 2001 - 2016 The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "src/engine/SCons/Scanner/LaTeXTests.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import SCons.compat

import collections
import os
import sys
import unittest

import TestCmd
import TestUnit

import SCons.Node.FS
import SCons.Scanner.LaTeX

test = TestCmd.TestCmd(workdir = '')

test.write('test1.latex',"""
\include{inc1}
\input{inc2}
include{incNO}
%\include{incNO}
xyzzy \include{inc6}
""")

test.write('test2.latex',"""
\include{inc1}
\include{inc3}
""")

test.write('test3.latex',"""
\includegraphics{inc4.eps}
\includegraphics[width=60mm]{inc5.xyz}
""")

test.subdir('subdir')

test.write('inc1.tex',"\n")
test.write('inc2.tex',"\n")
test.write(['subdir', 'inc3.tex'], "\n")
test.write(['subdir', 'inc4.eps'], "\n")
test.write('inc5.xyz', "\n")
test.write('inc6.tex', "\n")
test.write('incNO.tex', "\n")

# define some helpers:
#   copied from CTest.py
class DummyEnvironment(collections.UserDict):
    def __init__(self, **kw):
        collections.UserDict.__init__(self)
        self.data.update(kw)
        self.fs = SCons.Node.FS.FS(test.workpath(''))

    def Dictionary(self, *args):
        return self.data

    def subst(self, strSubst, target=None, source=None, conv=None):
        if strSubst[0] == '$':
            return self.data[strSubst[1:]]
        return strSubst

    def subst_list(self, strSubst, target=None, source=None, conv=None):
        if strSubst[0] == '$':
            return [self.data[strSubst[1:]]]
        return [[strSubst]]

    def subst_path(self, path, target=None, source=None, conv=None):
        if not isinstance(path, list):
            path = [path]
        return list(map(self.subst, path))

    def get_calculator(self):
        return None

    def get_factory(self, factory):
        return factory or self.fs.File

    def Dir(self, filename):
        return self.fs.Dir(filename)

    def File(self, filename):
        return self.fs.File(filename)

if os.path.normcase('foo') == os.path.normcase('FOO'):
    my_normpath = os.path.normcase
else:
    my_normpath = os.path.normpath

def deps_match(self, deps, headers):
    global my_normpath
    scanned = list(map(my_normpath, list(map(str, deps))))
    expect = list(map(my_normpath, headers))
    self.failUnless(scanned == expect, "expect %s != scanned %s" % (expect, scanned))


class LaTeXScannerTestCase1(unittest.TestCase):
    def runTest(self):
        env = DummyEnvironment(LATEXSUFFIXES = [".tex", ".ltx", ".latex"])
        s = SCons.Scanner.LaTeX.LaTeXScanner()
        path = s.path(env)
        deps = s(env.File('test1.latex'), env, path)
        headers = ['inc1.tex', 'inc2.tex', 'inc6.tex']
        deps_match(self, deps, headers)

class LaTeXScannerTestCase2(unittest.TestCase):
     def runTest(self):
         env = DummyEnvironment(TEXINPUTS=[test.workpath("subdir")],LATEXSUFFIXES = [".tex", ".ltx", ".latex"])
         s = SCons.Scanner.LaTeX.LaTeXScanner()
         path = s.path(env)
         deps = s(env.File('test2.latex'), env, path)
         headers = ['inc1.tex', 'subdir/inc3.tex']
         deps_match(self, deps, headers)

class LaTeXScannerTestCase3(unittest.TestCase):
     def runTest(self):
         env = DummyEnvironment(TEXINPUTS=[test.workpath("subdir")],LATEXSUFFIXES = [".tex", ".ltx", ".latex"])
         s = SCons.Scanner.LaTeX.LaTeXScanner()
         path = s.path(env)
         deps = s(env.File('test3.latex'), env, path)
         files = ['inc5.xyz', 'subdir/inc4.eps']
         deps_match(self, deps, files)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(LaTeXScannerTestCase1())
    suite.addTest(LaTeXScannerTestCase2())
    suite.addTest(LaTeXScannerTestCase3())
    return suite

if __name__ == "__main__":
    TestUnit.run(suite())

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
