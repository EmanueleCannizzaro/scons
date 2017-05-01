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

__revision__ = "test/RPATH.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import sys
import TestSCons

_exe = TestSCons._exe

test = TestSCons.TestSCons()

if sys.platform in ['cygwin', 'win32']:
    msg = "Can not test RPATH on '%s', skipping test.\n" % sys.platform
    test.skip_test(msg)

foo = test.workpath('foo' + _exe)

test.subdir('bar')

test.write('SConstruct', """\
SConscript('bar/SConscript')
Program('foo', 'foo.c', LIBS='bar', LIBPATH='bar', RPATH='bar')
""")

test.write('foo.c', """\
#include <stdlib.h>
int main() {
    void bar();
    bar();
    exit (0);
}
""")

test.write(['bar', 'SConscript'], """\
SharedLibrary('bar', 'bar.c')
""")

test.write(['bar', 'bar.c'], """\
#include <stdio.h>
void bar() {
    puts("bar");
}
""")

test.run(arguments='.')

test.run(program=foo, chdir=test.workpath('.'), stdout='bar\n')

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
