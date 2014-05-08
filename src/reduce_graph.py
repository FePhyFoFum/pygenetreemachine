import tree_utils,phylo3,sys
import networkx as nx
import matplotlib.pyplot as plt
import simple_combine

def reduce(graph):
    problem = True
    while problem:
        problem_nodes = []
        bad_out_dict = {}
        bad_in_dict = {}
        for i in graph.nodes():
            print i,len(graph.successors(i)),len(graph.predecessors(i))
            if len(graph.predecessors(i)) > 1:
                problem_nodes.append(i)
                bad_in_dict[i] = len(graph.predecessors(i))
                for j in graph.predecessors(i):
                    if j not in bad_out_dict:
                        bad_out_dict[j] = 0
                        bad_out_dict[j] += 1
        print "problems:",problem_nodes
        if len(problem_nodes) == 0:
            break
        for i in problem_nodes:
            pred = graph.predecessors(i)
            for j in pred:
                if graph.successors(j) > 2:
                    graph.remove_edge(j,i)
                    break
    return graph

#root is always 0, will change but 
def build_tree_from_graph(graph):
    root = phylo3.Node()
    root.label = "0"
    root.istip = False
    root.isroot = True
    root.length = 1
    nodes = {}
    nodes["0"] = root
    for i in graph.nodes():
        print i
        node = None
        if i not in nodes:
            node = phylo3.Node()
            node.label = i
            node.length = 1
            nodes[i] = node
        else:
            node = nodes[i]
        suc = graph.successors(i)
        if len(suc) > 0:
            for j in suc:
                cnode = None
                if j not in nodes:
                    cnode = phylo3.Node()
                    cnode.label = j
                    cnode.length = 1
                    node.istip = False
                    nodes[j] = cnode
                else:
                    cnode = nodes[j]
                node.add_child(cnode)
        else:
            node.istip = True
    return root

def clean_up_tree(tree):
    for i in tree.leaves():
        try:
            lab = int(i.label)
            print "fixing internal node:",lab
            par = i.parent
            par.remove_child(i)
            if len(par.children) == 1:
                ch = par.children[0]
                parpar = par.parent
                parpar.remove_child(par)
                parpar.add_child(ch)
            while len(par.children) == 0:
                parpar = par.parent
                parpar.remove_child(par)
                par = parpar
        except:
            continue
    return tree

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "python reduce_graph.py in.dot out.dot out.tre"
        sys.exit(0)

    graph = nx.read_dot(sys.argv[1])
    for i in graph.edges():
        try:
            graph[i[0]][i[1]]['weight'] = int(graph[i[0]][i[1]]['weight'])
        except:
            continue

    graph = reduce(graph)
    pos=nx.graphviz_layout(graph)
    nx.draw(graph,pos)
#    plt.show()
    nx.write_dot(graph,sys.argv[2])
    tree = build_tree_from_graph(graph)
    #cleaning up external internal nodes
    tree = clean_up_tree(tree)
    outfile = open(sys.argv[3],"w")
    outfile.write(tree_utils.tostring(tree,None)+";\n")
    outfile.close()
