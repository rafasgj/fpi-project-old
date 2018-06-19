#!/bin/sh

PYTHONPATH="$PYTHONPATH:../fpi" python3 -m behave --tags=-skip $*
