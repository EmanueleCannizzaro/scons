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

__revision__ = "test/overrides.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import TestSCons


test = TestSCons.TestSCons()


_python_ = TestSCons._python_

test.write('SConstruct', """
env = Environment(CCFLAGS='-DFOO', LIBS=['a'])
def build(target, source, env):
    print "env['CC'] =", env['CC']
    print "env['CCFLAGS'] =", env['CCFLAGS']
    print "env['LIBS'] =", env['LIBS']
builder = Builder(action=build, CC='buildcc', LIBS='buildlibs')
env['BUILDERS']['Build'] = builder

foo = env.Build('foo.out', 'foo.in',
                CC='mycc',
                CCFLAGS='$CCFLAGS -DBAR',
                LIBS = env['LIBS']+['b'])
bar = env.Build('bar.out', 'bar.in')
Default([foo, bar])
""")

test.write('foo.in', "foo.in\n")
test.write('bar.in', "bar.in\n")

test.run(arguments = "-Q", stdout = """\
build(["foo.out"], ["foo.in"])
env['CC'] = mycc
env['CCFLAGS'] = -DFOO -DBAR
env['LIBS'] = ['a', 'b']
build(["bar.out"], ["bar.in"])
env['CC'] = buildcc
env['CCFLAGS'] = -DFOO
env['LIBS'] = buildlibs
""")



test.write('SConstruct', """
env = Environment()
env.Program('hello', 'hello.c',
            CC=r'%(_python_)s mycc.py',
            LINK=r'%(_python_)s mylink.py',
            OBJSUFFIX='.not_obj',
            PROGSUFFIX='.not_exe')
""" % locals())

test.write('hello.c',"this ain't no c file!\n")

test.write('mycc.py',"""
open('hello.not_obj', 'wt').write('this is no object file!')
""")

test.write('mylink.py',"""
open('hello.not_exe', 'wt').write('this is not a program!')
""")

test.run(arguments='hello.not_exe')

assert test.read('hello.not_obj') == 'this is no object file!'
assert test.read('hello.not_exe') == 'this is not a program!'

test.up_to_date(arguments='hello.not_exe')



test.write('SConstruct', """\
env = Environment()
env.Program('goodbye', 'goodbye.c',
            CC=r'%(_python_)s mycc.py',
            LINK=r'%(_python_)s mylink.py',
            OBJSUFFIX='.not_obj',
            PROGSUFFIX='.not_exe',
            targets='ttt',
            sources='sss')
""" % locals())

test.write('goodbye.c',"this ain't no c file!\n")

test.write('mycc.py',"""
open('goodbye.not_obj', 'wt').write('this is no object file!')
""")

test.write('mylink.py',"""
open('goodbye.not_exe', 'wt').write('this is not a program!')
""")

test.run(arguments='goodbye.not_exe', stderr=None)
test.fail_test(not test.match_re(test.stderr(), r"""
scons: warning: Did you mean to use `(target|source)' instead of `(targets|sources)'\?
""" + TestSCons.file_expr + r"""
scons: warning: Did you mean to use `(target|source)' instead of `(targets|sources)'\?
""" + TestSCons.file_expr))

assert test.read('goodbye.not_obj') == 'this is no object file!'
assert test.read('goodbye.not_exe') == 'this is not a program!'



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
