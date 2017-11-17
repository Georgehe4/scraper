import blocksci
import re

chain = blocksci.Blockchain("/home/hturki/bitcoin-blocksci")
address_file = open("/home/hturki/btc_talk_data_1_5_7_241.txt", "r").read()
addresses = address_file[1:-1].split("', '")
len(addresses)

blocksci_addresses = {}

bad_addresses = set({addresses[20], addresses[497], addresses[512], addresses[862], addresses[941], addresses[1023], addresses[1164], addresses[1647], addresses[2226]})

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
