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

__revision__ = "test/RANLIB/RANLIBCOMSTR.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test that the $RANLIBCOMSTR construction variable allows you to
customize the displayed archive indexer string.
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()

ranlib = test.detect('RANLIB', 'ranlib')

if not ranlib:
    test.skip_test("Could not find 'ranlib', skipping test.\n")



test.write('myar.py', """
import sys
outfile = open(sys.argv[1], 'wb')
for f in sys.argv[2:]:
    infile = open(f, 'rb')
    for l in [l for l in infile.readlines() if l != '/*ar*/\\n']:
        outfile.write(l)
sys.exit(0)
""")

test.write('myranlib.py', """
import sys
lines = open(sys.argv[1], 'rb').readlines()
outfile = open(sys.argv[1], 'wb')
for l in [l for l in lines if l != '/*ranlib*/\\n']:
    outfile.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(tools=['default', 'ar'],
                  ARCOM = r'%(_python_)s myar.py $TARGET $SOURCES',
                  RANLIBCOM = r'%(_python_)s myranlib.py $TARGET',
                  RANLIBCOMSTR = 'Indexing $TARGET',
                  LIBPREFIX = '',
                  LIBSUFFIX = '.lib')
env.Library(target = 'output', source = ['file.1', 'file.2'])
""" % locals())

test.write('file.1', "file.1\n/*ar*/\n/*ranlib*/\n")
test.write('file.2', "file.2\n/*ar*/\n/*ranlib*/\n")

expect = test.wrap_stdout("""\
%(_python_)s myar.py output.lib file.1 file.2
Indexing output.lib
""" % locals())

test.run(stdout = expect)

test.must_match('output.lib', "file.1\nfile.2\n")



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
