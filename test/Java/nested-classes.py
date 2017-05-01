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

__revision__ = "test/Java/nested-classes.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test Java compilation with inner and anonymous classes (Issue 2087).
"""

import os

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()
where_javac, java_version = test.java_where_javac()

# Work around javac 1.4 not reporting its version:
java_version = java_version or "1.4"

# Skip this test as SCons doesn't (currently) predict the generated
# inner/anonymous class generated .class files generated by gcj
# and so will always fail 
if test.javac_is_gcj:
    test.skip_test('Test not valid for gcj (gnu java); skipping test(s).\n')


test.write('SConstruct', """
env = Environment()
env['JAVAVERSION'] = '%(java_version)s'
classes = env.Java(target = 'build', source = 'source')
env.Jar(target = 'anon.jar', source = classes)
""" % locals())

test.subdir('source', 'build')

test.write(['source', 'Test.java'], """\
public class Test {
  class Inner { };
  public void testAnon(Test test) { }
  public void testAnon(Inner inner) { }
  public Test ( ) {
    class Foo {
      public int reply ( ) {
        class Bar { };
        return 1 ; 
      } 
    } ;
    testAnon(new Test() { });
  }
  public Test (int a) {
    class Foo {
      public int reply ( ) {
        class Bar { };
        return 1 ; 
      } 
    } ;
    testAnon(new Test() { });
  }
  public Test (int a, int b) {
    class Foobar {
      public int reply ( ) { 
        class Bar { };
        return 1 ;
      } 
    } ;
    testAnon(new Test() { });
  }
  public Test (int a, int b, int c) {
    testAnon(new Test() { });
  }
  void run() {
    testAnon(new Inner() {
      public void execute() {
        testAnon(new Inner( ) {
          public void execute() {
            System.out.println("Inside execute()");
          }
        });
      }
    });
  }
}
""")

test.run(arguments = '.')

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: