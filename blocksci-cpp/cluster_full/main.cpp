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
#include <blocksci/scripts/scriptsfwd.hpp>
#include <blocksci/scripts/scripthash_script.hpp>
#include <set>

using namespace blocksci;


int main(int argc, const char *argv[]) {
    assert(argc == 4);

    Blockchain chain(argv[1]);
    ClusterManager manager(argv[2]);

    std::set<uint32_t> clustersOfInterest;
    std::ifstream infile(argv[3]);
    uint32_t clusterNum;
    while (infile >> clusterNum) {
        clustersOfInterest.insert(clusterNum);
    }

    std::ofstream myfile;
    myfile.open("clusters_full.csv");

    for (auto cluster : manager.getClusters()) {
        if (!clustersOfInterest.count(cluster.clusterNum)) {
            continue;
        }

        for (auto address : cluster.getAddresses()) {
            auto script = address.getScript();
            auto scriptStr = script.get()->toString();
            myfile << cluster.clusterNum << "," << address.addressNum << "," << address.type << ","
                   << scriptStr << "\n";
        }
    }

    myfile.close();

    return 0;
}
