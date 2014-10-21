#!/bin/bash

cat > interfaces << EOF
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth1
allow-hotplug eth1

iface eth1 inet static
    address 194.132.209.2 
    netmask 255.255.255.0
    broadcast 194.132.209.255
    gateway 194.132.209.1

# bridges 
EOF

for i in `seq 3 254`; do
cat >> interfaces << EOF

iface eth1 inet static
    address 194.132.209.$i
    netmask 255.255.255.0
EOF
done 
