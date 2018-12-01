import sys
import queue
import json
import time

if len(sys.argv) < 2:
	print("Usage:\npython3 pathfind.py <json input>")
	sys.exit(0)

filename = sys.argv[1]


data = json.loads(open(filename, "r").read())

class Edge:
	def __init__(self, ls, r):
		if r is 0:
			self.fromX = ls[0]
			self.fromY = ls[1]
			self.toX = ls[2]
			self.toY = ls[3][:-1]
		else:
			self.fromX = ls[2]
			self.fromY = ls[3][:-1]
			self.toX = ls[0]
			self.toY = ls[1]

		self.parent = None
		self.visited = False

	def getSourceName(self):
		return self.fromX+self.fromY

	def getDestName(self):
		return self.toX+self.toY

	def __str__(self):
		return self.getSourceName() + "|" + self.getDestName()

sources = ["6815946.038261843672.78242", "6815957.268881843079.85972", "6815953.440481843350.4143"]
sinks = ["6815718.619431843338.92843", "6815975.135641842907.57266"]


#begin Input
cords = open("zzzout.txt", "r")
pmap = {}
masterlist = []

for line in cords:
	temp = Edge(line.split(" "), 0)

	if temp.getSourceName() not in pmap.keys():
		pmap[temp.getSourceName()] = [temp]
	else:
		t = pmap[temp.getSourceName()]
		t.append(temp)
		pmap[temp.getSourceName()] = t



	temp = Edge(line.split(" "), 1)

	if temp.getSourceName() not in pmap.keys():
		pmap[temp.getSourceName()] = [temp]
	else:
		t = pmap[temp.getSourceName()]
		t.append(temp)
		pmap[temp.getSourceName()] = t
#end Input

#	print("for the record pmap.keys looks like: "+str(pmap.keys())+"\n\n\n")

#P: hashmap of edges
#   sourceName of source
#   destName of destination
#Q: boolean of if path exists
def BFS(edgeList, source, destination):
	head = None
	q = queue.Queue()

	if edgeList[source][0] == None:
		print("no path exists")
		sys.exit(0)
	q.put(edgeList[source][0])
	path = []

	while not q.empty():
		head = q.get()
		for edge in edgeList[head.getDestName()]:
			if not edge.visited:
				edge.visited = True
				q.put(edge)
				edge.parent = head
				if edge.getDestName() == destination and len(path) == 0:
					path.append(edge)

	if len(path) == 0:
		print("no path exists")
	else:
		while path[len(path)-1].getSourceName() != edgeList[source][0].getSourceName():
			path.append(path[len(path)-1].parent)

	for esses in edgeList.keys():
		for edge in edgeList[esses]:
			edge.parent = None
			edge.visited = None

	return path





for p in sources:
	for q in sinks:
		print("\n"+p + " to "+q+" is:")
		out = BFS(pmap, p, q)
		
		for e in out:
			print(e.fromX+", "+e.fromY+" -> "+e.toX+", "+e.toY)
