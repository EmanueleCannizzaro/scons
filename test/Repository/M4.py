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

__revision__ = "test/Repository/M4.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test that $M4 and $M4FLAGS work with repositories.
"""

import os

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()

test.subdir('work', 'repository', ['repository', 'src'])

test.write('mym4.py', """
import sys
contents = sys.stdin.read()
sys.stdout.write(contents.replace('M4', 'mym4.py'))
sys.exit(0)
""")

mym4_py = test.workpath('mym4.py')



opts = "-Y " + test.workpath('repository')

test.write(['repository', 'SConstruct'], """\
env = Environment(M4 = r'%(_python_)s %(mym4_py)s', tools=['default', 'm4'])
env.M4(target = 'aaa.x', source = 'aaa.x.m4')
SConscript('src/SConscript', "env", variant_dir="build")
""" % locals())

test.write(['repository', 'aaa.x.m4'], """\
line 1
M4
line 3
""")

test.write(['repository', 'src', 'SConscript'], """
Import("env")
env.M4('bbb.y', 'bbb.y.m4')
""")

test.write(['repository', 'src', 'bbb.y.m4'], """\
line 1 M4
line 2
line 3 M4
""")

#
# Make the repository non-writable,
# so we'll detect if we try to write into it accidentally.
test.writable('repository', 0)

#
test.run(chdir = 'work', options = opts, arguments = ".")

expect_aaa_x = """\
line 1
mym4.py
line 3
"""

expect_bbb_y = """\
line 1 mym4.py
line 2
line 3 mym4.py
"""

test.fail_test(test.read(test.workpath('work', 'aaa.x'), 'r') != expect_aaa_x)
test.fail_test(test.read(test.workpath('work', 'build', 'bbb.y'), 'r') != expect_bbb_y)

#
test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
