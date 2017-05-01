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

__revision__ = "test/MSVS/vs-14.0-files.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test that we can generate Visual Studio 14.0 project (.vcxproj) and
solution (.sln) files that look correct.
"""

import os

import TestSConsMSVS

test = TestSConsMSVS.TestSConsMSVS()
host_arch = test.get_vs_host_arch()


# Make the test infrastructure think we have this version of MSVS installed.
test._msvs_versions = ['14.0']



expected_slnfile = TestSConsMSVS.expected_slnfile_14_0
expected_vcprojfile = TestSConsMSVS.expected_vcprojfile_14_0
SConscript_contents = TestSConsMSVS.SConscript_contents_14_0



test.write('SConstruct', SConscript_contents%{'HOST_ARCH': host_arch})

test.run(arguments="Test.vcxproj")

test.must_exist(test.workpath('Test.vcxproj'))
test.must_exist(test.workpath('Test.vcxproj.filters'))
vcxproj = test.read('Test.vcxproj', 'r')
expect = test.msvs_substitute(expected_vcprojfile, '14.0', None, 'SConstruct')
# don't compare the pickled data
assert vcxproj[:len(expect)] == expect, test.diff_substr(expect, vcxproj)

test.must_exist(test.workpath('Test.sln'))
sln = test.read('Test.sln', 'r')
expect = test.msvs_substitute(expected_slnfile, '14.0', None, 'SConstruct')
# don't compare the pickled data
assert sln[:len(expect)] == expect, test.diff_substr(expect, sln)

test.run(arguments='-c .')

test.must_not_exist(test.workpath('Test.vcxproj'))
test.must_not_exist(test.workpath('Test.vcxproj.filters'))
test.must_not_exist(test.workpath('Test.sln'))

test.run(arguments='Test.vcxproj')

test.must_exist(test.workpath('Test.vcxproj'))
test.must_exist(test.workpath('Test.vcxproj.filters'))
test.must_exist(test.workpath('Test.sln'))

test.run(arguments='-c Test.sln')

test.must_not_exist(test.workpath('Test.vcxproj'))
test.must_not_exist(test.workpath('Test.vcxproj.filters'))
test.must_not_exist(test.workpath('Test.sln'))



# Test that running SCons with $PYTHON_ROOT in the environment
# changes the .vcxproj output as expected.
os.environ['PYTHON_ROOT'] = 'xyzzy'
python = os.path.join('$(PYTHON_ROOT)', os.path.split(TestSConsMSVS.python)[1])

test.run(arguments='Test.vcxproj')

test.must_exist(test.workpath('Test.vcxproj'))
vcxproj = test.read('Test.vcxproj', 'r')
expect = test.msvs_substitute(expected_vcprojfile, '14.0', None, 'SConstruct',
                              python=python)
# don't compare the pickled data
assert vcxproj[:len(expect)] == expect, test.diff_substr(expect, vcxproj)



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: