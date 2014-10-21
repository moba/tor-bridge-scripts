#!/bin/bash

IPRANGE="194.132.209."

for i in `seq -w 2 254`; do
 ORPORT=$(( ( RANDOM % (65535-1024) ) + 1024 ))
 OBFS3=$(( ( RANDOM % (65535-1024) )  + 1024 ))
 SCRAMBLESUIT=$(( ( RANDOM % (65535-1024) )  + 1024 ))
 FTE=$(( ( RANDOM % (65535-1024) )  + 1024 ))
 SCRAMBLESUITPWD=`python -c 'import base64,os; print base64.b32encode(os.urandom(20))'`

cat > tor/tor$i.cfg << EOF
Address $IPRANGE$i
OutboundBindAddress $IPRANGE$i 
ORPort $ORPORT 
ORListenAddress $IPRANGE$i:$ORPORT

DataDirectory /var/lib/tor/$i
PidFile /var/run/tor/tor$i.pid
Log notice file /var/log/tor/notices$i.log

ServerTransportPlugin obfs3,scramblesuit exec /usr/bin/obfsproxy managed
ServerTransportPlugin fte exec /usr/local/bin/fteproxy --mode server --managed 
ServerTransportListenAddr obfs3 $IPRANGE$i:$OBFS3 
ServerTransportListenAddr scramblesuit $IPRANGE$i:$SCRAMBLESUIT 
ServerTransportListenAddr fte $IPRANGE$i:$FTE

ServerTransportOptions scramblesuit password=$SCRAMBLESUITPWD

ContactInfo Torservers.net <admin .at. torservers .dot. net> 

RunAsDaemon 1
PublishServerDescriptor 1
SocksPort 0
BridgeRelay 1
ExitPolicy reject *:*
ExtORPort auto 
EOF
done 

# TODO
# dirty ...!

sed -i -e "s:209\.0:209\.:g" tor/*.cfg
