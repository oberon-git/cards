#!/bin/bash

git stash
git pull
export PYTHONPATH=${PYTHONPATH}:$~/Documents/Alexander/cards/src
python3 ~/Documents/Alexander/cards/src/client.py
