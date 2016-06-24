# /srv/salt/orch/do_complex_thing.sls
{% set tag = salt.pillar.get('event_tag') %}
{% set data = salt.pillar.get('event_data').get('post', {}) %}


# Pass data from the event to a custom runner function.
# The function expects a 'foo' argument.
do_first_thing:
  salt.runner:
    - name: test.sleep
    - s_time: {{ data.time }}

# Wait for the runner to finish then send an execution to minions.
# Forward some data from the event down to the minion's state run.
do_second_thing:
  salt.state:
    - tgt: {{ data.tgt }}
    - sls:
      - {{ data.sls }}
    - require:
      - salt: do_first_thing

