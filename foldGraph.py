import snap
import math
import time

edgeIndices = snap.TIntV()


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
file = open(".\lender_loans.txt", "r")
for line in file:
    numEdges += 1
    words = line.split()
    loanEdgeNodes.Add(words[0])
    lenderEdgeNodes.Add(words[1])
    myPair = snap.TStrPr(words[0], words[1])
    edgePairs.Add(myPair)
    #if numEdges >=1000:
    #    break
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
print "sorted lenderId"
file = open("lenderNameIdMap.map", "w")
for lenderId in sortedV:
    #print lenderId
    if lenderId != prevId:
        lenderNodes[lenderId] = ind
        file.write(lenderId + "\t" + str(ind)+ "\n")
        ind = ind + 1
        prevId = lenderId
        
file.close()
print "There are %d lenders" % lenderNodes.Len()

print "----------------Folded Lender to lender graph-----------------"
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

snap.SaveEdgeList(GLender, ".\GLender.edgelist", "Folded Lender Graph")

if (False):
    for EI in GLender.Edges():
       lenderId1 = EI.GetSrcNId()
       lenderId2 = EI.GetDstNId()
       lenderName1 = getKeyAtVal(lenderNodes, lenderId1)
       lenderName2 = getKeyAtVal(lenderNodes, lenderId2)
       print "(%s, %s)" % (lenderName1,lenderName2)

print "number of edges in lender to lender graph is %d" %GLender.GetEdges()


print "----------------Folded Loan to loan graph-----------------"
# undirected graph
GLoan = snap.TUNGraph.New()
# add the nodes
for nodeId in range(0, loanNodes.Len()):
    GLoan.AddNode(nodeId)
# add the edges    
prevLenderName = ''

for curEdge in range(0, numEdges):
    curLenderName = sortedV[curEdge]
    if curLenderName!=prevLenderName:
        edgeIndices.Clr()
        getIndicesWithVal(lenderEdgeNodes, curLenderName, 0, edgeIndices)
        for ind1 in edgeIndices:
            for ind2 in edgeIndices:
                if ind1!=ind2:
                    curLoanName1 = loanEdgeNodes[ind1]
                    curLoanId1 = loanNodes[curLoanName1]
                    curLoanName2 = loanEdgeNodes[ind2]
                    curLoanId2 = loanNodes[curLoanName2]
                    if not GLoan.IsEdge(curLoanId1, curLoanId2):
                        GLoan.AddEdge(curLoanId1, curLoanId2)
        prevLenderName = curLenderName           

snap.SaveEdgeList(GLoan, ".\GLoan.edgelist", "Folded Loan Graph")

if (False):
    for EI in GLoan.Edges():
       loanId1 = EI.GetSrcNId()
       loanId2 = EI.GetDstNId()
       loanName1 = getKeyAtVal(loanNodes, loanId1)
       loanName2 = getKeyAtVal(loanNodes, loanId2)
       print "(%s, %s)" % (loanName1,loanName2)   

print "number of edges in loan to loan graph is %d" %GLoan.GetEdges()      
    
elapsed_time = time.time() - startTime

print "total time is %d seconds" %elapsed_time 



















