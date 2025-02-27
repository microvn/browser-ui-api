#!/bin/bash
set -e

rm -f /tmp/.X99-lock

Xvfb :99 -ac -screen 0 1920x1080x24 -nolisten tcp &
sleep 5

x11vnc -display :99 \
       -rfbport 5900 \
       -listen 0.0.0.0 \
       -N -forever \
       -passwd secret \
       -shared &

exec tail -f /dev/null

# Run the Python application
exec python main.py