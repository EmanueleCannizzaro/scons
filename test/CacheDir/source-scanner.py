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

__revision__ = "test/CacheDir/source-scanner.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test retrieving derived files from a CacheDir.

This tests the case reported by Jeff Petkau (SourceForge bug #694744)
where a target is source for another target with a scanner, which used
to cause us to push the file to the CacheDir after the build signature
had already been cleared (as a sign that the built file should now
be rescanned).
"""

import TestSCons

test = TestSCons.TestSCons()

cache = test.workpath('cache')

test.subdir('cache', 'subdir')

test.write(['subdir', 'SConstruct'], """\
import SCons

CacheDir(r'%(cache)s')

def docopy(target,source,env):
    data = source[0].get_contents()
    f = open(target[0].rfile().get_abspath(), "wb")
    f.write(data)
    f.close()

def sillyScanner(node, env, dirs):
    print 'This is never called (unless we build file.out)'
    return []

SillyScanner = SCons.Scanner.Base(function = sillyScanner, skeys = ['.res'])

env = Environment(tools=[],
                  SCANNERS = [SillyScanner],
                  BUILDERS = {})

r = env.Command('file.res', 'file.ma', docopy)

env.Command('file.out', r, docopy)

# make r the default. Note that we don't even try to build file.out,
# and so SillyScanner never runs. The bug is the same if we build
# file.out, though.
Default(r)
""" % locals())

test.write(['subdir', 'file.ma'], "subdir/file.ma\n")

test.run(chdir = 'subdir')

test.must_not_exist(test.workpath(cache, 'N', 'None'))



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
