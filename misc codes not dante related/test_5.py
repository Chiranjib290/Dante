# coding=utf-8
# from tkinter import *
# from tkinter import ttk
import logging
LOG_FILE = "logs\\test_file.log"
# root = Tk()

# TOTAL_NODE = 0
# CURRENT_NODE = 0
# TOTAL_OPENED = 0

# inputframe = Frame(root)
# inputframe.pack(expand="yes", fill=X)

# ent = Entry(inputframe)
# ent.pack(side="left", fill=X)

# def do_me(node):
#     global TOTAL_NODE
#     if not(tree.item(node, "open")):
#         tree.item(node, open=True)
#         TOTAL_NODE += len(tree.get_children(node))

# def get_total_opened_node(total, node, child_node):
#     global TOTAL_OPENED
#     for child in tree.get_children(node):
#         opened = tree.item(child,"open")
#         if opened:
#             total = get_total_opened_node(total, child, child_node)[0] + 1
#         else:
#             total += 1
#             if child_node == child:
#                 TOTAL_OPENED = TOTAL_OPENED + total
#                 tree.item(node, open=True)
#     return total, TOTAL_OPENED

# def get_node_index(node):
#     t_node_cnt = 0
#     # t_current_total = 0
#     splitted_data = str(node).strip().split("/")
#     for cnt, _ in enumerate(splitted_data):
#         cur_payload = "/".join(splitted_data[:(cnt+1)])
#         parent = tree.parent(cur_payload)
#         cur_payload = "/" if cur_payload == "" else cur_payload
#         # opened_ = tree.item(cur_payload, "open")
#         # print(cur_payload, opened_, sep=" - ")
#         # if not(opened_):
#         #     tree.item(cur_payload, open=True)
#         if parent != "":
#             # t_node_cnt += get_total_opened_node(prev, parent, cur_payload)
#             t_node_cnt = get_node_number(t_node_cnt, parent, cur_payload)
#             print(t_node_cnt)
    
#     return t_node_cnt

# def get_node_number(prev, parent, child):
#     _total = prev
#     for children in tree.get_children(parent):
#         _opened = tree.item(children, "open")
#         if children == child:
#             tree.item(parent, open=True)
#             return _total + 1
#         else:
#             if _opened:
#                 _total = get_node_number(_total, children, None)
#                 _total += 1
#             else:
#                 _total += 1

#     return _total

# def check():
#     global TOTAL_OPENED
#     TOTAL_OPENED = 0
#     data = ent.get()
#     # splitted_data = str(data).strip().split("/")
#     # cur_payload = ""
#     # for cnt, d in enumerate(splitted_data):
#     #     cur_payload = "/".join(splitted_data[:(cnt+1)])
#     #     do_me(cur_payload)
#     total_node = get_node_index(data)
#     # print(total_)
#     print("M %d" % total_node)

# btn = Button(inputframe, text="Check", command=check)
# btn.pack(side="left")

# treeframe = Frame(root)
# treeframe.pack(expand="yes", fill=BOTH)
# tree = ttk.Treeview(treeframe, show="tree")

# scroll_y = ttk.Scrollbar(treeframe, orient=VERTICAL, command=tree.yview)
# scroll_y.pack(side=RIGHT, fill="y")

# tree.config(yscrollcommand=scroll_y.set)

# tree.insert("","end",iid="/", text="/")

# for i in range(1, 10):
#     tree.insert("/","end",iid="/"+str(i), text=str(i))
#     for j in range(1,4):
#         tree.insert("/"+str(i),"end", iid="/"+str(i)+"/"+str(i*j*100), text=str(i*j*100))
#         for k in range(5,9):
#             tree.insert("/"+str(i)+"/"+str(i*j*100),"end", iid="/"+str(i)+"/"+str(i*j*100)+"/"+str(i*k*100), text=str(i*k*100))

# tree.pack(fill="both")
# root.mainloop()



# from viewpoint_metadata_clean import MetaDataClean, METADATA_OPERATION
# # from logging_screen import METADATA_OPERATION

# md = MetaDataClean()
# ipath = "C:/Users/shouvikd256/Desktop/DPE/ViewPoint/MD-12974/aags_July20_2021_IT.xlsx"
# opath = "C:/Users/shouvikd256/Desktop/DPE/ViewPoint/MD-12974"

# st = md.config(ipath, opath)

# # operation = "CSV/Excel with One or More column"
# operation = METADATA_OPERATION["more_sheets"]

# out = md.run(operation)

# # print(METADATA_OPERATION)
# for o in out.get("message",[]):
#     print(o)

# out = {
# 'message': [
# 	{
# 		'Content ID': {
# 					'code': 200,
# 					'message': 'Successfully Generated'
# 					}
# 	},
# 	{
# 		'Guidance Terms': {
# 						'code': 200,
# 						'message': 'Successfully Generated'
# 						}
# 	},
# 	{
# 		'Suggested Guidance': {
# 						'code': 200,
# 						'message': 'Successfully Generated'
# 						}
# 	}
# 	],
# 	'code': 200
# }

# for o in out.get("message"):
#     print(o)

# op = {'Content ID': {'code': 200, 'message': 'Successfully Generated'}}

# for _, values in op.items():
#     print(values)

# import requests
# from dpe_validation import GenericFunctions

