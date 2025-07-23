@echo off
cd c:\Entwicklung\Software\spool-coder

REM Set the environment variable for Bambu XOR Key if needed
REM Replace "0123456789abcdef0123456789abcdef" with the actual key for production use
REM set BAMBU_XOR_KEY=0123456789abcdef0123456789abcdef

.venv\Scripts\python.exe main.py
