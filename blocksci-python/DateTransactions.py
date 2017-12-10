import blocksci
import re

chain = blocksci.Blockchain("/home/hturki/bitcoin-blocksci")
txs_of_interest = open("/home/hturki/txs_of_interest.csv", "r").read()[1:-1].split("\n")


dates = open('/home/hturki/tx_dates_of_interest.csv', 'w')
dates.write("tx_index,timestamp\n")

for line in txs_of_interest[1:]:
    tx = blocksci.Tx.tx_with_index(int(line))
    dates.write("%s,%d\n" % (line, tx.block.timestamp))

dates.close()
