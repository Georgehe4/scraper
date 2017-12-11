import snap
import matplotlib.pyplot as plt
import numpy as np
import math
import networkx as nx

# def averageShortestPath(graph):
#     avgShortestPathList = {}
#     for node1 in graph.Nodes():
#         n1id = node1.GetId()
#         for node2 in graph.Nodes():
#             n2id = node2.GetId()
#
#
#     print 'avgShortPath', np.mean(avgShortestPathList)

def degreeDistribution(graph):
    numNodes = float(graph.GetNodes())

    # in degree dist
    DegToCntV = snap.TIntPrV()
    snap.GetInDegCnt(graph, DegToCntV)
    xIn = []
    yIn = []
    for item in DegToCntV:
        xIn.append(item.GetVal1())
        yIn.append(item.GetVal2() / numNodes)
    print 'max in degree:', max(xIn)
    print 'min in degree:', min(xIn)

    # out degree dist
    DegToCntV = snap.TIntPrV()
    snap.GetOutDegCnt(graph, DegToCntV)
    xOut = []
    yOut = []
    for item in DegToCntV:
        xOut.append(item.GetVal1())
        yOut.append(item.GetVal2() / numNodes)
    print 'max out degree:', max(xOut)
    print 'min out degree:', min(xOut)

    # degree dist
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(graph, DegToCntV)
    x = []
    y = []
    x1 = [] # after pruning outliers
    y1 = [] # after pruning outliers
    outLimit = 10 ** 2.5 # 2.5 for prelim
    for item in DegToCntV:
        x.append(item.GetVal1())
        y.append(item.GetVal2() / numNodes)
        if item.GetVal1() < outLimit:
            x1.append(item.GetVal1())
            y1.append(item.GetVal2() / numNodes)

    xMin = min(x) - 0.5
    print 'max total degree:', max(x)
    print 'min total degree:', xMin

    # test
    # DegToCntV2 = snap.TIntPrV()
    # snap.GetDegCnt(graph2, DegToCntV2)
    # xG = []
    # yG = []
    # for item in DegToCntV2:
    #     xG.append(item.GetVal1())
    #     yG.append(item.GetVal2() / float(graph2.GetNodes()))
    # print xG
    # print yG
    # exit(1)

    # lse
    x1 = [math.log10(float(i)) for i in x1]
    y1 = [math.log10(float(i)) for i in y1]
    fit = np.polyfit(x1, y1, deg=1)
    print 'a: ' + str(fit[0]) + ', b: ' + str(fit[1])
    x1 = np.linspace(1, 10 ** 4, len(x))
    y1 = [i ** fit[0] * 10 ** fit[1] for i in x1]

    #
    # print len(x)
    # print np.dot(x, y)
    # print graph.GetNodes()
    # exit(1)
    m = graph.GetNodes()

    # todo try dict of x, y

    # mlle
    # for each x, sum over it y times where y is the num of occurrences (not proportion)
    alphaMLLE = 1 + (graph.GetNodes() / (sum([np.log(i / xMin) * y[x.index(i)] * m for i in x])))
    print alphaMLLE

    x2 = np.linspace(1, 10 ** 4, len(x))
    y2 = [((alphaMLLE - 1)/xMin) * ((i / xMin) ** (-1 * alphaMLLE)) for i in x2]

    dSum = 0
    numSamples = m
    for key in x:
        dSum += np.log(key) * y[x.index(key)] * m
    mlle = 1 + numSamples / float(dSum)
    print mlle

    # theoretical power pdf
    yPdf = [1 / float(i ** 2) for i in x2]

    # plot
    # plt.loglog(xIn, yIn, color='black', ls='None', marker='.', label='in degree')
    # plt.loglog(xOut, yOut, color='red', ls='None', marker='.', label='out degree')
    plt.loglog(x, y, color='blue', ls='None', marker='.', label='Degree Distribution')
    plt.loglog(x1, y1, color='red', ls='solid', marker='None', label='Least Squares Estimate')
    plt.loglog(x2, y2, color='green', ls='solid', marker='None', label='Max Log-Likelihood Estimate')
    # plt.loglog(xG, yG, color='black', ls='None', marker='.', label='generated power dist')
    # plt.loglog(x2, yPdf, color='black', ls='solid', marker='None', label='theoretical power law pdf')
    plt.xlabel('Node Degree')
    plt.ylabel('Proportion of Nodes')
    plt.title('Degree Distribution of BTCtalk and BTC subreddit')
    plt.legend()
    plt.show()
    return

# main/flow
# graph = snap.LoadEdgeList(snap.PNGraph, "cluster_links_without_0.csv", 0, 1, ',')
graph = snap.LoadEdgeList(snap.PNGraph, "cluster_links_without_0.csv", 0, 1, ',')
# print graph.GetNodes()
# print graph.GetEdges()
# exit(1)

# Rnd = snap.TRnd()
# graph2 = snap.GenPrefAttach(308780, 5, Rnd)

# edgeList = []
# nxgraph = nx.from_edgelist(edgeList)
# exit(1)

degreeDistribution(graph)
snap.PrintInfo(graph, 'btctalk + btc subreddit', 'graphinfo.txt', False)
print 'clustering coefficient:', snap.GetClustCf (graph, -1)