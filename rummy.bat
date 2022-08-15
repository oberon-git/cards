@echo off

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
        %@Try%
            py client.py
        %@EndTry%
        :@Catch
            echo You Do Not Have Python 3 Installed
        :@EndCatch
    :@EndCatch
:@EndCatch

