invoke_orchestrate_file:
  runner.state.orchestrate:
    - mods: orch.minion_started
    - pillar:
        event_tag: {{ tag }}
        event_data: {{ data | json() }}
