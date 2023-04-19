from dearpygui.dearpygui import get_item_children,get_item_pos,get_item_rect_size,node,node_attribute,mvNode_Attr_Static,add_text,set_item_pos,split_frame,get_item_label
from math import sqrt
from random import choice
from threading import Thread


import time

class Link:
	def __init__(self,node_1,node_2,editor) -> None:
		self.editor = editor
		self.origin = get_item_pos(self.editor)[0] + get_item_rect_size(self.editor)[0] / 2,get_item_pos(self.editor)[1] + get_item_rect_size(self.editor)[1] / 2
		self.node_1 = node_1
		self.node_2 = node_2

	def change_length(self,delta) -> int:
		slope = (get_item_pos(self.node_1)[1]-get_item_pos(self.node_2)[1])/(get_item_pos(self.node_1)[0]-get_item_pos(self.node_2)[0])


	def get_length(self) -> int:
		"""
		This function calculates the length of a line segment between two nodes using their positions.

		Returns:
		  The function `get_length` returns the length of the line segment between `node_1` and `node_2`
		using the distance formula.
		"""
		return sqrt((get_item_pos(self.node_2)[0] - get_item_pos(self.node_1)[0]) ** 2 + (get_item_pos(self.node_2)[1] - get_item_pos(self.node_1)[1]) ** 2)

	def draw(self) -> None:
		pass

	def get_outer_node(self) -> int:
		"""
		This function returns the node that is further from the origin.
		"""
		if sqrt((get_item_pos(self.node_1)[0] - get_item_pos(self.node_1)[0]) ** 2 + (get_item_pos(self.origin)[1] - get_item_pos(self.origin)[1]) ** 2) > sqrt((get_item_pos(self.node_2)[0] - get_item_pos(self.node_2)[0]) ** 2 + (get_item_pos(self.origin)[1] - get_item_pos(self.origin)[1]) ** 2):
			return self.node_1
		else:
			return self.node_2

	def get_inner_node(self) -> int:
		"""
		This function returns the node that is closer to the origin.
		"""
		if sqrt((get_item_pos(self.node_1)[0] - get_item_pos(self.node_1)[0]) ** 2 + (get_item_pos(self.origin)[1] - get_item_pos(self.origin)[1]) ** 2) < sqrt((get_item_pos(self.node_2)[0] - get_item_pos(self.node_2)[0]) ** 2 + (get_item_pos(self.origin)[1] - get_item_pos(self.origin)[1]) ** 2):
			return self.node_2
		else:
			return self.node_1

	def convertNodesToDPG(self) -> None:
		"""
		This function converts two nodes to DPG nodes using the createDPGNode function and assigns them to
		self.node_1 and self.node_2.
		"""
		self.node_1 = createDPGNode(self.node_1,self.editor)
		self.node_2 = createDPGNode(self.node_2,self.editor)

class RelationalNodeUI:
	"""A Relational UI (Wrapper) specifically made for [Heimdall](https://hdll.jcms.dev) based on the node editor from [dearpygui](https://github.com/hoffstadt/DearPyGui/issues)
	"""
	def __init__(self,node_editor_id,min_link_length=100,max_link_length=300) -> None:
		self.editor = node_editor_id
		self.settings = {"max_link_length": max_link_length,"min_link_length": min_link_length}

	def get_editor(self) -> int:
		"""
		This function returns the editor of an object as an integer.

		Returns:
		  The method `get_editor` is returning an integer value which is the value of the attribute `editor`
		of the object.
		"""
		return self.editor

	def visualize(self,root) -> None:
		self.createLinks(root)
		for link in self.links:
			link.convertNodesToDPG()
		for node in self.get_editor_nodes():
			self.randomiseNodePosition(node)

	def start(self):
		self.enforceRules = True
		self.ruleThread = Thread(target=self._enforceRules,daemon=True)
		self.ruleThread.start()

	def stop(self):
		self.enforceRules = False

	def _enforceRules(self): #TODO Broken cause i GPT'd it lmao
		while self.enforceRules:
			for link in self.links:
				if link.get_length() > self.settings["max_link_length"]:
					link.change_length(-1)
				elif link.get_length() < self.settings["max_link_length"]:
					link.change_length(1)
				else:
					continue

	def randomiseNodePosition(self,nodeId):
		origin = get_item_pos(self.editor)[0] + get_item_rect_size(self.editor)[0] / 2,get_item_pos(self.editor)[1] + get_item_rect_size(self.editor)[1] / 2
		x = (origin[0] - (get_item_rect_size(nodeId)[0] / 2))
		y = (origin[1] - (get_item_rect_size(nodeId)[1] / 2))
		if get_item_label(nodeId) != "ROOT":
			x += choice(range(-100,100))
			y += choice(range(-100,100))
		set_item_pos(nodeId,(x,y))

	def createLinks(self,root) -> None:
		"""
		This function creates links between nodes in a tree structure.

		Args:
		  root: The root parameter is a node object that represents the root of a tree data structure. It is
		the starting point for creating links between nodes in the tree.
		"""
		self.links = [Link(root,child,self.editor) for child in root._children]
		for node in (todo := root._children): # im not sure if this works
			self.links.extend(Link(node,child,self.editor) for child in node._children)
			todo.extend(node._children)

	def get_editor_nodes(self) -> list[int]:
		"""
		This function returns a list of integer IDs representing the child nodes of a given editor node.

		Returns:
		  A list of integers representing the children nodes of the "editor" node. The implementation uses
		the `get_item_children` function to retrieve the children nodes and then uses a Python walrus
		operator to assign the index of the children list to a variable named `children_index`. Finally, the
		function returns the children nodes by slicing the list starting from the index 1 (i.e., excluding
		the first element
		"""
		return get_item_children(self.editor)[children_index := 1]


def createDPGNode(hdllnode,editor) -> int:
	"""
	This function creates a DPG node with a title and description and returns its ID.

	Args:
	  hdllnode: This is a variable that represents a node in a hierarchical data structure. It is used
	to retrieve information about the node, such as its title and data.
	  editor: The editor parameter is a reference to the editor window or interface where the DPG
	node will be created.

	Returns:
	  an integer, which is the ID of a DPG node.
	"""
	try:
		return hdllnode.dpgID
	except AttributeError:
		title = hdllnode.data["title"]
		description = ''.join([value for field in hdllnode.data['data'] for key, value in field.items() if key != dp._internal.is_root_node])
		with node(label=title,parent=editor,) as nodeID:
			if description:
				with node_attribute(attribute_type=mvNode_Attr_Static):
					add_text(description)
		hdllnode.dpgID = nodeID
		return nodeID

# RelationalUI = RelationalNodeUI(dpg.add_node_editor(parent=window))
# nodeEditor = RelationalUI.get_editor()

# Test case
if __name__ == "__main__":
	from Node import Node
	from Data import datapoints as dp
	root = Node("ROOT")
	root.addDataField(dp._internal.is_root_node,True)
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
	dpg.create_viewport(title="Hello World", width=640, height=480)
	dpg.setup_dearpygui()
	with dpg.window(label="Example Window") as wnd:
		rng = RelationalNodeUI(dpg.add_node_editor(parent=wnd))
		dpg.add_button(label="vis",callback=lambda: rng.visualize(root))
		dpg.add_button(label="start",callback=lambda: rng.start())
		dpg.add_button(label="stop",callback=lambda: rng.stop())
	dpg.set_primary_window(wnd,True)
	dpg.show_viewport()
	dpg.start_dearpygui()