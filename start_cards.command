#!/bin/bash

dir=$(dirname "$0")
cd "$(dir)"

git stash
git pull
export PYTHONPATH=${PYTHONPATH}:$./src
python3 src/client.py
