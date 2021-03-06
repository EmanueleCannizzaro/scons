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

__revision__ = "test/textfile.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import TestSCons

import os

test = TestSCons.TestSCons()

foo1  = test.workpath('foo1.txt')
#foo2  = test.workpath('foo2.txt')
#foo1a = test.workpath('foo1a.txt')
#foo2a = test.workpath('foo2a.txt')

test.write('SConstruct', """
env = Environment(tools=['textfile'])
data0 = ['Goethe', 'Schiller']
data  = ['lalala', 42, data0, 'tanteratei']

env.Textfile('foo1', data)
env.Textfile('foo2', data, LINESEPARATOR='|*')
env.Textfile('foo1a.txt', data + [''])
env.Textfile('foo2a.txt', data + [''], LINESEPARATOR='|*')

# recreate the list with the data wrapped in Value()
data0 = list(map(Value, data0))
data = list(map(Value, data))
data[2] = data0

env.Substfile('bar1', data)
env.Substfile('bar2', data, LINESEPARATOR='|*')
data.append(Value(''))
env.Substfile('bar1a.txt', data)
env.Substfile('bar2a.txt', data, LINESEPARATOR='|*')
""")

test.run(arguments = '.')

textparts = ['lalala', '42',
             'Goethe', 'Schiller',
             'tanteratei']
foo1Text  = os.linesep.join(textparts)
foo2Text  = '|*'.join(textparts)
foo1aText = foo1Text + os.linesep
foo2aText = foo2Text + '|*'

test.up_to_date(arguments = '.')

files = list(map(test.workpath, (
            'foo1.txt', 'foo2.txt', 'foo1a.txt', 'foo2a.txt',
            'bar1',     'bar2',     'bar1a.txt', 'bar2a.txt',
        )))
def check_times():
    # make sure the files didn't get rewritten, because nothing changed:
    before = list(map(os.path.getmtime, files))
    # introduce a small delay, to make the test valid
    test.sleep()
    # should still be up-to-date
    test.up_to_date(arguments = '.')
    after = list(map(os.path.getmtime, files))
    test.fail_test(before != after)

# make sure that the file content is as expected
test.must_match('foo1.txt',  foo1Text)
test.must_match('bar1',      foo1Text)
test.must_match('foo2.txt',  foo2Text)
test.must_match('bar2',      foo2Text)
test.must_match('foo1a.txt', foo1aText)
test.must_match('bar1a.txt', foo1aText)
test.must_match('foo2a.txt', foo2aText)
test.must_match('bar2a.txt', foo2aText)
check_times()

# write the contents and make sure the files
# didn't get rewritten, because nothing changed:
test.write('foo1.txt',  foo1Text)
test.write('bar1',      foo1Text)
test.write('foo2.txt',  foo2Text)
test.write('bar2',      foo2Text)
test.write('foo1a.txt', foo1aText)
test.write('bar1a.txt', foo1aText)
test.write('foo2a.txt', foo2aText)
test.write('bar2a.txt', foo2aText)
check_times()

test.write('SConstruct', """
textlist = ['This line has no substitutions',
            'This line has @subst@ substitutions',
            'This line has %subst% substitutions',
           ]

sub1 = { '@subst@' : 'most' }
sub2 = { '%subst%' : 'many' }
sub3 = { '@subst@' : 'most' , '%subst%' : 'many' }

env = Environment(tools = ['textfile'])

t = env.Textfile('text', textlist)
# no substitutions
s = env.Substfile('sub1', t)
# one substitution
s = env.Substfile('sub2', s, SUBST_DICT = sub1)
# the other substution
s = env.Substfile('sub3', s, SUBST_DICT = sub2)
# the reverse direction
s = env.Substfile('sub4', t, SUBST_DICT = sub2)
s = env.Substfile('sub5', s, SUBST_DICT = sub1)
# both
s = env.Substfile('sub6', t, SUBST_DICT = sub3)
""")

test.run(arguments = '.')

line1  = 'This line has no substitutions'
line2a = 'This line has @subst@ substitutions'
line2b = 'This line has most substitutions'
line3a = 'This line has %subst% substitutions'
line3b = 'This line has many substitutions'

def matchem(file, lines):
    lines = os.linesep.join(lines)
    test.must_match(file, lines)

matchem('text.txt', [line1, line2a, line3a])
matchem('sub1', [line1, line2a, line3a])
matchem('sub2', [line1, line2b, line3a])
matchem('sub3', [line1, line2b, line3b])
matchem('sub4', [line1, line2a, line3b])
matchem('sub5', [line1, line2b, line3b])
matchem('sub6', [line1, line2b, line3b])

test.up_to_date(arguments = '.')

test.pass_test()
