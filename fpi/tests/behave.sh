#!/bin/sh

PYTHONPATH="$PYTHONPATH:.." python3 -m behave "$*"
