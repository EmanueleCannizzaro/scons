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

__revision__ = "test/YACC/YACCHFILESUFFIX.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test that setting the YACCHFILESUFFIX variable can reflect a yacc
utility that writes to an odd
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('myyacc.py', """\
import getopt
import os.path
import sys
opts, args = getopt.getopt(sys.argv[1:], 'do:')
for o, a in opts:
    if o == '-o':
        outfile = open(a, 'wb')
for f in args:
    infile = open(f, 'rb')
    for l in [l for l in infile.readlines() if l != '/*yacc*/\\n']:
        outfile.write(l)
outfile.close()
base, ext = os.path.splitext(args[0])
open(base+'.hsuffix', 'wb').write(" ".join(sys.argv)+'\\n')
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(tools=['default', 'yacc'],
                  YACC = r'%(_python_)s myyacc.py',
                  YACCFLAGS = '-d',
                  YACCHFILESUFFIX = '.hsuffix')
env.CFile(target = 'aaa', source = 'aaa.y')
env.CFile(target = 'bbb', source = 'bbb.yacc')
""" % locals())

test.write('aaa.y', "aaa.y\n/*yacc*/\n")
test.write('bbb.yacc', "bbb.yacc\n/*yacc*/\n")

test.run(arguments = '.')

test.must_match('aaa.c', "aaa.y\n")
test.must_match('aaa.hsuffix', "myyacc.py -d -o aaa.c aaa.y\n")
test.must_match('bbb.c', "bbb.yacc\n")
test.must_match('bbb.hsuffix', "myyacc.py -d -o bbb.c bbb.yacc\n")

test.up_to_date(arguments = '.')



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
