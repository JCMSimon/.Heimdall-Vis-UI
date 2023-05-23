from dearpygui.dearpygui import draw_line,draw_arrow,get_item_configuration,get_item_pos,get_item_rect_size,get_item_label,get_item_children,set_item_pos,node,node_attribute,mvNode_Attr_Static,add_text,delete_item
from math import sqrt
import time
import threading
from random import choice
from sympy import symbols, Eq, solve

class Link:
	def __init__(self,node_1,node_2,node_editor,child_link=False,root_link=False) -> None:
		self.child_link = child_link
		self.root_link = root_link
		self.node_1 = createDPGNode(node_1,node_editor) # Always the Parent node (for now)
		self.node_2 = createDPGNode(node_2,node_editor)

	def draw(self,drawList):
		#TODO instead of drawing into the middle draw to the closest edge that is in direction of link. (idk how yet lmfao)
		if self.child_link:
			return draw_line(getItemMiddle(self.node_2),getItemMiddle(self.node_1),parent=drawList,color=(255,0,0),thickness=1)
		elif self.root_link:
			return draw_line(getItemMiddle(self.node_2),getItemMiddle(self.node_1),parent=drawList,color=(0,255,0),thickness=1)
		else:
			return draw_arrow(getItemMiddle(self.node_2),getItemMiddle(self.node_1),parent=drawList,color=(255,255,255),thickness=3)

	def change_length(self,delta,dl=None):
		# get positions
		moveable_nodeID = [node for node in [self.node_2,self.node_1] if get_item_configuration(node)["draggable"]][0]
		static_nodeID = self.node_2 if moveable_nodeID == self.node_1 else self.node_1
		moveable_node_pos = get_item_pos(moveable_nodeID)
		static_node_pos = get_item_pos(static_nodeID)
		# calculate new positions
		pos_if_delta_neg,pos_if_delta_pos = find_new_coords(moveable_node_pos[0],moveable_node_pos[1],static_node_pos[0],static_node_pos[1],delta)
		# use new position
		if (moveable_node_pos[0] > static_node_pos[0] and delta > 0 or moveable_node_pos[0] <= static_node_pos[0] and moveable_node_pos[0] < static_node_pos[0] and delta <= 0):
			set_item_pos(moveable_nodeID,pos=pos_if_delta_pos)
		elif (moveable_node_pos[0] > static_node_pos[0] or moveable_node_pos[0] < static_node_pos[0]):
			set_item_pos(moveable_nodeID,pos=pos_if_delta_neg)
		print("moved")

	def get_length(self) -> int:
		x,y = getItemMiddle(self.node_1)
		x1,y1 = getItemMiddle(self.node_2)
		return round(sqrt((x1-x)**2 + (y1-y)**2))

