from dearpygui.dearpygui import get_item_children,get_item_pos,get_item_rect_size,node,node_attribute,mvNode_Attr_Static,add_text,set_item_pos,get_item_label
from math import sqrt
from random import choice

import time

class Link:
	def __init__(self,node_1,node_2,editor,is_child_link=False) -> None:
		self.is_child_link = is_child_link
		self.editor = editor
		self.node_1 = createDPGNode(node_1,self.editor) # Always the Parent node (for now)
		self.node_2 = createDPGNode(node_2,self.editor)

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
	def __init__(self,node_editor_id) -> None:
		self.editor = node_editor_id
		self.settings = {"max_link_length": 150,"min_link_length": 100}

	def get_editor(self) -> int:
		return self.editor

	def visualize(self,root) -> None:
		self.createLinks(root)
		for node in self.get_editor_nodes():
			self.randomiseNodePositions(node)


	def randomiseNodePositions(self,nodeId):
		origin = get_item_pos(self.editor)[0] + get_item_rect_size(self.editor)[0] / 2,get_item_pos(self.editor)[1] + get_item_rect_size(self.editor)[1] / 2
		x = (origin[0] - (get_item_rect_size(nodeId)[0] / 2))
		y = (origin[1] - (get_item_rect_size(nodeId)[1] / 2))
		if get_item_label(nodeId) != "ROOT":
			x += choice(range(-200,200))
			y += choice(range(-200,200))
		set_item_pos(nodeId,(x,y))

	def createLinks(self,root) -> None:
		childLists = [root._children]
		self.links = [Link(root,child,self.editor) for child in root._children]
		for node in (todo := root._children):
			childLists.append(node._children)
			self.links.extend(Link(node,child,self.editor) for child in node._children)
			todo.extend(node._children)
		for children in childLists:
			self.links.extend([Link(children[i],children[i+1],self.editor,is_child_link=True) for i in range(len(children) - 1)])
			if len(children) > 2:
				self.links.append(Link(children[-1],children[0],self.editor,is_child_link=True))

	def get_editor_nodes(self) -> list[int]:
		return get_item_children(self.editor)[children_index := 1]

def createDPGNode(hdllnode,editor) -> int:
	try:
		return hdllnode.dpgID
	except AttributeError:
		title = hdllnode.data["title"]
		description = ''.join([value for field in hdllnode.data['data'] for key, value in field.items() if hdllnode._is_root_node != True])
		with node(label=title,parent=editor) as nodeID:
			if description != "":
				with node_attribute(attribute_type=mvNode_Attr_Static):
					add_text(description)
			else:
				dpg.configure_item(nodeID,draggable=False)
		hdllnode.dpgID = nodeID
		return nodeID

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
	testResult4 = Node("Example Result 3")
	testResult4.addDataField(dp.username.google,"JustCallMeSimon")
	testResult5 = Node("Example Result 3")
	testResult5.addDataField(dp.username.google,"JustCallMeSimon")
	testResult6 = Node("Example Result 3")
	testResult6.addDataField(dp.username.google,"JustCallMeSimon")
	testResult7 = Node("Example Result 3")
	testResult7.addDataField(dp.username.google,"JustCallMeSimon")
	testResult2._children.append(testResult3)
	testResult2._children.append(testResult4)
	testResult2._children.append(testResult5)
	testResult2._children.append(testResult6)
	testResult2._children.append(testResult7)
	from dearpygui import dearpygui as dpg
	dpg.create_context()
	dpg.create_viewport(title="Hello World", width=640, height=500)
	dpg.setup_dearpygui()
	with dpg.window(label="Example Window") as wnd:
		rng = RelationalNodeUI(dpg.add_node_editor(parent=wnd,minimap=True))
		dpg.add_button(parent=wnd,label="vis",callback=lambda: rng.visualize(root))
		dpg.add_button(parent=wnd,label="all",callback=lambda: [link.change_length(1) for link in rng.links])
		dpg.add_button(parent=wnd,label="all",callback=lambda: [link.change_length(-1) for link in rng.links])
	dpg.set_primary_window(wnd,True)
	dpg.show_viewport()
	dpg.start_dearpygui()