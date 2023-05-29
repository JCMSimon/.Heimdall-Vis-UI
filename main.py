import dearpygui.dearpygui as dpg
from math import sqrt
import time
import threading
from random import choice

class Link:
	def __init__(self,node_1,node_2,node_editor) -> None:
		self.node_1 = createDPGNode(node_1,node_editor) # Always the Parent node (for now)
		self.node_2 = createDPGNode(node_2,node_editor)

	def draw(self,drawList):
	 	#TODO instead of drawing into the middle draw to the closest edge that is in direction of link. (idk how yet lmfao)

		node_1_poses = generate_anchor_points(self.node_1)
		node_2_poses = generate_anchor_points(self.node_2)

		poses = find_closest_points(node_1_poses,node_2_poses)
		return dpg.draw_arrow(poses[1],poses[0],parent=drawList,thickness=3)

	def get_length(self) -> int:
		x,y = getItemMiddle(self.node_1)
		x1,y1 = getItemMiddle(self.node_2)
		return round(sqrt((x1-x)**2 + (y1-y)**2))

class RelationalNodeUI:
	"""A Relational UI specifically made for [Heimdall](https://hdll.jcms.dev) based on the node editor from [dearpygui](https://github.com/hoffstadt/DearPyGui)
	"""
	def __init__(self,parent,width,height,) -> None:
		self.width = width
		self.height = height
		self.editor = dpg.add_node_editor(parent=parent,width=self.width,height=self.height)
		with dpg.theme() as editor_theme:
			with dpg.theme_component(dpg.mvAll):
				dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,0,0,category=dpg.mvThemeCat_Core)
				dpg.add_theme_style(dpg.mvNodeStyleVar_GridSpacing,0,category=dpg.mvThemeCat_Nodes)
				dpg.add_theme_style(dpg.mvNodeStyleVar_NodePadding,6,4,category=dpg.mvThemeCat_Nodes)
				dpg.add_theme_style(dpg.mvNodeStyleVar_NodeCornerRounding,0,category=dpg.mvThemeCat_Nodes)
				dpg.add_theme_style(dpg.mvNodeStyleVar_NodeBorderThickness,0,category=dpg.mvThemeCat_Nodes)
		dpg.bind_item_theme(parent,editor_theme)
		dpg.set_frame_callback(1,self.setup_draw_layer)

	def setup_draw_layer(self):
		with dpg.theme() as draw_window_theme:
			with dpg.theme_component(dpg.mvAll):
				dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,0,0,category=dpg.mvThemeCat_Core)
		with dpg.window(no_background=True,pos=dpg.get_item_pos(self.editor),width=self.width,height=self.height,no_move=True,no_title_bar=True,no_scrollbar=True,no_resize=True,max_size=(self.width,self.height),horizontal_scrollbar=False,min_size=(self.width,self.height),no_close=True,no_collapse=True) as drawWindow:
			dpg.bind_item_theme(drawWindow,draw_window_theme)
			self.drawList = dpg.add_drawlist(width=self.width,height=self.height,pos=dpg.get_item_pos(self.editor))

	def startInteractionThreads(self):
		self.drawThread = threading.Thread(target=self.drawLinks)
		self.dragThread = threading.Thread(target=self.handleDragging)
		self.drawThread.start()
		self.dragThread.start()

	def visualize(self,root) -> None:
		self.createLinks(root)
		# Center Root Node
		dpg.set_item_pos(self.get_editor_nodes()[0],getItemMiddle(self.editor))
		# Randomise other nodes
		for node in self.get_editor_nodes()[1:]:
			dpg.set_item_pos(node,(choice(range(self.width)),choice(range(self.height))))
		self.settings = {
		# Higher => Nodes further apart
		"repulsive_force_constant":3.0,
		# Higher => Connected Nodes further together
		"attractive_force_constant":0.5,
		# Higher => Nodes move less per iteration
		"damping_factor":0.1,
		# How far a Node can travel max
		"max_displacement_threshold":0.1,
		# Iterations
		"max_iterations":200,
		}

		# Iterative force calculations and position updates
		for _ in range(self.settings["max_iterations"]):
			max_displacement = 0.0
			# Reset net force
			net_forces = {node: [0.0, 0.0] for node in self.get_editor_nodes()}

		# Calculate repulsive forces
		for i, node1 in enumerate(self.get_editor_nodes()):
			pos1 = dpg.get_item_pos(node1)
			for node2 in self.get_editor_nodes()[i + 1:]:
				pos2 = dpg.get_item_pos(node2)
				displacement = [pos1[0] - pos2[0], pos1[1] - pos2[1]]
				distance_squared = displacement[0] ** 2 + displacement[1] ** 2
				distance = max(sqrt(distance_squared), 0.001)  # Avoid division by zero
				force_magnitude = self.settings["repulsive_force_constant"] / (distance_squared + 1e-6)  # Add a small value (epsilon) (anti zero division)
				force = [force_magnitude * (displacement[0] / distance),force_magnitude * (displacement[1] / distance)]
				net_forces[node1][0] += force[0]
				net_forces[node1][1] += force[1]
				net_forces[node2][0] -= force[0]
				net_forces[node2][1] -= force[1]

			# Calculate attractive forces
			for link in self.links:
				node1, node2 = link.node_1,link.node_2
				pos1 = dpg.get_item_pos(node1)
				pos2 = dpg.get_item_pos(node2)
				displacement = [pos1[0] - pos2[0], pos1[1] - pos2[1]]
				distance = max(sqrt(displacement[0] ** 2 + displacement[1] ** 2), 0.001)  # Avoid division by zero
				force_magnitude = self.settings["attractive_force_constant"] * distance
				force = [force_magnitude * (displacement[0] / distance),force_magnitude * (displacement[1] / distance)]
				net_forces[node1][0] -= force[0]
				net_forces[node1][1] -= force[1]
				net_forces[node2][0] += force[0]
				net_forces[node2][1] += force[1]

			# Update positions based on net forces
			for node in self.get_editor_nodes():
				displacement = net_forces[node]
				displacement[0] *= self.settings["damping_factor"]
				displacement[1] *= self.settings["damping_factor"]
				current_pos = dpg.get_item_pos(node)
				new_pos = [current_pos[0] + displacement[0], current_pos[1] + displacement[1]]
				dpg.set_item_pos(node, new_pos)

				# Calculate maximum displacement for convergence check
				max_displacement = max(max_displacement, sqrt(displacement[0] ** 2 + displacement[1] ** 2))

			# Check for convergence
			if max_displacement < self.settings["max_displacement_threshold"]:
				break

	def createLinks(self,root) -> None:
		self.links = [Link(root,child,self.editor) for child in root._children]
		todo = []
		todo.extend(root._children)
		for node in todo:
			self.links.extend(Link(node,child,self.editor) for child in node._children)
			todo.extend(node._children)

	def get_editor_nodes(self) -> list[int]:
		return dpg.get_item_children(self.editor)[childrenIndex := 1]

	def drawLinks(self):
		while True:
			list_of_drawn_elements = [link.draw(self.drawList) for link in self.links]
			time.sleep(1 / int(dpg.get_frame_rate()))
			for item in list_of_drawn_elements:
				dpg.delete_item(item)

	def handleDragging(self,isDragging = False):
		while True:
			time.sleep(0.016)
			if dpg.is_mouse_button_dragging(button=dpg.mvMouseButton_Left,threshold=0.05) and not isDragging and not dpg.is_mouse_button_released(button=dpg.mvMouseButton_Left):
				isDragging = True
				# allow start dragging for 2 ms
				drag_ts_timeout = time.time() + 0.02
			elif isDragging and not dpg.is_mouse_button_down(button=dpg.mvMouseButton_Left):
				isDragging = False
			if isDragging:
				if node := getNodeByPosition(self.get_editor_nodes(), dpg.get_drawing_mouse_pos()):
					if time.time() < drag_ts_timeout:
						# This makes it so that the node is relative to the mouse instead of snapping to the corner. WAY better ux
						mouseDelta = (dpg.get_drawing_mouse_pos()[0] - dpg.get_item_pos(node)[0],dpg.get_drawing_mouse_pos()[1] - dpg.get_item_pos(node)[1])
						while dpg.is_mouse_button_down(button=dpg.mvMouseButton_Left):
							dpg.set_item_pos(node,(dpg.get_drawing_mouse_pos()[0] - mouseDelta[0],dpg.get_drawing_mouse_pos()[1] - mouseDelta[1]))


