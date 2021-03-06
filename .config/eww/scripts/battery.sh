#!/bin/sh

# A dwm_bar function to read the battery level and status
# Joe Standring <git@joestandring.com>
# GNU GPLv3

    # Change BAT1 to whatever your battery is identified as. Typically BAT0 or BAT1
    CHARGE=$(cat /sys/class/power_supply/BAT0/capacity)
    STATUS=$(cat /sys/class/power_supply/BAT0/status)

    printf "%s" "$SEP1"
        if [ "$STATUS" = "Charging" ]; then
            printf "ο¦ " #"$CHARGE" "+" #π
    	elif [ $CHARGE -le 75 ] && [ $CHARGE -gt 50  ]; then
	    printf "βοβ" #"$CHARGE"
	elif [ $CHARGE -le 50 ] && [ $CHARGE -gt 25  ]; then
	    printf "βοΎβ" #"$CHARGE"
	elif [ $CHARGE -le 25 ] && [ $CHARGE -gt 10  ]; then
	    printf "βο»β" #"$CHARGE"
	elif [ $CHARGE -le 10 ]; then
	    printf "βοβ"  "!!"
        else
            printf "βοΈβ" #"$CHARGE" #π
        fi
    printf "%s" #"$SEP2"


