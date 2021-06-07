#instance of node that will be placed in matrix
class Node:
	#point = x,y positon of node
	#value = cost of traversing this node 
	#parent = the parent node to this node (used for connecting nodes when path building)
	#H = distance from end_node
	#G = distance from start_node
	def __init__(self, point):
		self.point = point
		self.value = 1
		self.parent = None
		self.H = 0
		self.G = 0
	
	#function to use whenever we are increasing the G count
	def move_cost(self, other):
		return self.value
	
#return the heuristic cost of this node 
def manhattan(current_node, goal_node):
	node_x, node_y = current_node.point
	goal_x, goal_y = goal_node.point

	dx = abs(node_x - goal_x)
	dy = abs(node_y - goal_y)
	cost = current_node.value
	return cost * (dx+dy)


#use this to determine the neighbors of the current node
def neighbors(current_node, matrix):
	x, y = current_node.point
	#dynamically get the neighbors x, y around in a 4 way direction (left, down, up, right)
	neighbor_list = [[x-1, y], [x, y - 1], [x, y + 1], [x+1, y] ]
	#combine it into 1 variable so you can return a list of all neighbors nodes	
	node_list = []	
	for neighbor in neighbor_list:
		neighbor_x, neighbor_y = neighbor[0], neighbor[1]
		for node in matrix:
			node_x, node_y = node.point
			if node_x == neighbor_x and node_y == neighbor_y:
				node_list.append(node)

	if node_list:
		return node_list[::-1]
	else:
		print("NO NEIGHBORS FOUND: ", current_node.point)
		return []


def astar(start_node, end_node, matrix):
	open_set = [start_node]
	closed_set = []
	current_node = start_node
	while open_set:
		#find the item in openset with the lowest F value:
		current_node = min(open_set, key=lambda f: f.G + f.H)
		#print("CURRENT NODE: ", current_node.point)
		if current_node == end_node:
			final_path = []
			while current_node.parent:
				final_path.append(current_node.parent)
				current_node = current_node.parent
			final_path.append(current_node)
			return final_path[::-1]

		open_set.remove(current_node)
		closed_set.append(current_node)
		#loop through the current nodes neighbors iteratively in order to determine the best path
		for node in neighbors(current_node, matrix):
			#skip if already in our closed_set
			if node in closed_set:
				continue
			
			#if it's not, check if the G score is better
			if node in open_set:
				new_g = current_node.G + current_node.move_cost(node)
				if node.G > new_g:
					#print("NODE INFO: ", node.point, node.G)
					#if it is, update the node to have a new parent
					node.G = new_g
					node.parent = current_node
			else:
				#if it's not in the open set, calculate its's G + H score 
				node.G = current_node.G + current_node.move_cost(node)
				node.H = manhattan(node, end_node)
				#print("NODE: ", node.point, "MANHATTAN DISTANCE: ", node.H, "NODE G: ", node.G)
				#set the parent to our current node
				node.parent = current_node
				#add it to the set afterwards
				open_set.append(node)
	
#script starts here
start_point = [6, 7]
end_point= [1, 1]

#populate the matrix with node instances
x_range = range(1, 10)
y_range = range(1, 10)
matrix = []
for x in x_range:
	for y in y_range:
		matrix.append(Node(point=[x,y]))

#create the instance of start node + end node 
for node in matrix:
	if Node(point=start_point).point == node.point:
		start_node = node 
	if Node(point=end_point).point == node.point:
		end_node = node

print("START NODE: ", start_node, start_node.point)
print("GOAL NODE: ", end_node, end_node.point)

#list of nodes that point the algo determined is the best way to get there
closed_set = astar(start_node, end_node, matrix)
print("POINT FOUND: ")
for i in closed_set:
	if i.parent:
		print(i, i.point, i.point)
