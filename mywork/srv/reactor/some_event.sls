# /srv/reactor/some_event.sls
invoke_orchestrate_file:
  runner.state.orchestrate:
    - mods: orch.do_complex_thing
