#!/bin/bash
# Script to be run once when the container is created.

#pip install -r requirements_notebooks.txt
python3.11 -m pip install --no-cache-dir --upgrade -r requirements_notebooks.txt
