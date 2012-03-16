import newick3,phylo3,sys
import networkx as nx
import matplotlib.pyplot as plt
import simple_combine

def get_tips(graph,node):
    names = []
    nds = nx.dfs_postorder_nodes(graph,node)
    for i in nds: 
        if len(graph.successors(i)) == 0:
            names.append(i)
    return names

def get_node_leaves(graph):
    node_leaves = {}
    for i in graph.nodes():
        node_leaves[i] = get_tips(graph,i)
    return node_leaves

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "python simple_add.py tree1 in.dot out.dot"
        sys.exit(0)
    infile = open(sys.argv[1],"r")
    intree1 = newick3.parse(infile.readline())
    infile.close()
    ingraph,node_leaves_in = simple_combine.process_tree_to_graph(intree1,1000)
    print "finished reading tree"
    
    graph = nx.read_dot(sys.argv[2])
    for i in graph.edges():
        try:
            graph[i[0]][i[1]]['weight'] = int(graph[i[0]][i[1]]['weight'])
        except:
            continue
    node_leaves = get_node_leaves(graph)
    print "finished processing graph"

    print "combining graphs"
    graph = simple_combine.combine_tree(graph,node_leaves,intree1)
    print "finished combining graphs"
#    graph = simple_combine.combine_graph_with_labels(graph,node_leaves,ingraph,node_leaves_in)
    pos=nx.graphviz_layout(graph)
    nx.draw(graph,pos)
#    plt.show()
    nx.write_dot(graph,sys.argv[3])
