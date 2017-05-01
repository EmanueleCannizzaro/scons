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

__revision__ = "test/runtest/src.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that we find tests under the src/ tree only if they end
with *Tests.py.
"""

import os

import TestRuntest

test = TestRuntest.TestRuntest()

test.subdir(['src'],
            ['src', 'suite'])

pythonstring = TestRuntest.pythonstring
src_passTests_py = os.path.join('src', 'passTests.py')
src_suite_passTests_py = os.path.join('src', 'suite', 'passTests.py')

test.write_passing_test(['src', 'pass.py'])

test.write_passing_test(['src', 'passTests.py'])

test.write_passing_test(['src', 'suite', 'pass.py'])

test.write_passing_test(['src', 'suite', 'passTests.py'])

expect_stdout = """\
%(pythonstring)s -tt %(src_passTests_py)s
PASSING TEST STDOUT
%(pythonstring)s -tt %(src_suite_passTests_py)s
PASSING TEST STDOUT
""" % locals()

expect_stderr = """\
PASSING TEST STDERR
PASSING TEST STDERR
""" % locals()

test.run(arguments='-k src', stdout=expect_stdout, stderr=expect_stderr)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
