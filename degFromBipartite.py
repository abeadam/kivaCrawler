import snap
import math
import time

startTime = time.time()

# Read the edges
print "----------------Reading The Bipartite Graph Edges-----------------"
loanEdgeNodes = snap.TStrV()
loanDeg = snap.TStrIntH()
lenderEdgeNodes = snap.TIntV()
lenderDeg = snap.TStrIntH()
edgePairs = snap.TStrPrV()
numEdges = 0
file = open(".\lender_loans.txt", "r")
for line in file:
    numEdges += 1
    words = line.split()
    loanEdgeNodes.Add(words[0])
    if(words[0] in loanDeg):
        loanDeg[words[0]] += 1
    else:
        loanDeg[words[0]] = 1
    lenderEdgeNodes.Add(words[1])
    if(words[1] in lenderDeg):
        lenderDeg[words[1]] += 1
    else:
        lenderDeg[words[1]] = 1
    myPair = snap.TStrPr(words[0], words[1])
    edgePairs.Add(myPair)
##    if numEdges >=10000:
##        break
file.close()

print "Edges from loans to lenders = %d" % numEdges

avgLenderDeg = 0.0
for lender in lenderDeg:
    avgLenderDeg += lenderDeg[lender]
avgLenderDeg = avgLenderDeg/lenderDeg.Len()

print "number of lenders is %d" % lenderDeg.Len()
print "average degree per lender is %f" %avgLenderDeg

avgLoanDeg = 0.0
for loan in loanDeg:
    avgLoanDeg += loanDeg[loan]
avgLoanDeg = avgLoanDeg/loanDeg.Len()

print "number of loans is %d" % loanDeg.Len()
print "average degree per loan is %f" %avgLoanDeg 

elapsed_time = time.time() - startTime

print "total time is %d seconds" %elapsed_time 



















