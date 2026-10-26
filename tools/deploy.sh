#!/bin/sh
# The only way to deploy pinkleaf.co.il. Runs the health check first and
# refuses to deploy if it fails. The catalogue lock (point 9) is in there, so
# a store whose names, photos or prices no longer match Kat's labels cannot go
# live, whichever session is driving.
#
#   sh tools/deploy.sh                 from Kat's Mac (netlify-cli, logged in)
#   sh tools/deploy.sh "<npx cmd>"     from a cloud session: pass the one-time
#                                      command the Netlify connector returned
set -e
cd "$(dirname "$0")/.."

if ! python3 tools/health_check.py; then
  echo
  echo "DEPLOY REFUSED: health check failed. Fix it (or get Kat's yes and run"
  echo "python3 tools/catalogue_lock.py approve <PVid>) and run this again."
  exit 1
fi

rm -rf tools/__pycache__ .netlify
if [ -n "$1" ]; then
  sh -c "$1"
else
  npx netlify-cli deploy --prod --dir .
fi
