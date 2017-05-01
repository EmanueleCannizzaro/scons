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

__revision__ = "test/SWIG/noproxy.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that SCons realizes the -noproxy option means no .py file will
be created.
"""

import os
import sys

import TestSCons

# swig-python expects specific filenames.
# the platform specific suffix won't necessarily work.
if sys.platform == 'win32':
    _dll = '.dll'
else:
    _dll   = '.so' 

test = TestSCons.TestSCons()

swig = test.where_is('swig')
if not swig:
    test.skip_test('Can not find installed "swig", skipping test.\n')

python, python_include, python_libpath, python_lib = \
             test.get_platform_python_info()
Python_h = os.path.join(python_include, 'Python.h')
if not os.path.exists(Python_h):
    test.skip_test('Can not find %s, skipping test.\n' % Python_h)

# handle testing on other platforms:
ldmodule_prefix = '_'

test.write("dependency.i", """\
%module dependency
""")

test.write("dependent.i", """\
%module dependent

%include dependency.i
""")

test.write('SConstruct', """
foo = Environment(SWIGFLAGS=['-python', '-noproxy'],
                  CPPPATH=[r'%(python_include)s'],
                  LDMODULEPREFIX='%(ldmodule_prefix)s',
                  LDMODULESUFFIX='%(_dll)s',
                  SWIG=[r'%(swig)s'],
                  LIBPATH=[r'%(python_libpath)s'],
                  LIBS='%(python_lib)s',
                  )

swig = foo.Dictionary('SWIG')
bar = foo.Clone(SWIG = [r'%(python)s', 'wrapper.py', swig])
foo.CFile(target = 'dependent', source = ['dependent.i'])
""" % locals())

test.run(arguments = '.')

# If we mistakenly depend on the .py file that SWIG didn't create
# (suppressed by the -noproxy option) then the build won't be up-to-date.
test.up_to_date(arguments = '.')



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
