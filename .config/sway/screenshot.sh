#!/usr/bin/env bash
filename="/home/steve/Képek/Képernyőképek/$(date +'%Y.%m.%d-%H:%m:%S').png"
touch $filename
grim $filename
