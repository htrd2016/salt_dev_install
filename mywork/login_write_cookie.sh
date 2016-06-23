curl http://localhost:8000/login \
      -c ~/cookies.txt \
      -H 'Accept: application/json' \
      -d username=yang \
      -d password=yang \
      -d eauth=pam
