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
__revision__ = "test/Interactive/Default-None.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that we get the expected error message when we use a "build"
command without arguments and there are no default targets (because they
explicitly called Default(None) in the SConstruct file).
"""

import TestSCons

test = TestSCons.TestSCons(combine=1)

test.write('SConstruct', """\
Command('foo.out', 'foo.in', Copy('$TARGET', '$SOURCE'))
Default(None)
Command('1', [], Touch('$TARGET'))
Command('2', [], Touch('$TARGET'))
""")

test.write('foo.in', "foo.in 1\n")



scons = test.start(arguments = '-Q --interactive')

scons.send("build\n")

scons.send("build foo.out\n")

scons.send("build 1\n")

test.wait_for(test.workpath('1'))

test.must_match(test.workpath('foo.out'), "foo.in 1\n")



test.write('foo.in', "foo.in 2\n")

# Verify that "scons" can be used as a synonmyn for the "build" command.
scons.send("scons\n")

scons.send("scons foo.out\n")

scons.send("build 2\n")

test.wait_for(test.workpath('2'))

test.must_match(test.workpath('foo.out'), "foo.in 2\n")



scons.send("build\n")

scons.send("build foo.out\n")

expect_stdout = """\
scons>>> scons: *** No targets specified and no Default() targets found.  Stop.
scons>>> Copy("foo.out", "foo.in")
scons>>> Touch("1")
scons>>> scons: *** No targets specified and no Default() targets found.  Stop.
scons>>> Copy("foo.out", "foo.in")
scons>>> Touch("2")
scons>>> scons: *** No targets specified and no Default() targets found.  Stop.
scons>>> scons: `foo.out' is up to date.
scons>>> 
"""

test.finish(scons, stdout = expect_stdout)



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
