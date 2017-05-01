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

__revision__ = "test/MSVC/pch-spaces-subdir.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify PCH works if variant dir has spaces in its name
"""

import time

import TestSCons

test = TestSCons.TestSCons(match = TestSCons.match_re)

test.skip_if_not_msvc()

test.write('Main.cpp', """\
#include "Precompiled.h"

int main()
{
    return testf();
}
""")

test.write('Precompiled.cpp', """\
#include "Precompiled.h"
""")

test.write('Precompiled.h', """\
#pragma once

static int testf()
{
    return 0;
}
""")

test.write('SConstruct', """\
SConscript('SConscript', variant_dir='Release Output', duplicate=0)
""")

test.write('SConscript', """\
env = Environment()

env['PCHSTOP'] = 'Precompiled.h'
env['PCH'] = env.PCH('Precompiled.cpp')[0]

env.Program('Main.cpp')
""")

test.run(arguments='.', stderr=None)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
