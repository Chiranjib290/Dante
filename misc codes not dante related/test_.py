# from tkinter import *

# main = Tk()
# # HEX_COLOR = ""
# main.geometry("300x450+300+100")
# textwizard = Text(main, undo=True)
# textwizard.pack()

# def get_data():
#     textlistbylines = textwizard.get("1.0", END).splitlines()
#     print(textlistbylines)

# btn = Button(main,text="ok", font=("Georgia",14), command=get_data)
# btn.pack(expand="yes")

# CURRENT = 255
# for i in range(400):
#     #rgb(0, 0, 255)
#     last = CURRENT-i
#     last = -(last) if(last < 0 ) else last
#     HEX_COLOR="#%02x%02x%02x" % (153, 0, last)
#     # print(HEX_COLOR)
#     l1 = Frame(main,bg=HEX_COLOR, height=1)
#     l1.place(x=0,y=i,relx=0, rely=0, relwidth=1)
#     # main.update()
# l1 = Label(main,bg="#7be800", text="Testing Background Image")
# l1.pack()
# l1 = Label(main,bg="#408000",text="Hello World",fg="white")
# l1.pack()
# # for co in [HEX_COLOR, "#408000"]:
# #     l1 = Label(main,bg=co)
# #     l1.pack(side="top", fill="x")

# # print(HEX_COLOR)
# main.mainloop()

# from getdatafromdpe import GetDataFromPayload
# from update_dpe_prop import UpdateDPEProperties

# gtp = UpdateDPEProperties("https://dpe-stg.pwc.com","shouvik.d.das@in.pwc.com","reset123")
# # out = gtp.getPropDataURL("/content/usergenerated/content/pwc/rm/en/shouvik/l3landing/2020/9/17/OnlineForm8155/1600340961790_4/1600340961790",
# # "formid, formType, pwcFormReferenceId, pwcFormFieldOrder")
# # print(out)

# # query = input("Enter Query Data: ")
# # prop = input("Enter Prop: ")

# query = input("File Name: ")

# # prop_list = [x.strip() for x in prop.split(",") if x.strip() != ""]
# data = gtp.sorted_excel_to_list(query,0)
# count_of_data = len(data)
# reformed = []
# payload_data = {}
# chunks = {}
# print(data)
# for i in range(count_of_data):
#     if i !=0:
#         if str(data[i-1][0]).strip() == str(data[i][0]).strip():
#             chunks[data[i][1]] = data[i][2]
#         else:
#             print(chunks)
#             chunks = {}
#             chunks[data[i][1]] = data[i][2]
#     else:
#         chunks[data[i][1]] = data[i][2]
# print(chunks)

# path:/content/cq:tags/pwc-gx "jcr:title":'Future in sight' "sling:resourceType":'cq/tagging/components/tag'
# sling:resourceType, jcr:title, cq:lastModified


# op = "+"
# list1 = [
#     [1,2],
#     [2,3],
#     [5,4]
# ]
# def add(a,b):
#     return a+b
# def sub(a,b):
#     return a-b

# def itere(func,l1):
#     for each in l1:
#         print(func(each[0], each[1]))

# if op == "+":
#     itere(add,list1)
# elif op=="-":
#     itere(sub, list1)

# from validate_redirect import RedirectValidation

# bv = RedirectValidation()
# l = bv.excel_to_list("../test_redirect.xlsx")

# # bv.validate_redirect("../test_redirect.xlsx")
# for each in l:
#     print(bv.check_redirect(each[0], each[1]))
# import logging
# from validate_redirect_content_path import ContentPathValidator


# logging.basicConfig(filename="test.log", filemode='a', level=logging.INFO,
#                             format='%(asctime)s - %(name)s - {%(module)s : %(funcName)s} - %(lineno)d - %(levelname)s - %(message)s')
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

# bv = ContentPathValidator()

# from cryptography.fernet import Fernet as CRISP

# ENCRYPTION_KEY = b'OajUImTpdXWDXrBS_WYffcVzZtxJxds1lrc0cF2YscE='

# def encrypt_passwd(passwd):
    
