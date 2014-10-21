#!/usr/bin/env python2

import os

if __name__ == "__main__":
    private_procs = []

    for fn in os.listdir('/etc/tor/'):
        if fn.endswith("cfg"):
            with open(os.path.join('/etc/tor', fn)) as f:
                if "PublishServerDescriptor 0" in f.read():
                    private_procs.append(
                        int(fn.replace('tor', '').replace('.cfg', ''))
                    )

    bridges = []
    for proc_number in private_procs:
        bridge = {}
        with open("/etc/tor/tor%i.cfg" % proc_number) as f:
            for l in f.readlines():
                if l.strip().startswith("ORListenAddress"):
                    bridge['orport'] = l.strip().split(" ")[1]
                if l.strip().startswith("ServerTransportListenAddr obfs3"):
                    bridge['obfs3'] = l.strip().split(" ")[2]
                if l.strip().startswith("ServerTransportListenAddr obfs2"):
                    bridge['obfs2'] = l.strip().split(" ")[2]
                if l.strip().startswith("ServerTransportListenAddr scramblesuit"):
                    bridge['scramblesuit'] = l.strip().split(" ")[2]
                if l.strip().startswith("ServerTransportOptions scramblesuit password="):
                    bridge['scramblesuit_password'] = l.strip().split(" ")[2].split("=")[1]
    with open("/var/lib/tor/%i/fingerprint" % proc_number) as f:
            bridge ['fingerprint'] = f.read().strip().split(" ")[1]
        bridges.append(bridge)

    print "Fingerprint;ORPort;OBFS2 Address;OBFS3 Address;Scramblesuit Address;Scramblesuit Password"
    for bridge in bridges:
        print "%s;%s;%s;%s;%s;%s" % (
            bridge['fingerprint'],
            bridge['orport'],
            bridge['obfs2'],
            bridge['obfs3'],
            bridge['scramblesuit'],
            bridge['scramblesuit_password'],
    )