# url = "https://dpe-qa.pwc.com/content/pwc/global/referencedata/bannedWords.json"
# authen = ("shouvik.d.das@in.pwc.com","boltaction")

# resp = requests.get(url, auth=authen, timeout = 10)

# print(resp.status_code)

# banned_words = resp.json()["bannedWords"]

# length = len(banned_words)

# print(length)

# mn = GenericFunctions.filter_utf8_chars("OP")
# print(mn)

# from tkinter import *
# from tkinter import ttk
# from dpe_crx_search_ui import PopUpWithTreeViewData

# root = Tk()

# main_label = Label(root, text="")
# main_label.pack()
# # tree = ttk.Treeview(root, show='headings', columns= ("1","2"))
# # tree.pack(fill="both", expand="yes", padx=20, pady=20, anchor = "center")

# # tree.column("1", width=100, stretch=YES)
# # tree.column("2", width=100, stretch=YES)

# # tree.heading("1", text="Property")
# # tree.heading("2", text="Value")

# # tree.tag_configure("tagred", background="#F16980", foreground="white")
# # # tree.tag_configure("tagred", background="red", foreground="white")

# # for i in range(10):
# #     tree.insert("", "end", values = (i+1, ((i+1)*100)), tags=("tagred"))

# # def fetch_tree_data(event):
# #     current = tree.focus()
# #     print(current)
# #     tags = list(tree.item(current, "tags"))
# #     if tags.count("tagred") > 0:
# #         tags.remove("tagred")
# #     print(tags)
# #     tree.item(current, tags=tags)
# #     print(tree.item(current))

# # tree.bind('<ButtonRelease-1>', fetch_tree_data)

# data = [
#     {
#         "action" : "Update",
#         "payload": "/content/pwc/rm/en/shouvik",
#         "property": "jcr:title",
#         "oldvalue" : "old_value",
#         "value" : "prop_new_value",
#     },
#     {
#         "action" : "Removed From CACHE",
#         "payload": "/content/pwc/rm/en/shouvik/prop",
#         "property": "test",
#         "value" : "prop_value",
#     },
#     {
#         "action" : "Paste",
#         "payload": "/content/pwc/rm/en/shouvik/prop",
#         "property": "test2",
#         "value" : "prop_value2",
#     },
#     {
#         "action" : "Added Property",
#         "payload": "/content/pwc/rm/en/shouvik/prop",
#         "property": "test3",
#         "value" : "prop_value3",
#     },
#     {
#         "action" : "Added to CACHE",
#         "payload": "/content/pwc/rm/en/shouvik/prop",
#         "property": "test4",
#         "value" : "prop_value4",
#     }
# ]

# def revert_prop(values):
#     print("Reverted!! " +str(values))
#     main_label.config(text=str(values))

# # PopUpWithTreeViewData(root, data, None,revert_prop)
# mn = ttk.Combobox(root, state="readonly", values=["True", "False"], width=20)
# mn.pack()

# root.mainloop()

# import logging
# from dpeinboxdashboard import DPEInboxDashboard

# logfile = "logs//test_log.log"
logging.basicConfig(handlers=[logging.FileHandler(filename=LOG_FILE, mode='a+', encoding='utf-8')],
                            format='%(asctime)s -> %(name)s -> {%(module)s : %(funcName)s} -> %(lineno)d -> %(levelname)s -> %(message)s', level=logging.DEBUG)

# dpedashboard = DPEInboxDashboard("https://dpe-stg.pwc.com","shouvik.d.das@in.pwc.com","serverdown")
# out = dpedashboard.get_form_data("Ready for processing", report_older=15)
# print(out)



#coding=utf-8
# from tkinter import *
# from tkinter import ttk

# root = Tk()

# root.geometry("300x300+300+300")

# root.resizable(width=False, height=True)

# root.mainloop()

# from update_dpe_prop import UpdateDPEProperties

# up = UpdateDPEProperties("test", "test", "test")
# file = "Files\\Naree_Tag_Update_Append_201021.xlsx"
# data = up.sorted_excel_to_list(file, False, 0)
# print(data)

# from asset_reference import AssetReference

# f = AssetReference()
# f.config("hh", "vv", "None", 4)
# print(f.get_dam_assets("us"))

# from validate_redirect_content_path import ContentPathValidator

# logging.basicConfig(handlers=[logging.FileHandler(filename=LOG_FILE, mode='a+', encoding='utf-8')],
#                             format='%(asctime)s -> %(name)s -> {%(module)s : %(funcName)s} -> %(lineno)d -> %(levelname)s -> %(message)s', level=logging.INFO)
# cpv = ContentPathValidator("shouvik.d.das@in.pwc.com","serverdown")
# content_path = "/content/pwc/rm/en/shouvik/test/test2/test11"
# status = cpv.remove_redirect(content_path, "stage", True)
# print(status)
from asset_reference import AssetReference

ast = AssetReference()
domain="https://dpe-stg.pwc.com"
username = "shouvik.d.das@in.pwc.com"
passwd = "serverdown"

ast.config(domain=domain, username=username, password=passwd)
assets = ast.get_dam_assets(territory='al').get("data",[])

for asset_no in range(0, 4):
    ast.find_asset_reference(assets[asset_no], "")
