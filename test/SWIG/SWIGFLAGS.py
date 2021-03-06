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

__revision__ = "test/SWIG/SWIGFLAGS.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that we can use ${SOURCE} expansions in $SWIGFLAGS.
"""

import sys
import TestSCons

test = TestSCons.TestSCons()

swig = test.where_is('swig')

if not swig:
    test.skip_test('Can not find installed "swig", skipping test.\n')



test.subdir('src')

test.write(['src', 'foo.i'], """\
%module foo

%include bar.i
""")

test.write(['src', 'bar.i'], """\
%module bar
""")

test.write('SConstruct', """
# Note that setting the -I option in $SWIGFLAGS is not good and the
# documentation says to use $SWIGPATH.  This is just for testing.
env = Environment(SWIGFLAGS='-python -I${SOURCE.dir}',
                  SWIG=r'%(swig)s')
env.CFile(target = 'foo', source = ['src/foo.i'])
""" % locals())

test.run()

test.up_to_date(arguments = "foo_wrap.c")



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
