#!/usr/bin/rrdcgi

<HTML>
<HEAD><TITLE>RRDCGI Demo</TITLE></HEAD>
<BODY>
<H1>RRDCGI Example Page</H1>
<P>
<RRD::GRAPH ../../load.png --lazy 
        --title="Temperatures" 
        --start=-930s --end -5s 
        --imginfo '<IMG SRC=../%s WIDTH=%lu HEIGHT=%lu >'
        DEF:x1=/tmp/rrd/mysqld_cpu.rrd:VALUE:AVERAGE
        AREA:x1#EDA362:x1>
</P>
</BODY>
</HTML>
