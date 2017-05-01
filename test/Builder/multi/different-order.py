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

__revision__ = "test/Builder/multi/different-order.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that a "multi" builder can NOT be called multiple times with
target lists that have different orders.  This is intentional; the
order of the targets matter to the builder because the build command
can contain things like ${TARGET[0]}.
"""

import TestSCons

test = TestSCons.TestSCons(match=TestSCons.match_re)

test.write('SConstruct', """\
def build(env, target, source):
    for t in target:
        file = open(str(target[0]), 'wb')
        for s in source:
            file.write(open(str(s), 'rb').read())

B = Builder(action=build, multi=1)
env = Environment(BUILDERS = { 'B' : B })
env.B(target = ['file10a.out', 'file10b.out'], source = 'file10.in')
env.B(target = ['file10b.out', 'file10a.out'], source = 'file10.in')
""")

test.write('file10.in', 'file10.in\n')

expect = TestSCons.re_escape("""
scons: *** Two different target lists have a target in common: file10b.out  (from ['file10a.out', 'file10b.out'] and from ['file10b.out', 'file10a.out'])
""") + TestSCons.file_expr

test.run(arguments='file10.out', status=2, stderr=expect)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: