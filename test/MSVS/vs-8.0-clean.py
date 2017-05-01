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

__revision__ = "test/MSVS/vs-8.0-clean.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify the -c option's ability to clean generated Visual Studio 8.0
project (.vcproj) and solution (.sln) files.
"""

import TestSConsMSVS

test = TestSConsMSVS.TestSConsMSVS()
host_arch = test.get_vs_host_arch()


# Make the test infrastructure think we have this version of MSVS installed.
test._msvs_versions = ['8.0']



expected_slnfile = TestSConsMSVS.expected_slnfile_8_0
expected_vcprojfile = TestSConsMSVS.expected_vcprojfile_8_0



test.write('SConstruct', """\
env=Environment(platform='win32', tools=['msvs'], MSVS_VERSION='8.0',
                CPPDEFINES=['DEF1', 'DEF2',('DEF3','1234')],
                CPPPATH=['inc1', 'inc2'],
                HOST_ARCH='%(HOST_ARCH)s')

testsrc = ['test1.cpp', 'test2.cpp']
testincs = ['sdk.h']
testlocalincs = ['test.h']
testresources = ['test.rc']
testmisc = ['readme.txt']

p = env.MSVSProject(target = 'Test.vcproj',
                    srcs = testsrc,
                    incs = testincs,
                    localincs = testlocalincs,
                    resources = testresources,
                    misc = testmisc,
                    buildtarget = 'Test.exe',
                    variant = 'Release',
                    auto_build_solution = 0)

env.MSVSSolution(target = 'Test.sln',
                 slnguid = '{SLNGUID}',
                 projects = [p],
                 variant = 'Release')
"""%{'HOST_ARCH': host_arch})

test.run(arguments=".")

test.must_exist(test.workpath('Test.vcproj'))
vcproj = test.read('Test.vcproj', 'r')
expect = test.msvs_substitute(expected_vcprojfile, '8.0', None, 'SConstruct')
# don't compare the pickled data
assert vcproj[:len(expect)] == expect, test.diff_substr(expect, vcproj)

test.must_exist(test.workpath('Test.sln'))
sln = test.read('Test.sln', 'r')
expect = test.msvs_substitute(expected_slnfile, '8.0', None, 'SConstruct')
# don't compare the pickled data
assert sln[:len(expect)] == expect, test.diff_substr(expect, sln)

test.run(arguments='-c .')

test.must_not_exist(test.workpath('Test.vcproj'))
test.must_not_exist(test.workpath('Test.sln'))

test.run(arguments='.')

test.must_exist(test.workpath('Test.vcproj'))
test.must_exist(test.workpath('Test.sln'))

test.run(arguments='-c Test.sln')

test.must_exist(test.workpath('Test.vcproj'))
test.must_not_exist(test.workpath('Test.sln'))

test.run(arguments='-c Test.vcproj')

test.must_not_exist(test.workpath('Test.vcproj'))



test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
