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

__revision__ = "src/test_aegistests.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify that we have proper Copyright notices on all the right files
in our distributions.

Note that this is a packaging test, not a functional test, so the
name of this script doesn't end in *Tests.py.
"""

import os
import popen2
import re
import sys

import TestSCons

test = TestSCons.TestSCons()

try:
    popen2.Popen3
except AttributeError:
    def get_stdout(command):
        (tochild, fromchild, childerr) = os.popen3(command)
        tochild.close()
        return fromchild.read()
else:
    def get_stdout(command):
        p = popen2.Popen3(command, 1)
        p.tochild.close()
        return p.fromchild.read()

output = get_stdout('aegis -list -unformatted pf') +\
         get_stdout('aegis -list -unformatted cf')
lines = output.split('\n')[:-1]
sources = [x for x in lines if x[:7] == 'source ']

re1 = re.compile(r' src/.*Tests\.py')
re2 = re.compile(r' src/test_.*\.py')
re3 = re.compile(r' test/.*\.py')

def filename_is_a_test(x):
    return re1.search(x) or re2.search(x) or re3.search(x)

test_files = list(filter(filename_is_a_test, sources))

if test_files:
    sys.stderr.write("Found the following files with test names not marked as Aegis tests:\n")
    sys.stderr.write('\t' + '\n\t'.join(test_files) + '\n')
    test.fail_test(1)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