def getNodeByPosition(nodes,mousepos):
	draggable_nodes = [node for node in nodes if dpg.get_item_configuration(node)["draggable"]]
	# generate bounding boxes for all nodes that are draggable
	for node in draggable_nodes:
		nodeBox = {node:(dpg.get_item_pos(node),[dpg.get_item_pos(node)[0] + dpg.get_item_rect_size(node)[0],dpg.get_item_pos(node)[1] + dpg.get_item_rect_size(node)[1]])}
		for nodeID, nodePos in nodeBox.items():
			x1, y1 = nodePos[0]
			x2, y2 = nodePos[1]
			if ( x1 > mousepos[0] or mousepos[0] > x2 or y1 > mousepos[1] or mousepos[1] > y2):
				continue
			return nodeID
	return None

def createDPGNode(hdllnode,editor) -> int:
	try:
		return hdllnode.dpgID
	except AttributeError:
		description = '\n'.join([value for field in hdllnode.data['data'] for key, value in field.items() if hdllnode._is_root_node != True])
		with dpg.node(label=hdllnode.data["title"],parent=editor) as DPGNodeID:
			if description != "":
				with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
					dpg.add_text(description)
			else:
				dpg.configure_item(DPGNodeID,draggable=False)
		hdllnode.dpgID = DPGNodeID
		return DPGNodeID

