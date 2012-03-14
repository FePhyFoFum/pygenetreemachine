import newick3,phylo3,sys
import networkx as nx
import matplotlib.pyplot as plt
import simple_combine

def get_node_leaves(graph):
    node_leaves = {}
    for i in graph.nodes():
        if len(graph.successors(i)) == 0:
            node_leaves[i] = [i]
        else:
            stack = [i]
            node_leaves[i] = []
            while len(stack) != 0:
                lab = stack.pop()
                if len(graph.successors(lab)) == 0:
                    node_leaves[i].append(lab)
                else:
                    for j in graph.successors(lab):
                        stack.append(j)
    return node_leaves

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "python simple_add.py tree1 in.dot out.dot"
        sys.exit(0)
    infile = open(sys.argv[1],"r")
    intree1 = newick3.parse(infile.readline())
    infile.close()
    ingraph,node_leaves_in = simple_combine.process_tree_to_graph(intree1,200)

    graph = nx.read_dot(sys.argv[2])
    for i in graph.edges():
        try:
            graph[i[0]][i[1]]['weight'] = int(graph[i[0]][i[1]]['weight'])
        except:
            continue
    node_leaves = get_node_leaves(graph)

#    graph = simple_combine.combine_tree(graph,node_leaves,intree1)
#    graph = nx.compose(graph,ingraph)
    graph = simple_combine.combine_graph_with_labels(graph,node_leaves,ingraph,node_leaves_in)
    pos=nx.graphviz_layout(graph)
    nx.draw(graph,pos)
    plt.show()
    nx.write_dot(graph,sys.argv[3])
