# Compatibility location

Installed workflows in `.github/workflows/` are authoritative. The old manual
installation process is retired. Historical staged files are in
`archive/staged-workflows-2026-10-06/`; do not install them.

`release_pin.yml` remains a byte-identical compatibility mirror because
`forge/tools/check_release_pin.mjs` retains this fallback. The repository
consistency gate checks mirror parity. Edit the installed workflow and update
this mirror together until that compatibility path is deliberately retired.
