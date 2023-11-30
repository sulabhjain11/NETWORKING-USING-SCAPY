from scapy.all import *
import random

source_ip = "192.168.163.128"
source_mac = "00:0c:29:a7:96:49"
destination_ip = "142.250.189.174"
destination_mac = "ff:ff:ff:ff:ff:ff"

def echo_request(source_ip,source_mac,destination_ip,destination_mac):
    pkt = Ether()/IP()/ICMP()
    # icmp's type is by default set to echo-request
	# randomly generate icmp's id and sequence as their default value of 0 might be blocked by all firewalls.
    pkt["Ethernet"].src = source_mac
    pkt["Ethernet"].dst = destination_mac
    pkt["IP"].src = source_ip
    pkt["IP"].dst = destination_ip
    pkt["IP"].ttl = 5
    pkt["ICMP"].id = random.randint(1, 100)
    pkt["ICMP"].seq = random.randint(1, 100)
    sendp(pkt)

echo_request(source_ip,source_mac,destination_ip,destination_mac)