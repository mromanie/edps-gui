port=7860
gui=$(find . -name 'edps-gui.py')
panel serve $gui --plugins edpsgui.pdf_handler --address 0.0.0.0 --port $port --allow-websocket-origin='*' >& /home/user/edps-gui.log
