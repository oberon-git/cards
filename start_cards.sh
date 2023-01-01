#!/bin/bash

git stash
git pull
export PYTHONPATH=${PYTHONPATH}:$./src
python3 ~/Documents/Alexander/cards/src/client.py > /dev/nul
