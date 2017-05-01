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

__revision__ = "test/custom-concat.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that _stripixes() can use a custom _concat() function through
the construction environment.
"""

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
def my_concat1(pref, list, suff, env, f=None):
    if f:
        list = f(list)
    list = ['my'+pref+x+suff+'1' for x in list]
    return list
myflags = '${_stripixes(MYPREFIX, LIST, MYSUFFIX, STRIPPREFIX, STRIPSUFFIX, __env__)}'
env1 = Environment(MYFLAGS=myflags, _concat = my_concat1,
                   MYPREFIX='p', MYSUFFIX='s',
                   STRIPPREFIX='xxx', STRIPSUFFIX='yyy',
                   LIST=['a', 'xxxb', 'cyyy', 'd'])
print env1.subst('$MYFLAGS')
""")

expect = test.wrap_stdout(read_str = "mypas1 mypbs1 mypcs1 mypds1\n",
                          build_str = "scons: `.' is up to date.\n")
test.run(arguments = '.', stdout = expect)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
