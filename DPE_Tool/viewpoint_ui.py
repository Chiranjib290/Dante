from tkinter import *
from tkinter import ttk, messagebox
import logging
import json

applogger = logging.getLogger()

class ViewpointHeaderEdit(Toplevel):
    """Toplevel for editing the accepted header in Vewpoint metadata clean"""
    def __init__(self, parent, *args, **kwargs):
        Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.close_window = None

    def config(self,application_name="DanTe", brandpic = None, close_pop_window =  None, width=350, height=410, x_pos=200, y_pos=100, datafile = None):
        self.close_window = close_pop_window
        self.iconphoto(False, brandpic)
        self.title(application_name + " - Edit/Add Header")
        self.geometry(f'{width}x{height}+{x_pos}+{y_pos}')
        self.parent.wm_attributes("-disabled", True)
        self.focus_set()
        self.transient(self.parent)
        self.protocol("WM_DELETE_WINDOW", lambda *args: close_pop_window(self))
        if datafile is None:
            self.datafile = "configfiles\header_file.txt"
        else:
            self.datafile = datafile

        with open(datafile, "r") as fin:
            self.data = fin.readlines()

    def main(self):
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

        if self.data is not None:
            for each in self.data:
                # tree_table.insert("", END, values=(each, self.data.get(each),))
                tree_table.insert("", END, values=(each.replace("\n", ""),))

        tree_table.bind("<Double-1>", lambda *args: self.on_select(tree_table, component_name_entry))
        component_save_btn.config(command=lambda *args: self.on_save(tree_table, component_name_entry))
        component_delete_btn.config(command=lambda *args: self.on_delete(tree_table, component_name_entry))

    def on_select(self, tree_table, c_name):
        selected = tree_table.selection()[0]
        selected_values = tree_table.item(selected, "values")
        c_name.delete(0, END)
        c_name.insert(0, selected_values[0])

    def on_save(self, tree_table, c_name):
        if self.data is not None:
            _comp_name = str(c_name.get()).strip()
            comp_name = f"{_comp_name}\n"
            added = False            

            if not(bool(_comp_name)):
                messagebox.showerror("Failed!!!", "Failed to Save, Empty Header Name", parent=self)
            else:
                if comp_name not in self.data:
                    self.data.append(comp_name)
                    added = True
                    c_name.delete(0, END)
                if not added:
                    messagebox.showerror("Warning!!!", "Header already present.", parent=self)

            self.refresh_table(tree_table, self.data)
            with open(self.datafile, "w+") as fout:
                fout.writelines(self.data)
        else:
            messagebox.showerror("Failed!!!", "No Data", parent=self)
    
    def on_delete(self, table, c_name):
        if self.data is not None:
            _comp_name = str(c_name.get()).strip()
            comp_name = f"{_comp_name}\n"

            selected_items = table.selection()
            if bool(selected_items):
                for item in selected_items:
                    selected_values = table.item(item, "values")
                    _comp = f"{selected_values[0]}\n"
                    if _comp in self.data:
                        self.data.remove(_comp)

            # if comp_name in self.data:
            #     self.data.remove(comp_name)
            else:
                messagebox.showerror("Failed!!!", "Invalid item to delete", parent=self)
                
            c_name.delete(0, END)

            self.refresh_table(table, self.data)
            with open(self.datafile, "w+") as fout:
                fout.writelines(self.data)
        else:
            messagebox.showerror("Failed!!!", "No Data", parent=self)

    def refresh_table(self, table, data):
        table.delete(*table.get_children())
        for each in data:
            table.insert("", END, values=(each.replace("\n", "")))
    