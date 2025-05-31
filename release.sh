#!/bin/bash
cd $(dirname $0)
git add .
git commit -m "Release: Self-healing, full compliance, auto-patch"
git push
git tag v2.0.1
git push origin v2.0.1
gh run list --repo jetstreamin/artemis-codexops
