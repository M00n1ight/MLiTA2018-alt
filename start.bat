explorer http://localhost:8080
start cmd /k node js\index.js
cd .\python
start "" "%~dp0\python.lnk" main.py %*
pause