#!/bin/bash

job_number=`ps -efww | grep edps-gui.py | grep panel | awk '{print $2}'`

if [[ -n $job_number ]]; then kill -9 $job_number ; fi
