{% set current_path = salt['environ.get']('PATH', '/bin:/home/test6/bin') %}
{% set data = salt.pillar.get('event_data') %}
minion_started_sls:
  cmd.run:
    - name: {{ ['python /home/test6/AutoIQ.py', data['id']]|join(' ') }}
    - env:
      - PATH: {{ [current_path, '/home/test6/salt_dev_env/bin/']|join(':') }}
    - reload_modules: True
