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

__revision__ = "test/Deprecated/Options/chdir.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that we can chdir() to the directory in which an Options
file lives by using the __name__ value.
"""

import TestSCons

test = TestSCons.TestSCons(match = TestSCons.match_re_dotall)

test.subdir('bin', 'subdir')

test.write('SConstruct', """\
opts = Options('../bin/opts.cfg', ARGUMENTS)
opts.Add('VARIABLE')
Export("opts")
SConscript('subdir/SConscript')
""")

SConscript_contents = """\
Import("opts")
env = Environment()
opts.Update(env)
print "VARIABLE =", repr(env['VARIABLE'])
"""

test.write(['bin', 'opts.cfg'], """\
import os
os.chdir(os.path.split(__name__)[0])
exec(open('opts2.cfg', 'rU').read())
""")

test.write(['bin', 'opts2.cfg'], """\
VARIABLE = 'opts2.cfg value'
""")

test.write(['subdir', 'SConscript'], SConscript_contents)

expect = """\
VARIABLE = 'opts2.cfg value'
"""

warnings = """
scons: warning: The Options class is deprecated; use the Variables class instead.
""" + TestSCons.file_expr

test.run(arguments = '-q -Q .', stdout=expect, stderr=warnings)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
