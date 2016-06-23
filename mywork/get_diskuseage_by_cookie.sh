curl localhost:8000/minions \
    -H "Accept: application/json" \
    -b ~/cookies.txt \
    -d tgt='*' \
    -d fun='status.diskusage'
