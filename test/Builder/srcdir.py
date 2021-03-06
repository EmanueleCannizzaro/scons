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

__revision__ = "test/Builder/srcdir.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that specifying a srcdir when calling a Builder correctly
prefixes each relative-path string with the specified srcdir.
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()

test.subdir('src', ['src', 'foo'])

file3 = test.workpath('file3')

test.write(['src', 'cat.py'], """\
import sys
o = open(sys.argv[1], 'wb')
for f in sys.argv[2:]:
    o.write(open(f, 'rb').read())
o.close()
""")

test.write(['src', 'SConstruct'], """\
Command('output',
        ['file1', File('file2'), r'%(file3)s', 'file4'],
        r'%(_python_)s cat.py $TARGET $SOURCES',
        srcdir='foo')
""" % locals())

test.write(['src', 'foo', 'file1'],     "file1\n")

test.write(['src', 'file2'],            "file2\n")

test.write(file3,                       "file3\n")

test.write(['src', 'foo', 'file4'],     "file4\n")

test.run(chdir = 'src', arguments = '.')

expected = """\
file1
file2
file3
file4
"""

test.must_match(['src', 'output'],  expected)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
