import snap
import numpy as np

graph = snap.LoadEdgeList(snap.PUNGraph, 'broad2010.csv', 0, 1, ',')
graphWCC = snap.GetMxWcc(graph)
shortPathList = []
for sNode in graphWCC.Nodes():
    s = sNode.GetId()
    shortPathListS = []
    NIdToDistH = snap.TIntH()
    snap.GetShortPath(graphWCC, s, NIdToDistH)
    for item in NIdToDistH:
        shortPathListS.append(NIdToDistH[item])
    shortPathList.append(np.mean(shortPathListS))
print np.mean(shortPathList)
print np.std(shortPathList)
print min(shortPathList)
print max(shortPathList)
print len(shortPathList)

graph = snap.LoadEdgeList(snap.PUNGraph, 'dev2010.csv', 0, 1, ',')
graphWCC = snap.GetMxWcc(graph)
shortPathList = []
for sNode in graphWCC.Nodes():
    s = sNode.GetId()
    shortPathListS = []
    NIdToDistH = snap.TIntH()
    snap.GetShortPath(graphWCC, s, NIdToDistH)
    for item in NIdToDistH:
        shortPathListS.append(NIdToDistH[item])
    shortPathList.append(np.mean(shortPathListS))
print np.mean(shortPathList)
print np.std(shortPathList)
print min(shortPathList)
print max(shortPathList)
print len(shortPathList)