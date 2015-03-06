#!/bin/bash

CPU=0
MEM=1
PRRD_DIR=/data/kpi/ipm/rrd/proc/
PRRD_FIELD=("cpu" "mem")
PRRD_FIELD_LEN=2

test -n $PRRD_DIR && mkdir -p $PRRD_DIR

while true; do
    read line
    # process row start with pid 
    pid=`echo $line | grep '^ *[0-9][0-9]*' | awk '{ print $1 }'`
    if [ -n "$pid" ]; then
        pname=`echo $line | awk '{ print $12 }'`
        pdata[$CPU]=`echo $line | awk '{ print $9 }'`
        pdata[$MEM]=`echo $line | awk '{ print $10 }'`

        echo $pname"---"${pdata[$CPU]}"---"${pdata[$MEM]}

        now=`date +%s`
        for ((i = 0; i < $PRRD_FIELD_LEN; i++)); do
            prrd_name=$PRRD_DIR$pname"_"${PRRD_FIELD[$i]}".rrd"
            if [ ! -e $prrd_name ]; then
                rrdtool create $prrd_name --start $now --step 3 DS:VALUE:GAUGE:90:U:U RRA:AVERAGE:0.5:1:1440
            fi
            echo "rrdtool update $prrd_name $now:${pdata[$i]}"
            rrdtool update $prrd_name $now:${pdata[$i]}
        done
    fi
done

