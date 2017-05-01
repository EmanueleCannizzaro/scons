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

__revision__ = "src/engine/SCons/Tool/wixTests.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import unittest
import os.path
import os
import sys

import SCons.Errors
from SCons.Tool.wix import *
from SCons.Environment import Environment

import TestCmd
import TestUnit


# create fake candle and light, so the tool's exists() method will succeed
test = TestCmd.TestCmd(workdir = '')
test.write('candle.exe', 'rem this is candle')
test.write('light.exe', 'rem this is light')
os.environ['PATH'] += os.pathsep + test.workdir

class WixTestCase(unittest.TestCase):
    def test_vars(self):
        """Test that WiX tool adds vars"""
        env = Environment(tools=['wix'])
        assert env['WIXCANDLE'] is not None
        assert env['WIXCANDLEFLAGS'] is not None
        assert env['WIXLIGHTFLAGS'] is not None
        assert env.subst('$WIXOBJSUF') == '.wixobj'
        assert env.subst('$WIXSRCSUF') == '.wxs'

if __name__ == "__main__":
    suite = unittest.makeSuite(WixTestCase, 'test_')
    TestUnit.run(suite)

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
