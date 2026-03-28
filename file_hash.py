#!/usr/bin/env python3
"""File hasher — compute and compare file hashes."""
import sys, hashlib
def hash_file(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk: break
            h.update(chunk)
    return h.hexdigest()
def cli():
    if len(sys.argv) < 2: print("Usage: file_hash <file> [algo] [--compare HASH]"); sys.exit(1)
    path = sys.argv[1]; algo = sys.argv[2] if len(sys.argv)>2 and not sys.argv[2].startswith("-") else "sha256"
    h = hash_file(path, algo)
    print(f"  {algo}: {h}")
    if "--compare" in sys.argv:
        expected = sys.argv[sys.argv.index("--compare")+1]
        print(f"  Match: {'✓' if h == expected.lower() else '✗'}")
if __name__ == "__main__": cli()