class RelationalNodeUI:
	"""A Relational UI (Wrapper) specifically made for [Heimdall](https://hdll.jcms.dev) based on the node editor from [dearpygui](https://github.com/hoffstadt/DearPyGui/issues)
	"""
	def __init__(self,parent,width,height,) -> None:
		with dpg.theme() as editor_theme:
			with dpg.theme_component(dpg.mvAll):
				dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,0,0,category=dpg.mvThemeCat_Core)
		self.editor = dpg.add_node_editor(parent=parent,width=width,height=height)
		dpg.bind_item_theme(parent,editor_theme)
		dpg.set_frame_callback(42,self.setup_draw_layer)

	def setup_draw_layer(self):
		with dpg.window(no_background=True,pos=dpg.get_item_pos(self.editor),width=dpg.get_item_rect_size(self.editor)[0],height=dpg.get_item_rect_size(self.editor)[1],no_move=True,no_title_bar=True,no_scrollbar=True,no_resize=True,max_size=(dpg.get_item_rect_size(self.editor)[0],dpg.get_item_rect_size(self.editor)[1]),horizontal_scrollbar=False,min_size=(dpg.get_item_rect_size(self.editor)[0],dpg.get_item_rect_size(self.editor)[1]),no_close=True,no_collapse=True,) as drawWindow:
			self.drawList = dpg.add_drawlist(width=dpg.get_item_rect_size(self.editor)[0],height=dpg.get_item_rect_size(self.editor)[1])

	def visualize(self,root) -> None:
		self.createLinks(root)
		self.randomiseNodePositions()
		# self.drawThread = threading.Thread(target=self.drawLinks)
		self.dragThread = threading.Thread(target=self.handleDragging)
		# self.drawThread.start()
		self.dragThread.start()
		for i in range(10):
			while True:
				for link in self.links:
					delta = 50 - link.get_length()
					link.change_length(delta,dl=self.drawList)
				break
			# while True:
		# 	for link in self.links:
		# 		if link.root_link:
		# 			if link.get_length() < 200:
		# 				link.change_length(1)
		# 		elif link.child_link:
		# 			if link.get_length() < 100:
		# 				link.change_length(1)
		# 		elif link.get_length() < 100:
		# 			link.change_length(1)
		# 		elif link.get_length() > 200:
		# 			link.change_length(-1)

	def randomiseNodePositions(self):
		for nodeId in self.get_editor_nodes():
			origin = get_item_pos(self.editor)[0] + get_item_rect_size(self.editor)[0] / 2,get_item_pos(self.editor)[1] + get_item_rect_size(self.editor)[1] / 2
			x = (origin[0] - (get_item_rect_size(nodeId)[0] / 2))
			y = (origin[1] - (get_item_rect_size(nodeId)[1] / 2))
			if get_item_label(nodeId) != "ROOT":
				x += choice((-1,1))
				y += choice((-1,1))
			set_item_pos(nodeId,(x,y))

	def createLinks(self,root) -> None:
		ListOfChildren = [root._children]
		self.links = [Link(root,child,self.editor) for child in root._children]
		todo = []
		todo.extend(root._children)
		for node in todo:
			if len(node._children) >= 2:
				ListOfChildren.append(node._children)
			self.links.extend(Link(node,child,self.editor) for child in node._children)
			self.links.append(Link(node,root,self.editor,root_link=True))
			todo.extend(node._children)
		for list in ListOfChildren:
			self.links.extend(Link(list[index], list[index + 1], self.editor, child_link=True) for index in range(len(list) - 1))

	def get_editor_nodes(self) -> list[int]:
		return get_item_children(self.editor)[children_index := 1]

	def drawLinks(self):
		list_of_drawn_elements = [link.draw(self.drawList) for link in self.links]
		time.sleep(1 / int(dpg.get_frame_rate()))
		for l in list_of_drawn_elements:
			dpg.delete_item(l)
		return

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
						mouseDelta = (dpg.get_drawing_mouse_pos()[0] - dpg.get_item_pos(node)[0],dpg.get_drawing_mouse_pos()[1] - dpg.get_item_pos(node)[1])
						while dpg.is_mouse_button_down(button=dpg.mvMouseButton_Left):
							# implement relative mouse delta shits
							dpg.set_item_pos(node,(dpg.get_drawing_mouse_pos()[0] - mouseDelta[0],dpg.get_drawing_mouse_pos()[1] - mouseDelta[1]))
		return

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
		description = ''.join([value for field in hdllnode.data['data'] for key, value in field.items() if hdllnode._is_root_node != True])
		with node(label=hdllnode.data["title"],parent=editor) as DPGNodeID:
			if description != "":
				with node_attribute(attribute_type=mvNode_Attr_Static):
					add_text(description)
			else:
				dpg.configure_item(DPGNodeID,draggable=False)
		hdllnode.dpgID = DPGNodeID
		return DPGNodeID

def getItemMiddle(item) -> tuple[float, float]:
	return [get_item_pos(item)[0] + get_item_rect_size(item)[0] / 2,get_item_pos(item)[1] + get_item_rect_size(item)[1] / 2]

