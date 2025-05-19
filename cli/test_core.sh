#!/bin/bash
set -e
python cli/self_test.py
curl -s http://localhost:8080/api/artemis | grep -i "status" && echo "API OK"
