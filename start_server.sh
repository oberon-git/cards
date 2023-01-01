#!/bin/bash

git stash
git pull
export PYTHONPATH=${PYTHONPATH}:$./src
python3 src/server.py
