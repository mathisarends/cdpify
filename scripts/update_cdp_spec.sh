#!/usr/bin/env bash
# Downloads the latest CDP protocol spec and regenerates cdpify/domains.
# Used by .github/workflows/update-cdp-spec.yaml to open a PR when the
# upstream spec changed. Can also be run locally: ./scripts/update_cdp_spec.sh
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "Regenerating CDP client from latest spec..."
uv run python -m cdpify.generator
