import dearpygui.dearpygui as dpg
from random import randint
import random

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
		editor = dpg.add_node_editor(callback=link_callback)
	dpg.set_primary_window("main", True)

def exit2():
	for node in nodes:
		print(f"id: {node}")
		pos = dpg.get_item_pos(node)
		print(f"id: {pos}")
	# get position of node here and print it.

def addrandom():
	global editor
	# node_master = dpg.get_item_children(editor)[1]
	# pos = [0,0]
	# if node_master:
	# 	for no in node_master:
	# 		pos = dpg.get_item_pos(no)
	# 		pos[0] += 80
	# 		pos[1] += 10

	nodeid = dpg.add_node(parent=editor,
						  tag=f"testNode{randint(0, 99999)}",
						  label=f"testNode{randint(0, 99999)}",
						#   draggable=False,
						  pos=(dpg.get_item_rect_size(editor)[0] / 2,dpg.get_item_rect_size(editor)[1] / 2)
						  )
	nodes.append(nodeid)
	print("Adding Random Node")

def linkrandom():
	global editor
	print("Linking 2 random Nodes")
	if len(nodes) >= 2:
		one = random.choice(nodes)
		two = random.choice(nodes)
		if one == two:
			print("same shit")
			linkrandom()
		dpg.add_node_attribute(label="test",parent=one)
		dpg.add_node_attribute(label="test2",parent=two,attribute_type=dpg.mvNode_Attr_Output)
		print(dpg.get_item_type(one))
		print(dpg.get_item_type(two))
		dpg.add_node_link(one,two,parent=editor)
	else:
		print("not long enogh")
		return

def link_callback(sender, app_data):
    print(app_data,sender)
	# app_data -> (link_id1, link_id2)
    # dpg.add_node_link(app_data[0], app_data[1], parent=sender)


if __name__ == "__main__":
	nodes = []
	print("Testing UI")
	main()
