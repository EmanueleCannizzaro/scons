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

__revision__ = "test/CacheDir/SideEffect.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test that use of SideEffect() doesn't interfere with CacheDir.
"""

import TestSCons

test = TestSCons.TestSCons()

test.subdir('cache', 'work')

cache = test.workpath('cache')

test.write(['work', 'SConstruct'], """\
def copy(source, target):
    open(target, "wb").write(open(source, "rb").read())

def build(env, source, target):
    s = str(source[0])
    t = str(target[0])
    copy(s, t)
    if target[0].side_effects:
        side_effect = open(str(target[0].side_effects[0]), "ab")
        side_effect.write(s + ' -> ' + t + '\\n')

CacheDir(r'%(cache)s')

Build = Builder(action=build)
env = Environment(BUILDERS={'Build':Build}, SUBDIR='subdir')
env.Build('f1.out', 'f1.in')
env.Build('f2.out', 'f2.in')
env.Build('f3.out', 'f3.in')
SideEffect('log.txt', ['f1.out', 'f2.out', 'f3.out'])
""" % locals())

test.write(['work', 'f1.in'], 'f1.in\n')
test.write(['work', 'f2.in'], 'f2.in\n')
test.write(['work', 'f3.in'], 'f3.in\n')

test.run(chdir='work', arguments='f1.out f2.out')

expect = """\
f1.in -> f1.out
f2.in -> f2.out
"""

test.must_match(['work', 'log.txt'], expect)



test.write(['work', 'f2.in'], 'f2.in 2 \n')

test.run(chdir='work', arguments='log.txt')

expect = """\
f1.in -> f1.out
f2.in -> f2.out
f2.in -> f2.out
f3.in -> f3.out
"""

test.must_match(['work', 'log.txt'], expect)



test.write(['work', 'f1.in'], 'f1.in 2 \n')

test.run(chdir='work', arguments=".")

expect = """\
f1.in -> f1.out
f2.in -> f2.out
f2.in -> f2.out
f3.in -> f3.out
f1.in -> f1.out
"""

test.must_match(['work', 'log.txt'], expect)



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
