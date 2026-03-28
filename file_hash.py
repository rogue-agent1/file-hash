#!/usr/bin/env python3
"""file_hash — Hash files with multiple algorithms and verify checksums."""
import sys, hashlib, os, argparse

ALGOS = ['md5','sha1','sha256','sha512']

def hash_file(path, algo='sha256'):
    h = hashlib.new(algo)
    with open(path, 'rb') as f:
        while chunk := f.read(8192): h.update(chunk)
    return h.hexdigest()

def cmd_hash(a):
    for f in a.files:
        if a.all:
            print(f'{f}:')
            for algo in ALGOS: print(f'  {algo:8s}: {hash_file(f, algo)}')
        else:
            print(f'{hash_file(f, a.algo)}  {f}')

def cmd_verify(a):
    expected = a.checksum.lower()
    actual = hash_file(a.file, a.algo)
    if actual == expected: print(f'✅ Match ({a.algo})')
    else: print(f'❌ Mismatch\n  Expected: {expected}\n  Got:      {actual}'); sys.exit(1)

def cmd_compare(a):
    h1, h2 = hash_file(a.file1, a.algo), hash_file(a.file2, a.algo)
    if h1 == h2: print(f'✅ Files are identical ({a.algo}: {h1[:16]}...)')
    else: print(f'❌ Files differ\n  {a.file1}: {h1}\n  {a.file2}: {h2}')

def main():
    p = argparse.ArgumentParser(description='File hashing tool')
    p.add_argument('-a','--algo', default='sha256', choices=ALGOS)
    s = p.add_subparsers(dest='cmd', required=True)
    sh = s.add_parser('hash'); sh.add_argument('files',nargs='+'); sh.add_argument('--all',action='store_true'); sh.set_defaults(func=cmd_hash)
    sv = s.add_parser('verify'); sv.add_argument('file'); sv.add_argument('checksum'); sv.set_defaults(func=cmd_verify)
    sc = s.add_parser('compare'); sc.add_argument('file1'); sc.add_argument('file2'); sc.set_defaults(func=cmd_compare)
    a = p.parse_args(); a.func(a)

if __name__=='__main__': main()
