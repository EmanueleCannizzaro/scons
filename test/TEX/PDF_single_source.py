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

__revision__ = "test/TEX/PDF_single_source.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test creation of a mulitple pdf's from a list of PostScript files.

Test courtesy Rob Managan.
"""

import TestSCons

test = TestSCons.TestSCons()

epstopdf = test.where_is('epstopdf')
if not epstopdf:
    test.skip_test("Could not find 'epstopdf'; skipping test.\n")


test.write(['SConstruct'], """\
import os

env = Environment(ENV = { 'PATH' : os.environ['PATH'] })

env.PDF(['Fig1.ps','Fig3.ps','Fig2.ps'])
""")


figure = """\
%!PS-Adobe-2.0 EPSF-2.0
%%Title: Fig1.fig
%%Creator: fig2dev Version 3.2 Patchlevel 4
%%CreationDate: Tue Apr 25 09:56:11 2006
%%For: managan@mangrove.llnl.gov (Rob Managan)
%%BoundingBox: 0 0 98 98
%%Magnification: 1.0000
%%EndComments
/$F2psDict 200 dict def
$F2psDict begin
$F2psDict /mtrx matrix put
/col-1 {0 setgray} bind def
/col0 {0.000 0.000 0.000 srgb} bind def

end
save
newpath 0 98 moveto 0 0 lineto 98 0 lineto 98 98 lineto closepath clip newpath
-24.9 108.2 translate
1 -1 scale

/cp {closepath} bind def
/ef {eofill} bind def
/gr {grestore} bind def
/gs {gsave} bind def
/rs {restore} bind def
/l {lineto} bind def
/m {moveto} bind def
/rm {rmoveto} bind def
/n {newpath} bind def
/s {stroke} bind def
/slc {setlinecap} bind def
/slj {setlinejoin} bind def
/slw {setlinewidth} bind def
/srgb {setrgbcolor} bind def
/sc {scale} bind def
/sf {setfont} bind def
/scf {scalefont} bind def
/tr {translate} bind def
 /DrawEllipse {
	/endangle exch def
	/startangle exch def
	/yrad exch def
	/xrad exch def
	/y exch def
	/x exch def
	/savematrix mtrx currentmatrix def
	x y tr xrad yrad sc 0 0 1 startangle endangle arc
	closepath
	savematrix setmatrix
	} def

/$F2psBegin {$F2psDict begin /$F2psEnteredState save def} def
/$F2psEnd {$F2psEnteredState restore end} def

$F2psBegin
10 setmiterlimit
 0.06299 0.06299 sc
%
% Fig objects follow
% 
7.500 slw
% Ellipse
n 1170 945 766 766 0 360 DrawEllipse gs col0 s gr

$F2psEnd
rs
"""
test.write('Fig1.ps',figure )
test.write('Fig2.ps',figure )
test.write('Fig3.ps',figure )


test.run(arguments = '.', stderr=None)


files = [
    'Fig1.pdf',
    'Fig2.pdf',
    'Fig3.pdf',
]

for f in files:
    test.must_exist(f)


test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