def find_new_coords(moveable_x, moveable_y, static_x, static_y, delta):
	# I dont really understand this math but smart ppl in discord.gg/math do.
	# Calculate the line slope
	start_time = time.time()
	try:
		line_slope = (static_y - moveable_y) / (static_x - moveable_x)
	except ZeroDivisionError:
		print(0)
		if moveable_x == static_x:
			return [moveable_x,moveable_y + delta]
		elif moveable_y == static_y:
			return [moveable_x + delta,moveable_y]
	# Calculate the line y-intercept
	line_intercept = moveable_y - line_slope * moveable_x
	# Define the variables
	new_x, new_y = symbols('new_x new_y')
	# Define the equation of the line AB (y = mx + c)
	line_eq = Eq(new_y, line_slope * new_x + line_intercept)
	# Define the equation for the distance between points A and (x, y) ((x - old_x)^2 + (y - old_y)^2 = delta^2)
	distance_eq = Eq((new_x - moveable_x) ** 2 + (new_y - moveable_y) ** 2, delta ** 2)
	elapsed_time = time.time() - start_time
	print(f"Calculation took {elapsed_time:.6f} seconds")
	return solve((line_eq, distance_eq), (new_x, new_y))

# Test case
if __name__ == "__main__":
	class dp:
		class _internal:
			is_root_node = "is_root_node"
		class username:
			discord = "JCMS#0557"
			youtube = "JustCallMeSimon"
			google = "JCMS"

	class Node():
		def __init__(self,title,color=None,debug=False,_is_root=False) -> None:
			self.data = {
				"title":title,
				"data":[],
				"image":None,
			}
			self._is_root_node = _is_root
			self._children = []

		def addDataField(self,datatype,data):
			self.data["data"].append({datatype:data})

########################################

	root = Node("ROOT",_is_root=True)
	testResult = Node("Example Result")
	testResult.addDataField(dp.username.discord,"JCMS#0557")
	root._children.append(testResult)
	testResult2 = Node("Example Result 2")
	testResult2.addDataField(dp.username.youtube,"JCMS_")
	root._children.append(testResult2)
	testResult3 = Node("Example Result 3")
	testResult3.addDataField(dp.username.google,"JustCallMeSimon")
	testResult4 = Node("Example Result 4")
	testResult4.addDataField(dp.username.google,"JustCallMeSimon")
	testResult5 = Node("Example Result 5")
	testResult5.addDataField(dp.username.google,"JustCallMeSimon")
	testResult6 = Node("Example Result 6")
	testResult6.addDataField(dp.username.google,"JustCallMeSimon")
	testResult7 = Node("Example Result 7")
	testResult7.addDataField(dp.username.google,"JustCallMeSimon")
	testResult2._children.append(testResult3)
	testResult2._children.append(testResult4)
	testResult2._children.append(testResult5)
	testResult2._children.append(testResult7)
	testResult3._children.append(testResult6)
	from dearpygui import dearpygui as dpg
	dpg.create_context()
	dpg.create_viewport(title="Hello World", width=1500, height=800)
	dpg.setup_dearpygui()
	with dpg.window(label="Example Window") as wnd:
		rng = RelationalNodeUI(parent=wnd,width=600,height=600)
		dpg.add_button(parent=wnd,label="repo",callback=lambda: rng.randomiseNodePositions())
		dpg.add_button(parent=wnd,label="vis",callback=lambda: rng.visualize(root))
		dpg.add_button(parent=wnd,label="away",callback=lambda: rng.links[0].change_length(10,rng.drawList))
		dpg.add_button(parent=wnd,label="close",callback=lambda: rng.links[0].change_length(-10,rng.drawList))
		dpg.add_button(parent=wnd,label="len",callback=lambda: print(rng.links[0].get_length()))
	dpg.set_primary_window(wnd,True)
	dpg.show_viewport()
	dpg.start_dearpygui()