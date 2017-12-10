import blocksci
import re
import sys

chain = blocksci.Blockchain("/home/hturki/bitcoin-blocksci.bak")
address_file = open("/home/hturki/otc_scores_dict.txt", "r").read()
addresses = list(map(lambda x: x.split('\'')[1], address_file[:-1].split("\n")))

blocksci_addresses = {}

bad_addresses = set()

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