#     crispy = CRISP(ENCRYPTION_KEY)
#     if not(isinstance(passwd, bytes)):
#         encoded_passwd = passwd.encode()
#     else:
#         encoded_passwd = passwd
#     encrypted_passwd = crispy.encrypt(encoded_passwd)

#     return encrypted_passwd.decode()

# def decrypt_passwd(encrypted_passwd):
        
#     crispy = CRISP(ENCRYPTION_KEY)
#     if not(isinstance(encrypted_passwd, bytes)):
#         encoded_passwd = encrypted_passwd.encode()
#     else:
#         encoded_passwd = encrypted_passwd
#     # encoded_passwd = encrypted_passwd.encode()
#     decrypted_passwd = crispy.decrypt(encoded_passwd)

#     return decrypted_passwd.decode()


# # INVALID_PATH_STRING = "/, /content, /var, /var/workflow, /apps/pwc, /bin, /etc"

# # encrypted = encrypt_passwd(INVALID_PATH_STRING)
# # print(encrypted)

# # print(decrypt_passwd(encrypted))

# with open("configfiles\\test.info") as fin:
#     data = fin.read()

# if data:
#     print("Pikachu: "+str(data))
# else:
#     print("Hello")


# from tkinter import *
# from tkinter import ttk
# from time import sleep
# import threading

# main = Tk()

# def update():
#     current_pos = 0
#     frac = (1/149)
#     for i in range(1,151):
#         updated_data = ("Pikachu - "+str(i),"Dinda - 0",)
#         data_tree.item(i, text=str(i), values=tuple(updated_data))
#         if i > 3:
#             current_pos = current_pos + frac
#         data_tree.yview_moveto(current_pos)
#         main.update()
#         sleep(0.8)

# def startThread():
#     t0 = threading.Thread(target=update)
#     t0.start()

# # # HEX_COLOR = ""
# main.geometry("400x450+300+100")
# btn_frame = Frame(main)
# btn_frame.pack()
# btn_main = Button(btn_frame, text="Submit", command=startThread)
# btn_main.pack()

# data_tree_frame = Frame(main)

# data_tree = ttk.Treeview(
#     data_tree_frame, show="headings", columns=(), selectmode="extended", height=5)

# data_tree_scroll_y = ttk.Scrollbar(
#     data_tree_frame, orient="vertical", command=data_tree.yview)
# data_tree.config(yscrollcommand=data_tree_scroll_y.set)
# data_tree_scroll_y.pack(side="right", fill="y")

# data_tree_scroll_x = ttk.Scrollbar(
#     data_tree_frame, orient="horizontal", command=data_tree.xview)
# data_tree.config(xscrollcommand=data_tree_scroll_x.set)
# data_tree_scroll_x.pack(side="bottom", fill="x")

# data_tree.pack(fill="both", expand="yes")

# data_tree_frame.pack(
#     fill="both", expand="yes", padx=5, pady=5)

# data_tree["columns"] = ("1", "2")

# each_col_width = 100

# data_tree.column(
#                     "1", width=each_col_width*2, stretch="yes")
# data_tree.column(
#     "2", width=each_col_width, stretch="yes", anchor="c")

# data_tree.heading("1", text="Payload")
# data_tree.heading("2", text="Property")
# main.update()

# for i in range(150):
#     _values = (str(i),"Dinda - "+str(i),)
#     data_tree.insert("", "end", iid=i+1, text=str(i+1), values=_values)

# main.mainloop()


# def sorted_excel(excelfile):
#     wb = xlrd.open_workbook(excelfile)
#     op_sheet = wb.sheet_by_index(0)
#     num_rows = op_sheet.nrows
#     num_cols = op_sheet.ncols
#     output_data = []
#     for row_num in range(1,num_rows):
#         init_row = None
#         value_type = op_sheet.cell_value(row_num,num_cols-1)
#         if value_type.lower().strip() == "multi":
#             value = op_sheet.cell_value(row_num,num_cols-2)
#             splitted_value = [x.strip() for x in value.split(",") if x.strip() != '']
#             if num_cols == 5:
#                 old_value = op_sheet.cell_value(row_num,2)
#                 splitted_old_value = [x.strip() for x in old_value.split(",") if x.strip() != '']
#                 init_row = [op_sheet.cell_value(row_num,0),op_sheet.cell_value(row_num,1),splitted_old_value, splitted_value]
#             elif num_cols == 4:
#                 init_row = [op_sheet.cell_value(row_num,0),op_sheet.cell_value(row_num,1), splitted_value]
#             else:
#                 init_row = []
#         else:
#             init_row = op_sheet.row_values(row_num)
#             init_row = init_row[:-1]
#         output_data.append(init_row)

