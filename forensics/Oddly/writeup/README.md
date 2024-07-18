# Writeup

We were given with a network capture packet (PCAP) file named 'oddly.pcap'. Before proceeding further, we initiated the initial analysis by examining the packet hierarchy and its structure.

### Intro
```sh
» tshark -r oddly.pcap -qz io,phs

===================================================================
Protocol Hierarchy Statistics
Filter:

frame                                    frames:776 bytes:3562082
  eth                                    frames:776 bytes:3562082
    ip                                   frames:776 bytes:3562082
      icmp                               frames:776 bytes:3562082
===================================================================

» tshark -r oddly.pcap | head
    1   0.000000   172.17.0.1 → 172.17.0.2   ICMP 105 Echo (ping) request  id=0x009e, seq=0/0, ttl=64
    2  -8.634514   172.17.0.2 → 172.17.0.1   ICMP 6840 Echo (ping) reply    id=0x0051, seq=0/0, ttl=64
    3 -15.798274   172.17.0.2 → 172.17.0.1   ICMP 66 Echo (ping) reply    id=0x0017, seq=0/0, ttl=64
    4   6.075767   172.17.0.1 → 172.17.0.2   ICMP 105 Echo (ping) request  id=0x00d0, seq=0/0, ttl=64
    5   0.836474   172.17.0.1 → 172.17.0.2   ICMP 105 Echo (ping) request  id=0x00a5, seq=0/0, ttl=64
    6 -12.786985   172.17.0.1 → 172.17.0.2   ICMP 105 Echo (ping) request  id=0x0030, seq=0/0, ttl=64
    7   5.616478   172.17.0.1 → 172.17.0.2   ICMP 105 Echo (ping) request  id=0x00cc, seq=0/0, ttl=64
    8 -11.178451   172.17.0.2 → 172.17.0.1   ICMP 66 Echo (ping) reply    id=0x003d, seq=0/0, ttl=64
    9  19.279498   172.17.0.1 → 172.17.0.2   ICMP 105 Echo (ping) request  id=0x0137, seq=0/0, ttl=64
    10  -8.960841   172.17.0.1 → 172.17.0.2   ICMP 105 Echo (ping) request  id=0x004f, seq=0/0, ttl=64
```
Upon inspection, the PCAP was found to contain ICMP traffic. Referring to the challenge description, the first anomaly noted was the apparent disorder of packets. This irregularity was identified by negative values in the 'frame.time_delta' section, which typically do not occur naturally unless packets were deliberately shuffled. Fortunately, we resolved this issue using 'reordercap', a tool that automatically arranges packets according to their actual timestamps.
```sh
» reordercap oddly.pcap oddly.pcapng
776 frames, 376 out of order

» tshark -r oddly.pcapng | head
    1   0.000000   172.17.0.1 → 172.17.0.2   ICMP 57 Echo (ping) request  id=0x0000, seq=0/0, ttl=64
    2   0.059703   172.17.0.2 → 172.17.0.1   ICMP 246 Echo (ping) reply    id=0x0000, seq=0/0, ttl=64
    3   1.378688   172.17.0.1 → 172.17.0.2   ICMP 61 Echo (ping) request  id=0x0001, seq=0/0, ttl=64
    4   1.417851   172.17.0.2 → 172.17.0.1   ICMP 77 Echo (ping) reply    id=0x0001, seq=0/0, ttl=64
    5   2.050788   172.17.0.1 → 172.17.0.2   ICMP 58 Echo (ping) request  id=0x0002, seq=0/0, ttl=64
    6   2.089784   172.17.0.2 → 172.17.0.1   ICMP 76 Echo (ping) reply    id=0x0002, seq=0/0, ttl=64
    7   5.435185   172.17.0.1 → 172.17.0.2   ICMP 61 Echo (ping) request  id=0x0003, seq=0/0, ttl=64
    8   5.465797   172.17.0.2 → 172.17.0.1   ICMP 388 Echo (ping) reply    id=0x0003, seq=0/0, ttl=64
    9   7.506671   172.17.0.1 → 172.17.0.2   ICMP 69 Echo (ping) request  id=0x0004, seq=0/0, ttl=64
   10   7.549780   172.17.0.2 → 172.17.0.1   ICMP 318 Echo (ping) reply    id=0x0004, seq=0/0, ttl=64
```
After restoring the correct packet order, we examined the ICMP data for both ICMP Requests and Reply, which, as per the challenge description, appeared to contain shell commands.
```sh
» tshark -r oddly.pcapng -Y 'frame.number eq 1' -Tfields -e data | xxd -r -p > request
» tshark -r oddly.pcapng -Y 'frame.number eq 2' -Tfields -e data | xxd -r -p > reply
» file request reply
request: zlib compressed data
reply:   zlib compressed data

» zlib-flate -uncompress < request
id | od

» zlib-flate -uncompress < reply
0000000 064565 036544 024060 067562 072157 020051 064547 036544
0000020 024060 067562 072157 020051 071147 072557 071560 030075
0000040 071050 067557 024564 030454 061050 067151 026051 024062
0000060 060544 066545 067157 026051 024063 074563 024563 032054
0000100 060450 066544 026051 024066 064544 065563 026051 030061
0000120 073450 062550 066145 026051 030461 063050 067554 070160
0000140 024571 031054 024060 064544 066141 072557 024564 031054
0000160 024066 060564 062560 026051 033462 073050 062151 067545
0000200 005051
0000202
```
Based on these findings, we concluded that the ICMP traffic indeed included shell executions on the server. The ICMP Request transmitted the initial command, while the ICMP Reply responded with the **od** output of that command. Due to the ICMP packet size limit of 65515 bytes, both command and output were compressed using Zlib. Before proceeding any further, let's briefly talk about **od**.

