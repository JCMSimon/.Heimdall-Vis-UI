from dearpygui.dearpygui import get_item_children,draw_line,get_item_pos,get_item_rect_size,node,node_attribute,mvNode_Attr_Static,add_text
from os.path import isfile
from math import sqrt

class Link:
	def __init__(self,node_1,node_2,editor) -> None:
		self.editor = editor
		self.origin = get_item_pos(self.editor)[0] + get_item_rect_size(self.editor)[0],get_item_pos(self.editor)[1] + get_item_rect_size(self.editor)[1]
		self.node_1 = node_1
		self.node_2 = node_2

	def change_length(self,delta) -> int:
		# push the most outer node in direction of the line
		# returns the length after changing it
		pass

	def get_length(self) -> int:
		p = get_item_pos(self.node_1)
		p1 = get_item_pos(self.node_2)
		return sqrt((p1[0] - p[0]) ** 2 + (p1[1] - p[1]) ** 2)

	def draw(self) -> None:
		self.link = draw_line(get_item_pos(self.node_1),get_item_pos(self.node_2),color=(0,0,0))

	def get_outer_node(self) -> int:
		# returns the node that is further from the origin
		pass

	def convertNodesToDPG(self):
		self.node_1 = createDPGNode(self.node_1,self.editor)
		self.node_2 = createDPGNode(self.node_2,self.editor)

class RelationalNodeUI:
	"""A Relational UI (Wrapper) specifically made for [Heimdall](https://hdll.jcms.dev) based on the node editor from [dearpygui](https://github.com/hoffstadt/DearPyGui/issues)
	"""
	def __init__(self,node_editor_id,min_link_length=100,max_link_length=300) -> int:
		self.editor = node_editor_id
		self.settings = {"max_link_length": max_link_length,"min_link_length": min_link_length}
		return self.editor

	def visualize(self,root):
		#Create Links
		self.createLinks(root)
		#Convert Nodes to dpg
		for link in self.links:
			link.convertNodesToDPG()
		#enforce links

	def createLinks(self,root):
		self.links = [Link(root,child,self.editor) for child in todo]
		for node in (todo := root._children): # im not sure if this works
			self.links.extend(Link(node,child,self.editor) for child in node._children)
			todo.extend(node._children)

	def get_editor_nodes(self) -> list[int]:
		return get_item_children(self.editor)[children_node_index := 1]

def createDPGNode(hdllnode,editor) -> int:
	title = hdllnode.data["title"]
	# description = "\n".join([line for key,line in list(hdllnode.data["data"])]) #idk maybe this will see
	description = "\n".join([line if key != "default" else "" for key, line in list(hdllnode.data["data"])])
	with node(label=title,parent=editor) as dpgNodeId:
		with node_attribute(attribute_type=mvNode_Attr_Static):
			add_text(description)
	return dpgNodeId

if __name__ == "__main__":
	test = RelationalNodeUI(placeholder := 5)