#     return output_data
    
    
    #output_data = [sheet.row_values(i) for i in range(sheet.nrows)]

# from tkinter import *
# from logging_screen import LoggingScreen
# from dpe_bulk_workflow_manager import RunWorkflow
# from datetime import datetime
# import logging
# import json


# mainwindow = Tk()

# logging.basicConfig(filename="logs\\test_log_file.log", filemode='a', level=logging.DEBUG,
#                             format='%(asctime)s -> %(name)s -> {%(module)s : %(funcName)s} -> %(lineno)d -> %(levelname)s -> %(message)s')

# # logfile = "logs\\mainlogfile_" + datetime.now().strftime("%m%d%Y") + ".log"
# logfile = "logs\\mainlogfile_01182021.log"

# # h = LoggingScreen(mainwindow,"DANTE","logo/logo.png", logfile)

# # f = StringVar()
# # f.set(0.0)

# generate_report_modal = Toplevel(mainwindow)
# mainwindow.wm_attributes("-disabled", True)
# generate_report_modal.focus_set()
# generate_report_modal.title(
#     "Enter Details")
# generate_report_modal.geometry("300x400+500+30")
# generate_report_modal.resizable(False, False)
# generate_report_modal.transient(mainwindow)

# # generate_report_modal.overrideredirect(True)

# varuserent = StringVar()
# varpassent = StringVar()
# varipdata = StringVar()

# def generate_report(uname, passwd, ip):
#     bn = RunWorkflow(ip, uname, passwd)
#     out = bn.sync_wf_models()
#     if isinstance(out,dict):
#         with open("configfiles\\wf_models_test.json", "w") as f:
#             json.dump(out, f, indent=4)
#     else:
#         if out == 401:
#             pass
#         else:
#             pass
        

# generate_report_modal.main_frame = Frame(
#     generate_report_modal)
# generate_report_modal.main_frame.pack(
#     side="top", fill="both", expand="yes")

# generate_report_modal.button_frame = Frame(
#     generate_report_modal)
# generate_report_modal.button_frame.pack(
#     side="bottom", fill="both", expand="yes")

# # Username
# generate_report_modal.username_labelframe = LabelFrame(
#     generate_report_modal, text="DPE Username")
# generate_report_modal.username_labelframe.pack(
#     fill="both", expand="yes", padx=10, pady=5, ipadx=5, ipady=5, anchor=CENTER)

# generate_report_modal.username_entry = Entry(
#     generate_report_modal.username_labelframe, textvariable=varuserent)
# generate_report_modal.username_entry.pack(
#     fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

# # Password
# generate_report_modal.password_labelframe = LabelFrame(
#     generate_report_modal, text="DPE Password")
# generate_report_modal.password_labelframe.pack(
#     fill="both", expand="yes", padx=10, pady=5, ipadx=5, ipady=5, anchor=CENTER)

# generate_report_modal.password_entry = Entry(
#     generate_report_modal.password_labelframe, show="*", textvariable=varpassent)
# generate_report_modal.password_entry.pack(
#     fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

# # Environment
# generate_report_modal.environment_labelframe = LabelFrame(
#     generate_report_modal, text="DPE Password")
# generate_report_modal.environment_labelframe.pack(
#     fill="both", expand="yes", padx=10, pady=5, ipadx=5, ipady=5, anchor=CENTER)

# generate_report_modal.ipent = Entry(
#     generate_report_modal.environment_labelframe, textvariable=varipdata)
# generate_report_modal.ipent.pack(fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

# generate_report_modal.button_submit = Button(
#     generate_report_modal.button_frame, text="Submit", command=lambda *args: generate_report(varuserent.get(),varpassent.get(), varipdata.get()))
# generate_report_modal.button_submit.pack(
#     expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

