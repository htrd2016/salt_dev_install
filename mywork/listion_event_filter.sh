curl -NsS localhost:8000/events?token="5a02e5d00047e187a769198ec336262c67b17bb3" |\
        awk '
            BEGIN { RS=""; FS="\\n" }
            $1 ~ /^tag: salt\/job\/[0-9]+\/new$/ { print $0 }
        '
