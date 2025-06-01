#!/bin/bash
# Script to be run once when the container is created.\

/usr/local/python/current/bin/python3.11 -m pip install -r /home/user/setup_files/requirements_notebooks.txt

#Needed to download files to the local machine: /workspaces is where JupyterLab allows to download the data from
ln -s /home/user/EDPS_data /workspaces/$(basename $GITHUB_REPOSITORY)/EDPS_data

cp /home/user/bin/utilities.py /workspaces/edps-gui/utilities.py
