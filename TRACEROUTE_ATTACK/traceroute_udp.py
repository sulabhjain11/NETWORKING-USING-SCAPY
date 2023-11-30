# UDP PACKET IS SENT WITH INCREMENTING TTL VALUE. IF THE SPECIFIED PORT IS RUNNING UDP(OPEN) AND IS UNLIKELY TO RESPOND
# IN SUCH CASES THAT DEVICE ENCAPSULATES THE RECEIVED PACKET INSIDE ITS ICMP TTL EXCEEDED PACKET and sendd it to the sender.
# UDP PORTS = [33434(for traceroute), 7(echo request within udp), 4500(ipsec for nat traversal),[49152,65535]]
# WHEN A ROUTER RECEIVES A TTL OF 1 - 1 =0, it sends an icmp ttl exceeded by embedding the ip+icmp of the received packet inside the sending icmp
from scapy.all import *
import random

source_ip = "192.168.1.4"
source_mac = "90:32:4b:21:66:3f"
destination_ip = "142.250.189.174"
destination_mac = "7c:a9:6b:28:1b:80" # this has to be the mac address of the first router, if you use broadcast address, it may not work
route = []
def process_function(a,b):
    if not b:
        print("received")
        for sent, received in a:
            if received["IP"].src not in route:
                route.append(received["IP"].src)
    else:
        print("not received")
        route.append("*")

def echo_request(source_ip,source_mac,destination_ip,destination_mac):
    pkt = Ether()/IP()/UDP()
    # icmp's type is by default set to echo-request
	# randomly generate icmp's id and sequence as their default value of 0 might be blocked by all firewalls.
    pkt["Ethernet"].src = source_mac
    pkt["Ethernet"].dst = destination_mac
    pkt["IP"].src = source_ip
    pkt["IP"].dst = destination_ip
    pkt["UDP"].dport = 33434
    for i in range(1,65):
        pkt["IP"].ttl = i
        a,b = srp(pkt,timeout=2)
        process_function(a,b)

def result():
    for i in route:
        print(i)
echo_request(source_ip,source_mac,destination_ip,destination_mac)
result()