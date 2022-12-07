@echo off

SETLOCAL
cd /Repos/cards
git pull
cd src
%@Try%
    python3 client.py
%@EndTry%
:@Catch
    %@Try%
        python client.py
    %@EndTry%
    :@Catch
        py client.py
    :@EndCatch
:@EndCatch
ENDLOCAL
