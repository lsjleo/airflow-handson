#!/bin/python3
# Usage: python jupyter_pass.py <password>
# This script hashes a password using SHA-1 and prints the hash.
# Make sure to install the required package if not already installed:
# pip install hashlib   

import hashlib
import sys

print(hashlib.sha1(sys.argv[1].encode()).hexdigest())