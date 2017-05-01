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

__revision__ = "test/Builder/multi/same-overrides.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that everything works if two multi calls have the same overrides.
"""

import TestSCons

test = TestSCons.TestSCons(match=TestSCons.match_re)

_python_ = TestSCons._python_

test.write('build.py', r"""#!/usr/bin/env python
import sys
def build(num, target, source):
    file = open(str(target), 'wb')
    file.write('%s\n'%num)
    for s in source:
        file.write(open(str(s), 'rb').read())
build(sys.argv[1],sys.argv[2],sys.argv[3:])
""")

test.write('SConstruct', """\
B = Builder(action=r'%(_python_)s build.py $foo $TARGET $SOURCES', multi=1)
env = Environment(BUILDERS = { 'B' : B })
env.B(target = 'file4.out', source = 'file4a.in', foo=3)
env.B(target = 'file4.out', source = 'file4b.in', foo=3)
""" % locals())

test.write('file4a.in', 'file4a.in\n')
test.write('file4b.in', 'file4b.in\n')

expect = ("""
scons: warning: Two different environments were specified for target file4.out,
\tbut they appear to have the same action: %s build.py .foo .TARGET .SOURCES
""" % TestSCons.re_escape(_python_)) + TestSCons.file_expr

test.run(arguments='file4.out', stderr=expect)

test.must_match('file4.out', "3\nfile4a.in\nfile4b.in\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: