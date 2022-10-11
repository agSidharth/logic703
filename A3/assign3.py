import sys
import re


def readFormulaFile(text):
    lines = text.strip().split('\n')

    num_clauses = -1
    num_props = -1
    formula_dict = {}
    clause_idx = 0
	
    for line in lines:
        clause_idx += 1
        words = line.split()

        if (words[0]=="c"):
            continue
        elif(words[0]=="p"):
            num_props = (int)(words[2])
            num_clauses = (int)(words[3])
            continue

        formula_dict[clause_idx] = []
        for prop in words:
            if(prop=="0"):
                break
            formula_dict[clause_idx].append((int)(prop))

    return formula_dict

def checkHorn(formula_dict):
	for clause_idx in formula_dict.keys():
		positive = False
		for prop in formula_dict[clause_idx]:
			if prop>0 and positive:
				return False
			elif prop>0:
				positive = True
	return True

def returnG(formula_dict):
	gDict = {}
	num_props = 0
	gIdx = 1

	for clause_idx in formula_dict.keys():
		formLen = len(formula_dict[clause_idx])
		for jdx in range(formLen):
			for kdx in range(jdx+1,formLen):
				p1 = formula_dict[clause_idx][jdx]
				p2 = formula_dict[clause_idx][kdx]
				if(p1!=p2):
					num_props = max(num_props,max(abs(p1),abs(p2)))
					gDict[gIdx] = [p1,p2]
					gIdx += 1
	return gDict,num_props,gIdx-1


def returnEdges(gDict,num_props):
	edges = {}
	Redges = {}

	for prop in range(1,num_props+1):
		edges[prop] = []
		edges[-1*prop] = []
		Redges[prop] = []
		Redges[-1*prop] = []


	for e in gDict.keys():
		p1 = gDict[e][0]
		p2 = gDict[e][1]

		edges[-1*p1].append(p2)
		edges[-1*p2].append(p1)
		Redges[p2].append(-1*p1)
		Redges[p1].append(-1*p2)
	
	return edges,Redges

def DFS(node,visited,edges,order,comp_num,comp_dict,dfsType):
	if(dfsType==1):
		visited[node] = True
		for adjNode in edges[node]:
			if(not visited[adjNode]):
				DFS(adjNode,visited,edges,order,comp_num,comp_dict,dfsType)
		order.append(node)
		return
	
	comp_dict[node] = comp_num
	for adjNode in edges[node]:
		if comp_dict[adjNode]==-1:
			DFS(adjNode,visited,edges,order,comp_num,comp_dict,dfsType)
	return 

def returnAssignment(formula_dict):
	gDict,num_props,num_clauses = returnG(formula_dict)
	edges,Redges = returnEdges(gDict,num_props)

	visited = {}
	Nodes = []
	comp_dict = {}
	order = []
	comp_num = 0
	assignment = []

	for prop in range(1,num_props+1):
		Nodes.append(prop)
		Nodes.append(-1*prop)
		visited[prop] = False
		visited[-1*prop] = False
		comp_dict[prop] = -1
		comp_dict[-1*prop] = -1

	for node in Nodes:
		if(not visited[node]):
			DFS(node,visited,edges,order,0,[],1)
	
	orderDict = {}
	for node in order:
		if abs(node) not in orderDict:
			if(node>0): orderDict[abs(node)] = True				# edge from -1*p to p
			else: orderDict[abs(node)] = False					# edge from p to -1*p

	order.reverse()
	for node in order:
		if (comp_dict[node]==-1):
			DFS(node,visited,Redges,order,comp_num,comp_dict,2)
			comp_num += 1
	
	for idx in range(len(Nodes)):
		if(idx%2==1): continue
		node = Nodes[idx]
		if comp_dict[node]==comp_dict[-1*node]: return [],False
		if(orderDict[abs(node)]): assignment.append(abs(node))	
		idx += 2
	
	return assignment,True


def solve(inputString, n):
	formula_dict = readFormulaFile(inputString)

	if(n==1):
		if(checkHorn(formula_dict)):
			return "already horn"
		else:
			return "not horn"
	elif(n==2):
		gDict,num_props,num_clauses = returnG(formula_dict)

		final_ans = "c 2-CNF formula which is sat iff input is renamable Horn\n"
		final_ans += "p cnf "+str(num_props)+" "+str(num_clauses) + "\n"

		for gIdx in gDict.keys():
			final_ans += str(gDict[gIdx][0])+" "+str(gDict[gIdx][1])+" 0" + "\n"
		return final_ans
	elif(n==3):
		if(checkHorn(formula_dict)):
			return "already horn"

		assignment,test = returnAssignment(formula_dict)
		if(not test):
			return "not renamable"
		else:
			return "renamable"

	elif(n==4):
		if(checkHorn(formula_dict)):
			return "already horn"

		assignment,test = returnAssignment(formula_dict)
		if(not test):
			return "not renamable"

		assignment.sort()
		final_ans = ""
		for assi in assignment:
			final_ans += str(assi) + " "

		return final_ans
	return "nil"

# Main function: do NOT change this.
if __name__=="__main__":
	inputFile = sys.argv[1]
	n = int(sys.argv[2])
	with open(inputFile, 'r') as f:
		inputString = f.read()
		print(solve(inputString, n))