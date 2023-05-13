from typing import NoReturn
import dearpygui.dearpygui as dpg
import time

dpg.create_context()

with dpg.theme() as transp_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

def drag():
	print("yp")

def create():
	sz = dpg.get_item_rect_size(ne)
	ps = dpg.get_item_pos(ne)
	offset = 8
	x = ps[0] + offset
	y = ps[1] + offset
	with dpg.window(pos=(x,y),width=sz[0],height=sz[1],no_move=True,no_title_bar=True,no_scrollbar=True,no_resize=True,max_size=(sz[0],sz[1]),) as drawWindow:
		dpg.bind_item_theme(dpg.last_item(), transp_theme)
		global drawLayer
		drawLayer = dpg.add_drawlist(width=sz[0],height=sz[1])

		with dpg.item_handler_registry():
			dpg.add_item_clicked_handler(callback=lambda:print("yo"))

	x = ps[0] + (sz[0] / 2)
	y = ps[1] + (sz[1] / 2)

	while True:
		arrow = dpg.draw_arrow((x,y),dpg.get_mouse_pos(),color=(255,0,0),thickness=50,parent=drawLayer)
		time.sleep(0.005)
		dpg.delete_item(arrow)



global wnd
with dpg.window(label="Drawing Test") as wnd:
	global ne
	ne = dpg.add_node_editor(parent=wnd,width=500,height=500)
	dpg.add_button(parent=wnd,label="create",callback=create)

dpg.set_primary_window(wnd,True)
dpg.create_viewport(title='Test', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()