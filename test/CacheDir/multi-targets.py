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

__revision__ = "test/CacheDir/multi-targets.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test that multiple target files get retrieved from a CacheDir correctly.
"""

import TestSCons

test = TestSCons.TestSCons()

test.subdir('cache', 'multiple')

cache = test.workpath('cache')

multiple_bar = test.workpath('multiple', 'bar')
multiple_foo = test.workpath('multiple', 'foo')

test.write(['multiple', 'SConstruct'], """\
def touch(env, source, target):
    open('foo', 'w').write("")
    open('bar', 'w').write("")
CacheDir(r'%(cache)s')
env = Environment()
env.Command(['foo', 'bar'], ['input'], touch)
""" % locals())

test.write(['multiple', 'input'], "multiple/input\n")

test.run(chdir = 'multiple')

test.must_exist(multiple_foo)
test.must_exist(multiple_bar)

test.run(chdir = 'multiple', arguments = '-c')

test.must_not_exist(multiple_foo)
test.must_not_exist(multiple_bar)

test.run(chdir = 'multiple')

test.must_exist(multiple_foo)
test.must_exist(multiple_bar)



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
