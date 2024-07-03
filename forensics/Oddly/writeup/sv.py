from scapy.all import *

# https://gist.github.com/hanasuru/d3c39a0f2f55d45f9bca0860836a50c7
from rod import ROD

import zlib
import re
import os

# Reorder packets based on timestamp order
os.system('reordercap oddly.pcap oddly.pcapng')

packets = rdpcap('oddly.pcapng')
rule = re.compile(rb'dd if=/dev/loop1 bs=(\d+) skip=(\d+) count=(\d+)')

# Allocate big buffer
fd = open('storage.img', 'wb')
fd.write(b'\x00' * int(7e+6))

for enum, pkt in enumerate(packets):
    icmp = pkt[ICMP]
    data = zlib.decompress(pkt.load)

    if icmp.type == 8:
        if rule.search(data):
            bs, skip, count = map(int, rule.findall(data)[0])
    else:
        data = data.decode()
        data = ROD(data.splitlines()).ascii

        if enum > 21:
            fd.seek(bs*skip)
            fd.write(data)

# Exfiltrate each of flag.txt inside disk image
os.system("echo bad6e0ff0b407254b5563fef9160c80a | sudo cryptsetup luksOpen storage.img storage")
os.system("sudo fls /dev/mapper/storage | sort -t_ -k2 -n | grep -oP '\d+(?=:.f)' | xargs -l sudo icat /dev/mapper/storage $1 | paste -sd ''")
os.system("sudo cryptsetup luksClose storage")
