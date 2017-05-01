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

__revision__ = "test/Configure/SConscript.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that Configure contexts from multiple subsidiary SConscript
files work without error.
"""

import TestSCons

test = TestSCons.TestSCons()

test.subdir(['dir1'],
            ['dir2'],
            ['dir2', 'sub1'],
            ['dir2', 'sub1', 'sub2'])

test.write('SConstruct', """\
env = Environment()
SConscript(dirs=['dir1', 'dir2'], exports="env")
""")

test.write(['dir1', 'SConscript'], """
Import("env")
conf = env.Configure()
conf.Finish()
""")

test.write(['dir2', 'SConscript'], """
Import("env")
conf = env.Configure()
conf.Finish()
SConscript(dirs=['sub1'], exports="env")
""")

test.write(['dir2', 'sub1', 'SConscript'], """
Import("env")
conf = env.Configure()
conf.Finish()
SConscript(dirs=['sub2'], exports="env")
""")

test.write(['dir2', 'sub1', 'sub2', 'SConscript'], """
Import("env")
conf = env.Configure()
conf.Finish()
""")

test.run()

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: