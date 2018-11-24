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

	def getSourceName(self):
		return self.fromX+self.fromY

	def getDestName(self):
		return self.toX+self.toY

	def __str__(self):
		return self.getSourceName() + "|" + self.getDestName()



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


#	print("for the record pmap.keys looks like: "+str(pmap.keys())+"\n\n\n")

#P: hashmap of edges
#   sourceName of source
#   destName of destination
#Q: boolean of if path exists
def BFS(edgeList, source, destination):
	q = queue.Queue()
	q.put(source)	#list of sources
	visited = []
	while not q.empty():
		temp = q.get()
		if temp not in visited:
			visited.append(temp)
			if temp in edgeList.keys():
				for dest in edgeList[temp]:
					q.put(dest.getDestName())
					dest.parent = temp
					if dest.getDestName() == destination:
						return True
				

	print(len(visited))

	return False

for key in pmap.keys():
	print(pmap[key])
source = "6815946.038261843672.78242"
sink = "6815718.619431843338.92843"
print(BFS(pmap, source, sink))




