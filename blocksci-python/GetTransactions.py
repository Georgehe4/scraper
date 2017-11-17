import blocksci
import re

chain = blocksci.Blockchain("/home/hturki/bitcoin-blocksci")
prefix = len("address_type.")

addresses_of_interest = open("/home/hturki/addresses_to_get_transactions_of.csv", "r").read()[1:-1].split("\n")

address_set = set()
for line in addresses_of_interest:
    values = line.split(",")
    address_set.add((values[0], values[1]))

inputs = open('/home/hturki/input_transactions_of_interest.csv', 'w')
inputs.write("block_id,tx_index,index,address_num,address_type,amount\n")

outputs = open('/home/hturki/output_transactions_of_interest.csv', 'w')
outputs.write("block_id,tx_index,index,address_num,address_type,amount\n")

links = open('/home/hturki/tx_flows_of_interest.csv', 'w')
links.write("tx_index,from_address_type,from_address_type,to_address_num,to_address_type\n")

for block in chain.__iter__():
    print("Processing block %d" % block.height)
    for tx in block.__iter__():
        printTx = False
        for i in range(len(tx.ins)):
            address_num = str(tx.ins[i].address.address_num)
            address_type = str(tx.ins[i].address.type)[prefix:]
            if (address_num, address_type) in address_set:
                printTx = True
                break

        if printTx is False:
            for i in range(len(tx.outs)):
                address_num = str(tx.outs[i].address.address_num)
                address_type = str(tx.outs[i].address.type)[prefix:]
                if (address_num, address_type) in address_set:
                    printTx = True
                    break

        if printTx is True:
            for i in range(len(tx.ins)):
                address_num = str(tx.ins[i].address.address_num)
                address_type = str(tx.ins[i].address.type)[prefix:]
                inputs.write("%d,%d,%d,%s,%s,%d\n" % (block.height, tx.index, i, address_num, address_type, tx.ins[i].value))

            for i in range(len(tx.outs)):
                address_num = str(tx.outs[i].address.address_num)
                address_type = str(tx.outs[i].address.type)[prefix:]
                outputs.write("%d,%d,%d,%s,%s,%d\n" % (block.height, tx.index, i, address_num, address_type, tx.outs[i].value))
            
            for i in range(len(tx.ins)):
                from_address_num = tx.ins[i].address.address_num
                from_address_type = str(tx.ins[i].address.type)[prefix:]
                
                for j in range(len(tx.outs)):
                    to_address_num = tx.outs[j].address.address_num
                    to_address_type = str(tx.outs[j].address.type)[prefix:]
                    links.write("%d,%d,%s,%d,%s\n" % (tx.index, from_address_num, from_address_type, to_address_num, to_address_type))
                    
inputs.close()
outputs.close()
links.close()

