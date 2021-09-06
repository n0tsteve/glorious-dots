PHONEID=36e60e4dcbc22003

if pgrep -x "kdeconnectd" > /dev/null; then
    if qdbus org.kde.kdeconnect /modules/kdeconnect/devices/$PHONEID org.kde.kdeconnect.device.isReachable | grep true > /dev/null; then
        echo ' '$(qdbus org.kde.kdeconnect /modules/kdeconnect/devices/$PHONEID/battery org.kde.kdeconnect.device.battery.charge)%
    else
        echo ' '
    fi
else
    echo ' ?'
fi
