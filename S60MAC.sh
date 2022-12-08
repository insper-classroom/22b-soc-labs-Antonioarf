#!/bin/bash

case "$1" in
start)
    printf "Setting ip: "
    /sbin/ifconfig eth0 169.254.0.13 netmask 255.255.0.0 up
    [ $? = 0 ] && echo "OK" || echo "FAIL"
    ;; 
*)
    exit 1
    ;;
esac