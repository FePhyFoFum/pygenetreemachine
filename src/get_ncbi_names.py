import sys,os,sqlite3

"""
the infile has the format of the id from the sqlite
"""

#need to use this database because of the ids
database = "/home/smitty/Desktop/pln.db"

plants_ncbi_id = 3193

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "python get_ncbi_names.py name outfile"
		sys.exit(0)
	con = sqlite3.connect(database)
	cur = con.cursor()
	left = 0 
	right = 0
#	cur.execute("SELECT left_value,right_value from taxonomy where ncbi_id = ?",(plants_ncbi_id,))
	cur.execute("SELECT left_value,right_value from taxonomy where edited_name = ?;",(sys.argv[1],))
	a = cur.fetchall()
	left = int(a[0][0])
	right = int(a[0][1])

	outfile = open(sys.argv[2],"w")
	sql = "SELECT ncbi_id,edited_name from taxonomy where left_value > "+str(left)+" and right_value < "+str(right)+" and node_rank = 'family' and name_class = 'scientific name';"
	print sql
	cur.execute(sql)
	a = cur.fetchall()
	for i in a:
		print i
		outfile.write(str(i[0])+","+str(i[1])+"\n")
	outfile.close()
