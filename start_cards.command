#!/bin/bash

echo "$0"
cd "$0"

git stash
git pull
export PYTHONPATH=${PYTHONPATH}:$./src
python3 src/client.py
