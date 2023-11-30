# RESULT: I am reciving a ping request with the data included in it.
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

# Define the data to send inside icmp layer
data = "This is the data to send through the ICMP tunnel." #sending a normal message
pkt = pkt/data

# sending the constructed packet
sendp(pkt)