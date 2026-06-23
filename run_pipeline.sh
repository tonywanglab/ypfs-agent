#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
LOG=pipeline_full.log
MIN_FREE_GB="${MIN_FREE_GB:-15}"

free_gb() {
  df -g . | awk 'NR==2 {print $4}'
}

if [[ "$(free_gb)" -lt "$MIN_FREE_GB" ]]; then
  echo "ERROR: need at least ${MIN_FREE_GB}GB free on this volume (have $(free_gb)GB)."
  echo "Free disk space, then rerun: ./run_pipeline.sh"
  exit 1
fi

{
  echo "=== Phase 1a: pdf_to_markdown $(date) ==="
  echo "markdown on disk: $(ls markdown/*.md 2>/dev/null | wc -l | tr -d ' ')"
  # Skip already-converted docs unless FORCE=1
  PY="${PY:-.venv/bin/python}"
  MIN_FREE_MB="${MIN_FREE_MB:-1024}"
  if [[ "${FORCE:-}" == "1" ]]; then
    "$PY" pdf_to_markdown.py --all --force --min-free-mb "$MIN_FREE_MB"
  else
    "$PY" pdf_to_markdown.py --all --min-free-mb "$MIN_FREE_MB"
  fi
  echo "=== Phase 1b: annotate_figures $(date) ==="
  "$PY" annotate_figures.py --all --force
  echo "=== Audit $(date) ==="
  "$PY" test_ocr_quality.py
  echo "=== Done $(date) ==="
  echo "markdown: $(ls markdown/*.md 2>/dev/null | wc -l | tr -d ' ')"
  echo "assets dirs: $(ls -d assets/*/ 2>/dev/null | wc -l | tr -d ' ')"
} 2>&1 | tee -a "$LOG"
