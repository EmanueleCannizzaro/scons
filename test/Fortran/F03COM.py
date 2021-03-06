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

__revision__ = "test/Fortran/F03COM.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import TestSCons

from common import write_fake_link

_python_ = TestSCons._python_
_exe   = TestSCons._exe

test = TestSCons.TestSCons()

write_fake_link(test)

test.write('myfortran.py', r"""
import sys
comment = '#' + sys.argv[1]
outfile = open(sys.argv[2], 'wb')
infile = open(sys.argv[3], 'rb')
for l in infile.readlines():
    if l[:len(comment)] != comment:
        outfile.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(LINK = r'%(_python_)s mylink.py',
                  LINKFLAGS = [],
                  F03COM = r'%(_python_)s myfortran.py f03 $TARGET $SOURCES',
                  F03PPCOM = r'%(_python_)s myfortran.py f03pp $TARGET $SOURCES',
                  FORTRANCOM = r'%(_python_)s myfortran.py fortran $TARGET $SOURCES',
                  FORTRANPPCOM = r'%(_python_)s myfortran.py fortranpp $TARGET $SOURCES')
env.Program(target = 'test01', source = 'test01.f')
env.Program(target = 'test02', source = 'test02.F')
env.Program(target = 'test03', source = 'test03.for')
env.Program(target = 'test04', source = 'test04.FOR')
env.Program(target = 'test05', source = 'test05.ftn')
env.Program(target = 'test06', source = 'test06.FTN')
env.Program(target = 'test07', source = 'test07.fpp')
env.Program(target = 'test08', source = 'test08.FPP')
env.Program(target = 'test13', source = 'test13.f03')
env.Program(target = 'test14', source = 'test14.F03')
env2 = Environment(LINK = r'%(_python_)s mylink.py',
                   LINKFLAGS = [],
                   F03COM = r'%(_python_)s myfortran.py f03 $TARGET $SOURCES',
                   F03PPCOM = r'%(_python_)s myfortran.py f03pp $TARGET $SOURCES')
env2.Program(target = 'test21', source = 'test21.f03')
env2.Program(target = 'test22', source = 'test22.F03')
""" % locals())

test.write('test01.f',   "This is a .f file.\n#link\n#fortran\n")
test.write('test02.F',   "This is a .F file.\n#link\n#fortranpp\n")
test.write('test03.for', "This is a .for file.\n#link\n#fortran\n")
test.write('test04.FOR', "This is a .FOR file.\n#link\n#fortranpp\n")
test.write('test05.ftn', "This is a .ftn file.\n#link\n#fortran\n")
test.write('test06.FTN', "This is a .FTN file.\n#link\n#fortranpp\n")
test.write('test07.fpp', "This is a .fpp file.\n#link\n#fortranpp\n")
test.write('test08.FPP', "This is a .FPP file.\n#link\n#fortranpp\n")
test.write('test13.f03', "This is a .f03 file.\n#link\n#f03\n")
test.write('test14.F03', "This is a .F03 file.\n#link\n#f03pp\n")

test.write('test21.f03', "This is a .f03 file.\n#link\n#f03\n")
test.write('test22.F03', "This is a .F03 file.\n#link\n#f03pp\n")

test.run(arguments = '.', stderr = None)

test.must_match('test01' + _exe, "This is a .f file.\n")
test.must_match('test02' + _exe, "This is a .F file.\n")
test.must_match('test03' + _exe, "This is a .for file.\n")
test.must_match('test04' + _exe, "This is a .FOR file.\n")
test.must_match('test05' + _exe, "This is a .ftn file.\n")
test.must_match('test06' + _exe, "This is a .FTN file.\n")
test.must_match('test07' + _exe, "This is a .fpp file.\n")
test.must_match('test08' + _exe, "This is a .FPP file.\n")
test.must_match('test13' + _exe, "This is a .f03 file.\n")
test.must_match('test14' + _exe, "This is a .F03 file.\n")

test.must_match('test21' + _exe, "This is a .f03 file.\n")
test.must_match('test22' + _exe, "This is a .F03 file.\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
