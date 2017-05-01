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

__revision__ = "test/LEX/LEXFLAGS.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import os

import TestSCons

_python_ = TestSCons._python_
_exe   = TestSCons._exe

test = TestSCons.TestSCons()

test.subdir('in')



test.write('mylex.py', """
import getopt
import sys
cmd_opts, args = getopt.getopt(sys.argv[1:], 'I:tx', [])
opt_string = ''
i_arguments = ''
for opt, arg in cmd_opts:
    if opt == '-I': i_arguments = i_arguments + ' ' + arg
    else: opt_string = opt_string + ' ' + opt
for a in args:
    contents = open(a, 'rb').read()
    contents = contents.replace('LEXFLAGS', opt_string)
    contents = contents.replace('I_ARGS', i_arguments)
    sys.stdout.write(contents)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(LEX = r'%(_python_)s mylex.py',
                  LEXFLAGS = '-x -I${TARGET.dir} -I${SOURCE.dir}',
                  tools=['default', 'lex'])
env.CFile(target = 'out/aaa', source = 'in/aaa.l')
""" % locals())

test.write(['in', 'aaa.l'],		"aaa.l\nLEXFLAGS\nI_ARGS\n")

test.run('.', stderr = None)

# Read in with mode='r' because mylex.py implicitley wrote to stdout
# with mode='w'.
test.must_match(['out', 'aaa.c'],	"aaa.l\n -x -t\n out in\n", mode='r')



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
