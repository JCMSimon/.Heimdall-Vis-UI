from typing import NoReturn
import dearpygui.dearpygui as dpg
import time

dpg.create_context()

with dpg.theme() as transp_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

def drag(pos):
	nodeBoxes = {item:(dpg.get_item_pos(item),
[dpg.get_item_pos(item)[0] + dpg.get_item_rect_size(item)[0],
 dpg.get_item_pos(item)[1] + dpg.get_item_rect_size(item)[1]])
 for item in dpg.get_item_children(ne)[1]}
	for key, value in nodeBoxes.items():
		x1, y1 = value[0]
		x2, y2 = value[1]
		box = dpg.draw_rectangle(pmin=value[0],pmax=value[1],parent=drawLayer)
		if x1 <= pos[0] and pos[0] <= x2 and y1 <= pos[1] and pos[1] <= y2:
			print("Mouse position is inside the bounding box of key:", dpg.get_item_label(key))
			item = key
			while dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
				dpg.set_item_pos(item,(dpg.get_mouse_pos()[0] - dpg.get_item_rect_size(item)[0] / 2,dpg.get_mouse_pos()[1] - dpg.get_item_rect_size(item)[1] / 2))
			break


def create():
	sz = dpg.get_item_rect_size(ne)
	ps = dpg.get_item_pos(ne)
	offset = 0
	x = ps[0] + offset
	y = ps[1] + offset
	with dpg.window(pos=(x,y),width=sz[0],height=sz[1],no_move=True,no_title_bar=True,no_scrollbar=True,no_resize=True,max_size=(sz[0],sz[1]),) as drawWindow:
		dpg.bind_item_theme(dpg.last_item(), transp_theme)
		global drawLayer
		drawLayer = dpg.add_drawlist(width=sz[0],height=sz[1],tag="drawlist")
	# x = ps[0] + (sz[0] / 2)
	# y = ps[1] + (sz[1] / 2)
	dragging = False
	while True:
		arrow = dpg.draw_arrow(dpg.get_item_pos(n1),dpg.get_item_pos(n2),color=(255,0,0),thickness=5,parent=drawLayer)
		if dragging:
			if not dpg.is_mouse_button_down(button=dpg.mvMouseButton_Left):
				dragging = False
		if dpg.is_mouse_button_dragging(button=dpg.mvMouseButton_Left,threshold=0.2):
			if dragging:
				if dpg.is_mouse_button_released(button=dpg.mvMouseButton_Left):
					dragging = False
			else:
				pos = dpg.get_mouse_pos()
				drag(pos)
				dragging = True
		time.sleep(0.005)
		dpg.delete_item(arrow)



global wnd
with dpg.window(label="Drawing Test") as wnd:
	global ne
	ne = dpg.add_node_editor(parent=wnd,width=500,height=500)
	global n1,n2
	n1 = dpg.add_node(label="test",parent=ne)
	n2 = dpg.add_node(label="test1",parent=ne)
	dpg.add_button(parent=wnd,label="create",callback=create)

dpg.set_primary_window(wnd,True)
dpg.create_viewport(title='Test', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()