### Literature Study
GNU **od** is a command-line utility used to display data in various human-readable formats. By default, it reads file contents in 16-byte chunks, presenting them in octal representation. Here's a brief overview of how od typically functions and how we can recover the original data:
```sh
» echo -n ab | od
0000000 061141
0000002
» python
>>> import struct
>>> struct.pack('<H', int('061141', 8))
b'ab'
```
Essentially, the process involves converting each octal column into a base-10 integer and then repacking it into a byte string. However, we also need to account for cases where there are repeated bytes in the input file. Unlike **xxd**, od represents identical lines of output with `*` to reduce redundancy and save storage space.
```sh
» python -c 'print("A"*128 + "B")' | od
0000000 040501 040501 040501 040501 040501 040501 040501 040501
*
0000200 005102
0000202
```
In the example provided, although multiple lines were repeated, the `*` symbol appeared only once. Therefore, it's essential to track the byte offset to accurately determine the number of repeated lines. For implementation details of the od reversal process, refer to our [code](https://gist.github.com/hanasuru/d3c39a0f2f55d45f9bca0860836a50c7)
```sh
» echo abc | od | rod
abc

» md5sum /bin/bash
d7bc3ce3b6b7ac53ba2918a97d806418  /bin/bash

» od /bin/bash | rod | md5sum
d7bc3ce3b6b7ac53ba2918a97d806418  -
```

