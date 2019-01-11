#!/bin/bash

fuser 8080/tcp -k
echo 8080 port is clear
fuser 8081/tcp -k
echo 8081 port is clear

echo Launching the program
cd js
gnome-terminal -e "nodejs index.js"
cd ../python
gnome-terminal -e "./py_launcher.sh"