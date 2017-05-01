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

__revision__ = "test/LINK/SHLINK.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import os

import TestSCons

_python_ = TestSCons._python_
dll_   = TestSCons.dll_
_shlib = TestSCons._dll

test = TestSCons.TestSCons()

test.write("wrapper.py",
"""import os
import sys
open('%s', 'wb').write("wrapper.py\\n")
os.system(" ".join(sys.argv[1:]))
""" % test.workpath('wrapper.out').replace('\\', '\\\\'))

test.write('SConstruct', """
foo = Environment()
shlink = foo.Dictionary('SHLINK')
bar = Environment(SHLINK = r'%(_python_)s wrapper.py ' + shlink)
foo.SharedLibrary(target = 'foo', source = 'foo.c')
bar.SharedLibrary(target = 'bar', source = 'bar.c')
""" % locals())

test.write('foo.c', r"""
#include <stdio.h>

void
test()
{
        printf("foo.c\n");
        fflush(stdout);
}
""")

test.write('bar.c', r"""
#include <stdio.h>

void
test()
{
        printf("foo.c\n");
        fflush(stdout);
}
""")

test.run(arguments = dll_ + 'foo' + _shlib)

test.fail_test(os.path.exists(test.workpath('wrapper.out')))

test.run(arguments = dll_ + 'bar' + _shlib)

test.fail_test(test.read('wrapper.out') != "wrapper.py\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
