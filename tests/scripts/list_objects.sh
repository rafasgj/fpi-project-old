#!/bin/sh

version="α-1"

if [ $# -ne 2 ]
then
    echo -e "usage: `basename $0` <object_type> <sqlite_file>"
    echo -e "\nValid objects for version ${version}:"
    echo -e "\tassets"
    echo -e "\timages"
    echo -e "\nNot all objects might be available in every f/π version."
    exit 1
fi

object="$1"
cat="$2"

echo "select * from ${object} ;" | sqlite3 ${cat}

