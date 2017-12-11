import snap
import matplotlib.pyplot as plt

# specify input files
broadFiles = []
devFiles = []
for i in xrange(8):
    broadFiles.append('broad' + str(2010 + i) + '.csv')
    devFiles.append('dev' + str(2010 + i) + '.csv')

numNodesB = []
for filename in broadFiles:
    graph = snap.LoadEdgeList(snap.PNGraph, filename, 0, 1, ',')
    numNodesB.append(graph.GetNodes())

numNodesD = []
for filename in devFiles:
    graph = snap.LoadEdgeList(snap.PNGraph, filename, 0, 1, ',')
    numNodesD.append(graph.GetNodes())

x = [2010 + i for i in xrange(8)]

# max scc size
plt.plot(x, numNodesB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, numNodesD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Number of Nodes')
# plt.title('Max Strongly-Connected Component Size Over Time')
plt.legend()
plt.savefig('numNodes.png')
plt.clf()