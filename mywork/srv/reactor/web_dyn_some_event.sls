web_dyn_invoke_orchestrate_file:
  runner.state.orchestrate:
    - mods: orch.web_dyn_do_complex_thing
    - pillar:
        event_tag: {{ tag }}
        event_data: {{ data | json() }}

