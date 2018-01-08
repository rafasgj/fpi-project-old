#!/bin/sh

for feature in `ls -1d *.features | sort`
do
    behave-3 "${feature}" || exit $?
done
