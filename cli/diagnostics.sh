#!/bin/bash
./project_sync_diagnostics.sh | grep -E 'branch|Untracked files|MISSING|OK:|Recent commits'
