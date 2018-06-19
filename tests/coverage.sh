#!/bin/sh

BEHAVE='behave --tags=-skip'

PYTHONPATH="$PYTHONPATH:../fpi"

APPEND=''
[ -f .coverage ] && APPEND='--append'

python3 -m coverage run $APPEND --source=../fpi -m $BEHAVE $*
python3 -m coverage report

