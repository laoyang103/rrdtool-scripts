#!/bin/bash

RRD_DIR=/data/kpi/ipm/rrd/proc/
RRD_LIST=`ls $RRD_DIR`
PNG_HEIGHT=100
PNG_WIDTH=243
WEB_DIR="../"
PHY_DIR="../../"

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
echo $FETCH_START_TSS" "$FETCH_END_TSS"</br>"

# graph all rrd image
for rrd in $RRD_LIST; do
    rrd_name=$RRD_DIR$rrd
    png_name=${rrd/.rrd/.png}

    test -e $rrd_name && rrdtool graph $PHY_DIR$png_name\
                --title="${png_name/_/ /} load" \
                --start=$FETCH_START_TSS --end $FETCH_END_TSS \
                -l 0 -a PNG -X 0 \
                -h $PNG_HEIGHT -w $PNG_WIDTH \
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

    if test -e $PHY_DIR$png_name; then
        echo "<IMG SRC="$WEB_DIR$png_name" >"
    fi
done

echo "</BODY>"
echo "</HTML>"

# */5 * * * * /bin/bash /opt/apache-tomcat-6.0.37/webapps/examples/WEB-INF/cgi/probe.sh | /opt/apache-tomcat-6.0.37/webapps/examples/WEB-INF/cgi/coll.sh
