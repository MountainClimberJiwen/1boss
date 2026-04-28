#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/jiwen/PycharmProjects/iboss/vue"

cd "$ROOT"
npm install
exec npm run dev
