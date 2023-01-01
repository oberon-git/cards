#!/bin/bash

dir=~/Documents/Alexander/cards # $(dirname "$0")
cd "$dir" || exit

git stash
git pull
export PYTHONPATH=${PYTHONPATH}:$./src
python3 src/client.py
