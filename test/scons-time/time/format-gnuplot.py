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

__revision__ = "test/scons-time/time/format-gnuplot.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Verify the time --format=gnuplot option.
"""

import TestSCons_time

test = TestSCons_time.TestSCons_time()

test.fake_logfile('foo-000-0.log', 0)
test.fake_logfile('foo-000-1.log', 0)
test.fake_logfile('foo-000-2.log', 0)

test.fake_logfile('foo-001-0.log', 1)
test.fake_logfile('foo-001-1.log', 1)
test.fake_logfile('foo-001-2.log', 1)

expect_notitle = """\
set key bottom left
plot '-' title "Startup" with lines lt 1, \\
     '-' title "Full build" with lines lt 2, \\
     '-' title "Up-to-date build" with lines lt 3
# Startup
0 11.123456
1 11.123456
e
# Full build
0 11.123456
1 11.123456
e
# Up-to-date build
0 11.123456
1 11.123456
e
"""

expect_title = 'set title "TITLE"\n' + expect_notitle

test.run(arguments = 'time --fmt gnuplot', stdout=expect_notitle)

test.run(arguments = 'time --fmt=gnuplot --title TITLE', stdout=expect_title)

test.run(arguments = 'time --format gnuplot --title TITLE', stdout=expect_title)

test.run(arguments = 'time --format=gnuplot', stdout=expect_notitle)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
