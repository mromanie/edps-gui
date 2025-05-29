#!/bin/bash

source /home/user/venv/bin/activate

port=7860
gui=$(find /home/user -name 'edps-gui.py')
repo_name=$(basename $GITHUB_REPOSITORY)
domain=`echo $GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN | sed 's/app.//g'`

panel serve $gui --plugins edpsgui.pdf_handler --address 0.0.0.0 --port $port --allow-websocket-origin='*' >& /home/user/edps-gui.log &

echo "Open the GUI at: https://${CODESPACE_NAME}-${port}.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}/${repo_name}"

echo Port $port is open by default, but private. To make it public, open the Codespace not in JupyterLab editor mode at:
echo "   https://${CODESPACE_NAME}.${domain}/${repo_name}"
echo and follow the instructions at:
echo https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace?tool=webui#sharing-a-port
