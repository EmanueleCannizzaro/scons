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

__revision__ = "test/warning-TargetNotBuiltWarning.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', """
foo = Command('foo.out', [], '@echo boo')
bill = Command('bill.out', [], Touch('$TARGET'))
Depends(bill, foo)
Alias('jim', bill)
""")

test.run(arguments='-Q jim', stdout = 'boo\nTouch("bill.out")\n')

test.run(arguments='-Q jim --warning=target-not-built',
         stdout = "boo\nscons: `jim' is up to date.\n",
         stderr = None)
test.must_contain_all_lines(test.stderr(),
                            'scons: warning: Cannot find target foo.out after building')

test.run(arguments='-Q jim --warning=target-not-built -n',
         stdout = "scons: `jim' is up to date.\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: