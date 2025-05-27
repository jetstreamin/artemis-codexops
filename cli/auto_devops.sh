#!/bin/bash
# Artemis CodexOps: Automated DevOps Loop (local test, deploy, live test, fix, repeat)

MAX_ITER=250
ITER=1

while [ $ITER -le $MAX_ITER ]; do
  echo "=== Iteration $ITER/$MAX_ITER ==="

  echo "1. Running local tests..."
  make test || {
    echo "Local tests failed. Attempting auto-fix (lint/format)..."
    make lint || true
    make format || true
    make test || { echo "Auto-fix failed. Manual intervention required."; exit 1; }
  }

  echo "2. Deploying to AWS..."
  make deploy-all || { echo "Deploy failed. Retrying..."; sleep 10; continue; }

  echo "3. Running live endpoint health checks..."
  # Example: check main dashboard and API endpoints (add more as needed)
  curl -sf https://your-dashboard-url/ > /dev/null || { echo "Dashboard health check failed. Retrying..."; sleep 10; continue; }
  curl -sf https://your-api-url/plugins > /dev/null || { echo "API health check failed. Retrying..."; sleep 10; continue; }

  echo "All tests passed and deployment is healthy."
  exit 0

  ITER=$((ITER+1))
done

echo "Max iterations reached. Some tests or deployments may still be failing."
exit 1
