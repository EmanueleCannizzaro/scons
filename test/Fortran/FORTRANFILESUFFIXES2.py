#!/usr/bin/env python
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

__revision__ = "test/Fortran/FORTRANFILESUFFIXES2.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import TestSCons

from common import write_fake_link

_python_ = TestSCons._python_
_exe   = TestSCons._exe

test = TestSCons.TestSCons()

write_fake_link(test)

test.write('myfortran.py', r"""
import getopt
import sys
comment = '#' + sys.argv[1]
opts, args = getopt.getopt(sys.argv[2:], 'co:')
for opt, arg in opts:
    if opt == '-o': out = arg
infile = open(args[0], 'rb')
outfile = open(out, 'wb')
for l in infile.readlines():
    if l[:len(comment)] != comment:
        outfile.write(l)
sys.exit(0)
""")

# Test non default file suffix: .f, .f90 and .f95 for FORTRAN
test.write('SConstruct', """
env = Environment(LINK = r'%(_python_)s mylink.py',
                  LINKFLAGS = [],
                  F77 = r'%(_python_)s myfortran.py g77',
                  FORTRAN = r'%(_python_)s myfortran.py fortran',
                  FORTRANFILESUFFIXES = ['.f', '.f95', '.f90', '.ffake'],
                  tools = ['default', 'fortran'])
#print env.Dump()
env.Program(target = 'test01', source = 'test01.f')
env.Program(target = 'test02', source = 'test02.f90')
env.Program(target = 'test03', source = 'test03.f95')
env.Program(target = 'test04', source = 'test04.ffake')
env.Program(target = 'test05', source = 'test05.f77')
""" % locals())

test.write('test01.f',   "This is a .f file.\n#link\n#fortran\n")
test.write('test02.f90',   "This is a .f90 file.\n#link\n#fortran\n")
test.write('test03.f95', "This is a .f95 file.\n#link\n#fortran\n")
test.write('test04.ffake', "This is a .ffake file.\n#link\n#fortran\n")
test.write('test05.f77', "This is a .f77 file.\n#link\n#g77\n")

test.run(arguments = '.', stderr = None)

test.must_match('test01' + _exe, "This is a .f file.\n")
test.must_match('test02' + _exe, "This is a .f90 file.\n")
test.must_match('test03' + _exe, "This is a .f95 file.\n")
test.must_match('test04' + _exe, "This is a .ffake file.\n")
test.must_match('test05' + _exe, "This is a .f77 file.\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
