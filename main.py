from dearpygui.dearpygui import draw_line,get_item_pos,get_item_rect_size

class Link:
	def __init__(self,node_1,node_2,color) -> None:
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

	def setup(self) -> None:
		self.origin = get_item_pos(self.editor)[0] + get_item_rect_size(self.editor)[0],get_item_pos(self.editor)[1] + get_item_rect_size(self.editor)[1]

	def visualize(self,root):
		pass # idfk


if __name__ == "__main__":
	test = RelationalNodeUI(placeholder := 5)





























# self.data = {
# 			"title":title,
# 			"data":[],
# 			"image":None,
# 		}

	# def get_editor_nodes(self) -> list[int]:
	# 	return get_item_children(self.editor)[children_node_index := 1]

# while self.todo:
# 			for node in self.todo:
# 				for dataField in node.data["data"]: # this might be wrong syntax. it should loop through data fields
# 					for datatype,data in dataField.items():
# 						plugins = self.pluginRegister.getPluginNamesByType(datatype)
# 						results = []
# 						for plugin in plugins:
# 							try:
# 								results.extend(self.pluginRegister.runPlugin(plugin,data))
# 							except (TypeError,IndexError):
# 								self.logger.infoMsg(f"{plugin} returned no results")
# 				node._children.extend(results)
# 				self.todo.extend(results)
# 				self.todo.remove(node)
# 		# Visualize whole Tree
# 		self.nodeInterFace.visualize(self.root)
