#!/bin/sh

entries=" Hibernate\n Logout\n⏾ Suspend\n Reboot\n Shutdown"
selected=$(echo -e $entries|rofi -dmenu | awk '{print tolower($2)}')

case $selected in
  hibernate)
    exec systemctl hibernate;;
  logout)
    exec swaymsg exit;;
  suspend)
    exec systemctl suspend;;
  reboot)
    exec systemctl reboot;;
  shutdown)
    exec systemctl poweroff -i;;
esac
