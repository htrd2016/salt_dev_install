# Pass data from the event to a custom runner function.
# The function expects a 'foo' argument.
do_first_thing:
  salt.runner:
    - name: test.sleep
    - s_time: 10

# Wait for the runner to finish then send an execution to minions.
# Forward some data from the event down to the minion's state run.
do_second_thing:
  salt.state:
    - tgt: "saltdev"
    - sls:
      - send_event2
    - require:
      - salt: do_first_thing

