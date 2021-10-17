#!/usr/bin/env bash
declare -i temp
temp=$(cat /sys/class/thermal/thermal_zone1/temp)
declare -i result
result=$temp/1000
echo $result
