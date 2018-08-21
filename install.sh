#!/bin/bash

# Remove old package
cd /edx/app/edxapp
sudo rm -rf constructcpsxblock

# Move things into place and install
cd -
sudo cp -R constructcpsxblock /edx/app/edxapp/constructcpsxblock

cd /edx/app/edxapp
sudo -u edxapp /edx/bin/pip.edxapp install constructcpsxblock/ --upgrade --no-deps

# Restart edX
sudo /edx/bin/supervisorctl restart edxapp:*