# # f.trace("w",lambda *args: validate(f))

# # def validate(sdt):
# #     dt = sdt.get()
# #     if dt.strip() != "":
# #         if dt[-1] == ".":
# #             if dt.count(".") > 1:
# #                 print("Here")
# #                 sdt.set(dt[:-1])
# #         elif not(dt[-1].isnumeric() or dt[-1] == "."):
# #             sdt.set(dt[:-1])
            
# # def getValue():
# #     try:
# #         print(f.get())
# #     except:
# #         print(0)

# # b = Button(mainwindow,text="Click", command=getValue)
# # b.pack()



# mainwindow.mainloop()

# from predefined_dpe_reports import PreDefinedReports

# pd = PreDefinedReports("https://dpe-stg.pwc.com","shouvik.d.das@in.pwc.com","reset123")

# # pd.territory_published_page_report("rm","cq:tags, jcr:content/jcr:title, activatedInPublish")
# out = pd.global_arch_contact_form_territory("lv","2021","0","sendEmailTo,queryDetails, querysubject,pwcFormUrl,email")
# print(out)

from dpeinboxdashboard import DPEInboxDashboard
from clearstuckform import ClearStuckForm

# d = DPEInboxDashboard("https://dpe-stg.pwc.com","s","d")
# p = d.get_form_data("Ready for processing")
# d = ClearStuckForm("https://dpe-stg.pwc.com","shouvik.d.das@in.pwc.com","reset123")
# # uri = "/content/usergenerated/content/pwc/rm/en/shouvik/l3landing/2021/2/26/OnlineForm8155/1614314219315_2/1614314219315"
# # p = d.check_form_router(uri, "stage")
# p = d.retrievedata('2019-06-01','2019-07-29','',["Ready for processing"])

# print(p)

import requests
import calendar
import time

# url = 'https://dpe-stg.pwc.com/libs/cq/workflow/content/inbox/list.json?_dc=1614449847630&filter-itemType=workitem&filter-model=%2Fvar%2Fworkflow%2Fmodels%2Fpwc-form-submission-mx-lookup-check-v2&filter-step=node6'

# authen = ("shouvik.d.das@in.pwc.com","reset123")

# p = requests.get(url, auth=authen, timeout = 10)

# # print(p.json())

lowerbound = '2021-1-19'
upperbound = '2021-1-21'

# lowerbound_in_sec = int(calendar.timegm(time.strptime(lowerbound, '%Y-%m-%d')) * 1000)
# upperbound_in_sec = int(calendar.timegm(time.strptime(upperbound, '%Y-%m-%d')) * 1000)
# print("Lo :"+str(lowerbound_in_sec))
# print("Up :"+str(upperbound_in_sec))

# for each_data in p.json()["items"]:
#     print(each_data["startTime"])
#     if each_data["startTime"] > lowerbound_in_sec and each_data["startTime"] < upperbound_in_sec:
#         print(each_data["item"])
#         print(each_data["payload"])
#         print(each_data["payloadSummary"]["description"])
    # print(each_data["startTime"])
    # print(type(each_data["startTime"]))
    # print(each_data)

# from clearDPEInboxItems import ClearDPEInboxItems

# p = ClearDPEInboxItems("Mx Lookup","https://dpe-stg.pwc.com","shouvik.d.das@in.pwc.com","reset123")

# d = p.retrieve_list("mx lookup", lowerbound, upperbound)

# print(d)

# class Application(tk.Frame):
#     def __init__(self, root):
#         self.root = root
#         self.upperbounddate = None
#         self.initialize_user_interface()
#         screen_width = self.root.winfo_screenwidth()
#         screen_height = self.root.winfo_screenheight()
#         print(screen_width, screen_height, sep=" ")
#         self.root.protocol(
#             "WM_DELETE_WINDOW", lambda *args: self.close_this_window()
#         )
#         self.terminate_thread = False
 
#     def initialize_user_interface(self):
#         # Configure the root object for the Application
#         self.root.title("Application")
#         # self.root.grid_rowconfigure(0, weight=1)
#         # self.root.grid_columnconfigure(0, weight=1)
#         self.root.config(background="green")
#         self.root.maxsize(440,500)
#         self.root.minsize(240,300)
 
