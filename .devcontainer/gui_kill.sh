#!/bin/bash

kill $(ps -efww | grep edps-gui | grep panel | awk '{print $2}')
