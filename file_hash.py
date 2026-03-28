#!/usr/bin/env python3
"""file_hash - Hash files with multiple algorithms."""
import sys,hashlib,os
ALGOS=["md5","sha1","sha256","sha512"]
def hash_file(path,algo="sha256",chunk=8192):
    h=hashlib.new(algo)
    with open(path,"rb") as f:
        while True:
            data=f.read(chunk)
            if not data:break
            h.update(data)
    return h.hexdigest()
def verify(path,expected,algo="sha256"):
    return hash_file(path,algo)==expected.lower()
if __name__=="__main__":
    if len(sys.argv)<2:print("Usage: file_hash.py <file> [algo] [--verify hash]");sys.exit(1)
    path=sys.argv[1];algo=sys.argv[2] if len(sys.argv)>2 and sys.argv[2] in ALGOS else "sha256"
    if "--verify" in sys.argv:
        idx=sys.argv.index("--verify");expected=sys.argv[idx+1]
        print("MATCH ✓" if verify(path,expected,algo) else "MISMATCH ✗")
    elif "--all" in sys.argv:
        for a in ALGOS:print(f"{a:>6}: {hash_file(path,a)}")
    else:
        print(f"{hash_file(path,algo)}  {path}")
