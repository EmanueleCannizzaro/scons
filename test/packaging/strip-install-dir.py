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

__revision__ = "test/packaging/strip-install-dir.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test stripping the InstallBuilder of the Package source file.
"""

import TestSCons

python = TestSCons.python

test = TestSCons.TestSCons()

tar = test.detect('TAR', 'tar')

if not tar:
    test.skip_test('tar not found, skipping test\n')

test.write( 'main.c', '' )
test.write('SConstruct', """
prog = Install( '/bin', 'main.c' )
env=Environment(tools=['default', 'packaging'])
env.Package( NAME    = 'foo',
             VERSION = '1.2.3',
             source  = [ prog ],
            )
""")

expected = """scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
Copy file(s): "main.c" to "foo-1.2.3/bin/main.c"
tar -zc -f foo-1.2.3.tar.gz foo-1.2.3/bin/main.c
scons: done building targets.
"""

test.run(arguments='', stderr = None, stdout=expected)

test.must_not_exist( 'bin/main.c' )
test.must_not_exist( '/bin/main.c' )

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
