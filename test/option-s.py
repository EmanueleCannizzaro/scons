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

__revision__ = "test/option-s.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import os.path

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()

test.write('build.py', r"""
import sys
file = open(sys.argv[1], 'wb')
file.write("build.py: %s\n" % sys.argv[1])
file.close()
""")

test.write('SConstruct', """
MyBuild = Builder(action = r'%(_python_)s build.py $TARGET')
env = Environment(BUILDERS = { 'MyBuild' : MyBuild })
env.MyBuild(target = 'f1.out', source = 'f1.in')
env.MyBuild(target = 'f2.out', source = 'f2.in')
""" % locals())

test.write('f1.in', "f1.in\n")
test.write('f2.in', "f2.in\n")

test.run(arguments = '-s f1.out f2.out', stdout = "")
test.fail_test(not os.path.exists(test.workpath('f1.out')))
test.fail_test(not os.path.exists(test.workpath('f2.out')))

test.unlink('f1.out')
test.unlink('f2.out')

test.run(arguments = '--silent f1.out f2.out', stdout = "")
test.fail_test(not os.path.exists(test.workpath('f1.out')))
test.fail_test(not os.path.exists(test.workpath('f2.out')))

test.unlink('f1.out')
test.unlink('f2.out')

test.run(arguments = '--quiet f1.out f2.out', stdout = "")
test.fail_test(not os.path.exists(test.workpath('f1.out')))
test.fail_test(not os.path.exists(test.workpath('f2.out')))

# -C should also be quiet Issue#2796
test.subdir( 'sub' )
test.write(['sub','SConstruct'],"")
test.run(arguments = '-s -C sub', stdout = "" )

test.pass_test()
 

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
