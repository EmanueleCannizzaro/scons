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

__revision__ = "test/TEX/input_docClass.py rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"

"""
Test creation of a LaTeX document that uses \input{filename}
to set the documentclass. When the file has .tex we have to search 
to find the documentclass command.

Test courtesy Rob Managan.
"""

import TestSCons

test = TestSCons.TestSCons()

latex = test.where_is('latex')
if not latex:
    test.skip_test("Could not find 'latex'; skipping test.\n")

test.write(['SConstruct'], """\
import os

env = Environment()

test = env.PDF(source='test.tex')
""")

test.write(['test.tex'],
r"""
\input{theClass}

\begin{document}
 
\title{Report Title}

\author{A. N. Author}
 
\maketitle 
 
\begin{abstract}
there is no abstract
\end{abstract}

\tableofcontents
\listoffigures

\chapter{Introduction}

The introduction is short.

\section{Acknowledgements}

The Acknowledgements are shown as well.  

\end{document}
""")

test.write(['theClass.tex'],
r"""
\documentclass{report}

""")

# makeindex will write status messages to stderr (grrr...), so ignore it.
test.run(arguments = '.', stderr=None)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