def getItemMiddle(item) -> tuple[float, float]:
	return [dpg.get_item_pos(item)[0] + dpg.get_item_rect_size(item)[0] / 2,dpg.get_item_pos(item)[1] + dpg.get_item_rect_size(item)[1] / 2]

def generate_anchor_points(node):
	position = dpg.get_item_pos(node)
	width = dpg.get_item_rect_size(node)[0]
	height = dpg.get_item_rect_size(node)[1]

	# Calculate the coordinates of the four corners
	top_left = position
	top_right = (position[0] + width, position[1])
	bottom_left = (position[0], position[1] + height)
	bottom_right = (position[0] + width, position[1] + height)

	# Calculate the coordinates of the midpoints on each side
	top_midpoint = (position[0] + width // 2, position[1])
	bottom_midpoint = (position[0] + width // 2, position[1] + height)
	left_midpoint = (position[0], position[1] + height // 2)
	right_midpoint = (position[0] + width, position[1] + height // 2)

	# i decided to only go with the sides and not corner cause it looks nicer imo
	return [
		# top_left,
		# top_right,
		# bottom_left,
		# bottom_right,
		top_midpoint,
		bottom_midpoint,
		left_midpoint,
		right_midpoint,
	]

def find_closest_points(points1, points2):
    closest_distance = float('inf')
    closest_points = None
    # Iterate over each pair of points from both lists
    for point1 in points1:
        for point2 in points2:
            # Calculate the Euclidean distance between the two points
            distance = sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

            # Update the closest distance and points if the current distance is smaller
            if distance < closest_distance:
                closest_distance = distance
                closest_points = (point1, point2)
    return closest_points


# ########################################
# # Test case
# if __name__ == "__main__":
# 	class dp:
# 		class _internal:
# 			is_root_node = "is_root_node"
# 		class username:
# 			discord = "JCMS#0557"
# 			youtube = "JustCallMeSimon"
# 			google = "JCMS"

# 	class Node():
# 		def __init__(self,title,color=None,debug=False,_is_root=False) -> None:
# 			self.data = {
# 				"title":title,
# 				"data":[],
# 				"image":None,
# 			}
# 			self._is_root_node = _is_root
# 			self._children = []

# 		def addDataField(self,datatype,data):
# 			self.data["data"].append({datatype:data})

# 	# TREE START
# 	root = Node("ROOT",_is_root=True)
# 	exampleResult1 = Node("Example Result 1")
# 	exampleResult1.addDataField("dp.username.discord", "User1#1234")
# 	root._children.append(exampleResult1)

# 	# Random data for Example Result 2
# 	exampleResult2 = Node("Example Result 2")
# 	exampleResult2.addDataField("dp.username.youtube", "User2")
# 	exampleResult2.addDataField("dp.username.twitter", "User2Tweets")
# 	root._children.append(exampleResult2)

# 	# Random data for Example Result 3
# 	exampleResult3 = Node("Example Result 3")
# 	exampleResult3.addDataField("dp.username.google", "User3")
# 	exampleResult3.addDataField("dp.username.linkedin", "User3LinkedIn")
# 	root._children.append(exampleResult3)

# 	# Random data for Example Result 4
# 	exampleResult4 = Node("Example Result 4")
# 	exampleResult4.addDataField("dp.username.facebook", "User4")
# 	exampleResult4.addDataField("dp.username.instagram", "User4Insta")
# 	root._children.append(exampleResult4)

# 	# Random data for Example Result 5
# 	exampleResult5 = Node("Example Result 5")
# 	exampleResult5.addDataField("dp.username.discord", "User5#5678")
# 	root._children.append(exampleResult5)

# 	# Random data for Example Result 6
# 	exampleResult6 = Node("Example Result 6")
# 	exampleResult6.addDataField("dp.username.youtube", "User6")
# 	root._children.append(exampleResult6)	# TREE END
# 	dpg.create_context()
# 	dpg.create_viewport(title="Hello World", width=1500, height=800)
# 	dpg.setup_dearpygui()
# 	with dpg.window(label="Example Window") as wnd:
# 		rng = RelationalNodeUI(parent=wnd,width=1200,height=600)
# 		dpg.add_button(parent=wnd,label="visualize tree",callback=lambda: rng.visualize(root))
# 		dpg.add_button(parent=wnd,label="draw arrows and handle drag",callback=lambda: rng.startInteractionThreads())
# 	dpg.set_primary_window(wnd,True)
# 	dpg.show_viewport()
# 	dpg.start_dearpygui()