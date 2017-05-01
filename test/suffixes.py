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

__revision__ = "test/suffixes.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test handling of file suffixes.
"""

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
def cat(env, source, target):
    target = str(target[0])
    f = open(target, "wb")
    for src in source:
        f.write(open(str(src), "rb").read())
    f.close()
Cat = Builder(action=cat, suffix='.out')
env = Environment(BUILDERS = {'Cat':Cat})
env.Cat('file1', 'file1.in')
env.Cat('file2.out', 'file2.in')
env.Cat('file3.xyz', 'file3.in')
env.Cat('file4.123', 'file4.in')
""")

test.write('file1.in', "file1.in\n")
test.write('file2.in', "file2.in\n")
test.write('file3.in', "file3.in\n")
test.write('file4.in', "file4.in\n")

test.run(arguments = '.')

test.must_match('file1.out', "file1.in\n")
test.must_match('file2.out', "file2.in\n")
test.must_match('file3.xyz', "file3.in\n")
test.must_match('file4.123.out', "file4.in\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
