# this is an active arp scanner. either scan using local broadcast or send an arp request to all possible devices in the network.
from scapy.all import *

ip_scanner = "192.168.1.6" #/24 address
mac_scanner = "00:c0:ca:98:77:eb"
ip_broadcast = "255.255.255.255" # another way is the directed broadcast(network.255)
pkt = Ether()/ARP()
g_responded = []
def local_broadcast_arpscanner(ip_broadcast):
	pkt = Ether()/ARP()
	pkt["Ether"].src = mac_scanner
	pkt["ARP"].op = 1 # who-has
	pkt["ARP"].hwsrc = mac_scanner
	pkt["ARP"].psrc = ip_scanner
	pkt["ARP"].pdst = ip_broadcast
	pkt.show()
	sendp(pkt)
def individual_arp_request(ip=ip_scanner):
	pkt = Ether()/ARP()
	pkt["Ether"].src = mac_scanner
	pkt["ARP"].op = 1 # who-has
	pkt["ARP"].hwsrc = mac_scanner
	pkt["ARP"].psrc = ip_scanner
	ip_split = ip.split(".")
	for i in range(1,5):
		try:
        		print(i)
        		ip_split[3] = str(i)
        		ip = ".".join(ip_split)
        		pkt["ARP"].pdst = ip
        		response, unanswered = srp(pkt,timeout=1) # wait for one second and stop listening for a response
        		g_responded.append(response)
		except KeyboardInterrupt:
        		print("Interrupted...")
        		break
	print(g_responded)
#local_broadcast_arpscanner(ip_broadcast)
individual_arp_request(ip=ip_scanner)

