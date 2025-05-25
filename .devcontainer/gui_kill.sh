#!/bin/bash

job_number=`ps -efww | grep edps-gui | grep panel | awk '{print $2}'`

if [[ -n $job_number ]]; then kill $job_number ; fi
