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

__revision__ = "test/Deprecated/SourceCode/RCS/RCS_COCOM.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test setting the $RCS_COCOM variable.
"""

import os

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons(match = TestSCons.match_re_dotall)

test.write('SConscript', """
Environment(tools = ['RCS']).RCS()
""")

msg_rcs = """The RCS() factory is deprecated and there is no replacement."""
warn_rcs = test.deprecated_fatal('deprecated-build-dir', msg_rcs)
msg_sc = """SourceCode() has been deprecated and there is no replacement.
\tIf you need this function, please contact scons-dev@scons.org"""
warn_sc = test.deprecated_wrap(msg_sc)

test.subdir('RCS', ['RCS', 'sub'], 'sub')

sub_RCS = os.path.join('sub', 'RCS')
sub_SConscript = os.path.join('sub', 'SConscript')
sub_all = os.path.join('sub', 'all')
sub_ddd_in = os.path.join('sub', 'ddd.in')
sub_ddd_out = os.path.join('sub', 'ddd.out')
sub_eee_in = os.path.join('sub', 'eee.in')
sub_eee_out = os.path.join('sub', 'eee.out')
sub_fff_in = os.path.join('sub', 'fff.in')
sub_fff_out = os.path.join('sub', 'fff.out')

test.write('my-rcs-co.py', """
import shutil
import sys
for f in sys.argv[1:]:
    shutil.copy('RCS/'+f, f)
""")

test.write('SConstruct', """
SetOption('warn', 'deprecated-source-code')
def cat(env, source, target):
    target = str(target[0])
    f = open(target, "wb")
    for src in source:
        f.write(open(str(src), "rb").read())
    f.close()
env = Environment(TOOLS = ['default', 'RCS'],
                  BUILDERS={'Cat':Builder(action=cat)},
                  RCS_COCOM=r'%(_python_)s my-rcs-co.py $TARGET')
env.Cat('aaa.out', 'aaa.in')
env.Cat('bbb.out', 'bbb.in')
env.Cat('ccc.out', 'ccc.in')
env.Cat('all', ['aaa.out', 'bbb.out', 'ccc.out'])
env.SourceCode('.', env.RCS())
SConscript('sub/SConscript', "env")
""" % locals())

test.write(['RCS', 'sub', 'SConscript'], """\
Import("env")
env.Cat('ddd.out', 'ddd.in')
env.Cat('eee.out', 'eee.in')
env.Cat('fff.out', 'fff.in')
env.Cat('all', ['ddd.out', 'eee.out', 'fff.out'])
""")

test.write(['RCS', 'aaa.in'], "RCS/aaa.in\n")
test.write('bbb.in', "checked-out bbb.in\n")
test.write(['RCS', 'ccc.in'], "RCS/ccc.in\n")

test.write(['RCS', 'sub', 'ddd.in'], "RCS/sub/ddd.in\n")
test.write(['sub', 'eee.in'], "checked-out sub/eee.in\n")
test.write(['RCS', 'sub', 'fff.in'], "RCS/sub/fff.in\n")

read_str = """\
%(_python_)s my-rcs-co.py %(sub_SConscript)s
""" % locals()

build_str = """\
%(_python_)s my-rcs-co.py aaa.in
cat(["aaa.out"], ["aaa.in"])
cat(["bbb.out"], ["bbb.in"])
%(_python_)s my-rcs-co.py ccc.in
cat(["ccc.out"], ["ccc.in"])
cat(["all"], ["aaa.out", "bbb.out", "ccc.out"])
%(_python_)s my-rcs-co.py %(sub_ddd_in)s
cat(["%(sub_ddd_out)s"], ["%(sub_ddd_in)s"])
cat(["%(sub_eee_out)s"], ["%(sub_eee_in)s"])
%(_python_)s my-rcs-co.py %(sub_fff_in)s
cat(["%(sub_fff_out)s"], ["%(sub_fff_in)s"])
cat(["%(sub_all)s"], ["%(sub_ddd_out)s", "%(sub_eee_out)s", "%(sub_fff_out)s"])
""" % locals()

stdout = test.wrap_stdout(read_str = read_str, build_str = build_str)

test.run(arguments = '.',
         stdout = TestSCons.re_escape(stdout),
         stderr = warn_rcs + warn_sc)

test.must_match('all',
                "RCS/aaa.in\nchecked-out bbb.in\nRCS/ccc.in\n")

test.must_match(['sub', 'all'],
                "RCS/sub/ddd.in\nchecked-out sub/eee.in\nRCS/sub/fff.in\n")


test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: