#!/bin/bash
cd /e/rekishikaisetu-honnoji
for t in shio atsumori zehi hito_shiro itsukushima; do
  echo "== $t start $(date +%H:%M:%S)"
  python scripts/solo_ship.py clips $t 2>&1 | tail -4
  echo "== $t end $(date +%H:%M:%S)"
done
echo QUEUE_DONE
