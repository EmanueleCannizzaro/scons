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

__revision__ = "test/Repository/InstallAs.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import os.path

import TestSCons

test = TestSCons.TestSCons()

test.subdir('install', 'repository', 'work')

install = test.workpath('install')
install_file1_out = test.workpath('install', 'file1.out')
install_file2_out = test.workpath('install', 'file2.out')
install_file3_out = test.workpath('install', 'file3.out')

opts = "-Y " + test.workpath('repository')

#
test.write(['repository', 'SConstruct'], r"""
env = Environment()
env.InstallAs(r'%s', 'file1.in')
env.InstallAs([r'%s', r'%s'], ['file2.in', 'file3.in'])
""" % (install_file1_out, install_file2_out, install_file3_out))

test.write(['repository', 'file1.in'], "repository/file1.in\n")
test.write(['repository', 'file2.in'], "repository/file2.in\n")
test.write(['repository', 'file3.in'], "repository/file3.in\n")

# Make the entire repository non-writable, so we'll detect
# if we try to write into it accidentally.
test.writable('repository', 0)

test.run(chdir = 'work', options = opts, arguments = install)

test.fail_test(test.read(install_file1_out) != "repository/file1.in\n")
test.fail_test(test.read(install_file2_out) != "repository/file2.in\n")
test.fail_test(test.read(install_file3_out) != "repository/file3.in\n")

test.up_to_date(chdir = 'work', options = opts, arguments = install)

#
test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: