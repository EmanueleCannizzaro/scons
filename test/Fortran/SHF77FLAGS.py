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

__revision__ = "test/Fortran/SHF77FLAGS.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import TestSCons

_python_ = TestSCons._python_

_obj = TestSCons._shobj
obj_ = TestSCons.shobj_

test = TestSCons.TestSCons()



test.write('myg77.py', r"""
import getopt
import sys
opts, args = getopt.getopt(sys.argv[1:], 'cf:K:o:x')
optstring = ''
for opt, arg in opts:
    if opt == '-o': out = arg
    elif opt not in ('-f', '-K'): optstring = optstring + ' ' + opt
infile = open(args[0], 'rb')
outfile = open(out, 'wb')
outfile.write(optstring + "\n")
for l in infile.readlines():
    if l[:4] != '#g77':
        outfile.write(l)
sys.exit(0)
""")



test.write('SConstruct', """
env = Environment(SHF77 = r'%(_python_)s myg77.py')
env.Append(SHF77FLAGS = '-x')
env.SharedObject(target = 'test09', source = 'test09.f77')
env.SharedObject(target = 'test10', source = 'test10.F77')
""" % locals())

test.write('test09.f77', "This is a .f77 file.\n#g77\n")
test.write('test10.F77', "This is a .F77 file.\n#g77\n")

test.run(arguments = '.', stderr = None)

test.must_match(obj_ + 'test09' + _obj, " -c -x\nThis is a .f77 file.\n")
test.must_match(obj_ + 'test10' + _obj, " -c -x\nThis is a .F77 file.\n")


fc = 'f77'
g77 = test.detect_tool(fc)

if g77:

    test.write("wrapper.py",
"""import os
import sys
open('%s', 'wb').write("wrapper.py\\n")
os.system(" ".join(sys.argv[1:]))
""" % test.workpath('wrapper.out').replace('\\', '\\\\'))

    test.write('SConstruct', """
foo = Environment(SHF77 = '%(fc)s')
shf77 = foo.Dictionary('SHF77')
bar = foo.Clone(SHF77 = r'%(_python_)s wrapper.py ' + shf77,
                tools = ["default", 'f77'], F77FILESUFFIXES = [".f"])
bar.Append(SHF77FLAGS = '-Ix')
foo.SharedLibrary(target = 'foo/foo', source = 'foo.f')
bar.SharedLibrary(target = 'bar/bar', source = 'bar.f')
""" % locals())

    test.write('foo.f', r"""
      PROGRAM FOO
      PRINT *,'foo.f'
      STOP
      END
""")

    test.write('bar.f', r"""
      PROGRAM BAR
      PRINT *,'bar.f'
      STOP
      END
""")


    test.run(arguments = 'foo', stderr = None)

    test.must_not_exist('wrapper.out')

    import sys
    if sys.platform[:5] == 'sunos':
        test.run(arguments = 'bar', stderr = None)
    else:
        test.run(arguments = 'bar')

    test.must_match('wrapper.out', "wrapper.py\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
