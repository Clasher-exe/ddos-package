import scapy.all as scapy

# Function to get the local network IP range
def get_ip_range():
    # Assuming you're on a typical home network. Replace with your own subnet if needed
    ip = scapy.conf.route.route("0.0.0.0")[2]
    return ip.rsplit('.', 1)[0] + '.1/24'  # This gives you something like 192.168.1.1/24

# Function to scan the network and get a list of IPs
def scan_network():
    ip_range = get_ip_range()
    print(f"Scanning network: {ip_range}")
    
    # ARP request to find all devices
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast frame to reach all devices
    arp_request_broadcast = broadcast/arp_request
    
    # Send the request and receive the response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    print("\nDevices found:")
    devices = []
    for element in answered_list:
        devices.append(element[1].psrc)  # Get the IP addresses of devices
        print(f"IP Address: {element[1].psrc}")
    return devices

if __name__ == "__main__":
    devices = scan_network()
    print(f"\nAll active devices on the network: {devices}")