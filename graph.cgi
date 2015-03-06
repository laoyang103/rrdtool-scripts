#!/bin/bash

CPU=0
MEM=1
PRRD_DIR=/data/kpi/ipm/rrd/proc/
PRRD_FIELD=("cpu" "mem")
PRRD_FIELD_LEN=2
PROC_LIST=("java" "mysqld" "ipmtube" "ipms" "rrdcached")
PROC_LIST_LEN=5
PNG_HEIGHT=334
PNG_WIDTH=543

echo "Content-Type: text/html"
echo ""
echo "<HTML>"
echo "<HEAD><TITLE>RRDCGI Demo</TITLE></HEAD>"
echo "<BODY>"
echo "<H1>RRDCGI Example Page</H1>"
echo "<P>"

for ((i = 0; i < $PROC_LIST_LEN; i++)); do
    for ((j = 0; j < $PRRD_FIELD_LEN; j++)); do
        proc_name=${PROC_LIST[$i]}
        field_name=${PRRD_FIELD[$j]}
        prefix=$proc_name"_"$field_name
        png_name=../../$prefix".png"
        rrd_name=$PRRD_DIR$prefix".rrd"

        test -e $rrd_name && rrdtool graph $png_name\
                    --title="$proc_name $field_name load" \
                    --start=-930s --end -5s \
                    -h 334 -w 543 -l 0 -a PNG -X 0 \
                    DEF:x1=$rrd_name:VALUE:AVERAGE \
                    VDEF:min=x1,MINIMUM \
                    VDEF:max=x1,MAXIMUM \
                    VDEF:avg=x1,AVERAGE \
                    VDEF:lst=x1,LAST \
                    "COMMENT: \l" \
                    "COMMENT:                  Minimum" \
                    "COMMENT:           Maximum" \
                    "COMMENT:         Average" \
                    "COMMENT:           Current" \
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

# */5 * * * * /bin/bash killall -9 coll.sh;/opt/apache-tomcat-6.0.37/webapps/examples/WEB-INF/cgi/probe.sh | /opt/apache-tomcat-6.0.37/webapps/examples/WEB-INF/cgi/coll.sh
