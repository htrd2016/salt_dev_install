install nano on my minion:
  local.pkg.install:
    - tgt: '*'
    - arg:
      - nano
