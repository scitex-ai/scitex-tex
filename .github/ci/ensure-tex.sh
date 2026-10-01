#!/usr/bin/env bash
# Source this script before owning PDF tests. Extract only into job-owned
# scratch; no HOME installation, PATH symlink, mutable release, or apt changes.
set -euo pipefail
: "${TMPDIR:?TMPDIR must name job-owned writable scratch}"
case "$TMPDIR" in /*) ;; *) echo "::error::TMPDIR must be absolute"; exit 1 ;; esac
TEX_JOB_ROOT="$(mktemp -d "$TMPDIR/scitex-tex-compiler.XXXXXXXX")"
TEX_ARCHIVE="$TEX_JOB_ROOT/TinyTeX-1-linux-x86_64-v2026.10.tar.xz"
TEX_SHA256="4d519d6236ee6798e3ec0d8e2093d1fda01aeb267aa22c2a5586d76bcfce6566"
curl -fsSL --retry 3 -o "$TEX_ARCHIVE" \
    https://github.com/rstudio/tinytex-releases/releases/download/v2026.10/TinyTeX-1-linux-x86_64-v2026.10.tar.xz
printf '%s  %s\n' "$TEX_SHA256" "$TEX_ARCHIVE" | sha256sum --check --status
tar -xJf "$TEX_ARCHIVE" -C "$TEX_JOB_ROOT"
export PATH="$TEX_JOB_ROOT/.TinyTeX/bin/x86_64-linux:$PATH"
command -v pdflatex >/dev/null
pdflatex --version | head -n 2
echo "tex-compiler: TinyTeX-1 v2026.10 sha256=$TEX_SHA256 (verified; job-owned)"
