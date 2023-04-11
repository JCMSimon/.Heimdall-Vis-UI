import contextlib
from dearpygui.dearpygui import get_item_children,draw_line,get_item_pos,get_item_rect_size,node,node_attribute,mvNode_Attr_Static,add_text
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
		self.link = draw_line(get_item_pos(self.node_1),get_item_pos(self.node_2),color=(0,0,0),parent=self.editor)

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

	def get_editor(self):
		return self.editor

	def visualize(self,root):
		#Create Links
		self.createLinks(root)
		#Convert Nodes to dpg
		for link in self.links:
			link.convertNodesToDPG()
		#enforce links

	def createLinks(self,root):
		self.links = [Link(root,child,self.editor) for child in root._children]
		for node in (todo := root._children): # im not sure if this works
			self.links.extend(Link(node,child,self.editor) for child in node._children)
			todo.extend(node._children)

	def get_editor_nodes(self) -> list[int]:
		return get_item_children(self.editor)[children_node_index := 1]

	def _show_info(self):
		print(f"""
{self.editor}
{self.settings}
{self.get_editor_nodes()}
""")
		with contextlib.suppress(Exception):
			print(self.links)
			for link in self.links:
				print(link.node_1.data)
				print(link.node_2.data)
				print(link.origin)
				print(link.get_length())

	def draw(self):
		for link in self.links:
			link.draw()

def createDPGNode(hdllnode,editor) -> int:
	if not hasattr(hdllnode,"transformedToDPGNode"):
		title = hdllnode.data["title"]
		description = ''.join([value for field in hdllnode.data['data'] for key, value in field.items() if key != dp._internal.is_root_node])
		with node(label=title,parent=editor) as dpgNodeId:
			if description != "":
				with node_attribute(attribute_type=mvNode_Attr_Static):
					add_text(description)
		hdllnode.transformedToDPGNode = True
		return dpgNodeId

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
	testResult2._children.append(testResult3)

	from dearpygui import dearpygui as dpg
	dpg.create_context()
	dpg.create_viewport(title="Hello World", width=640, height=480)
	dpg.setup_dearpygui()
	with dpg.window(label="Example Window") as wnd:
		rng = RelationalNodeUI(dpg.add_node_editor(parent=wnd))
		dpg.add_button(label="info",callback=lambda: rng._show_info())
		dpg.add_button(label="vis",callback=lambda: rng.visualize(root))
		dpg.add_button(label="draw",callback=lambda: rng.draw())
	dpg.set_primary_window(wnd,True)
	dpg.show_viewport()
	dpg.start_dearpygui()