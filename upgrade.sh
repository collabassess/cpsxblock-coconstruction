#!/bin/bash

exec `git pull origin master`
exec `npm run build`
exec `./install.sh`