import dearpygui.dearpygui as dpg
from random import randint

def main():
	dpg.create_context()
	dpg.create_viewport()
	dpg.setup_dearpygui()
	dpg.show_viewport()
	setup()
	dpg.start_dearpygui()
	exit2()
	pass

def setup():
	with dpg.window(tag="main"):
		dpg.add_button(label="Add Random Node",callback=addrandom)
		dpg.add_button(label="Link 2 random Nodes",callback=linkrandom)
		global editor
		editor = dpg.add_node_editor()
	dpg.set_primary_window("main", True)

def exit2():
	for node in nodes:
		print(f"id: {node}")
		print("pos" + dpg.get_item_pos(str(node)))

def addrandom():
	global editor
	nodeid = dpg.add_node(parent=editor,
	tag=f"testNode{randint(0,99999)}",
	label="random"
	)
	nodes.append(nodeid)
	print("Adding Random Node")


def linkrandom():
	print("Linking 2 random Nodes")



if __name__ == "__main__":
	nodes = []
	print("Testing UI")
	main()
