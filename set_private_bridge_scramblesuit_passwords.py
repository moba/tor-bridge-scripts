#!/usr/bin/env python2

import random
import os

from string import digits, ascii_letters

def get_random_string(len):
    name_chars = ascii_letters+digits
    chars = ""

    for x in range(len):
        chars += random.choice(name_chars)

    return chars

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
        with open("/etc/tor/tor%i.cfg" % proc_number, "a") as f:
             f.write("\n ServerTransportOptions scramblesuit password=%s" % get_random_string(16))
