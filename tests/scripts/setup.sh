#!/bin/sh

. `dirname $0`/Common.os

Prepare

Mount -ro data/samples.vfat data/samples

Unprepare 
