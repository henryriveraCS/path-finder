import math
from operator import attrgetter

class Node:
	def __init__(self, point):
		self.point = point
		self.cost = 1
		self.distance = 100000
		self.G = 0
		self.H = 0
		self.parent = None
	
	def move_cost(self):
		return self.cost

def neighbors(current_node, matrix, DIRECTION):
	x,y = current_node.point
		
	if DIRECTION == 4:
		neighbor_list = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
	#else:	
	#	neighbor_list = [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1), (x-1, y), (x+1, y), (x, y-1), (x, y+1)]
	
	node_list = []
	for neighbor in neighbor_list:
		for node in matrix:
			if neighbor == node.point:
				node_list.append(node)
	
	return node_list

#find and return the tentative distance to the current node to the start node
def dijkstra_distance(prev_node, current_node, start_node):
	#because start node has a cost of 0 -> manually return 1 so it can add it to the neighboring node
	if start_node:
		return 0
	else:
		current_cost = prev_node.distance + current_node.move_cost
		return current_cost


def dijkstra(start_node, end_node, matrix, DIRECTION):
	v_set = [] #visited nodes
	u_set = matrix #un-visited nodes
	
	#first iteration will be starting node with a distance set to 0
	start_node.distance = 0
	current_node = start_node
	u_set.remove(current_node)
	while current_node != end_node:
		#remove current_node from U_set since it is going to be explroed now
		#u_set.remove(current_node)
		print("CURRENT NODE: ", current_node.point, current_node.distance)
		neighbor_nodes = neighbors(current_node, matrix, DIRECTION)

		#update the distance of every neighbor node to the appropiate cost
		for node in neighbor_nodes:
			tentative_cost = current_node.distance + node.move_cost()
			if node in v_set:
				continue
			else:
				#if the tentative distance is less than the nodes current value -> re-assign it
				if tentative_cost < node.distance:
					node.distance = tentative_cost
					node.parent = current_node
					#now that the value is updated -> replace the outdated instance with the new one
					for i in u_set:
						if i.point == node.point:
							i = node
							print("UPDATED NODE: ", i.point, i.distance)

		#now that all neighbor distances have been updated -> set current node as visited
		v_set.append(current_node)
		#now assign current_node to an unvisited node with minimal distance (from starting point)
		lowest_cost_node = min(u_set, key=attrgetter("distance"))

		print("LOWEST COST NODE: ", lowest_cost_node, lowest_cost_node.point, lowest_cost_node.distance)
		#DELETE THIS ONCE ALGO IS FINISHED
		current_node = lowest_cost_node
		u_set.remove(current_node)
		print("NEWLY ASSIGNED CURRENT_NODE: ", current_node, current_node.point, current_node.distance)

	#this will run after the end node has been found
	while current_node.parent:
		print("PATH TO FINAL NODE: ", current_node, current_node.point, current_node.distance)
		current_node = current_node.parent

start_point = (0, 0)
end_point = (6, 4)
DIRECTION = 4

matrix = []
x_range = 15
y_range = 15
for x in range(x_range):
	for y in range(y_range):
		matrix.append(Node((x, y)))	

for node in matrix:
	if node.point == start_point:
		start_node = node
	if node.point == end_point:
		end_node = node

#the first iteration of start node must be 0 (0 distance travelled)
result = dijkstra(start_node, end_node, matrix, DIRECTION)
