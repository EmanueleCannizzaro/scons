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

__revision__ = "test/Ghostscript/GSFLAGS.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import os
import sys

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('mygs.py', r"""
import getopt
import os
import sys
cmd_opts, args = getopt.getopt(sys.argv[1:], 's:x', [])
opt_string = ''
for opt, arg in cmd_opts:
    if opt == '-s':
        if arg[:11] == 'OutputFile=':
            out_file = open(arg[11:], 'wb')
    else:
        opt_string = opt_string + ' ' + opt
infile = open(args[0], 'rb')
out_file.write(opt_string + "\n")
for l in infile.readlines():
    if l[:3] != '#ps':
        out_file.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(GS = r'%(_python_)s mygs.py', GSFLAGS = '-x',
                  tools = ['gs'])
env.PDF(target = 'test1.pdf', source = 'test1.ps')
""" % locals())

test.write('test1.ps', """\
This is a .ps test.
#ps
""")

test.run(arguments = '.', stderr = None)

test.fail_test(test.read('test1.pdf') != " -x\nThis is a .ps test.\n")



if sys.platform == 'win32':
    gs_executable = 'gswin32c'
elif sys.platform == 'os2':
    gs_executable = 'gsos2'
else:
    gs_executable = 'gs'
gs = test.where_is(gs_executable)

if gs:

    test.write("wrapper.py", """import os
import sys
cmd = " ".join(sys.argv[1:])
open('%s', 'ab').write("%%s\\n" %% cmd)
os.system(cmd)
""" % test.workpath('wrapper.out').replace('\\', '\\\\'))

    test.write('SConstruct', """\
import os
ENV = { 'PATH' : os.environ['PATH'] }
foo = Environment(ENV = ENV)
foo.Append(GSFLAGS = '-q')
foo.PDF(target = 'foo.pdf', source = 'foo.ps')
""")

    input = """\
%!PS-Adobe
100 100 moveto /Times-Roman findfont 24 scalefont (Hello, world!) show showpage
"""

    test.write('foo.ps', input)

    test.run(arguments = 'foo.pdf', stderr = None)

    test.fail_test(not os.path.exists(test.workpath('foo.pdf')))

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
