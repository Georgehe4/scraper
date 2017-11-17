import blocksci
import re
import sys

chain = blocksci.Blockchain("/home/hturki/bitcoin-blocksci.bak")
address_file = open("/home/hturki/stackoverflow_addr_raw.txt", "r").read()
addresses = address_file[1:-1].split("', '")
len(addresses)

blocksci_addresses = {}

bad_addresses = set({addresses[10], addresses[18], addresses[85], addresses[204], addresses[298], addresses[302], addresses[314], addresses[340], addresses[393], addresses[500], addresses[549], addresses[715], addresses[729], addresses[736], addresses[776], addresses[1033], addresses[1131], addresses[1136], addresses[1186]})

for address in addresses:
    if len(address) != 34 or re.match(r"[a-zA-Z1-9]{27,35}$", address) is None:
        print("%s not an address" % address)
    elif (address in bad_addresses):
        print("%s makes BlockSci segfault" % address)
    else:
        blocksci_addresses[address] = (blocksci.Address.from_string(address))
        print("%s parsed correctly" % address)
    sys.stdout.flush()

prefix = len("address_type.")
for address in blocksci_addresses:
    blocksci_address = blocksci_addresses[address]
    if (blocksci_address != None):
        print("%s,%d,%s" % (address, blocksci_address.address_num, str(blocksci_address.type)[prefix:]))
