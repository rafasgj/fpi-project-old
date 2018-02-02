#!/bin/sh

Mount() {
    [ $# -lt 2 ] &&  Die "Mount requires, at least, 'device' and 'mount point'."
    
    opt="users"
    [ "$1" == "-ro" ] && { opt="$opt,ro"; o=" as Read Only,"; shift; }
    dev=$1
    shift
    mp=$1
    shift
   
    echo "Mounting ${dev} to ${mp},${o} using adequate priviledges." 
    sudo mount -o "${opt}" "${dev}" "${mp}"
}

Unmount() {
    while [ $# -gt 1 ]
    do
        sudo umount "$1"
        shift
    done
}

