import matplotlib.pyplot as plt
import string

# import results from file
avgClustCoeffB = []
maxSCCsizeB = []
maxWCCsizeB = []
avgDegreeB = []
powerLawAlphaB = []
avgClustCoeffERB = []
avgShortPathB = []

avgClustCoeffD = []
maxSCCsizeD = []
maxWCCsizeD = []
avgDegreeD = []
powerLawAlphaD = []
avgClustCoeffERD = []
avgShortPathD = []

with open('resultsB.txt') as f:
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    avgClustCoeffB = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    maxSCCsizeB = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    maxWCCsizeB = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    avgDegreeB = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    powerLawAlphaB = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    avgClustCoeffERB = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    avgShortPathB = line

with open('resultsD.txt') as f:
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    avgClustCoeffD = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    maxSCCsizeD = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    maxWCCsizeD = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    avgDegreeD = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    powerLawAlphaD = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    avgClustCoeffERD = line
    line = f.readline().split(', ')
    line[0] = line[0].replace('[', '')
    line[7] = line[7].replace(']\n', '')
    avgShortPathD = line

# plots follow:
x = [2010 + i for i in xrange(8)] # list of time slices

# average clustering coefficient
plt.plot(x, avgClustCoeffB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, avgClustCoeffD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.plot(x, avgClustCoeffERB, color='red', ls='dashed', marker='.', label='G(n,m) Random Graph for General')
plt.plot(x, avgClustCoeffERD, color='blue', ls='dashed', marker='.', label='G(n,m) Random Graph for Developer')
plt.xlabel('Year')
plt.ylabel('Average Clustering Coefficient')
# plt.title('Average Clustering Coefficient Over Time')
plt.legend()
plt.savefig('avgClustCoeff.png')
plt.clf()

# max scc size
plt.plot(x, maxSCCsizeB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, maxSCCsizeD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Proportion of Nodes')
# plt.title('Max Strongly-Connected Component Size Over Time')
plt.legend()
plt.savefig('maxSCCsize.png')
plt.clf()

# max wcc size
plt.plot(x, maxWCCsizeB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, maxWCCsizeD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Proportion of Nodes')
# plt.title('Max Weakly-Connected Component Size Over Time')
plt.legend()
plt.savefig('maxWCCsize.png')
plt.clf()

# average degree size
plt.plot(x, avgDegreeB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, avgDegreeD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Average Node Degree')
# plt.title('Average Node Degree Over Time')
plt.legend()
plt.savefig('avgDegree.png')
plt.clf()

# power law exponent
plt.plot(x, powerLawAlphaB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, powerLawAlphaD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Power Law Exponent')
# plt.title('Power Law Exponent Over Time')
plt.legend()
plt.savefig('powerLawAlpha.png')
plt.clf()

# average shortest path
plt.plot(x, avgShortPathB, color='red', ls='solid', marker='.', label='General Bitcoin Community')
plt.plot(x, avgShortPathD, color='blue', ls='solid', marker='.', label='Developer Community')
plt.xlabel('Year')
plt.ylabel('Estimated Average Shortest Path Length')
# plt.title('Estimated Average Shortest Path Length Over Time')
plt.legend()
plt.savefig('avgShortPath.png')
plt.clf()