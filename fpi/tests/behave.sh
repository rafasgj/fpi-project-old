#!/bin/sh

for feature in `ls -1d *.features | sort`
do
    pushd "${feature}" >/dev/null 2>&1
    PYTHONPATH="$PYTHONPATH:../.." behave-3 || exit $?
    popd >/dev/null 2>&1
done
