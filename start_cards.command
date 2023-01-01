#!/bin/bash

git stash
git pull
cd "$0"
export PYTHONPATH=${PYTHONPATH}:$./src
python3 src/client.py
