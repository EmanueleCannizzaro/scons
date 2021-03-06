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

__revision__ = "test/Fortran/SHF90COMSTR.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('myfc.py', r"""
import sys
fline = '#'+sys.argv[1]+'\n'
outfile = open(sys.argv[2], 'wb')
infile = open(sys.argv[3], 'rb')
for l in [l for l in infile.readlines() if l != fline]:
    outfile.write(l)
sys.exit(0)
""")

if not TestSCons.case_sensitive_suffixes('.f','.F'):
    f90pp = 'f90'
else:
    f90pp = 'f90pp'


test.write('SConstruct', """
env = Environment(SHF90COM = r'%(_python_)s myfc.py f90 $TARGET $SOURCES',
                  SHF90COMSTR = 'Building f90 $TARGET from $SOURCES',
                  SHF90PPCOM = r'%(_python_)s myfc.py f90pp $TARGET $SOURCES',
                  SHF90PPCOMSTR = 'Building f90pp $TARGET from $SOURCES',
                  SHOBJPREFIX='', SHOBJSUFFIX='.shobj')
env.SharedObject(source = 'test01.f90')
env.SharedObject(source = 'test02.F90')
""" % locals())

test.write('test01.f90',        "A .f90 file.\n#f90\n")
test.write('test02.F90',        "A .F90 file.\n#%s\n" % f90pp)

test.run(stdout = test.wrap_stdout("""\
Building f90 test01.shobj from test01.f90
Building %(f90pp)s test02.shobj from test02.F90
""" % locals()))

test.must_match('test01.shobj', "A .f90 file.\n")
test.must_match('test02.shobj', "A .F90 file.\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
