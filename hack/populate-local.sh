#!/usr/bin/env bash
set -euo pipefail

#!/usr/bin/env bash
set -euo pipefail

pushd src/backend/src/

python3 ./tests/populate.py \
  --database-engine="sqlite" \
|| popd && exit 1

popd