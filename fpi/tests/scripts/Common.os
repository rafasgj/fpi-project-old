#!/bin/sh

Die() {
    echo -e "$*"
    exit 1
}

Quiet() {
    eval "$*" >/dev/null 2>/dev/null
}

Prepare() {
    Quiet pushd `dirname $0`/..
}

Unprepare() {
    Quiet popd
}

. `dirname $0`/`uname`.os

