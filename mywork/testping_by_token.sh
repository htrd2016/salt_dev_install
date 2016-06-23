curl http://localhost:8000 \
    -H 'Accept: application/json' \
    -H 'X-Auth-Token: e22f12fe18974e181d22a1d51c9be13d8dad948d'\
    -d client=local \
    -d tgt='*' \
    -d fun=test.ping
