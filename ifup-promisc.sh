#!/bin/bash

ifaces=`ifconfig -a | grep "Link en" | awk '{print $1}' | xargs`

for iface in $ifaces; do
    iface_out=`ifconfig $iface`
    if [[ "$iface_out" =~ "inet addr" ]]; then
        continue
    else
        ifconfig $iface up
        ifconfig $iface promisc
        break
    fi
done

