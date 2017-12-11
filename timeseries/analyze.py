import snap
import numpy as np
import matplotlib.pyplot as plt

# compute metrics
def analyze(graph):

    n = graph.GetNodes()
    m = graph.GetEdges()

    maxSCCsize = snap.GetMxSccSz(graph)
    maxWCCsize = snap.GetMxWccSz(graph)
    avgDegree = (m * float(2)) / n

    # estimate power law exponent
    degs = []
    degCounts = []
    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(graph, DegToCntV)
    for item in DegToCntV:
        degs.append(item.GetVal1())
        degCounts.append(item.GetVal2())
    xMin = min(degs) - 0.5
    m = graph.GetNodes()
    alphaMLLE = 1 + (m / (sum([np.log(i / xMin) * degCounts[degs.index(i)] for i in degs])))

    # erdos-renyi clustering coefficient
    graphER = snap.GenRndGnm(snap.PUNGraph, n, m)
    avgClustCoeffER = snap.GetClustCf(graphER, -1)

    # average shortest path
    graphWCC = snap.GetMxWcc(graph)
    avgClustCoeff = snap.GetClustCf(graphWCC, -1)
    numSamples = min(graphWCC.GetNodes(), 617) # all nodes or sample size
    Rnd = snap.TRnd(42)
    Rnd.Randomize()
    shortPathList = []
    for i in xrange(numSamples):
        s = graphWCC.GetRndNId(Rnd)
        NIdToDistH = snap.TIntH()
        snap.GetShortPath(graphWCC, s, NIdToDistH)
        for item in NIdToDistH:
            shortPathList.append(NIdToDistH[item])
    avgShortPath = np.mean(shortPathList)

    return avgClustCoeff, maxSCCsize, maxWCCsize, avgDegree, alphaMLLE, avgClustCoeffER, avgShortPath

### program flow

# specify input files
broadFiles = []
devFiles = []
for i in xrange(8):
    broadFiles.append('broad' + str(2010 + i) + '.csv')
    devFiles.append('dev' + str(2010 + i) + '.csv')

# compute broad results
avgClustCoeffB = []
maxSCCsizeB = []
maxWCCsizeB = []
avgDegreeB = []
powerLawAlphaB = []
avgClustCoeffERB = []
avgShortPathB = []
for filename in broadFiles:
    print filename
    graph = snap.LoadEdgeList(snap.PNGraph, filename, 0, 1, ',')
    results = analyze(graph)
    avgClustCoeffB.append(results[0])
    maxSCCsizeB.append(results[1])
    maxWCCsizeB.append(results[2])
    avgDegreeB.append(results[3])
    powerLawAlphaB.append(results[4])
    avgClustCoeffERB.append(results[5])
    avgShortPathB.append(results[6])

# write results to file
with open('resultsB.txt', 'w') as f:
    f.write(str(avgClustCoeffB) + '\n')
    f.write(str(maxSCCsizeB) + '\n')
    f.write(str(maxWCCsizeB) + '\n')
    f.write(str(avgDegreeB) + '\n')
    f.write(str(powerLawAlphaB) + '\n')
    f.write(str(avgClustCoeffERB) + '\n')
    f.write(str(avgShortPathB) + '\n')

# compute dev results
avgClustCoeffD = []
maxSCCsizeD = []
maxWCCsizeD = []
avgDegreeD = []
powerLawAlphaD = []
avgClustCoeffERD = []
avgShortPathD = []
for filename in devFiles:
    print filename
    graph = snap.LoadEdgeList(snap.PNGraph, filename, 0, 1, ',')
    results = analyze(graph)
    avgClustCoeffD.append(results[0])
    maxSCCsizeD.append(results[1])
    maxWCCsizeD.append(results[2])
    avgDegreeD.append(results[3])
    powerLawAlphaD.append(results[4])
    avgClustCoeffERD.append(results[5])
    avgShortPathD.append(results[6])

# write results to file
with open('resultsD.txt', 'w') as f:
    f.write(str(avgClustCoeffD) + '\n')
    f.write(str(maxSCCsizeD) + '\n')
    f.write(str(maxWCCsizeD) + '\n')
    f.write(str(avgDegreeD) + '\n')
    f.write(str(powerLawAlphaD) + '\n')
    f.write(str(avgClustCoeffERD) + '\n')
    f.write(str(avgShortPathD) + '\n')

# plots follow:
x = [2010 + i for i in xrange(8)] # list of time slices

# average clustering coefficient
plt.plot(x, avgClustCoeffB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, avgClustCoeffD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.plot(x, avgClustCoeffERB, color='red', ls='dashed', marker='.', label='G(n,m) Random Graph for General')
plt.plot(x, avgClustCoeffERD, color='blue', ls='dashed', marker='.', label='G(n,m) Random Graph for Developer')
plt.xlabel('Year')
plt.ylabel('Average Clustering Coefficient')
plt.title('Average Clustering Coefficient Over Time')
plt.legend()
plt.savefig('avgClustCoeff.png')
plt.clf()

# max scc size
plt.plot(x, maxSCCsizeB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, maxSCCsizeD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Proportion of Nodes')
plt.title('Max Strongly-Connected Component Size Over Time')
plt.legend()
plt.savefig('maxSCCsize.png')
plt.clf()

# max wcc size
plt.plot(x, maxWCCsizeB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, maxWCCsizeD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Proportion of Nodes')
plt.title('Max Weakly-Connected Component Size Over Time')
plt.legend()
plt.savefig('maxWCCsize.png')
plt.clf()

# average degree size
plt.plot(x, avgDegreeB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, avgDegreeD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Average Node Degree')
plt.title('Average Node Degree Over Time')
plt.legend()
plt.savefig('avgDegree.png')
plt.clf()

# power law exponent
plt.plot(x, powerLawAlphaB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, powerLawAlphaD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Power Law Exponent')
plt.title('Power Law Exponent Over Time')
plt.legend()
plt.savefig('powerLawAlpha.png')
plt.clf()

# average shortest path
plt.plot(x, avgShortPathB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, avgShortPathD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Estimated Shortest Path Length')
plt.title('Estimated Shortest Path Length Over Time')
plt.legend()
plt.savefig('avgShortPath.png')
plt.clf()