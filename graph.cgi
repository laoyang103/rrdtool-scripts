#!/bin/bash

CPU=0
MEM=1
PRRD_DIR=/data/kpi/ipm/rrd/proc/
PRRD_FIELD=("cpu" "mem")
PRRD_FIELD_LEN=2
PROC_LIST=("java" "mysqld" "ipmtube" "ipms" "tcpreplay" "rrdcached")
PROC_LIST_LEN=6

echo "Content-Type: text/html"
echo ""
echo "<HTML>"
echo "<HEAD><TITLE>The key process status</TITLE></HEAD>"
echo "<BODY>"
echo "<P>"

# parse post or get param
SAVEIFS=$IFS
IFS='=&'
[ -z "$QUERY_STRING" ] && read -t 1 QUERY_STRING
PARAM=($QUERY_STRING)
IFS=$SAVEIFS
for ((i = 0; i < ${#PARAM[@]}; i+=2)); do
    declare param_${PARAM[i]}=${PARAM[i+1]}
done

# parse start and end timestamp
FETCH_START_TSS=-930s
FETCH_END_TSS=-3s
[[ $param_start_tss =~ ^[0-9][0-9]*$ ]] && FETCH_START_TSS=$param_start_tss
[[ $param_end_tss   =~ ^[0-9][0-9]*$ ]] && FETCH_END_TSS=$param_end_tss

# debug echo
echo $FETCH_START_TSS
echo $FETCH_END_TSS

# graph all process cpu and memory load image
for ((i = 0; i < $PROC_LIST_LEN; i++)); do
    for ((j = 0; j < $PRRD_FIELD_LEN; j++)); do
        proc_name=${PROC_LIST[$i]}
        field_name=${PRRD_FIELD[$j]}
        prefix=$proc_name"_"$field_name
        png_name=../../$prefix".png"
        rrd_name=$PRRD_DIR$prefix".rrd"

        test -e $rrd_name && rrdtool graph $png_name\
                    --title="$proc_name $field_name load" \
                    --start=$FETCH_START_TSS --end $FETCH_END_TSS \
                    -h 100 -w 243 -l 0 -a PNG -X 0 \
                    DEF:x1=$rrd_name:VALUE:AVERAGE \
                    VDEF:min=x1,MINIMUM \
                    VDEF:max=x1,MAXIMUM \
                    VDEF:avg=x1,AVERAGE \
                    VDEF:lst=x1,LAST \
                    "COMMENT:\t Min" \
                    "COMMENT:    Max" \
                    "COMMENT:    Ave" \
                    "COMMENT:    Cur" \
                    "COMMENT: \l" \
                    AREA:x1#EDA362:${PRRD_FIELD[$j]}  \
                    "GPRINT:min:%5.2lf " \
                    "GPRINT:max:%5.2lf " \
                    "GPRINT:avg:%5.2lf " \
                    "GPRINT:lst:%5.2lf " > /dev/null

        if test -e $png_name; then
            echo "<IMG SRC=../$prefix".png" WIDTH=$PNG_WIDTH HEIGHT=$PNG_HEIGHT >"
        fi
    done
done

echo "</BODY>"
echo "</HTML>"

# */5 * * * * /bin/bash /opt/apache-tomcat-6.0.37/webapps/examples/WEB-INF/cgi/probe.sh | /opt/apache-tomcat-6.0.37/webapps/examples/WEB-INF/cgi/coll.sh