#         # Define the different GUI widgets
#         self.name_label = tk.Label(self.root, text="Name:")
#         self.name_entry = tk.Entry(self.root)
#         self.name_label.grid(row=0, column=0, sticky=tk.W)
#         self.name_entry.grid(row=0, column=1)
 
#         self.idnumber_label = tk.Label(self.root, text="ID")
#         self.idnumber_entry = tk.Entry(self.root)
#         self.idnumber_label.grid(row=1, column=0, sticky=tk.W)
#         self.idnumber_entry.grid(row=1, column=1)
 
#         self.submit_button = tk.Button(self.root, text="Insert", command=self.insert_data)
#         self.submit_button.grid(row=2, column=1, sticky=tk.W)
 
#         self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
#         self.exit_button.grid(row=0, column=3)

#         self.select_button = tk.Button(self.root, text="Select", command=self.select_all)
#         self.select_button.grid(row=0, column=4)

#         self.select_none_button = tk.Button(self.root, text="Select None", command=self.select_remove)
#         self.select_none_button.grid(row=1, column=4)

#         self.print_button = tk.Button(self.root, text="Print", command=self.print_selected)
#         self.print_button.grid(row=2, column=4)
#         self.print_button = tk.Button(self.root, text="Change", command=self.change_data)
#         self.print_button.grid(row=2, column=2)
#         self.cal_button = tk.Button(self.root, text="Cal", command=self.selectUpperBound)
#         self.cal_button.grid(row=3, column=2)
        
        
#         # Set the treeview
#         self.tree = ttk.Treeview(self.root, columns=('Name', 'ID'))
 
#         # Set the heading (Attribute Names)
#         self.tree.heading('#0', text='Item')
#         self.tree.heading('#1', text='Name')
#         self.tree.heading('#2', text='ID')
 
#         # Specify attributes of the columns (We want to stretch it!)
#         self.tree.column('#0', stretch=tk.YES)
#         self.tree.column('#1', stretch=tk.YES)
#         self.tree.column('#2', stretch=tk.YES)
 
#         self.tree.grid(row=4, columnspan=4, sticky='nsew')
#         self.treeview = self.tree
 
#         self.id = 0
#         self.iid = 1
 
#     def insert_data(self):
#         _values = [(1,2),(1,4)]
#         # self.treeview.insert('', 'end',
#         #                      values=_values)
#         self.treeview.insert('', 'end', iid=self.iid, text="Item_" + str(self.id),
#                              values=("Name: " + self.name_entry.get(),
#                                      self.idnumber_entry.get()))
#         self.iid = self.iid + 1
#         self.id = self.id + 1

#     def select_all(self):
#         self.treeview.selection_set(self.treeview.get_children())

#     def select_remove(self):
#         self.treeview.selection_remove(self.treeview.get_children())

#     def print_selected(self):
#         p = [9,8,3]
#         items = self.treeview.selection()

#         for item in items:
#             print(item)
#             print(self.tree.item(item)["values"])

#             # print(p[int(item)])

#     def selectUpperBound(self):
#         def setupperbound():
#             self.upperbounddate.set(cal.selection_get())
#             caltop.destroy()

#         btn_x = 200
#         btn_y = 200

#         caltop = tk.Toplevel(self.root)
#         caltop.geometry("300x300+{}+{}".format(btn_x, btn_y))
#         # caltop.attributes("-topmost", "true")
#         caltop.transient(self.root)
#         caltop.attributes("-topmost", True)
#         caltop.overrideredirect(True)
#         t_day = datetime.now().day
#         t_month = datetime.now().month
#         t_year = datetime.now().year
#         cal = Calendar(
#             caltop,
#             font="Georgia",
#             selectmode="day",
#             cursor="arrow",
#             year=t_year,
#             month=t_month,
#             day=t_day,
#         )
#         cal.pack(fill="both", expand="yes")
#         tk.Button(caltop, width=10, text="Ok", command=setupperbound).pack()
#         tk.Button(caltop, text="Cancel", width=10, command=lambda *args: caltop.destroy()).pack()

