from tkinter import *
from tkinter import ttk, messagebox
import logging
import json
from os import path as os_path

class EditComponentResource(Toplevel):
    """docstring for EditComponentResource."""
    def __init__(self, parent, *args, **kwargs):
        Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.logger = logging.getLogger()
        self.close_window = None

    def config(self,application_name="DanTe", brandpic = None, close_pop_window =  None, width=550, height=410, x_pos=200, y_pos=100, datafile = None):
        self.close_window = close_pop_window
        self.iconphoto(False, brandpic)
        self.title(application_name + " - Edit/Add Component Resource")
        self.geometry(f'{width}x{height}+{x_pos}+{y_pos}')
        self.parent.wm_attributes("-disabled", True)
        self.focus_set()
        self.transient(self.parent)
        self.protocol("WM_DELETE_WINDOW", lambda *args: close_pop_window(self))
        if datafile is None:
            self.datafile = "configfiles\componenet_resourcetype.json"
        else:
            self.datafile = datafile

        self.filename, self.fileext = os_path.splitext(datafile)
        self.data = None
        with open(datafile, "r") as fin:
            if self.fileext == ".json":
                self.data = json.loads(fin.read())
            elif self.fileext == ".txt":
                self.data = fin.read()
        # print(self.data)

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

        component_resource_lframe = LabelFrame(input_frame, text="Component Resource Type")
        component_resource_entry = ttk.Entry(component_resource_lframe)
        component_resource_entry.pack(fill="both", expand="yes")
        component_resource_lframe.pack(fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
        button_frame.pack(fill="x", expand="yes")
        component_save_btn = ttk.Button(button_frame, text="Save")
        component_save_btn.pack(side = RIGHT, padx=5, pady=5, ipadx=5, ipady=5, anchor="e")

        component_delete_btn = ttk.Button(button_frame, text="Delete Selected")
        component_delete_btn.pack(side = RIGHT, padx=5, pady=5, ipadx=5, ipady=5, anchor="e")

        tree_table = ttk.Treeview(treeview_frame, column=("Name", "Resource Type"), show="headings")
        tree_table_scroll_y = ttk.Scrollbar(treeview_frame, orient=VERTICAL, command=tree_table.yview)
        tree_table_scroll_y.pack(side="right", fill="y")
        tree_table_scroll_x = ttk.Scrollbar(treeview_frame, orient=HORIZONTAL, command=tree_table.xview)
        tree_table_scroll_x.pack(side="bottom", fill="x")

        tree_table.config(yscrollcommand=tree_table_scroll_y.set)
        tree_table.config(xscrollcommand=tree_table_scroll_x.set)

        tree_table.pack(fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10, anchor="center")

        tree_table.column("Name", minwidth=200, width=200, anchor='nw')
        tree_table.column("Resource Type", minwidth=200, anchor='nw', stretch="yes")

        tree_table.heading("Name", text="Name")
        tree_table.heading("Resource Type", text="Resource Type")

        if self.data is not None:
            for each in self.data:
                # tree_table.insert("", END, values=(each, self.data.get(each),))
                tree_table.insert("", END, values=(each, self.data.get(each),))

        tree_table.bind("<Double-1>", lambda *args: self.on_select(tree_table, component_name_entry, component_resource_entry))
        component_save_btn.config(command=lambda *args: self.on_save(tree_table, component_name_entry, component_resource_entry))
        component_delete_btn.config(command=lambda *args: self.on_delete(tree_table, component_name_entry, component_resource_entry))

    def on_select(self, tree_table, c_name, c_resource):
        selected = tree_table.selection()[0]
        selected_values = tree_table.item(selected, "values")
        # print(selected_values)
        c_name.delete(0, END)
        c_resource.delete(0, END)
        c_name.insert(0, selected_values[0])
        c_resource.insert(0, selected_values[1])

    def on_save(self, tree_table, c_name, c_resource):
        if self.data is not None:
            comp_name = str(c_name.get()).strip()
            comp_resource_type = str(c_resource.get()).strip()
            added = False
            for key in self.data:
                if key.lower() == comp_name.lower():
                    self.data[key] = comp_resource_type
                    added = True

            if not(added) and bool(comp_name) and bool(comp_resource_type):
                self.data[comp_name.title()] = comp_resource_type
            elif not(bool(comp_name)):
                messagebox.showerror("Failed!!!", "Failed to Save, Empty Component Name", parent=self)
            elif not(bool(comp_resource_type)):
                messagebox.showerror("Failed!!!", "Failed to Save, Empty Component Resourcetype", parent=self)
            else:
                messagebox.showerror("Failed!!!", "Some Error occurred", parent=self)
            
            self.refresh_table(tree_table, self.data)
            with open(self.datafile, "w") as fout:
                json.dump(self.data, fout, indent=4)
        else:
            messagebox.showerror("Failed!!!", "No Data", parent=self)
    
    def on_delete(self, table, c_name, c_resource):
        if self.data is not None:
            comp_name = str(c_name.get()).strip()
            comp_resource_type = str(c_resource.get()).strip()
            if comp_name in self.data:
                self.data.pop(comp_name)
            else:
                messagebox.showerror("Failed!!!", "Invalid item to delete", parent=self)
                
            c_name.delete(0, END)
            c_resource.delete(0, END)

            self.refresh_table(table, self.data)
            with open(self.datafile, "w") as fout:
                json.dump(self.data, fout, indent=4)
        else:
            messagebox.showerror("Failed!!!", "No Data", parent=self)

    def refresh_table(self, table, data):
        table.delete(*table.get_children())
        for each in data:
            table.insert("", END, values=(each, data[each],))
    