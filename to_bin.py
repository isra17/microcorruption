#!/usr/bin/env python3
import re
import os
import sys
target = sys.argv[1]
basename, _ = os.path.splitext(os.path.basename(target))
targetf = open(target,"r")
mapf = open(basename + ".map", 'w')
binf = open(basename + ".bin", 'wb')

last_addr = 0
b = bytearray()
for l in targetf:
    if l.strip() in ['','...']:
        continue
    addr = int(l[:4], 16)
    if l[4] == ':':
        chunk = bytes.fromhex(re.findall('((?:[0-9a-f]{4} )+)',
            l[5:])[0])
        npad = addr - last_addr
        b.extend(b'\x00' * npad + chunk)
        last_addr = addr + len(chunk)
    elif l[5] == '<':
        mapf.write('{:x}: {}\n'.format(addr, l.split('<')[1].split('>')[0]))
binf.write(b)
targetf.close()
mapf.close()
binf.close()

