from dearpygui.dearpygui import get_item_children,get_item_pos,get_item_rect_size,node,node_attribute,mvNode_Attr_Static,add_text,split_frame
from math import sqrt

class Link:
	def __init__(self,node_1,node_2,editor) -> None:
		self.editor = editor
		self.origin = get_item_pos(self.editor)[0] + get_item_rect_size(self.editor)[0] / 2,get_item_pos(self.editor)[1] + get_item_rect_size(self.editor)[1] / 2
		self.node_1 = node_1
		self.node_2 = node_2

	def change_length(self,delta) -> int:
		slope = (get_item_pos(self.node_1)[1]-get_item_pos(self.node_2)[1])/(get_item_pos(self.node_1)[0]-get_item_pos(self.node_2)[0])
		# m=(y2-y1)/(x2-x1)
		# push the most inner node in direction of the line
		# returns the length after changing it

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
		origin = get_item_pos(editor)[0] + get_item_rect_size(editor)[0] / 2,get_item_pos(editor)[1] + get_item_rect_size(editor)[1] / 2
		title = hdllnode.data["title"]
		description = ''.join([value for field in hdllnode.data['data'] for key, value in field.items() if key != dp._internal.is_root_node]) #change import
		with node(label=title,parent=editor,pos=[origin[0] + range(-(get_item_rect_size(editor)[0] / 2),(get_item_rect_size(editor)[0] / 2)),origin[1] + range(-(get_item_rect_size(editor)[1] / 2),(get_item_rect_size(editor)[1] / 2))]) as nodeID:
			if description != "":
				with node_attribute(attribute_type=mvNode_Attr_Static):
					add_text(description)
		hdllnode.dpgID = nodeID
		split_frame()
		return nodeID

# RelationalUI = RelationalNodeUI(dpg.add_node_editor(parent=window))
# nodeEditor = RelationalUI.get_editor()



