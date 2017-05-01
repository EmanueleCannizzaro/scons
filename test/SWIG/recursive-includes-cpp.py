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

__revision__ = "test/SWIG/recursive-includes-cpp.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that SWIG include directives produce the correct dependencies
in cases of recursive inclusion.
"""

import os
import TestSCons
from SCons.Defaults import DefaultEnvironment

DefaultEnvironment( tools = [ 'swig' ] )

test = TestSCons.TestSCons()

# Check for prerequisites of this test.
for pre_req in ['swig', 'python']:
    if not test.where_is(pre_req):
        test.skip_test('Can not find installed "' + pre_req + '", skipping test.%s' % os.linesep)

test.write("recursive.h", """\
/* An empty header file. */
""")

test.write("main.h", """\
#include "recursive.h"
""")

test.write("main.c", """\
#include "main.h"
""")

test.write("mod.i", """\
%module mod

%include "main.h"

#include "main.h"
""")

test.write('SConstruct', """\
import distutils.sysconfig

DefaultEnvironment( tools = [ 'swig' ] )

env = Environment(
    SWIGFLAGS = [
        '-python'
    ],
    CPPPATH = [ 
        distutils.sysconfig.get_python_inc()
    ],
    SHLIBPREFIX = ""
)

env.SharedLibrary(
    'mod.so',
    [
        "mod.i",
        "main.c",
    ]
)
""")

expectMain = """\
+-main.os
  +-main.c
  +-main.h
  +-recursive.h"""

expectMod = """\
+-mod_wrap.os
  +-mod_wrap.c
  | +-mod.i
  | +-main.h
  | +-recursive.h"""

# Validate that the recursive dependencies are found with SWIG scanning first.
test.run( arguments = '--tree=all mod_wrap.os main.os' )

test.must_contain_all( test.stdout(), expectMain )
test.must_contain_all( test.stdout(), expectMod )

# Validate that the recursive dependencies are found consistently.
test.run( arguments = '--tree=all main.os mod_wrap.os' )

test.must_contain_all( test.stdout(), expectMain )
test.must_contain_all( test.stdout(), expectMod )

test.run()
test.up_to_date()

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
