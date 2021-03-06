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

__revision__ = "test/YACC/YACCVCGFILESUFFIX.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test setting the YACCVCGFILESUFFIX variable.
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('myyacc.py', """\
import getopt
import os.path
import sys
vcg = None
opts, args = getopt.getopt(sys.argv[1:], 'go:')
for o, a in opts:
    if o == '-g':
        vcg = 1
    elif o == '-o':
        outfile = open(a, 'wb')
for f in args:
    infile = open(f, 'rb')
    for l in [l for l in infile.readlines() if l != '/*yacc*/\\n']:
        outfile.write(l)
outfile.close()
if vcg:
    base, ext = os.path.splitext(args[0])
    open(base+'.vcgsuffix', 'wb').write(" ".join(sys.argv)+'\\n')
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(tools=['default', 'yacc'],
                  YACC = r'%(_python_)s myyacc.py',
                  YACCVCGFILESUFFIX = '.vcgsuffix')
env.CXXFile(target = 'aaa', source = 'aaa.yy')
env.CXXFile(target = 'bbb', source = 'bbb.yy', YACCFLAGS = '-g')
""" % locals())

test.write('aaa.yy', "aaa.yy\n/*yacc*/\n")
test.write('bbb.yy', "bbb.yy\n/*yacc*/\n")

test.run(arguments = '.')

test.must_match('aaa.cc', "aaa.yy\n")
test.must_not_exist('aaa.vcg')
test.must_not_exist('aaa.vcgsuffix')

test.must_match('bbb.cc', "bbb.yy\n")
test.must_not_exist('bbb.vcg')
test.must_match('bbb.vcgsuffix', "myyacc.py -g -o bbb.cc bbb.yy\n")

test.up_to_date(arguments = '.')



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
