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

__revision__ = "test/Java/JARFLAGS.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

import os

import TestSCons

test = TestSCons.TestSCons()

test.subdir('src')

where_javac, java_version = test.java_where_javac()
where_jar = test.java_where_jar()



test.write('SConstruct', """
env = Environment(tools = ['javac', 'jar'],
                  JAVAC = r'%(where_javac)s',
                  JAR = r'%(where_jar)s',
                  JARFLAGS = 'cvf')
env['JARFLAGS'] = 'cvf'
class_files = env.Java(target = 'classes', source = 'src')
env.Jar(target = 'test.jar', source = class_files)
""" % locals())

test.write(['src', 'Example1.java'], """\
package src;

public class Example1
{

     public static void main(String[] args)
     {

     }

}
""")

expect = test.wrap_stdout("""\
%(where_javac)s -d classes -sourcepath src src/Example1\.java
%(where_jar)s cvf test.jar -C classes src/Example1\.class
.*
adding: src/Example1\.class.*
""" % locals())

expect = expect.replace('/', os.sep)

test.run(arguments = '.',
         match=TestSCons.match_re_dotall,
         stdout = expect)

test.must_exist('test.jar')

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
