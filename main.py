from dearpygui.dearpygui import get_item_children,get_item_pos,get_item_rect_size,node,node_attribute,mvNode_Attr_Static,add_text,set_item_pos,get_item_label
from math import sqrt
import time
import threading
from random import choice

class Link:
	def __init__(self,node_1,node_2,node_editor,child_link=False) -> None:
		self.child_link = child_link
		self.node_1 = createDPGNode(node_1,node_editor) # Always the Parent node (for now)
		self.node_2 = createDPGNode(node_2,node_editor)

	def draw(self,drawList):
		color = (255, 0, 0, 255) if self.child_link else (255, 255, 255, 255)
		#instead of drawing into the middle draw to the closest edge that is in direction of link. (idk how yet lmfao)
		return dpg.draw_arrow(getItemMiddle(self.node_2),getItemMiddle(self.node_1),parent=drawList,color=color,thickness=3)

	def change_length(self,delta):
		x,y = getItemMiddle(self.node_1)
		x1,y1 = getItemMiddle(self.node_2)
		try:
			slope =  (y1-y)/(x1-x)
		except ZeroDivisionError:
			return
		else:
			if x1 < x and y1 < y or (x1 <= x or y1 >= y) and x1 < x and y1 > y:
				new_y = (y1 - delta * slope) - get_item_rect_size(self.node_2)[1]/2
				new_x = (x1 - delta) - get_item_rect_size(self.node_2)[0]/2
			elif x1 > x and y1 < y or x1 > x and y1 > y:
				new_y = (y1 + delta * slope) - get_item_rect_size(self.node_2)[1]/2
				new_x = (x1 + delta) - get_item_rect_size(self.node_2)[0]/2
			else:
				return
		set_item_pos(self.node_2,[new_x,new_y])

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
		self.drawThread = threading.Thread(target=self.drawLinks)
		self.dragThread = threading.Thread(target=self.handleDragging)
		self.drawThread.start()
		self.dragThread.start()

	def randomiseNodePositions(self):
		for nodeId in self.get_editor_nodes():
			origin = get_item_pos(self.editor)[0] + get_item_rect_size(self.editor)[0] / 2,get_item_pos(self.editor)[1] + get_item_rect_size(self.editor)[1] / 2
			x = (origin[0] - (get_item_rect_size(nodeId)[0] / 2))
			y = (origin[1] - (get_item_rect_size(nodeId)[1] / 2))
			if get_item_label(nodeId) != "ROOT":
				x += choice(range(-200,200))
				y += choice(range(-200,200))
			set_item_pos(nodeId,(x,y))

	def createLinks(self,root) -> None:
		self.links = [Link(root,child,self.editor) for child in root._children]
		todo = root._children
		for node in (todo):
			self.links.extend(Link(node,child,self.editor) for child in node._children)
			todo.extend(node._children)

	def get_editor_nodes(self) -> list[int]:
		return get_item_children(self.editor)[children_index := 1]

	def drawLinks(self):
		while True:
			lista = [link.draw(self.drawList) for link in self.links]
			time.sleep(1 / int(dpg.get_frame_rate()))
			for l in lista:
				dpg.delete_item(l)
		return

	def handleDragging(self,isDragging = False):
		while True:
			time.sleep(0.016)
			if dpg.is_mouse_button_dragging(button=dpg.mvMouseButton_Left,threshold=0.05) and not isDragging and not dpg.is_mouse_button_released(button=dpg.mvMouseButton_Left):
				isDragging = True
			elif isDragging and not dpg.is_mouse_button_down(button=dpg.mvMouseButton_Left):
				isDragging = False
			if isDragging:
				if node := getNodeByPosition(self.get_editor_nodes(), dpg.get_drawing_mouse_pos()):
					while dpg.is_mouse_button_down(button=dpg.mvMouseButton_Left):
						# implement relative mouse delta shits
						dpg.set_item_pos(node,dpg.get_drawing_mouse_pos())
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
			print("Mouse position is inside the bounding box of key:", dpg.get_item_label(nodeID))
			return nodeID
	return None

	# for item in dpg.get_item_children(ne)[1]}
	# 	nodeBoxes = {item:(dpg.get_item_pos(item),[dpg.get_item_pos(item)[0] + dpg.get_item_rect_size(item)[0],dpg.get_item_pos(item)[1] + dpg.get_item_rect_size(item)[1]])
	# 	for key, value in nodeBoxes.items():
	# 		x1, y1 = value[0]
	# 		x2, y2 = value[1]
	# 		box = dpg.draw_rectangle(pmin=value[0],pmax=value[1],parent=drawLayer)
	# 		if x1 <= pos[0] and pos[0] <= x2 and y1 <= pos[1] and pos[1] <= y2:
	# 			print("Mouse position is inside the bounding box of key:", dpg.get_item_label(key))
	# 			item = key
	# 			while dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
	# 				dpg.set_item_pos(item,(dpg.get_mouse_pos()[0] - dpg.get_item_rect_size(item)[0] / 2,dpg.get_mouse_pos()[1] - dpg.get_item_rect_size(item)[1] / 2))
	# 			break

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
	# testResult6 = Node("Example Result 3")
	# testResult6.addDataField(dp.username.google,"JustCallMeSimon")
	# testResult7 = Node("Example Result 3")
	# testResult7.addDataField(dp.username.google,"JustCallMeSimon")
	testResult2._children.append(testResult3)
	testResult2._children.append(testResult4)
	testResult2._children.append(testResult5)
	# testResult2._children.append(testResult6)
	# testResult2._children.append(testResult7)
	from dearpygui import dearpygui as dpg
	dpg.create_context()
	dpg.create_viewport(title="Hello World", width=1500, height=800)
	dpg.setup_dearpygui()
	with dpg.window(label="Example Window") as wnd:
		rng = RelationalNodeUI(parent=wnd,width=600,height=600)
		dpg.add_button(parent=wnd,label="repo",callback=lambda: rng.randomiseNodePositions())
		dpg.add_button(parent=wnd,label="vis",callback=lambda: rng.visualize(root))
		dpg.add_button(parent=wnd,label="end",callback=lambda: rng.end())
	dpg.set_primary_window(wnd,True)
	dpg.show_viewport()
	dpg.start_dearpygui()