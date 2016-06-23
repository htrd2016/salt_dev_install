curl http://localhost:8000 \
      -b ~/cookies.txt \
      -H 'Accept: application/json' \
      -d client=local \
      -d tgt='*' \
      -d fun=test.ping
