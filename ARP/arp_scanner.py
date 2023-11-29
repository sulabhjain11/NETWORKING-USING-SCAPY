# this is an active arp scanner. either scan using local broadcast or send an arp request to all possible devices in the network.
# MULTIPROCESSING HAS BEEN USED
from scapy.all import *
import signal # IF THE USER PRESSES CONTROL C WHILE THE PACKET IS BEING SENT ,IT WILL NOT BE INTERRUPTED
import sys
import multiprocessing

ip_scanner = "192.168.163.128" #/24 address
mac_scanner = "00:0c:29:a7:96:49"
ip_broadcast = "255.255.255.255" # another way is the directed broadcast(network.255)
pkt = Ether()/ARP()
g_responded = []
def local_broadcast_arpscanner(pkt,ip_broadcast):
	pkt["Ether"].src = mac_scanner
	pkt["ARP"].op = 1 # who-has
	pkt["ARP"].hwsrc = mac_scanner
	pkt["ARP"].psrc = ip_scanner
	pkt["ARP"].pdst = ip_broadcast
	pkt.show()
	sendp(pkt)
# def individual_arp_request(pkt,ip_scanner,mac_scanner):
# 	pkt["Ether"].src = mac_scanner
# 	pkt["ARP"].op = 1 # who-has
# 	pkt["ARP"].hwsrc = mac_scanner
# 	pkt["ARP"].psrc = ip_scanner
# 	ip_split = ip_scanner.split(".")
# 	for i in range(1, 255):
# 		ip_split[3] = str(i)
# 		ip_target = ".".join(ip_split)
# 		pkt["ARP"].pdst = ip_target
# 		result = srp(pkt, timeout=2)[0]
# 		g_responded.append(result)
# 	print("hello there")
# 	process_packet() # if there was no interruption from keyboard in the above process

def process_packet(results):
	pass
	# print(g_responded)
	for result in results:
		for sent,answered in result:
			print(f"ip:{answered.psrc}, mac:{answered.hwsrc}")
def signal_handler(signal, frame):
	print("Interrupt received.")
	process_packet()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#local_broadcast_arpscanner(pkt,ip_broadcast)
# individual_arp_request(pkt,ip_scanner,mac_scanner)


def individual_arp_requestt(v):
	pkt["Ether"].src = mac_scanner
	pkt["ARP"].op = 1 # who-has
	pkt["ARP"].hwsrc = mac_scanner
	pkt["ARP"].psrc = ip_scanner
	ip_split = ip_scanner.split(".")
	ip_split[3] = str(v)
	ip_target = ".".join(ip_split)
	pkt["ARP"].pdst = ip_target
	result = srp(pkt, timeout=2,verbose=False)[0]
	return result
	# g_responded.append(result)

pool_obj = multiprocessing.Pool(50)
results = pool_obj.map(individual_arp_requestt,range(1,255))
pool_obj.close()

process_packet(results) # if there was no interruption from keyboard in the above process