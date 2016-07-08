{% set current_path = salt['environ.get']('PATH', '/bin:/usr/bin') %}
{% set data = salt.pillar.get('event_data') %}
minion_started_sls:
  cmd.run:
    - name: {{ ['python /srv/salt/base/python/AutoIQ.py', data['id']]|join(' ') }}
    - env:
      - PATH: {{ [current_path, '/usr/bin/python/']|join(':') }}
    - reload_modules: True
