#!/bin/sh
# Regenerate assets/pinkleaf-tailwind.css from the classes used in index.html.
#
# The site used to load Tailwind's Play CDN, which their docs say is for
# development only: it ships ~360 KB of JS and builds the stylesheet in the
# browser on every visit. This produces the same utilities ahead of time,
# around 10 KB.
#
# Run from the repo root after adding any new Tailwind utility class:
#   sh tools/build_tailwind.sh
set -e
cd "$(dirname "$0")/.."
tmp=$(mktemp -d)
printf '@tailwind base;\n@tailwind components;\n@tailwind utilities;\n' > "$tmp/in.css"
cat > "$tmp/tailwind.config.js" <<CFG
module.exports = { content: ['$PWD/index.html'], theme: { extend: {} } };
CFG
npx -y tailwindcss@3 -c "$tmp/tailwind.config.js" -i "$tmp/in.css" -o assets/pinkleaf-tailwind.css --minify
rm -rf "$tmp"
echo "wrote assets/pinkleaf-tailwind.css"
