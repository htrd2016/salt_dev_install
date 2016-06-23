curl localhost:8000/run \
    -H 'Accept: application/x-yaml' \
    -d client='local' \
    -d tgt='*' \
    -d fun='test.ping' \
    -d username='yang' \
    -d password='yang' \
    -d eauth='pam'
