#!/bin/bash

# Uninstall old copies of XBlock
sudo -u edxapp /edx/bin/pip.edxapp uninstall constructcpsxblock
cd /edx/app/edxapp
sudo rm -rf constructcpsxblock

# Move things into place and install
cd -
sudo mv constructcpsxblock /edx/app/edxapp/constructcpsxblock

cd /edx/app/edxapp
sudo -u edxapp /edx/bin/pip.edxapp install constructcpsxblock/ --upgrade --no-deps

# Restart edX
sudo /edx/bin/supervisorctl restart edxapp:*