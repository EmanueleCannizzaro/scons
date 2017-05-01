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

__revision__ = "test/SWIG/SWIGPATH.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that use of SWIGPATH finds dependency files in subdirectories.
"""

import TestSCons

test = TestSCons.TestSCons()

swig = test.where_is('swig')
if not swig:
    test.skip_test('Can not find installed "swig", skipping test.\n')

python = test.where_is('python')
if not python:
    test,skip_test('Can not find installed "python", skipping test.\n')


test.subdir('inc1', 'inc2')

test.write(['inc2', 'dependency.i'], """\
%module dependency
""")

test.write("dependent.i", """\
%module dependent

%include dependency.i
""")

test.write('SConstruct', """
foo = Environment(SWIGFLAGS='-python',
                  SWIG='%(swig)s',
                  SWIGPATH=['inc1', 'inc2'])
swig = foo.Dictionary('SWIG')
bar = foo.Clone(SWIG = [r'%(python)s', 'wrapper.py', swig])
foo.CFile(target = 'dependent', source = ['dependent.i'])
""" % locals())

test.run()

test.up_to_date(arguments = "dependent_wrap.c")

test.write(['inc1', 'dependency.i'], """\
%module dependency

extern char *dependency_1();
""")

test.not_up_to_date(arguments = "dependent_wrap.c")

test.write(['inc2', 'dependency.i'], """\
%module dependency
extern char *dependency_2();
""")

test.up_to_date(arguments = "dependent_wrap.c")

test.unlink(['inc1', 'dependency.i'])

test.not_up_to_date(arguments = "dependent_wrap.c")

test.up_to_date(arguments = "dependent_wrap.c")



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: