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

__revision__ = "test/VariantDir/under.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test various combinations of variant_dir when the source directory is,
or is not, underneath the SConstruct directory.
"""

import TestSCons

test = TestSCons.TestSCons()

test.subdir('work', ['work', 'sub'], 'other')

test.write(['work', 'SConscript'], """\
f = Command("file.out", "file.in", Copy("$TARGET", "$SOURCE"))
Default(f)
""")

test.write(['work', 'file.in'], "work/file.in\n")



test.write(['work', 'sub', 'SConstruct'], """\
SConscript('../SConscript', variant_dir='build1')
""")

test.run(chdir='work/sub')

test.must_match(['work', 'sub', 'build1', 'file.out'], "work/file.in\n")



test.write(['work', 'sub', 'SConstruct'], """
SConscript('../SConscript', variant_dir='../build2')
""")

test.run(chdir='work/sub')

test.must_match(['work', 'build2', 'file.out'], "work/file.in\n")



test.write(['work', 'sub', 'SConstruct'], """
SConscript('../SConscript', variant_dir='../../build3')
""")

test.run(chdir='work/sub')

test.must_match(['build3', 'file.out'], "work/file.in\n")



test.write(['work', 'SConstruct'], """
SConscript('../other/SConscript', variant_dir='build4')
""")

test.write(['other', 'SConscript'], """\
f = Command("file.out", "file.in", Copy("$TARGET", "$SOURCE"))
Default(f)
""")

test.write(['other', 'file.in'], "other/file.in\n")

test.run(chdir='work')

test.must_match(['work', 'build4', 'file.out'], "other/file.in\n")



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
