#!/usr/bin/env python3

import subprocess

file = open('ss.txt', 'r')
subprocess.run(['ss', '-tip', 'state', 'established'], stdout = file)
