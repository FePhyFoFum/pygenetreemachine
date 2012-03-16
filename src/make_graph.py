import networkx as nx
import matplotlib.pyplot as plt
import sys
import simple_combine
import newick3,phylo3

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python make_graph.py in.tre out.dot"
        sys.exit(0)

    infile = open(sys.argv[1],"r")
    intree1 = newick3.parse(infile.readline())
    ingraph,node_leaves_in = simple_combine.process_tree_to_graph(intree1,0)
    nx.write_dot(ingraph,sys.argv[2])
    infile.close()
