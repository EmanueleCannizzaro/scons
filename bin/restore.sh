#!/usr/bin/env sh
#
# Simple hack script to restore __revision__, __COPYRIGHT_, 2.5.1
# and other similar variables to what gets checked in to source.  This
# comes in handy when people send in diffs based on the released source.
#

if test "X$*" = "X"; then
    DIRS="src test"
else
    DIRS="$*"
fi

SEPARATOR="================================================================================"

header() {
    arg_space="$1 "
    dots=`echo "$arg_space" | sed 's/./\./g'`
    echo "$SEPARATOR" | sed "s;$dots;$arg_space;"
}

for i in `find $DIRS -name '*.py'`; do
    header $i
    ed $i <<EOF
g/Copyright (c) 2001.*SCons Foundation/s//Copyright (c) 2001 - 2016 The SCons Foundation/p
w
/^__revision__ = /s/= .*/= "bin/restore.sh rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog"/p
w
q
EOF
done

for i in `find $DIRS -name 'scons.bat'`; do
    header $i
    ed $i <<EOF
g/Copyright (c) 2001.*SCons Foundation/s//Copyright (c) 2001 - 2016 The SCons Foundation/p
w
/^@REM src\/script\/scons.bat/s/@REM .* knight/@REM bin/restore.sh rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog/p
w
q
EOF
done

for i in `find $DIRS -name '__init__.py' -o -name 'scons.py' -o -name 'sconsign.py'`; do
    header $i
    ed $i <<EOF
/^__version__ = /s/= .*/= "2.5.1"/p
w
/^__build__ = /s/= .*/= "rel_2.5.1:3735:9dc6cee5c168[MODIFIED]"/p
w
/^__buildsys__ = /s/= .*/= "mongodog"/p
w
/^__date__ = /s/= .*/= "2016/11/03 14:02:02"/p
w
/^__developer__ = /s/= .*/= "bdbaddog"/p
w
q
EOF
done

for i in `find $DIRS -name 'setup.py'`; do
    header $i
    ed $i <<EOF
/^ *version = /s/= .*/= "2.5.1",/p
w
q
EOF
done

for i in `find $DIRS -name '*.txt'`; do
    header $i
    ed $i <<EOF
g/Copyright (c) 2001.*SCons Foundation/s//Copyright (c) 2001 - 2016 The SCons Foundation/p
w
/# [^ ]* 0.96.[CD][0-9]* [0-9\/]* [0-9:]* knight$/s/.*/# bin/restore.sh rel_2.5.1:3735:9dc6cee5c168 2016/11/03 14:02:02 bdbaddog/p
w
/Version [0-9][0-9]*\.[0-9][0-9]*/s//Version 2.5.1/p
w
q
EOF
done

for i in `find $DIRS -name '*.xml'`; do
    header $i
    ed $i <<EOF
g/Copyright (c) 2001.*SCons Foundation/s//Copyright (c) 2001 - 2016 The SCons Foundation/p
w
q
EOF
done
