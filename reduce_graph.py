import newick3,phylo3,sys
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
    nodes = {}
    nodes["0"] = root
    for i in graph.nodes():
        print i
        node = None
        if i not in nodes:
            node = phylo3.Node()
            node.label = i
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
                    node.istip = False
                    nodes[j] = cnode
                else:
                    cnode = nodes[j]
                node.add_child(cnode)
        else:
            node.istip = True
    return root

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
    outfile = open(sys.argv[3],"w")
    outfile.write(newick3.tostring(tree)+";\n")
    outfile.close()
