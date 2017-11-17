//
//  main.cpp
//  blocksci-test
//
//  Created by Harry Kalodner on 1/3/17.
//  Copyright © 2017 Harry Kalodner. All rights reserved.
//

#include <blocksci/blocksci.hpp>
#include <libcluster/cluster_manager.hpp>
#include <libcluster/cluster.hpp>
#include <iostream>
#include <fstream>

using namespace blocksci;


int main(int argc, const char *argv[]) {
    assert(argc == 2);

    ClusterManager manager(argv[1]);

//    std::vector<uint32_t> sizes;
//    sizes.reserve(manager.clusterCount());
//    for (auto cluster : manager.getClusters()) {
//        auto size = cluster.getAddressCount(blocksci::AddressType::Enum::PUBKEYHASH) + cluster.getAddressCount(blocksci::AddressType::Enum::SCRIPTHASH);
//        std::cout << size << "\n";
//    }

    std::ofstream myfile;
    myfile.open("clusters.csv");

    for (auto cluster : manager.getClusters()) {
        for (auto address : cluster.getAddresses()) {
            myfile << cluster.clusterNum << "," << address.addressNum << "," << address.type << "\n";
        }
    }

    myfile.close();

    return 0;
}
