#!/usr/bin/env bash
sudo apt-get update && sudo apt-get install -y xvfb x11vnc fluxbox websockify novnc
Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1
fluxbox &
x11vnc -display :1 -nopw -forever -shared -rfbport 5900 &
websockify --web=/usr/share/novnc 6080 localhost:5900 &
