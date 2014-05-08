import string, sys
from shlex import shlex
from phylo3 import Node
import StringIO




class Tokenizer(shlex):
    """Provides tokens for parsing Newick-format trees"""
    def __init__(self, infile):
        shlex.__init__(self, infile)
        self.commenters = ''
        self.wordchars = self.wordchars+'-.|\\/'
        self.quotes = "'"

    def parse_comment(self):
        comment = ""
        while 1:
            token = self.get_token()
	    comment += token
            if token == '':
                sys.stdout.write('EOF encountered mid-comment!\n')
                break
            elif token == ']':
                break
            elif token == '[':
                self.parse_comment()
            else:
                pass
        return comment[:-1] 

def read_treestring(inputstr):
    curnode = None
    rootnode = None
    keepgoing = True
    start = True
    curcharint = 0
    nextchar = inputstr[curcharint]
    while keepgoing:
        if nextchar == '(':
            if start == True:
                start = False
                root = Node()
                root.istip = False
                root.isroot = True
                curnode = root
                rootnode = root
            else:
                newnode = Node()
                newnode.istip = False
                curnode.add_child(newnode)
                curnode = newnode
        elif nextchar == ')':
            curnode = curnode.parent
            curcharint += 1
            nextchar = inputstr[curcharint]
            name = ""
            goingName = True
            if nextchar in [",",")",":",";","["]:
                goingName = False
            while goingName == True:
                name = name + nextchar
                curcharint += 1
                nextchar = inputstr[curcharint]
                if nextchar in [",",")",":",";","["]:
                    goingName = False
                    break
            curnode.label = name
            curcharint -= 1
        elif nextchar == ',':
            curnode = curnode.parent
        # branch length
        elif nextchar == ':':
            curcharint += 1
            nextchar = inputstr[curcharint]
            brlen = ""
            goingbrln = True
            while goingbrln:
                brlen = brlen + nextchar
                curcharint += 1
                nextchar = inputstr[curcharint]
                if nextchar in [",",")",":",";","["]:
                    goingbrln = False
                    break
            try:
                curnode.length = float(brlen)
            except:
                print "error with branch length:",brlen
            curcharint -= 1
        # comment
        elif nextchar == '[':
            curcharint += 1
            nextchar = inputstr[curcharint]
            comment = ""
            goingnote = True
            while goingnote:
                comment = comment+nextchar
                curcharint += 1
                nextchar = inputstr[curcharint]
                if nextchar == ']':
                    goingnote = False
                    break
            curnode.comment = comment
            curcharint -= 1
        elif nextchar == ';':
            keepgoing = False
        elif nextchar == ' ':
            continue
        # leaf node
        else:
            newnode = Node()
            curnode.add_child(newnode)
            newnode.istip = True
            nodename = ""
            goingname = True
            while goingname == True:
                nodename = nodename + nextchar
                curcharint += 1
                nextchar = inputstr[curcharint]
                if nextchar in [",",")",":","["]:
                    goingname = False
                    break
            newnode.label = nodename
            curnode = newnode
            curcharint -= 1
        if curcharint < len(inputstr)-1:
            curcharint += 1
        nextchar = inputstr[curcharint]
    return rootnode

        
def to_string(node, length_fmt=":%s"):
    if not node.istip:
        node_str = "(%s)%s" % \
                   (",".join([ to_string(child, length_fmt) \
                               for child in node.children ]),
                    node.label or ""
                    )
    else:
        node_str = "%s" % node.label

    if node.length is not None:
        length_str = length_fmt % node.length
        #length_str = ':%f' % node.length
        #length_str = str(length_str)
    else:
        length_str = ""

    s = "%s%s" % (node_str, length_str)
    return s

tostring = to_string

if __name__ == "__main__":
    #import ascii
    s = "(a:3,(b:1e-05,c:1.3)int_|_and_33.5:5)root;"
    #s = "(a,b,c,d,e,f,g);"
    n = read_treestring(s)
    print
    #print ascii.render(n)
    print(s)
    print(to_string(n))
    #print n.next.back.label
