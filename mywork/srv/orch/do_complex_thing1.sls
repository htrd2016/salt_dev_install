do_second_thing:
  salt.state:
    - tgt: "*"
    - sls:
      - send_event1
