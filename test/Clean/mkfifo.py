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

__revision__ = "test/Clean/mkfifo.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that SCons reports an error when cleaning up a target directory
containing a named pipe created with o.mkfifo().
"""

import os

import TestSCons

test = TestSCons.TestSCons()

if not hasattr(os, 'mkfifo'):
    test.skip_test('No os.mkfifo() function; skipping test\n')

test.write('SConstruct', """\
Execute(Mkdir("testdir"))
dir = Dir("testdir")
Clean(dir, 'testdir')
""")

test.run(arguments='-Q -q', stdout='Mkdir("testdir")\n')

os.mkfifo('testdir/namedpipe')

expect1 = """\
Mkdir("testdir")
Path '%s' exists but isn't a file or directory.
scons: Could not remove 'testdir': Directory not empty
""" % os.path.join('testdir', 'namedpipe')

expect2 = """\
Mkdir("testdir")
Path '%s' exists but isn't a file or directory.
scons: Could not remove 'testdir': File exists
""" % os.path.join('testdir', 'namedpipe')

test.run(arguments='-c -Q -q')

if test.stdout() not in [expect1, expect2]:
    test.diff(expect1, test.stdout(), 'STDOUT ')
    test.fail_test()
 
test.must_exist(test.workpath('testdir/namedpipe'))

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
