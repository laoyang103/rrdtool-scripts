#!/bin/bash

CPU=0
MEM=1
PRRD_DIR=/data/kpi/ipm/rrd/proc/
PRRD_FIELD=("cpu" "mem")
PRRD_FIELD_LEN=2
START_TIME=`date +%s`
LIFE_TIME=300

test -n $PRRD_DIR && mkdir -p $PRRD_DIR

while true; do
    read -t 10 line

    now=`date +%s`
    if [ `expr $now - $START_TIME` -gt $LIFE_TIME ]; then
        exit
    fi

    # CPU row start with string "%Cpu(s)"
    is_cpu=`echo $line | grep 'Cpu'`
    if [ -n "$is_cpu" ]; then
        cpu_array=(`echo $line | cut -f 2 -d ':' | sed 's/,//g'`)
        for ((i = 0; i < ${#cpu_array[@]}; i+=2)); do
            crrd_name=$PRRD_DIR"cpu_"${cpu_array[$i+1]}".rrd"
            if [ ! -e $crrd_name ]; then
                rrdtool create $crrd_name --start $now --step 3 DS:VALUE:GAUGE:90:U:U RRA:AVERAGE:0.5:1:14400
            fi
            echo "rrdtool update $crrd_name $now:${cpu_array[$i]}"
            rrdtool update $crrd_name $now:${cpu_array[$i]}
        done
    fi

    # process row start with pid 
    pid=`echo $line | grep '^ *[0-9][0-9]*' | awk '{ print $1 }'`
    if [ -n "$pid" ]; then
        pname=`echo $line | awk '{ print $12 }'`
        pdata[$CPU]=`echo $line | awk '{ print $9 }'`
        pdata[$MEM]=`echo $line | awk '{ print $10 }'`

        for ((i = 0; i < $PRRD_FIELD_LEN; i++)); do
            prrd_name=$PRRD_DIR$pname"_"${PRRD_FIELD[$i]}".rrd"
            if [ ! -e $prrd_name ]; then
                rrdtool create $prrd_name --start $now --step 3 DS:VALUE:GAUGE:90:U:U RRA:AVERAGE:0.5:1:14400
            fi
            echo "rrdtool update $prrd_name $now:${pdata[$i]}"
            rrdtool update $prrd_name $now:${pdata[$i]}
        done
    fi
done

