import blocksci
import re

chain = blocksci.Blockchain("/home/hturki/bitcoin-blocksci")
address_file = open("/home/hturki/reddit_addresses_full.txt", "r").read()
addresses = address_file[3:-1].split("', u'")
len(addresses)

blocksci_addresses = {}

bad_addresses = set({addresses[11})

for address in addresses:
    if len(address) != 34 or re.match(r"[a-zA-Z1-9]{27,35}$", address) is None:
        print("%s not an address" % address)
    elif (address in bad_addresses):
        print("%s makes BlockSci segfault" % address)
    else:
        blocksci_addresses[address] = (blocksci.Address.from_string(address))
        print("%s parsed correctly" % address)

prefix = len("address_type.")
for address in blocksci_addresses:
    blocksci_address = blocksci_addresses[address]
    if (blocksci_address != None):
        print("%s,%d,%s" % (address, blocksci_address.address_num, str(blocksci_address.type)[prefix:]))