#     def change_data(self):
#         # print(self.treeview.get_children())
#         update_thread = threading.Thread(target=self.indeterminate_prog)
#         update_thread.start()

#     def update_data(self):
#         for i in range(50):
#             if self.terminate_thread:
#                 break
#             else:
#                 print(i)
#                 sleep(0.5)

#     def indeterminate_prog(self):
#         while not(self.terminate_thread):
#             self.prog = ttk.Progressbar(self.root, orient="horizontal",
#                             mode="indeterminate")
#             self.prog.grid(row=5, columnspan=4, sticky='nsew')
#             self.prog.start(50)
    
#     def close_this_window(self):
#         self.terminate_thread = True
#         print(self.terminate_thread)
#         self.root.destroy()
 
# app = Application(tk.Tk())
# app.root.mainloop()

# from update_dpe_prop import UpdateDPEProperties
# from dpe_validation import GenericFunctions

# # op = UpdateDPEProperties("1", "2", "3")
# # file = "Files\\DPE_Bulk_Update_set_Old_Val.xlsx"

# # out = op.reform_data(file, 1)

# # print(out)
# inp = "///OPko/pl"

# print(GenericFunctions.generate_five_years_past())
# import tkinter as tk
# import tkinter.ttk as ttk
# from tkcalendar import Calendar
# from datetime import datetime
# import threading
# from time import sleep
# from PIL import ImageTk, Image

# changeme = False

# root = tk.Tk()
# root.geometry("300x300")
# brand_pic_file = "logo//logo.png"

# def fetch():
#     pass
        


# button1 = tk.Button(root, text="Fetch", command= fetch)
# button1.pack()

# # progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, mode="indeterminate")
# # progress_bar.pack(fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")
# def open_popup():
#     global root
#     popup = tk.Toplevel(root)
#     # brand_pic_f = tk.PhotoImage(file=brand_pic_file)
#     img_o = Image.open(brand_pic_file)
#     img_c = img_o.resize((20,20))
#     brand_pic = ImageTk.PhotoImage(img_c)
#     def reopenroot(r):
#         global changeme
#         popup.destroy()
#         changeme = True

#     def fetch_1():
#         # tree.selection_remove(tree.selection())
#         # print(tree.get_children('1200'))
#         print(tree.focus())

#     popup.protocol(
#             "WM_DELETE_WINDOW", lambda root=root: reopenroot(root)
#         )

#     popup.geometry("700x700")
#     button_1 = tk.Button(popup, text="Fetch", command= fetch_1)
#     button_1.pack()
#     frame1 = tk.Frame(popup)
#     frame1.pack()
#     # Set the treeview
    
#     tree = ttk.Treeview(frame1, columns=('#1', '#2'), height=15)

    
#     # Specify attributes of the columns (We want to stretch it!)
#     tree.column('#0', stretch=tk.YES, width=30)
#     tree.column('#1', stretch=tk.YES, width=150)
#     tree.column('#2', stretch=tk.YES, width=200)

#     # Set the heading (Attribute Names)
#     tree.heading('#0', text='Item')
#     tree.heading('#1', text='Name')
#     tree.heading('#2', text='ID')


#     tree_scroll = ttk.Scrollbar(
#             frame1, orient="vertical", command=tree.yview)
#     tree.config(yscrollcommand=tree_scroll.set)
#     tree_scroll.pack(side="right", fill="both")
#     def getDataandCopy(e):
#         root.clipboard_clear()  # clear clipboard contents
#         for i in tree.selection():
#             item = tree.item(i)
#             values = item["values"]
#             root.clipboard_append("\t".join(values))
#             # append new value to clipbaord
#             root.clipboard_append("\n")
            
#     tree.pack(expand="yes", fill="both")
#     tree.bind("<<Copy>>", getDataandCopy)
#     tree.bind('<Control-a>', lambda *args: tree.selection_set(tree.get_children()))
#     tree.bind('<Control-z>', lambda *args: tree.selection_remove(tree.selection()))
#     tree.bind('<Control-b>', lambda *args: print(tree["columns"]))
#     tree.bind('<ButtonRelease-1>', lambda *args: fetch_1())

