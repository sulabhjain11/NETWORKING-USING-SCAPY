# RESULT: I am receiving a ping request with the data included in it.
from scapy.all import *
import random

# Define the source and destination IP addresses
src_ip = "192.168.163.128"
dst_ip = "192.168.1.4"

# CREATING THE LAYERS
pkt = Ether()/IP()/ICMP()

# defining the ethernet layer
pkt["Ethernet"].src = "00:0c:29:a7:96:49"
pkt["Ethernet"].dst = "00:50:56:e7:1a:49"

# defining the ip layer
pkt["IP"].src = "192.168.163.128"
pkt["IP"].dst = "192.168.163.2"

# Create an ICMP echo request packet
# type has to be echo request or echo response for data of any size to be embedded to it.
pkt["ICMP"].id = random.randint(1,100)
pkt["ICMP"].seq = random.randint(1,100)

# Methods to encapsulate udp packets inside icmp packet when udp packets are blocked by firewall
pkt1 = pkt/UDP()
sendp(pkt1)
pkt2 = pkt/IP()/UDP()
sendp(pkt2)
pkt3 = pkt/Ether()/IP()/UDP()
sendp(pkt3)

# Methods to encapsulate tcp packets inside icmp packet when tcp packets are blocked by firewall
pkt1 = pkt/TCP()
sendp(pkt1)
pkt2 = pkt/IP()/TCP()
sendp(pkt2)
pkt3 = pkt/Ether()/IP()/TCP()
sendp(pkt3)
