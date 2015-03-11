#!/bin/bash

pid_list=2147483647
proc_list="java mysqld ipmtube ipms"
output_times=100

for proc in $proc_list; do
    pids=`ps -e | grep $proc | awk '{ print $1 }' | xargs | sed 's/ /,/g'`
    if [ $pids ]; then
        pid_list=$pid_list","$pids
    fi
done

top -n $output_times -b -p $pid_list -d 3
