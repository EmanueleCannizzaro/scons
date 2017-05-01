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

__revision__ = "test/VariantDir/CPPPATH-subdir.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test handling of the current directory (.) in CPPPATH when
the include path contains a subdirectory.

This tests for a regression found in 0.96.90 by Chad Austin.
"""

import TestSCons

test = TestSCons.TestSCons()

test.subdir('src', ['src', 'glscry'])

test.write('SConstruct', """\
env = Environment()
Export('env')
SConscript(dirs=['src'], variant_dir='build', duplicate=0)
""")


test.write(['src', 'SConscript'], """\
SConscript(dirs=['glscry'])
""")


test.write(['src', 'glscry', 'SConscript'], """\
Import('*')
env = env.Clone()
env.Append(CPPPATH=['.'])
env.Library('foo', 'foo.c')
""")

test.write(['src', 'glscry', 'foo.c'], """\
#include <foo.h>
int foo(void) { return 0; }
""")


test.write(['src', 'glscry', 'foo.h'], "\n")

test.run(arguments = '.',
         stderr = TestSCons.noisy_ar,
         match = TestSCons.match_re_dotall)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
