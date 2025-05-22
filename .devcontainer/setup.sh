#!/bin/bash

port=7860
gui=$(find . -name 'edps-gui.py')
repo_name=$(basename $GITHUB_REPOSITORY)

panel serve $gui --plugins edpsgui.pdf_handler --address 0.0.0.0 --port $port --allow-websocket-origin='*' >& /home/user/edps-gui.log &

echo >> .bashrc
echo "echo Start the GUI at: https://${CODESPACE_NAME}-${port}.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/${repo_name}" >> .bashrc

exec bash --login
