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

__revision__ = "test/scons-time/func/function.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify use of the --func and --function options to select functions
other than the default _main().
"""

import TestSCons_time

test = TestSCons_time.TestSCons_time(match = TestSCons_time.match_re)

try:
    import pstats
except ImportError:
    test.skip_test('No pstats module, skipping test.\n')

test.profile_data('foo.prof', 'prof.py', '_main', """\
def f1():
    pass
def f3():
    pass
def _main():
    f1()
    f3()
""")

expect1 = r'\d.\d\d\d prof\.py:1\(f1\)' + '\n'
expect3 = r'\d.\d\d\d prof\.py:3\(f3\)' + '\n'

test.run(arguments = 'func --func f1 foo.prof', stdout = expect1)

test.run(arguments = 'func --function f3 foo.prof', stdout = expect3)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
