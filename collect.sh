#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
    echo "please pass some hosts to connect to"
    exit 1
fi

parallel ssh {} "ss -H -tipa state connected exclude time-wait exclude fin-wait-2" ::: $@ > ss.txt
