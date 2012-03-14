import sys,os,sqlite3,phylo3,newick3

"""
the infile has the format of the id from the sqlite
"""

#need to use this database because of the ids
database = "/home/smitty/Desktop/pln.update.db"

plants_ncbi_id = 3193

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "python make_ncbi_tree.py rootname infile outtree"
		sys.exit(0)
	infile = open(sys.argv[2],"r")
	id_names_dict = {}
	for i in infile:
		spls = i.strip().split(",")
		id_names_dict[spls[0]] = spls[1]
	
	node_ids_dict = {}
	root_node = phylo3.Node()
	root_node.isroot = True
	root_node.label = "root"
	con = sqlite3.connect(database)
	cur = con.cursor()
	cur.execute("SELECT ncbi_id from taxonomy where edited_name = ?",(sys.argv[1],))
	a = cur.fetchall()
	root_id = int(a[0][0])
	node_ids_dict[root_id] = root_node
	count = 0
	for i in id_names_dict:
		id_ = i
		name = id_names_dict[i]
		curnode = phylo3.Node()
		curnode.label = name
		curnode.istip = True
		node_ids_dict[id_] = curnode
		while id_ != root_id:
			#get parent
			cur.execute("SELECT parent_ncbi_id,edited_name from taxonomy where ncbi_id = ?",(id_,))
			a = cur.fetchall()
			nid = int(a[0][0])
			nname = str(a[0][1])
			if nid not in node_ids_dict:
				#make new node
				pcurnode = phylo3.Node()
				pcurnode.label = nname.replace(" ","_").replace("(","_").replace(")","_")
				node_ids_dict[nid] = pcurnode
				pcurnode.add_child(curnode)
				curnode = pcurnode
				id_ = nid
			else:
				node_ids_dict[nid].add_child(curnode)
				success = True
				break
		if success == False:
			root_node.add_child(curnode)
		if count % 100 == 0:
			print count
		count += 1
	
	leaves = root_node.leaves()
	count = 0
	for i in leaves:
		cur = i
		while cur != root_node:
			par = cur.parent
			if par != root_node:
				if len(par.children) == 1:
					parpar = par.parent
					parpar.remove_child(par)
					parpar.add_child(cur)
				else:
					cur = par
			if cur.parent == root_node or cur == root_node:
				break
		if count % 100 == 0:
			print count
		count += 1
	for i in root_node.iternodes():
		if len(i.children) > 0:
			i.label = ""
		i.length = 1.0

	outfile = open(sys.argv[3],"w")
	outfile.write(newick3.tostring(root_node,None)+";")
	outfile.close()
