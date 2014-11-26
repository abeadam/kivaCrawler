import snap
graph = snap.LoadEdgeList(snap.PNGraph, "GLender.edgelist",0,1)
snap.DrawGViz(graph, snap.gvlDot, "testGraph.png", "lender lender graph")