#!/bin/bash
# Script to be run once when the container is created.\

/usr/local/python/current/bin/python3.11 -m pip install -r /home/user/setup_files/requirements_notebooks.txt
ln -s /home/user/EDPS_data /workspaces/$(basename $GITHUB_REPOSITORY)/EDPS_data
