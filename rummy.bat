@echo off

cd /Repos/cards
git pull
cd src
python3 client.py