### Analysis
After understanding the concept, it's time to analyze what the actor did inside the server, starting by exfiltrating both ICMP request and reply data.
```sh
# Request
» tshark -r oddly.pcapng -Y 'icmp.type eq 8' -Tfields -e data | xargs -IZ bash -c 'echo Z | xxd -r -p > data; echo $(zlib-flate -uncompress < data)'

id | od
whoami | od
pwd | od
ls -la | od
cat /etc/hosts | od
cat /etc/passwd | od
cat requirements.txt | od
cat init.sh | od
cat server.py | od
file /tmp/storage.img | od
df -h | od
dd if=/dev/loop1 bs=6000 skip=187 count=2 2>/dev/null | od
dd if=/dev/loop1 bs=6000 skip=304 count=1 2>/dev/null | od
--snip--
dd if=/dev/loop1 bs=6000 skip=400 count=2 2>/dev/null | od
dd if=/dev/loop1 bs=6000 skip=160 count=1 2>/dev/null | od
dd if=/dev/loop1 bs=6000 skip=34 count=2 2>/dev/null | od
```
```sh
# Reply
» tshark -r oddly.pcapng -Y 'icmp.type eq 0' -Tfields -e data | xargs -IZ bash -c 'echo Z | xxd -r -p > data; zlib-flate -uncompress < data | rod; echo'

uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)

root

/app

total 20
drwxr-xr-x    1 root     root          4096 Jul  3 18:53 .
drwxr-xr-x    1 root     root          4096 Jul  3 18:54 ..
-rwxr-xr-x    1 root     root           211 Jul  3 18:53 init.sh
-rw-r--r--    1 root     root            21 Jul  2 12:37 requirements.txt
-rwxr-xr-x    1 root     root          1281 Jul  3 18:27 server.py

127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.17.0.2      bad6e0ff0b407254b5563fef9160c80a

root:x:0:0:root:/root:/bin/sh
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin

netfilterqueue
scapy
#!bin/sh
iptables -A INPUT -p icmp -j NFQUEUE --queue-num 1
iptables -A INPUT -p icmp -j NFQUEUE --queue-num 0
losetup /dev/loop1 /tmp/storage.img
hostname | cryptsetup luksOpen /dev/loop1 storage
/app/server.py
--snip--
```
Based on the output above, we can clearly see the actor was trying to enumerate basic information within the server. Furthermore, the attacker attempted to dump the mounted disk storage using **dd**. Originally, the disk image was a LUKS-protected image, but since the configuration file `init.sh` was also exposed, we know that the password was simply the server's **hostname**, which is `bad6e0ff0b407254b5563fef9160c80a`.

Since the disk image could be considered confidential, we tried to reconstruct the disk image based on the dd arguments and its output. Here's our implementation code.
```py
from scapy.all import *
from rod import ROD

import zlib
import re

packets = rdpcap('oddly.pcapng')
rule = re.compile(rb'dd if=/dev/loop1 bs=(\d+) skip=(\d+) count=(\d+)')

# Allocate big buffer
fd = open('storage.img', 'wb')
fd.write(b'\x00' * int(7e+6))

for enum, pkt in enumerate(packets):
    icmp = pkt[ICMP]
    data = zlib.decompress(pkt.load)

    if icmp.type == 8:
        print(f'$ {data.decode()}')
        if rule.search(data):
            bs, skip, count = map(int, rule.findall(data)[0])
    else:
        data = data.decode()
        data = ROD(data.splitlines()).ascii

        if enum > 21:
            fd.seek(bs*skip)
            fd.write(data)

        else:
            print(data.decode())
```
After that, we simply mounted and examined the disk image using the information we got from the previous step.
```sh
» echo bad6e0ff0b407254b5563fef9160c80a | sudo cryptsetup luksOpen storage.img storage
» sudo fls /dev/mapper/storage
r/r * 9:        flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_59.txt
r/r * 16:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_58.txt
r/r * 23:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_54.txt
r/r * 30:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_30.txt
r/r * 37:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_61.txt
r/r * 44:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_36.txt
r/r * 51:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_17.txt
r/r * 58:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_42.txt
r/r * 65:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_65.txt
r/r * 72:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_53.txt
r/r * 79:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_19.txt
r/r * 86:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_70.txt
r/r * 93:       flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_9.txt
r/r * 100:      flaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaag_27.txt
--snip--
v/v 98131:      $MBR
v/v 98132:      $FAT1
v/v 98133:      $FAT2
V/V 98134:      $OrphanFiles
```
There we could see that there were several flag artifacts that seemed to have been deleted. Fortunately, the data sectors themselves were not missing, so the information was mostly recoverable.
```sh
» sudo fls /dev/mapper/storage | sort -t_ -k2 -n | grep -oP '\d+(?=:.f)' | xargs -l sudo icat /dev/mapper/storage $1 | paste -sd ''
gemastik{it_was_truly_odd_enough_to_craft_an_od_bash_shell_using_icmp}
```

### Flag
>gemastik{it_was_truly_odd_enough_to_craft_an_od_bash_shell_using_icmp}