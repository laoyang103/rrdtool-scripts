#!/bin/bash

pid_list=2147483647
proc_list="java mysqld ipmtube ipms tcpreplay rrdcached"
output_times=100

for proc in $proc_list; do
    pid=`ps -e | grep $proc | sed -n 1,1p | awk '{ print $1 }'`
    if [ $pid ]; then
        pid_list=$pid_list","$pid
    fi
done

top -n $output_times -b -p $pid_list -d 3
