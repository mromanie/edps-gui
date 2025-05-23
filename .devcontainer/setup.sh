#!/bin/bash

echo >> .profile
echo alias start_gui='/home/user/bin/start_gui.sh' >> .profile
echo alias check_gui='ps -ef | grep panel' >> .profile