#     drove = ["/content/"+str(x) for x in range(30)]
#     # thread_status = []
#     print(drove)
#     def dv(data):
#         # global drove
#         # global brand_pic
#         # print(brand_pic)
#         try:
#             for _dv in data:
#                 if not(changeme):
#                     tree.insert("", "end", image=brand_pic, iid=str(_dv)+"/1", values = (_dv, _dv, ))
#                     drove.remove(_dv)
#                     popup.update()
#                     # print(drove)
#                     time.sleep(1)
#                 else:
#                     print("Closed!!?")
#         except:
#             print("Closed!!")
            
#         if not(bool(drove)):
#             print("Finished")
#         else:
#             print(drove)

#     urls = []
#     max_val = len(drove)//6
#     for i in range(6):
#         chunks = []
#         for y in range(max_val):
#             chunks.append(drove[(max_val*i) + y])
#         urls.append(chunks)
#     threads = []

#     for j in range(6):
#         t0 = threading.Thread(target=dv, args=(urls[j],))
#         t0.daemon = True
#         t0.start()
#         threads.append(t0)


# button1 = tk.Button(root, text="Open popup", command=open_popup)
# button1.pack()
# root.mainloop()

# 0,1,2,3,..... 24
# 25,26,27..... 49
#https://dpe-stg.pwc.com/etc/importers/bulkeditor/query.json?query=path%3A%2Fcontent%2Fusergenerated%2Farchive%2Fcontent%2Fpwc%2Fglobal%2Fforms%2FcontactUsForm%2F2020%2F3%20territory%3Abe&tidy=true&cols=territory&_dc=1617523265615

# from predefined_dpe_reports import PreDefinedReports
# from urllib.parse import quote, unquote

# pd = PreDefinedReports("https://dpe-stg.pwc.com","shouvik.d.das@in.pwc.com","reset123")

# # out = pd.user_defined_report("type=cq:Page",["1","3","5"],"Query Builder")
# # out = pd.user_defined_report("type:Page",["1","3","5"],"Bulk Editor")

# # m = unquote("https://dpe-stg.pwc.com/etc/importers/bulkeditor/query.json?query=path%3A%2Fcontent%2Fusergenerated%2Farchive%2Fcontent%2Fpwc%2Fglobal%2Fforms%2FcontactUsForm%2F2020%20territory%3Abe&tidy=true&cols=territory&_dc=1617523265615")

# # print(out)
# # print(m)

# # query = "p.limit=-1&path=%2Fcontent%2Fpwc%2Frm%2Fen%2Fshouvik&path.flat=true&type=cq%3aPage"
# # query1 = "path:/content/usergenerated/archive/content/pwc/global/forms/contactUsForm/2020/3 territory:be"
# # out = pd.user_defined_report(query1,["territory","formType","sling:resourcetype"],"Bulk Editor")
# # out = pd.user_defined_report(query,["jcr:content/jcr:title","jcr:content/activatedInPublish","jcr:content/content-free-1-7a70-par/startlongform/eventStartDate"],"Query Builder")

# # print(out)
# pathvar = "%2Fcontent%2Fpwc%2Frm%2Fen%2Fshouvik"
# typevar = "cq%Page"
# # query = "p.limit=-1&path=/content/pwc/rm&path.flat=true&type={type1var}"

# # print(query.format(pathvar=pathvar))
# l = [pathvar, typevar]
# import re
# from dpe_validation import GenericFunctions

# query = "path:/content/pwc/rm \"sling:re\":'/pwc/comp' type:{typevar}"
# # pat = "\{\w+\}"
# # m = re.findall(pat, query) 
# # print(m)
# # out = query
# # # print(out)
# # # p = 'pathvar=pathvar, type1var=typevar'
# # for i, each in enumerate(m):
# #     out = out.replace(each,l[i])

# # print(out)
# query_s = query.split(" ")
# out = GenericFunctions.validate_query(query_s, "bulk editor", ["/content/pwc"])

# print("Final %s" % out)


# from validate_redirect_content_path import ContentPathValidator

# mn = ContentPathValidator("uname", "passwd")

# print(mn.path_selector("stage", False))

from tkinter import *

main = Tk()

ent = Entry(main)
ent.pack()

ent.insert(0, "Shouvik")

main.mainloop()