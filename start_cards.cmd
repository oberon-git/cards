@ECHO OFF
SETLOCAL
    SET PYTHONPATH=%PYTHONPATH%;.\src
    python3 src/client.py > nul
ENDLOCAL
