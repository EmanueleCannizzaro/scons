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

__revision__ = "test/CacheDir/option--cf.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test populating a CacheDir with the --cache-force option.
"""

import os.path
import shutil

import TestSCons

test = TestSCons.TestSCons()

test.subdir('cache', 'src')

test.write(['src', 'SConstruct'], """
def cat(env, source, target):
    target = str(target[0])
    open('cat.out', 'ab').write(target + "\\n")
    f = open(target, "wb")
    for src in source:
        f.write(open(str(src), "rb").read())
    f.close()
env = Environment(BUILDERS={'Cat':Builder(action=cat)})
env.Cat('aaa.out', 'aaa.in')
env.Cat('bbb.out', 'bbb.in')
env.Cat('ccc.out', 'ccc.in')
env.Cat('all', ['aaa.out', 'bbb.out', 'ccc.out'])
CacheDir(r'%s')
""" % test.workpath('cache'))

test.write(['src', 'aaa.in'], "aaa.in\n")
test.write(['src', 'bbb.in'], "bbb.in\n")
test.write(['src', 'ccc.in'], "ccc.in\n")

# Verify that a normal build works correctly, and clean up.
# This should populate the cache with our derived files.
test.run(chdir = 'src', arguments = '.')

test.fail_test(test.read(['src', 'all']) != "aaa.in\nbbb.in\nccc.in\n")
test.fail_test(test.read(['src', 'cat.out']) != "aaa.out\nbbb.out\nccc.out\nall\n")

test.up_to_date(chdir = 'src', arguments = '.')

test.run(chdir = 'src', arguments = '-c .')
test.unlink(['src', 'cat.out'])

# Verify that we now retrieve the derived files from cache,
# not rebuild them.  DO NOT CLEAN UP.
test.run(chdir = 'src', arguments = '.', stdout = test.wrap_stdout("""\
Retrieved `aaa.out' from cache
Retrieved `bbb.out' from cache
Retrieved `ccc.out' from cache
Retrieved `all' from cache
"""))

test.fail_test(os.path.exists(test.workpath('src', 'cat.out')))

test.up_to_date(chdir = 'src', arguments = '.')

# Blow away and recreate the CacheDir, then verify that --cache-force
# repopulates the cache with the local built targets.  DO NOT CLEAN UP.
shutil.rmtree(test.workpath('cache'))
test.subdir('cache')

test.run(chdir = 'src', arguments = '--cache-force .')

test.run(chdir = 'src', arguments = '-c .')

test.run(chdir = 'src', arguments = '.', stdout = test.wrap_stdout("""\
Retrieved `aaa.out' from cache
Retrieved `bbb.out' from cache
Retrieved `ccc.out' from cache
Retrieved `all' from cache
"""))

test.fail_test(os.path.exists(test.workpath('src', 'cat.out')))

# Blow away and recreate the CacheDir, then verify that --cache-populate
# repopulates the cache with the local built targets.  DO NOT CLEAN UP.
shutil.rmtree(test.workpath('cache'))
test.subdir('cache')

test.run(chdir = 'src', arguments = '--cache-populate .')

test.run(chdir = 'src', arguments = '-c .')

test.run(chdir = 'src', arguments = '.', stdout = test.wrap_stdout("""\
Retrieved `aaa.out' from cache
Retrieved `bbb.out' from cache
Retrieved `ccc.out' from cache
Retrieved `all' from cache
"""))

test.fail_test(os.path.exists(test.workpath('src', 'cat.out')))

# All done.
test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
