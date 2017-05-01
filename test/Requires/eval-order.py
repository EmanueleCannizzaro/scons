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

__revision__ = "test/Requires/eval-order.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that env.Requires() nodes are evaluated before other children.
"""

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
def copy_and_create_func(target, source, env):
    fp = open(str(target[0]), 'wb')
    for s in source:
        fp.write(open(str(s), 'rb').read())
    fp.close()
    open('file.in', 'wb').write("file.in 1\\n")
    return None
copy_and_create = Action(copy_and_create_func)
env = Environment()
env.Requires('file.out', 'prereq.out')
env.Command('file.out', 'file.in', Copy('$TARGET', '$SOURCES'))
env.Command('prereq.out', 'prereq.in', copy_and_create)
""")

test.write('prereq.in', "prereq.in 1\n")

# First:  build file.out.  prereq.out should be built first, and if
# not, we'll get an error when the build action tries to use it to
# build file.out.

test.run(arguments = 'file.out')

test.must_match('prereq.out', "prereq.in 1\n")
test.must_match('file.out', "file.in 1\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
