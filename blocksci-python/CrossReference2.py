import blocksci
import re

chain = blocksci.Blockchain("/home/hturki/bitcoin-blocksci")

tagged_addresses = open("/home/hturki/blockchaininfo-11112017.txt", "r").read().split("\n")


enriched = open('/home/hturki/matched_tagged_addresses_3.csv', 'w')
enriched.write("script,name,address_num,address_type\n")

prefix = len("address_type.")

tagged_address_map = {}

for tagged_address in tagged_addresses[37110:]:
    split = tagged_address.split("\t")
    script = split[0]
    blocksci_address = blocksci.Address.from_string(script)
    if blocksci_address is None:
        print("%s address was not matched" % script)
    else:
        address_type = str(blocksci_address.type)[prefix:]
        enriched.write("%s,%s,%d,%s\n" % (script, split[1], blocksci_address.address_num, address_type))
        enriched.flush()

enriched.close()
