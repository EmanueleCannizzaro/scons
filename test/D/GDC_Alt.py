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

#  Amended by Russel Winder <russel@russel.org.uk> 2010-05-05

__revision__ = "test/D/GDC_Alt.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import TestSCons

_exe = TestSCons._exe
test = TestSCons.TestSCons()

if not test.where_is('gdc'):
    test.skip_test("Could not find 'gdc', skipping test.\n")

test.write('SConstruct', """\
import os
env = Environment(tools=['gdc', 'link'])
if env['PLATFORM'] == 'cygwin': env['OBJSUFFIX'] = '.obj'  # trick DMD
env.Program('foo', 'foo.d')
""")

test.write('foo.d', """\
import std.stdio;
int main(string[] args) {
    printf("Hello!");
    return 0;
}
""")

test.run()

test.run(program=test.workpath('foo'+_exe))

test.fail_test(not test.stdout() == 'Hello!')

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
