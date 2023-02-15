#!/usr/bin/env python3
import hashlib
import sys

target = sys.argv[1]

i = 0
while True:
    h = hashlib.sha1(str(i).encode('ascii')).hexdigest()
    if h.endswith(target):
        print(i)
        break

    i += 1
