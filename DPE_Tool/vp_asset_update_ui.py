from tkinter import *
from tkinter import ttk, messagebox
import logging
# import ctypes

# ctypes.windll.shcore.SetProcessDpiAwareness(2)

applogger = logging.getLogger()
applogger.setLevel(logging.DEBUG)

class ViewpointAssetUpdate(Toplevel):
    """Toplevel for editing the accepted header in Vewpoint metadata clean"""
    def __init__(self, parent, *args, **kwargs):
        try:
            Toplevel.__init__(self, parent, *args, **kwargs)
            self.parent = parent
            self.close_window = None
        except:
            applogger.error("Below Exception has occurred.\n", exc_info=True)

    def config(self, application_name="D&P Tool", brandpic = None, close_pop_window =  None, width=350, height=410, x_pos=200, y_pos=100):
        try:
            if close_pop_window is None:
                raise ValueError("Please provide close_pop_window method.")
            self.close_window = close_pop_window
            
            if brandpic: self.iconphoto(False, brandpic)
            self.title(application_name + " - Asset Update")
            self.geometry(f'{width}x{height}+{x_pos}+{y_pos}')
            self.state('zoomed')
            # self.overrideredirect(1)
            self.parent.wm_attributes("-disabled", True)
            self.focus_set()
            # self.transient(self.parent)
            self.protocol("WM_DELETE_WINDOW", lambda *args: close_pop_window(self, self.parent))
            self.main()
        except:
            applogger.error("Below Exception has occurred.\n", exc_info=True)

    def main(self):
        try:
            main_frame = Frame(self)
            main_frame.pack(fill="both", expand="yes")

            input_frame = Frame(main_frame)
            button_frame = Frame(input_frame)
            treeview_frame = Frame(main_frame)

            input_frame.pack(fill="x", expand="yes")
            treeview_frame.pack(fill="both", expand="yes")

            component_name_lframe = LabelFrame(input_frame, text="Component Name")
            component_name_entry = ttk.Entry(component_name_lframe)
            component_name_entry.pack(fill="both", expand="yes")
            component_name_lframe.pack(fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            # component_resource_lframe = LabelFrame(input_frame, text="Component Resource Type")
            # component_resource_entry = ttk.Entry(component_resource_lframe)
            # component_resource_entry.pack(fill="both", expand="yes")
            # component_resource_lframe.pack(fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
            button_frame.pack(fill="x", expand="yes")
            component_save_btn = ttk.Button(button_frame, text="Save")
            component_save_btn.pack(side = RIGHT, padx=5, pady=5, ipadx=5, ipady=5, anchor="e")

            component_delete_btn = ttk.Button(button_frame, text="Delete")
            component_delete_btn.pack(side = RIGHT, padx=5, pady=5, ipadx=5, ipady=5, anchor="e")

            tree_table = ttk.Treeview(treeview_frame, column=("Header Name", ), show="headings")
            tree_table_scroll_y = ttk.Scrollbar(treeview_frame, orient=VERTICAL, command=tree_table.yview)
            tree_table_scroll_y.pack(side="right", fill="y")
            tree_table_scroll_x = ttk.Scrollbar(treeview_frame, orient=HORIZONTAL, command=tree_table.xview)
            tree_table_scroll_x.pack(side="bottom", fill="x")

            tree_table.config(yscrollcommand=tree_table_scroll_y.set)
            tree_table.config(xscrollcommand=tree_table_scroll_x.set)

            tree_table.pack(fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10, anchor="center")

            tree_table.column("Header Name", minwidth=200, anchor='nw', stretch="yes")

            tree_table.heading("Header Name", text="Header Name")
        except:
            applogger.error("Below Exception has occurred.\n", exc_info=True)

    def refresh_table(self, table, data):
        try:
            table.delete(*table.get_children())
            for each in data:
                table.insert("", END, values=(each.replace("\n", "")))
        except:
            applogger.error("Below Exception has occurred.\n", exc_info=True)