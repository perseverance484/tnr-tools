# Sourced by run.sh and tools/test_gencheck.sh.
# run_generator_checks CMD...: runs every command (each one string, evaluated as-is), appending its
# output to stdout. Returns 1 if ANY command exits nonzero or prints "STALE", else 0. Every command
# runs even after an earlier failure, so the log always shows the full picture (review F2: a grouped
# `{ a; b; } || x` only saw the last command's status).
run_generator_checks() {
  local status=0 cmd out rc
  for cmd in "$@"; do
    out="$(eval "$cmd" 2>&1)"; rc=$?
    printf '%s\n' "$out"
    if [[ $rc -ne 0 ]]; then
      printf 'GENERATOR CHECK FAILED (exit %s): %s\n' "$rc" "$cmd"; status=1
    elif grep -q "STALE" <<<"$out"; then
      printf 'GENERATOR CHECK STALE: %s\n' "$cmd"; status=1
    fi
  done
  return "$status"
}
