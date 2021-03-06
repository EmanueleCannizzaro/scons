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

__revision__ = "test/TAR/TARCOM.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test the ability to configure the $TARCOM construction variable.
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('mytar.py', r"""
import sys
outfile = open(sys.argv[1], 'wb')
infile = open(sys.argv[2], 'rb')
for l in [l for l in infile.readlines() if l != '/*tar*/\n']:
    outfile.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(TOOLS = ['tar'],
                  TARCOM = r'%(_python_)s mytar.py $TARGET $SOURCE')
env.Tar('test1.tar', 'test1.in')
""" % locals())

test.write('test1.in', """\
test1.in
/*tar*/
""")

test.run()

test.must_match('test1.tar', "test1.in\n")



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
