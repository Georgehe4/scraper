import blocksci
import re

chain = blocksci.Blockchain("/home/hturki/bitcoin-blocksci")
suspicious_addresses = open("/home/hturki/suspicious_addresses_2.csv", "r").read()[1:-1].split("\n")

info = open('/home/hturki/suspicious_clusters_with_addresses_2.csv', 'w')
info.write("cluster_id,address_num,address_type,address\n")

for line in suspicious_addresses[1:]:
    address_num = int(line.split(",")[1])
    info.write(line + "," + blocksci.Address(address_num, blocksci.address_type.pubkeyhash).script.address + "\n")

info.close()
