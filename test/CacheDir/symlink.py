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

__revision__ = "test/CacheDir/symlink.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that we push and retrieve a built symlink to/from a CacheDir()
as an actualy symlink, not by copying the file contents.
"""

import os

import TestSCons

test = TestSCons.TestSCons()

if not hasattr(os, 'symlink'):
    import sys
    test.skip_test('%s has no os.symlink() method; skipping test\n' % sys.executable)

test.write('SConstruct', """\
CacheDir('cache')
import os
Symlink = Action(lambda target, source, env:
                        os.symlink(str(source[0]), str(target[0])),
                 "os.symlink($SOURCE, $TARGET)")
Command('file.symlink', 'file.txt', Symlink)
""")

test.write('file.txt', "file.txt\n")

test.run(arguments = '.')

test.fail_test(not os.path.islink('file.symlink'))
test.must_match('file.symlink', "file.txt\n")

test.run(arguments = '-c .')

test.must_not_exist('file.symlink')

test.run(arguments = '.')

test.fail_test(not os.path.islink('file.symlink'))
test.must_match('file.symlink', "file.txt\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
