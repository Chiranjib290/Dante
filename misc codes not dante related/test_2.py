# from dpe_validation import GenericFunctions

# VERSION_INFO = GenericFunctions.read_yaml_file("version_info.yml")
# print(VERSION_INFO)
# version_info_details = f'''App Version: {VERSION_INFO.get("Version", "X.X.X")}
# Creator: Shouvik Das, Senior Associate of PwC India Pvt.Ltd.
# Created Date: {VERSION_INFO.get("CreatedDate", "10-10-2020")}\nLast Updated'''

# print(version_info_details)

from tkinter import *
from tkinter import ttk
from ui_component import EditComponentResource
from viewpoint_ui import ViewpointHeaderEdit

app = Tk()
style = ttk.Style()
style.configure("nodetree.Treeview", indent=2, font=("Georgia", 10, "normal"), )
# tree = ttk.Treeview(app, selectmode="browse", show="tree", height=5, style = "nodetree.Treeview")

# tree.column("#0", minwidth=10, anchor='w')
# # tree.insert("", "end", iid="1", values=(1, "ER", "BN", "GHHHH"))
# tree.insert(parent="", index=1, iid=1, text="This is",)
# tree.insert(parent="1", index=2, iid=2, text="This is 2",)
# tree.insert(parent="2", index=3, iid=3, text="This is 3",)
# tree.pack(fill="both", anchor="c")

# frame1 = Frame(app, height=300)
# frame1.pack(fill="both", expand="yes")
# frame2 = Frame(app, height=400)
# frame2.pack(fill="both", expand="yes")
import os
import json

BASE_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BRAND_PIC_FILE = os.path.join(BASE_SCRIPT_PATH, "logo", "logo.png")
DATA_FILE = os.path.join(BASE_SCRIPT_PATH, "configfiles", "componenet_resourcetype.json")
DATA_FILE2 = os.path.join(BASE_SCRIPT_PATH, "configfiles", "componenet_resourcetype2.json")
DATA_FILE3 = os.path.join(BASE_SCRIPT_PATH, "configfiles", "header_file2.txt")

def close_pop_window(popup):
    try:
        app.focus_set()
        app.wm_attributes("-disabled", False)
        popup.destroy()
    except Exception as e:
        print(e)
brandpic = PhotoImage(file=BRAND_PIC_FILE)
bn = ViewpointHeaderEdit(app)
bn.config(application_name = "DanTe", brandpic=brandpic, close_pop_window=close_pop_window, datafile=DATA_FILE3)
bn.main()
app.resource_type_data = bn.data
print(app.resource_type_data)
app.wait_window(bn)
app.resource_type_data = bn.data
print(app.resource_type_data)
# def resize_window(label, *args, **kwargs):
#     event  =args[0]
#     width = event.width
#     label.configure(wraplength = width-10)

# app.state("zoomed")
# l1 = ttk.Label(app, text="Welcome to DPE Automation Tool.", font=("Georgia", 50))
# l1.grid(row=0, column = 0, padx=10, ipadx=10, pady=10, ipady=10)

# l2_text = "This tool is used for reporting, bulk updates and other important work related to DPE."+\
#     "The most use is for reporting which is based on Query Debugger."

# l2 = ttk.Label(app, text=l2_text, font=("Georgia", 22))
# l2.grid(row=1, column = 0, padx=10, ipadx=10, pady=10, ipady=10)

# app.grid_columnconfigure(0, weight=1)

# l1.bind("<Configure>", lambda *args: resize_window(l1, *args))
# l2.bind("<Configure>", lambda *args: resize_window(l2, *args))
app.mainloop()