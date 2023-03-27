# problem. not all nodes can have a link in some way cause it odd

from dearpygui.dearpygui import get_item_children,draw_line,get_item_pos

class Settings:
	class link_with_relation:
		min_length = 0
		max_length = 0
		color = "#FFFFFF"
	class link_with_no_relation:
		min_length = 0
		max_length = 0
		color = "#000000"

class Link:
	def __init__(self,origin,node_1,node_2,color,relevant=False) -> None:
		self.color = color
		self.node_1 = node_1
		self.node_2 = node_2

	def change_length(self,delta,origin) -> int:
		# push the most outer node in direction of the line
		# returns the length after changing it
		pass

	def get_length(self) -> int:
		pass

	def draw(self) -> None:
		draw_line(get_item_pos(self.node_1),get_item_pos(self.node_2),color=self.color)

	def get_outer_node(self,origin) -> int:
		# returns the node that is further from the origin
		pass

class RelationalNodeUI:
	"""A Relational UI (Wrapper) specifically made for [Heimdall](https://hdll.jcms.dev) based on the node editor from [dearpygui](https://github.com/hoffstadt/DearPyGui/issues)
	"""
	def __init__(self,node_editor_id,) -> int:
		self.editor = node_editor_id
		return self.editor

	def get_editor_nodes(self) -> list[int]:
		return get_item_children(self.editor)[children_node_index := 1]

	def visualize_tree_data(self,root) -> None:
		"""Heimdall specific"""
		todo = root._children
		while todo:
			for node in todo:
				for datapoint in node.data["data"]: #TODO gotta check the syntax on this!
					print(
						"create a node",
						"create a link to the parrent and make it relevant",
						"set the node to a random position inside 50% of the editor",)
		print("enforce Link rules")

	def create_unrelated_links(self) -> None:
		# create a unrelated link between all nodes
 		pass

	def create_node_from_datapoint(self):
		# create a dpg node from the data
		pass

if __name__ == "__main__":
	test = RelationalNodeUI(placeholder := 5)