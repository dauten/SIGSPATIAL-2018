import sys
import queue
import json
import time

if len(sys.argv) < 2:
	print("Usage:\npython3 pathfind.py <json input>")
	sys.exit(0)

filename = sys.argv[1]


data = json.loads(open(filename, "r").read())
#very primitive, very bad arg parsing, I know
if len(sys.argv) > 2 and sys.argv[2] == "-v":
	print(json.dumps(data, indent=4))
	
class Edge:
	def __init__(self, ls, r):
		if r is 0:
			self.fromX = ls[0]
			self.fromY = ls[1]
			self.toX = ls[2]
			self.toY = ls[3]
		else:
			self.fromX = ls[2]
			self.fromY = ls[3]
			self.toX = ls[0]
			self.toY = ls[1]

		self.parent = None
		self.visited = False

	def getSourceName(self):
		return str(self.fromX)+str(self.fromY)

	def getDestName(self):
		return str(self.toX)+str(self.toY)

	def __str__(self):
		return self.getSourceName() + "|" + self.getDestName()

sources = []
for line in open("starting.txt", "r").read().split("\n"):
	if line != '': sources.append(line)
sinks = []


#begin Input
pmap = {}
masterlist = []

#get sinks
for line in data["controllers"]:
	sinks.append(str(line["geometry"]["x"])+str(line["geometry"]["y"]))

# get the graph edges
paths = []
for row in data['rows']:
	
	edges =  row['viaGeometry']
	edges = edges.get('paths')
	if edges != None:
		edges = edges[0]
		edges = [ (x[0],x[1] ) for x in edges ]
	paths.append( edges )

for p in paths:
	if p != None:
		for i in range(1, len(p)):
			edge = Edge([p[i-1][0], p[i-1][1], p[i][0], p[i][1]], 1)	

			if edge.getSourceName() in pmap.keys():
				temp = pmap[edge.getSourceName()]
				temp.append(edge)
				pmap[edge.getSourceName()] = temp
			else:
				pmap[edge.getSourceName()] = [edge]
#end Input


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
		if head.getDestName() in edgeList.keys():
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
			print(str(e.fromX)+", "+str(e.fromY)+" -> "+str(e.toX)+", "+str(e.toY))
