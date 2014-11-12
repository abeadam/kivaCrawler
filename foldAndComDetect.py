import snap
import math
import time

edgeIndices = snap.TIntV()
fileName = "nodeCommunity.txt"
fileName2 = "communitySize.txt" 

# assume at each key, there is a unique integer value and the intgers are sorted
# and at cntinuous + 1 increment
def getKeyAtVal(strIntH, val):
    index = 0
    for key in strIntH:
        if val == index:
            break;
        else:
            index = index + 1
    return key

def getPartOfVector(strV, first, last):
    vecPart = snap.TStrV()
    for ind in range(first, last+1):
        vecPart.Add(strV[ind])
    return vecPart
        
# get all indices that have this value
def getIndicesWithVal(strV, val, first, edgeIndices):
    myInd = strV.SearchForw(val,0)
    if myInd == -1:
        return
    if strV.Len()==1:
        edgeIndices.Add(first)
       # print "%s at %d" %(val,first)
        return
    
    myLen = strV.Len()
    half = int(math.floor(myLen/2.0))
   # print "first, half, length = (%d, %d, %d)" % (first, half, myLen)

    leftPart = snap.TStrV()
    #strV.GetSubValV(0, half-1, leftPart)
    leftPart = getPartOfVector(strV, 0, half-1,0)
    getIndicesWithVal(leftPart, val, first, edgeIndices)
    
    rightPart = snap.TStrV()
    #strV.GetSubValV(half, myLen-1, rightPart)
    rightPart = getPartOfVector(strV, half, myLen-1,1)
    first = first + half
    getIndicesWithVal(rightPart, val, first, edgeIndices)




startTime = time.time()

# Read the edges
print "----------------Reading The Bipartite Graph Edges-----------------"
loanEdgeNodes = snap.TStrV()
lenderEdgeNodes = snap.TStrV()
edgePairs = snap.TStrPrV()
numEdges = 0
file = open("lender_loans.txt", "r")
for line in file:
    numEdges += 1
    words = line.split()
    loanEdgeNodes.Add(words[0])
    lenderEdgeNodes.Add(words[1])
    myPair = snap.TStrPr(words[0], words[1])
    edgePairs.Add(myPair)
    if numEdges >=1000:
        break
file.close()

print "Edges from loans to lenders = %d" % numEdges

print "----------------Loan Nodes-----------------" 
loanNodes = snap.TStrIntH()
prevId = ''
ind = 0
file = open("loanNameIdMap.map", "w")
for loanId in loanEdgeNodes:
    if loanId != prevId:
        loanNodes[loanId] = ind
        file.write(loanId + "\t" + str(ind)+ "\n")
        ind = ind + 1
        prevId = loanId        
file.close()
print "There are %d loans" % loanNodes.Len()

print "----------------Lender Nodes-----------------"
lenderNodes = snap.TStrIntH() 
sortedV = snap.TStrV()
# copy into sortedV and sort it
for lenderId in lenderEdgeNodes:
    sortedV.Add(lenderId)    
sortedV.Sort(True)

prevId = ''
ind = 0
idToName = snap.TIntStrH()
print "sorted lenderId"
file = open("lenderNameIdMap.map", "w")
for lenderId in sortedV:
    #print lenderId
    if lenderId != prevId:
        lenderNodes[lenderId] = ind
        idToName[ind] = lenderId
        file.write(lenderId + "\t" + str(ind)+ "\n")
        ind = ind + 1
        prevId = lenderId
        
file.close()
print "There are %d lenders" % lenderNodes.Len()

print "----------------Folding Lender to lender graph-----------------"
# undirected graph
GLender = snap.TUNGraph.New()
# add the nodes
for nodeId in range(0, lenderNodes.Len()):
    GLender.AddNode(nodeId)
# add the edges
prevLoanName = ''
prevLenderIds = snap.TIntV()
for curEdge in range(0, numEdges):
    curLoanName = loanEdgeNodes[curEdge]
    curLenderId = lenderNodes[lenderEdgeNodes[curEdge]] 
    if curLoanName == prevLoanName:
        for prevLenderId in prevLenderIds:
            GLender.AddEdge(curLenderId, prevLenderId)
        prevLenderIds.Add(curLenderId)
    else:
        prevLenderIds.Clr()
        prevLenderIds.Add(curLenderId)            
    prevLoanName = curLoanName

snap.SaveEdgeList(GLender, "GLender.edgelist", "Folded Lender Graph")

if (False):
    for EI in GLender.Edges():
       lenderId1 = EI.GetSrcNId()
       lenderId2 = EI.GetDstNId()
       lenderName1 = getKeyAtVal(lenderNodes, lenderId1)
       lenderName2 = getKeyAtVal(lenderNodes, lenderId2)
       print "(%s, %s)" % (lenderName1,lenderName2)

print "number of edges in lender to lender graph is %d" %GLender.GetEdges()
elapsed_time = time.time() - startTime

print "total folding time is %d seconds" %elapsed_time


print "------------------Community Detection---------------------"
CmtyV = snap.TCnComV()
modularity = snap.CommunityCNM(GLender, CmtyV)

file = open(fileName, "w")
file2 = open(fileName2, "w")
communityCount = 0
numNodes = 0
for Cmty in CmtyV:
   # print "Community: %d" % communityCount
    file2.write(str(communityCount) + "\t"+ str(Cmty.Len())+ "\n")
    for NI in Cmty:          
        numNodes = numNodes + 1
        file.write(str(idToName[NI]) + "\t"  + str(communityCount) + "\n")
  #  print "%d processed nodes" % numNodes 
    communityCount+=1
file.close()
file2.close()
print "The modularity of the network is %f" % modularity
print "The total number of communities is %d" % CmtyV.Len()
elapsed_time = time.time() - startTime

print "total Community Detection time is %d seconds" %elapsed_time 
