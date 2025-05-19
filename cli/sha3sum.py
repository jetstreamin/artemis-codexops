#!/usr/bin/env python3
# Usage: python cli/sha3sum.py <file>
import sys, hashlib
for f in sys.argv[1:]:
    with open(f, "rb") as fh:
        d = fh.read()
        print(f"{hashlib.sha3_256(d).hexdigest()}  {f}")
