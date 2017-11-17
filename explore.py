import snap
import matplotlib.pyplot as plt
import numpy as np
import math

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
    x1 = []
    y1 = []
    outLimit = 10 ** 2.5
    for item in DegToCntV:
        x.append(item.GetVal1())
        y.append(item.GetVal2() / numNodes)
        if item.GetVal1() < outLimit:
            x1.append(item.GetVal1())
            y1.append(item.GetVal2() / numNodes)

    print 'max total degree:', max(x)
    print 'min total degree:', min(x)

    # lse
    x1 = [math.log10(float(i)) for i in x1]
    y1 = [math.log10(float(i)) for i in y1]
    fit = np.polyfit(x1, y1, deg=1)
    print 'a: ' + str(fit[0]) + ', b: ' + str(fit[1])
    x1 = np.linspace(1, 10 ** 3, len(x))
    y1 = [i ** fit[0] * 10 ** fit[1] for i in x1]

    # plot
    # plt.loglog(xIn, yIn, color='black', ls='None', marker='.', label='in degree')
    # plt.loglog(xOut, yOut, color='red', ls='None', marker='.', label='out degree')
    plt.loglog(x, y, color='blue', ls='None', marker='.', label='total degree')
    plt.loglog(x1, y1, color='red', ls='solid', marker='None', label='total degree lse')
    plt.xlabel('node degree')
    plt.ylabel('proportion of nodes')
    plt.title('Degree distribution of btctalk and btc subreddit')
    plt.legend()
    plt.show()
    return

# main/flow
graph = snap.LoadEdgeList(snap.PNGraph, "cluster_links_without_0.csv", 0, 1, ',')
degreeDistribution(graph)
snap.PrintInfo(graph, 'btctalk + btc subreddit', 'graphinfo.txt', False)
print 'clustering coefficient:', snap.GetClustCf (graph, -1)