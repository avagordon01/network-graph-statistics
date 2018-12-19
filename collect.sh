#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
    echo "please pass some hosts to connect to"
    exit 1
fi

parallel ssh {} "ss -tipa state connected exclude time-wait | tail -n +2" ::: $@ > ss.txt
