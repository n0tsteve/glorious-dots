#!/bin/bash
playerctl pause &
pactl set-sink-mute @DEFAULT_SINK@ toggle &
~/.config/sway/lock.sh
