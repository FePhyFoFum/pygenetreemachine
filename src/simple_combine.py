import newick3,phylo3,sys
import networkx as nx
import matplotlib.pyplot as plt
import random

def get_leaf_names(lvs):
    ret = []
    for i in lvs:
        ret.append(i.label)
    return ret

def process_tree_to_graph(tree,startingnum):
    graph = nx.DiGraph()
    node_leaves = {}
    count = startingnum
    for i in tree.iternodes(order=0):
        nd = None
        ed = None
        if i.parent == None:
            i.label = str(count)
            count += 1
            nd = i.label
            node_leaves[nd] = get_leaf_names(i.leaves())
            graph.add_node(nd)
        elif i.label != None:
            nd = i.label
            node_leaves[nd] = get_leaf_names(i.leaves())
            graph.add_node(nd)
            graph.add_edge(i.parent.label,nd,weight = 1)
        else:
            i.label = str(count)
            count += 1
            nd = i.label
            node_leaves[nd] = get_leaf_names(i.leaves())
            graph.add_node(nd)
            graph.add_edge(i.parent.label,nd,weight =1)
#    nx.draw_graphviz(graph)
#    plt.show()
    return graph,node_leaves

def get_graph_edge(node_leaves,lvs,plvs,names_not_in_tree,names_not_in_graph):
    parent = None
    child = None
    for i in node_leaves:
        if (set(lvs)-names_not_in_graph) == (set(node_leaves[i])-names_not_in_tree):
            child = i
    for i in node_leaves:
        if (set(plvs)-names_not_in_graph) == (set(node_leaves[i])-names_not_in_tree):
            parent = i
    return parent,child

#returns the deepest completely matching mrca
def get_graph_mrca(node_leaves,names,names_not_in_new,names_not_in_graph):
    mrca = None
    size = 0
    for i in node_leaves:
        if (set(names)-names_not_in_graph) == (set(node_leaves[i])-names_not_in_new):
            if len(node_leaves[i]) > size:
                mrca = i
                size = len(node_leaves[i])
    return mrca

#intended to relable new graph with the labels from the old, if matching
#then use compose
def combine_graph_with_labels(graph,node_leaves,graph2,node_leaves2):
    gnames = []
    maxcount = 0
    for i in graph.nodes():
        if len(graph.successors(i)) == 0:
            gnames.append(i)
        else: #just getting max internal node count, should hash this
            if int(i) >= maxcount:
                maxcount  = int(i)+1
    graph2names = []
    graph2newnames = []
    for i in graph2.nodes():
        if len(graph2.successors(i)) == 0:
            graph2names.append(i)
            if i not in gnames:
                graph2newnames.append(i)
        else: #just getting max internal node count, should hash this
            if int(i) >= maxcount:
                maxcount  = int(i)+1
    names_not_in_new = set(set(gnames) - set(graph2names))
    names_not_in_old = set(graph2newnames)
    for i in graph2.nodes():
        if len(graph2.successors(i)) > 0:#internal
            nd = get_graph_mrca(node_leaves,node_leaves2[i],names_not_in_new,names_not_in_old)
            if nd == None:
                #get edges with i
                nd = str(maxcount)
                maxcount += 1
                suc = graph2.successors(i)
                pred  =graph2.predecessors(i)
                graph2.remove_node(i)
                graph2.add_node(nd)
                for j in pred:
                    graph2.add_edge(j,nd)
                for j in suc:
                    graph2.add_edge(nd,j)
                node_leaves2[nd] = node_leaves2[i]
                del node_leaves2[i]
            else:
                #get edges with i
                suc = graph2.successors(i)
                pred  =graph2.predecessors(i)
                graph2.remove_node(i)
                graph2.add_node(nd)
                for j in pred:
                    graph2.add_edge(j,nd)
                for j in suc:
                    graph2.add_edge(nd,j)
                node_leaves2[nd] = node_leaves2[i]
                del node_leaves2[i]
    return nx.compose(graph,graph2)

def combine_tree(graph,node_leaves,tree):
 #   print graph.nodes()
    gnames = []
    new_names = [] #names not yet really in the graph
    names_not_in_tree = []
    maxcount = 0
    tree_leaf_names = get_leaf_names(tree.leaves())
    for i in graph.nodes():
 #       print i,graph.out_edges(i),graph.in_degree(i),graph.successors(i),graph.predecessors(i)
        if len(graph.successors(i)) == 0:
            gnames.append(i)
        else: #just getting max internal node count
            if int(i) >= maxcount:
                maxcount  = int(i)+1
    names_not_in_tree = set(set(gnames) - set(tree_leaf_names))
 #   print gnames
 #   print maxcount
    for i in tree.leaves():
        if i.label not in gnames:
            nd = i.label
            graph.add_node(nd)
            node_leaves[nd] = get_leaf_names(i.leaves())
            new_names.append(nd)
    new_names = set(new_names)
    for i in tree.iternodes(order=1):
        if i.parent == None:
            continue
        else:
#            print i.label,i.parent.label
            lvs = get_leaf_names(i.leaves())
            plvs = get_leaf_names(i.parent.leaves())
            parent,child = get_graph_edge(node_leaves,lvs,plvs,names_not_in_tree,new_names)
            if len(i.children) == 0:
                child = i.label
            print parent,child
            #add if parent and child are disconnected (multiple nodes in between)
            #add if child isn't there
            #add if non overlapping taxa
            if parent and child:
                try:
                    graph[parent][child]['weight'] += 1
                except:
                    graph.add_edge(parent,child,weight=1)
                    print "adding edge",parent,child
            elif parent == None and child:
                i.parent.label = str(maxcount)
                maxcount += 1
                graph.add_node(i.parent.label)
                print "adding node",i.parent.label
                graph.add_edge(i.parent.label,child,weight = 1)
                print "adding edge",i.parent.label,child
                node_leaves[i.parent.label] = get_leaf_names(i.parent.leaves())
#                sys.exit(0)
            elif parent == None and child == None:
                if len(i.children) == 0:
                    child = i.label
                else:
                    i.label = str(maxcount)
                    child = i.label
                    maxcount += 1
                    graph.add_node(child)
                    print "adding node",child
                    node_leaves[child] = get_leaf_names(i.leaves())
                i.parent.label = str(maxcount)
                maxcount += 1
                graph.add_node(i.parent.label)
                print "adding node",i.parent.label
                graph.add_edge(i.parent.label,child,weight = 1)
                print "adding edge",i.parent.label,child
                node_leaves[i.parent.label] = get_leaf_names(i.parent.leaves())
    return graph

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "python simple_combine.py tree1 tree2 out.dot"
        sys.exit(0)
    infile = open(sys.argv[1],"r")
    intree1 = newick3.parse(infile.readline())
    infile.close()
    graph1,node_leaves1 = process_tree_to_graph(intree1,0)
    infile = open(sys.argv[2],"r")
    intree2 = newick3.parse(infile.readline())
    infile.close()
    graph2,node_leaves2 = process_tree_to_graph(intree2,100)

#    graph = combine_tree(graph1,node_leaves1,intree2)
#    graph = nx.compose(graph1,graph2)
    graph = combine_graph_with_labels(graph1,node_leaves1,graph2,node_leaves2)
    pos=nx.graphviz_layout(graph)
    nx.draw(graph,pos)
    plt.show()
    nx.write_dot(graph,sys.argv[3])
