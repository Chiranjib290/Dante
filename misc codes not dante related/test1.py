# coding=utf-8
from tkinter import *
from tkinter import ttk, PhotoImage, messagebox, filedialog
import tkinter.font as tkFont
import logging
from datetime import datetime
from dpe_bulk_workflow_manager import RunWorkflow
from PIL import Image, ImageTk
import webbrowser
import os
import xlsxwriter
import threading
from time import sleep
import sys
from editconfig import EditConfig
from dpe_validation import GenericFunctions


SCREEN_WIDTH = 1320
SCREEN_HEIGHT = 768
ADMIN_USERS = ['shouvik.d.das@in.pwc.com', 'shouvik.d.das@pwc.com',
               'maidul.haque@in.pwc.com', 'maidul.haque@pwc.com',
               'chiranjib.bhattacharyya@pwc.com','chiranjib.bhattacharyya@in.pwc.com']
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
else:
    BASE_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
BRAND_PIC_FILE = os.path.join(BASE_SCRIPT_PATH, "logo", "logo.png")
BASIC_CONFIG_FILE = os.path.join(
    BASE_SCRIPT_PATH, "configfiles", "basicconfig.json")
WF_MODEL_FILE = os.path.join(
    BASE_SCRIPT_PATH, "configfiles", "wf_models.json")
CONFIG_FILE = os.path.join(BASE_SCRIPT_PATH, "configfiles", "config.json")
OPERATION_CODE_FILE = os.path.join(
    BASE_SCRIPT_PATH, "configfiles", "operationcode.json")
TERRITORY_FILE = os.path.join(
    BASE_SCRIPT_PATH, "configfiles", "all_territories.xlsx")
FORBIDDEN_PATH_FILE = os.path.join(
    BASE_SCRIPT_PATH, "configfiles", "forbidden_path.info")
USER_DEF_FILE = os.path.join(
    BASE_SCRIPT_PATH, "configfiles", "user_defined_reports.json")
RESOURCE_TYPE_FILE = os.path.join(
    BASE_SCRIPT_PATH, "configfiles", "componenet_resourcetype.json")
with open(FORBIDDEN_PATH_FILE, "r") as f:
    INVALID_PATH_ENCRYPTED_DATA = f.read()

edcfg = EditConfig()
basicconfigdata = edcfg.readConfig(BASIC_CONFIG_FILE)
configdata = edcfg.readConfig(CONFIG_FILE)
operationdata = edcfg.readConfig(OPERATION_CODE_FILE)


SELECTED_THEME = basicconfigdata["selected theme"]
DEFAULT_ENVIRONMENT = "PRODUCTION"

# Font Details
FONT_NAME = "Georgia"
FONT_SIZE = 12
# End Font Details

# Application Name
APPLICATION_NAME = "DanTe"

FORBIDDEN_PATH = GenericFunctions.decrypt_passwd(INVALID_PATH_ENCRYPTED_DATA)
INVALID_PATH_STRING = "/, /content, /var, /var/workflow, /apps/pwc, /bin, /etc" \
    if FORBIDDEN_PATH == "" else FORBIDDEN_PATH

ALLOWED_CRX_PATH_FILE = os.path.join(BASE_SCRIPT_PATH, "configfiles", "crx_allowed_path.dat")
ALLOWED_CRX_DE_PATH = edcfg.read_pickle_data(ALLOWED_CRX_PATH_FILE)

VERSION_INFO_FILE = os.path.join(BASE_SCRIPT_PATH, "configfiles", "version_info.yml")
VERSION_INFO = GenericFunctions.read_yaml_file(VERSION_INFO_FILE)



LOG_FILE = "mainlogfile_" + datetime.now().strftime("%m%d%Y") + ".log"
LOG_FILE_WITH_DEST = os.path.join(
    BASE_SCRIPT_PATH, "logs", LOG_FILE)
logger = logging.getLogger()
log_level = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
logger.setLevel(log_level[configdata["loglevel"]])

BRAND_PIC_FILE = os.path.join(BASE_SCRIPT_PATH, "logo", "logo.png")
BACKGROUND_IMAGE_1 = os.path.join(BASE_SCRIPT_PATH, "images", "bg.png")
# BACKGROUND_IMAGE_2 = os.path.join(BASE_SCRIPT_PATH,"images","bg1.jpg")
ICON_FOLDER = os.path.join(BASE_SCRIPT_PATH, "images", "crxde_icons")

FORBIDDEN_PATH = GenericFunctions.decrypt_passwd(INVALID_PATH_ENCRYPTED_DATA)
INVALID_PATH_STRING = "/, /content, /var, /var/workflow, /apps/pwc, /bin, /etc" \
    if FORBIDDEN_PATH == "" else FORBIDDEN_PATH

ALLOWED_CRX_PATH_FILE = os.path.join(BASE_SCRIPT_PATH, "configfiles", "crx_allowed_path.dat")
ALLOWED_CRX_DE_PATH = edcfg.read_pickle_data(ALLOWED_CRX_PATH_FILE)

VERSION_INFO_FILE = os.path.join(BASE_SCRIPT_PATH, "configfiles", "version_info.yml")
VERSION_INFO = GenericFunctions.read_yaml_file(VERSION_INFO_FILE)


class BulkWorkflowManager:
    def __init__(self, master):
        #self.master = Toplevel(master)
        self.master = master
        self.master.state('zoomed')
        #master.withdraw()
        self.master.title(
            APPLICATION_NAME + " - " + "Bulk Workflow Manager"
        )
        self.master.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.master.brandpic = PhotoImage(
            file=BRAND_PIC_FILE)
        self.master.iconphoto(False, self.brandpic)
        # self.stylemaster = ttk.Style()
        self.master.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.master.configdata = configdata
        self.master.excelfile = ""
        self.master.payload_data = []
        self.redirect_dpe_prop_inst = None
        self.master.initial_redirect_validated = False
        self.workflow_model_data = [
            x.strip() for x in operationdata["workflow models"].split(",") if x.strip() != ""]

        # self.mastermaindesign()selected_excelfile
        self.create_menu_bar()
        self.maindesign()
    
    def create_menu_bar(self):
        try:
            self.main_menu = Menu(self.master)
            self.main_menu.add_cascade(
                label="Edit Workflow List", command=self.select_add_workflow)
            self.master.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state("zoomed")
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.master.destroy()
            root.after(1000, self.changeRoot(root))
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def initiate_var(self):
        try:
            self.varenvdata.set(DEFAULT_ENVIRONMENT)
            selected_env = self.varenvdata.get().lower()
            self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                    basicconfigdata.get(str(selected_env)+"_passwd","")) if basicconfigdata.get(str(selected_env)+"_passwd","").strip() != "" else basicconfigdata.get(str(selected_env)+"_passwd","").strip()
            self.varuserent.set(
                    basicconfigdata.get(str(selected_env)+"_username",""))
            #self.var_selected_source.set("Source Data from Excel")
            self.varipdata.set("")
            self.varpassent.set(self.decrypted_passwd)
            self.varexcelfile.set("Browse & Select Excel File")
            self.var_selected_wf_model.set("--SELECT--")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def define_style(self):
        try:
            self.window_style = ttk.Style()
            self.window_style.configure(
                "treeStyle.Treeview", highlightthickness=2, bd=2, font=(FONT_NAME, FONT_SIZE))
            self.window_style.configure(
                "treeStyle.Treeview.Heading", font=(FONT_NAME, FONT_SIZE, "bold"))
            self.window_style.configure(
                "smallBtn.TButton", font=(FONT_NAME, 8), relief="flat")
            self.window_style.configure(
                "mainBtn.TButton", font=(FONT_NAME, FONT_SIZE), relief="flat")
            self.window_style.configure("scrollbarmain.TScrollbar", background="Green", darkcolor="DarkGreen",
                                        lightcolor="LightGreen", troughcolor="gray", bordercolor="blue", arrowcolor="white")
            self.window_style.configure(
                "green.Horizontal.TProgressbar", foreground='green', background='darkgreen')

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def maindesign(self):
        try:
            # Declare String Variable
            self.define_style()

            # String Variable
            #self.var_selected_source = StringVar()
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varexcelfile = StringVar()
            self.var_selected_wf_model = StringVar()

            # Initiate String Variable
            self.initiate_var()
            #print(self.var_selected_source.get())
            # Validation
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))

            # Frame Creation
            self.main_frame = Frame(self.master)
            self.main_frame.pack(fill="x")

            self.main_btn_frame_sep = ttk.Separator(
                self.master)
            self.main_btn_frame_sep.pack(fill="x", padx=5, pady=10)

            self.main_btn_frame = Frame(self.master)
            self.main_btn_frame.pack(fill="x")

            self.btn_frame_details_sep = ttk.Separator(
                self.master)
            self.btn_frame_details_sep.pack(fill="x", padx=5, pady=10)

            self.main_details_frame = Frame(self.master)
            self.main_details_frame.pack(fill="both")

            # Adding Widget
            # User Entry
            self.userlabelframe = LabelFrame(
                self.main_frame, text="DPE Username", padx=5, pady=5)
            self.userlabelframe.grid(
                row=0, column=2, columnspan=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.userent = Entry(self.userlabelframe,
                                 textvariable=self.varuserent)
            self.userent.grid(row=0, column=0, padx=5, pady=5,
                              ipadx=5, ipady=5, sticky="nsew")
            self.userlabelframe.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_columnconfigure(2, weight=1)

            # Password Entry
            self.passlabelframe = LabelFrame(
                self.main_frame, text="DPE Password", padx=5, pady=5)
            self.passlabelframe.grid(
                row=0, column=3, columnspan=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.passent = Entry(self.passlabelframe,
                                 show="*", textvariable=self.varpassent)
            self.passent.grid(row=0, column=0, padx=5, pady=5,
                              ipadx=5, ipady=5, sticky="nsew")
            self.passlabelframe.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_columnconfigure(3, weight=1)

            # Ip Frame
            self.iplabelframe = LabelFrame(
                self.main_frame, text="Select Env or Enter IP(should start with http://)", padx=10, pady=10)
            # self.envdata = ["", "Stage", "Production", "QA", "IP"]
            env_data = configdata.get("environments",[])
            self.envdata = env_data.copy()
            # self.envdata.insert(0,"")
            # self.envent = ttk.OptionMenu(
            #     self.iplabelframe, self.varenvdata, *self.envdata)  # command=ipchange
            self.envent = ttk.Combobox(
                self.iplabelframe, textvariable = self.varenvdata.get(), values = self.envdata, state="readonly")
            self.envent.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.iplabelframe.grid_columnconfigure(0, weight=1)
            self.ipenter = ttk.Entry(
                self.iplabelframe, textvariable=self.varipdata)
            self.iplabelframe.grid(
                row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.main_frame.grid_columnconfigure(0, weight=1)

            # Select label Frame:
            self.selectionlabelframe = LabelFrame(
                self.main_frame, text="Select the source & Enter Details", padx=5, pady=5)
            self.selectionlabelframe.grid(
                row=1, column=0, columnspan=3, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            # self.source_dropdown_data = [
            #     "", "Source Data from Excel"]  # , "Use Query Builder"
            # self.source_dropdown_ent = ttk.OptionMenu(
            #     self.selectionlabelframe, self.var_selected_source, *self.source_dropdown_data)  # , command=self.changecheckbox
            # self.source_dropdown_ent.grid(row=0, column=0, padx=5,
            #                               pady=5, sticky="nsew")

            # Query Window or Excel Window
            self.select_file_btn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.select_file_btn.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.selected_file_label = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..", textvariable=self.varexcelfile.get(), font=(FONT_NAME, FONT_SIZE - 2),
                                                 )
            self.selected_file_label.grid(
                row=0, column=2, padx=5, pady=5, sticky="nsew")

            self.selectionlabelframe.grid_columnconfigure(2, weight=1)

            # # Workflow Models
            self.workflow_model_frame = LabelFrame(
                self.main_frame, text="Select a Workflow Model")
            self.workflow_model_frame.grid(
                row=1, column=3, padx=5, pady=(13, 7), sticky="nsew")

            # self.workflow_model_data

            self.workflow_select_ent = ttk.Combobox(
                self.workflow_model_frame, textvariable=self.var_selected_wf_model, state="readonly", values=self.workflow_model_data)
            self.workflow_select_ent.grid(
                row=0, column=0, padx=5, pady=10, ipadx=5, ipady=5, sticky="nsew")
            self.workflow_model_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_columnconfigure(3, weight=1)

            # Button
            self.run_wf_model_btn = ttk.Button(
                self.main_btn_frame, text="Run Workflow", style="mainBtn.TButton", command=self.validate_and_run_workflow)  # , command=self.retrvdata
            self.run_wf_model_btn.pack(
                side="left", expand="yes", pady=5, ipadx=5, ipady=5)
            self.resetbtn = ttk.Button(
                self.main_btn_frame, text="Reset All", style="mainBtn.TButton", command=self.resetAll)  # , command=self.resetAll
            self.resetbtn.pack(side="left", expand="yes",
                               pady=5, ipadx=5, ipady=5)
            self.exitbtn = ttk.Button(self.main_btn_frame, text="Exit Window", style="mainBtn.TButton",
                                      command=lambda root=self.master: self.reopenroot(root))
            self.exitbtn.pack(side="left", expand="yes",
                              pady=5, ipadx=5, ipady=5)

            # Data View
            self.small_btn_frame = Frame(self.main_details_frame)
            self.small_btn_frame.pack(
                side="top", anchor="nw", fill="x")

            # self.export_btn = ttk.Button(
            #     self.small_btn_frame, text="Update",state="disabled", style="smallBtn.TButton", command=self.update_data_in_dpe)  # , command=self.exportData
            # self.export_btn.pack(side="left", padx=5, pady=0, anchor="w")

            self.total_hits_label = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE - 2))
            self.total_hits_label.pack(side="left", padx=5, pady=0, anchor="w")

            self.retrieve_data_count_label = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE-2))
            self.retrieve_data_count_label.pack(
                side="left", padx=5, pady=0, anchor="w")

            # Tree Frame
            self.data_tree_frame = Frame(self.main_details_frame)

            self.data_tree = ttk.Treeview(
                self.data_tree_frame, style="treeStyle.Treeview", show="headings", columns=("1", "2", "3"), selectmode="extended", height=20)

            self.data_tree_scroll_y = ttk.Scrollbar(
                self.data_tree_frame, orient="vertical", command=self.data_tree.yview)
            self.data_tree.config(yscrollcommand=self.data_tree_scroll_y.set)
            self.data_tree_scroll_y.pack(side="right", fill="y")

            self.data_tree_scroll_x = ttk.Scrollbar(
                self.data_tree_frame, orient="horizontal", command=self.data_tree.xview)
            self.data_tree.config(xscrollcommand=self.data_tree_scroll_x.set)
            self.data_tree_scroll_x.pack(side="bottom", fill="x")

            self.data_tree.pack(fill="both", expand="yes")

            # self.data_tree.bind("<<Copy>>", self.getDataandCopy)
            # self.data_tree.bind('<Double-Button-1>', self.edit_data_popup)

            self.data_tree_frame.pack(
                fill="both", padx=5, pady=10)

            self.master.update()

            table_width = self.data_tree.winfo_width()
            _width = int(table_width * 0.4)
            status_width = int(table_width * 0.2)

            self.data_tree.column("1", width=_width, stretch="yes")
            self.data_tree.column("2", width=_width, stretch="yes", anchor="c")
            self.data_tree.column("3", width=status_width,stretch="yes", anchor="c")

            self.data_tree.heading("1", text="Payload")
            self.data_tree.heading("2", text="WorkFlow Title(optional)")
            self.data_tree.heading("3", text="Status")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    ### Function / Callback
    def select_add_workflow(self):
        try:
            self.master.select_and_add_wf_modal = Toplevel(
                self.master)
            self.master.wm_attributes("-disabled", True)
            self.master.select_and_add_wf_modal.focus_set()
            self.master.select_and_add_wf_modal.iconphoto(False, self.brandpic)
            self.master.select_and_add_wf_modal.geometry("+300+100")
            self.master.select_and_add_wf_modal.minsize(650, 450)
            self.master.select_and_add_wf_modal.maxsize(650, SCREEN_HEIGHT)
            self.master.select_and_add_wf_modal.resizable(width=False, height=True)
            self.master.select_and_add_wf_modal.title(
                APPLICATION_NAME + " - Workflow List")
            self.master.select_and_add_wf_modal.transient(
                self.master)
            self.master.select_and_add_wf_modal.protocol(
                "WM_DELETE_WINDOW", lambda *args: self.close_this_window(self.master.select_and_add_wf_modal))

            def add_wf_model():
                try:
                    selected_wf = self.master.select_and_add_wf_modal.left_tree.selection()
                    logger.debug("Selected Left WF: "+str(selected_wf))
                    if bool(selected_wf):
                        for _each_select in selected_wf:
                            _item = self.master.select_and_add_wf_modal.left_tree.item(_each_select)
                            _values = _item["values"]
                            logger.debug("Selected Left table Values: "+str(_values))
                            self.master.select_and_add_wf_modal.right_tree.insert("","end",iid=self.last_item_iid_of_sel_wf + 1, values= _values)
                            self.master.select_and_add_wf_modal.left_tree.delete(_each_select)
                            self.last_item_iid_of_sel_wf += 1
                    else:
                        messagebox.showwarning("Warning!!", "Please Select a Workflow", parent=self.master.select_and_add_wf_modal)
                except:
                    logger.error("Below Exception occurred\n", exc_info=True)
            
            def remove_wf_model():
                try:
                    selected_wf = self.master.select_and_add_wf_modal.right_tree.selection()
                    logger.debug("Selected Right WF: "+str(selected_wf))
                    if bool(selected_wf):
                        for _each_select in selected_wf:
                            _item = self.master.select_and_add_wf_modal.right_tree.item(_each_select)
                            _values = _item["values"]
                            logger.debug("Selected Right Tables Values: "+str(_values))
                            self.master.select_and_add_wf_modal.left_tree.insert("","end",iid=self.last_item_iid_of_all_wf + 1, values= _values)
                            self.master.select_and_add_wf_modal.right_tree.delete(_each_select)
                            self.last_item_iid_of_all_wf += 1
                    else:
                        messagebox.showwarning("Warning!!", "Please Select a Workflow", parent=self.master.select_and_add_wf_modal)
                except:
                    logger.error("Below Exception occurred\n", exc_info=True)

            def save_wf_model():
                try:
                    global operationdata
                    self.workflow_model_data = []
                    all_wf = self.master.select_and_add_wf_modal.right_tree.get_children()
                    for _each_child in all_wf:
                        _val = self.master.select_and_add_wf_modal.right_tree.item(_each_child, "values")
                        self.workflow_model_data.append(_val[0])

                    self.workflow_model_data.sort()
                    logger.debug("ALL Selected WFs: "+str(self.workflow_model_data))
                    operationdata["workflow models"] = ",".join(self.workflow_model_data)
                    status = edcfg.updateConfig(operationdata, OPERATION_CODE_FILE)
                    if status:
                        self.workflow_select_ent.config(values=self.workflow_model_data)
                        messagebox.showinfo("Success!!","Data has been saved succefully.")
                        self.close_this_window(self.master.select_and_add_wf_modal)
                    else:
                        messagebox.showerror("Error!!","Failed to Save Data. Please check logs")

                except:
                    logger.error("Below Exception occurred\n", exc_info=True)
            
            self.master.select_and_add_wf_modal.label_frame = Frame(self.master.select_and_add_wf_modal)
            self.master.select_and_add_wf_modal.label_frame.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.master.select_and_add_wf_modal.tree_frame = Frame(self.master.select_and_add_wf_modal)
            self.master.select_and_add_wf_modal.tree_frame.pack(fill="both", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.master.select_and_add_wf_modal.btn_frame = Frame(self.master.select_and_add_wf_modal)
            self.master.select_and_add_wf_modal.btn_frame.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.master.select_and_add_wf_modal.left_tree_frame = Frame(self.master.select_and_add_wf_modal.tree_frame)
            self.master.select_and_add_wf_modal.left_tree_frame.pack(side="left", fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.master.select_and_add_wf_modal.middle_btn_frame = Frame(self.master.select_and_add_wf_modal.tree_frame)
            self.master.select_and_add_wf_modal.middle_btn_frame.pack(side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.master.select_and_add_wf_modal.right_tree_frame = Frame(self.master.select_and_add_wf_modal.tree_frame)
            self.master.select_and_add_wf_modal.right_tree_frame.pack(side="left", fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.master.select_and_add_wf_modal.title_label = Label(self.master.select_and_add_wf_modal.label_frame, text="Select and Add Workflow", anchor="center", font=("Georgia", 12, "bold"))
            self.master.select_and_add_wf_modal.title_label.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.master.select_and_add_wf_modal.title_label = Label(self.master.select_and_add_wf_modal.label_frame, text="Workflow(s)\t\t\t\tSelected Workflow", font=("Georgia", 10, "bold"))
            self.master.select_and_add_wf_modal.title_label.pack(fill="x", padx=5, ipadx=5)

            self.master.select_and_add_wf_modal.left_tree = ttk.Treeview(self.master.select_and_add_wf_modal.left_tree_frame, show="headings", column=("Workflow"), height=12,)
            self.master.select_and_add_wf_modal.left_tree_scroll_y = ttk.Scrollbar(self.master.select_and_add_wf_modal.left_tree_frame, command=self.master.select_and_add_wf_modal.left_tree.yview)
            self.master.select_and_add_wf_modal.left_tree.config(yscrollcommand=self.master.select_and_add_wf_modal.left_tree_scroll_y.set)
            self.master.select_and_add_wf_modal.left_tree_scroll_y.pack(side="right", fill="y")
            self.master.select_and_add_wf_modal.left_tree.pack(fill="both", expand="yes")
            self.master.select_and_add_wf_modal.left_tree.column("Workflow", minwidth=150, stretch=YES)
            self.master.select_and_add_wf_modal.left_tree.heading("Workflow", text="Workflow", anchor=CENTER)

            self.master.select_and_add_wf_modal.middle_add_btn = ttk.Button(self.master.select_and_add_wf_modal.middle_btn_frame, text=">>", style="smallBtn.TButton", command=add_wf_model)
            self.master.select_and_add_wf_modal.middle_add_btn.pack(padx=5,pady=5, ipadx=1, ipady=1, anchor="center")
            self.master.select_and_add_wf_modal.middle_remove_btn = ttk.Button(self.master.select_and_add_wf_modal.middle_btn_frame, text="<<", style="smallBtn.TButton", command=remove_wf_model)
            self.master.select_and_add_wf_modal.middle_remove_btn.pack(padx=5,pady=5, ipadx=1, ipady=1, anchor="center")

            self.master.select_and_add_wf_modal.right_tree = ttk.Treeview(self.master.select_and_add_wf_modal.right_tree_frame, show="headings", column=("Selected_Workflow"), height=12,)
            self.master.select_and_add_wf_modal.right_tree_scroll_y = ttk.Scrollbar(self.master.select_and_add_wf_modal.right_tree_frame, command=self.master.select_and_add_wf_modal.right_tree.yview)
            self.master.select_and_add_wf_modal.right_tree.config(yscrollcommand=self.master.select_and_add_wf_modal.right_tree_scroll_y.set)
            self.master.select_and_add_wf_modal.right_tree_scroll_y.pack(side="right", fill="y")
            self.master.select_and_add_wf_modal.right_tree.pack(fill="both", expand="yes")
            self.master.select_and_add_wf_modal.right_tree.column("Selected_Workflow", minwidth=150, stretch=YES)
            self.master.select_and_add_wf_modal.right_tree.heading("Selected_Workflow", text="Selected Workflow", anchor=CENTER)

            self.master.select_and_add_wf_modal.save_btn = ttk.Button(self.master.select_and_add_wf_modal.btn_frame, text="Save", command=save_wf_model)
            self.master.select_and_add_wf_modal.save_btn.pack(side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.master.select_and_add_wf_modal.exit_btn = ttk.Button(self.master.select_and_add_wf_modal.btn_frame, text="Exit", command=lambda *args: self.close_this_window(self.master.select_and_add_wf_modal))
            self.master.select_and_add_wf_modal.exit_btn.pack(side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            for _id, _each_selected_wf in enumerate(self.workflow_model_data):
                self.master.select_and_add_wf_modal.right_tree.insert("","end", iid=_id+1, values=(_each_selected_wf,))

            all_workflows = edcfg.readConfig(WF_MODEL_FILE)
            for _id, _each_all_wf in enumerate(all_workflows):
                if _each_all_wf not in self.workflow_model_data:
                    self.master.select_and_add_wf_modal.left_tree.insert("","end", iid=_id+1, values=(_each_all_wf,))

            self.last_item_iid_of_sel_wf = len(self.master.select_and_add_wf_modal.right_tree.get_children())
            self.last_item_iid_of_all_wf = len(all_workflows)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def close_this_window(self, wind):
        try:
            self.master.focus_set()
            self.master.wm_attributes("-disabled", False)
            wind.destroy()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
    
    def ipchange(self, value):
        try:
            if value.lower() == "ip":
                self.ipenter.grid(row=0, column=1, padx=10,
                                  pady=10, sticky="nsew")
                self.iplabelframe.grid_columnconfigure(1, weight=1)
                self.varuserent.set("")
                self.varpassent.set("")

            else:
                if self.ipenter.winfo_ismapped():
                    self.ipenter.grid_forget()

                self.iplabelframe.grid_columnconfigure(0, weight=1)
                self.iplabelframe.grid_columnconfigure(1, weight=0)

                selected_env = value.lower()
                self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                    basicconfigdata.get(str(selected_env)+"_passwd","")) if basicconfigdata.get(str(selected_env)+"_passwd","").strip() != "" else basicconfigdata.get(str(selected_env)+"_passwd","").strip()
                self.varuserent.set(
                    basicconfigdata.get(str(selected_env)+"_username",""))
                self.varpassent.set(self.decrypted_passwd)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def checkipdata(self, varipdata):
        try:
            if len(self.varipdata.get()) > 7 and self.varipdata.get()[0:7] != "http://":
                self.varipdata.set("")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def insert_into_table(self, pos, table_values):
        try:
            self.data_tree.insert("", "end", iid=pos,
                                  text=str(pos), values=table_values)
            self.data_tree.yview_moveto(1)
            self.master.update()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openexcelfile(self):
        try:
            logger.debug("--Single Redirect--")
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.master.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.master.excelfile:
                logger.debug("Selected Excel File: " +
                             self.master.excelfile)
                self.varexcelfile.set(self.master.excelfile)
                #print(self.varexcelfile.get())
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_inputs(self, uname, passwd, environment, selected_ip, selected_wf, excel_file):
        try:
            output_status = False
            is_not_empty_uname = bool(uname)
            logger.debug("Username Not Empty: "+str(is_not_empty_uname))

            is_not_empty_passwd = bool(passwd)
            logger.debug("Password Not Empty: "+str(is_not_empty_passwd))

            is_not_empty_ip = bool(selected_ip)
            logger.debug("IP Not Empty: "+str(is_not_empty_ip))

            is_not_empty_wf_model = bool(selected_wf)
            logger.debug("WF Not Empty: "+str(is_not_empty_wf_model))

            is_valid_file = True if excel_file != "" and excel_file is not None else False
            logger.debug("Valid File: "+str(is_valid_file))

            allowed_file_types = [".xlsx", ".xls", ".xlsm"]
            is_valid_excel_file = GenericFunctions.is_valid_file_types(
                excel_file, allowed_file_types) if is_valid_file else False
            logger.debug("Valid Excel File: "+str(is_valid_excel_file))

            is_valid_ip = GenericFunctions.validateIP(
                selected_ip, environment) if is_not_empty_ip else False
            logger.debug("Valid IP: "+str(is_valid_ip))

            is_valid_model_id = True if selected_wf != "--SELECT--" else False
            logger.debug("Valid Workflow: "+str(is_valid_model_id))

            if is_not_empty_ip and is_not_empty_uname and is_not_empty_passwd and is_valid_file and is_valid_excel_file and is_valid_ip and is_valid_model_id and is_not_empty_wf_model:
                output_status = True

            else:
                error_list = []
                if not(is_not_empty_uname):
                    error_list.append("\nUsername Can't be Empty")

                if not(is_not_empty_passwd):
                    error_list.append("\nPassword Can't be Empty")

                if not(is_not_empty_ip):
                    error_list.append("\nIP Can't be Empty")

                if not(is_valid_file):
                    error_list.append("\nPlease select a File")

                if not(is_valid_model_id):
                    error_list.append("\nPlease select a Valid Model")

                if not(is_not_empty_wf_model):
                    error_list.append("\nWF Model can't be empty")

                if not(is_valid_excel_file):
                    error_list.append(
                        "\nInvalid Selected File. Only accepts below\n"+",".join(allowed_file_types))

                if not(is_valid_ip):
                    error_list.append(
                        "\nInvalid IP, Please select/enter correct IP")

                if bool(error_list):
                    messagebox.showerror("Below Error has occurred", "Please see the below list"+".".join(
                        error_list), parent=self.master)
                    logger.error("Below Error has occurred" +
                                 ".".join(error_list))

            logger.info("Data Validation Status: " + str(output_status))
            return output_status

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def open_popup_modal(self, error_data):
        try:
            pass
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_and_run_workflow(self):
        try:
            disable_btn = True
            disable_model = True
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.master.update()

            uname = self.varuserent.get().strip()
            passwd = self.varpassent.get().strip()

            environment = self.varenvdata.get().lower()
            selected_ip = (self.varipdata.get().lower().strip()
                           if environment == "ip" else configdata[environment])
            excel_file = self.master.excelfile
            selected_wf = self.var_selected_wf_model.get()
            run_the_operation = True
            if environment.lower() == "production":
                run_the_operation = messagebox.askyesnocancel(
                    "Please confirm", "Do you want to Run\nthe Operation in Production?", parent=self.master)

            if run_the_operation:
                is_validated = self.validate_inputs(
                    uname, passwd, environment, selected_ip, selected_wf, excel_file)

                if is_validated:
                    self.toggleInputField("disabled")
                    self.master.update()

                    self.run_workflow_instances = RunWorkflow(
                        selected_ip, uname, passwd)
                    all_payloads = self.run_workflow_instances.excel_to_list(
                        excel_file)
                    count_of_payloads = len(all_payloads)
                    self.total_hits_label.config(
                        text="Total: "+str(count_of_payloads), fg="black")

                    logger.debug("Total Number of Payloads: " +
                                 str(count_of_payloads))
                    logger.debug(all_payloads)

                    select_wf_status = self.run_workflow_instances.set_model(
                        selected_wf)

                    if select_wf_status:

                        self.master.progress_bar = ttk.Progressbar(
                            self.small_btn_frame, orient=HORIZONTAL, maximum=count_of_payloads, mode="determinate", style="green.Horizontal.TProgressbar")
                        self.master.progress_bar.pack(
                            fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")

                        for i, each_payload in enumerate(all_payloads):
                            output_status = self.run_workflow_instances.bulk_run_workflow(
                                each_payload)
                            if output_status >= 200 and output_status < 207:
                                table_values = (each_payload[0],each_payload[1], "Completed")
                                self.insert_into_table(i, table_values)
                                self.retrieve_data_count_label.config(
                                    text="Current: "+str(i+1), fg="black")
                            elif output_status == 404:
                                table_values = (each_payload[0],each_payload[1], "Invalid Payload")
                                self.insert_into_table(i, table_values)
                                self.retrieve_data_count_label.config(
                                    text="Current: "+str(i+1), fg="black")
                            elif output_status == 401:
                                msg = "Invalid UserName and Password"
                                self.retrieve_data_count_label.config(
                                    text="", fg="black")
                                self.total_hits_label.config(
                                    text=msg, fg="red")
                                self.userent["state"] = "normal"
                                self.passent["state"] = "normal"
                                self.run_wf_model_btn["state"] = "normal"

                                disable_btn = False
                                break
                            
                            elif output_status == 999:
                                table_values = (each_payload[0],each_payload[1], "Exception")
                                self.insert_into_table(i, table_values)
                                self.retrieve_data_count_label.config(
                                    text="Current: "+str(i+1), fg="black")
                            elif output_status is None:
                                msg = "Invalid Workflow Model"
                                self.retrieve_data_count_label.config(
                                    text="", fg="black")
                                self.total_hits_label.config(
                                    text=msg, fg="red")
                                self.workflow_select_ent["state"] = "readonly"

                                disable_model = False
                                break
                            else:
                                table_values = (
                                    each_payload[0],each_payload[1], "Error - "+str(output_status))
                                self.insert_into_table(i, table_values)
                                self.retrieve_data_count_label.config(
                                    text="Current: "+str(i+1), fg="black")

                            self.master.update()

                            self.master.progress_bar["value"] = i+1
                            self.master.update()
                            sleep(configdata["sleeptime"])

                        self.master.progress_bar.destroy()

                        if disable_btn:
                            self.userent["state"] = "disabled"
                            self.passent["state"] = "disabled"

                        if disable_model:
                            self.workflow_select_ent["state"] = "disabled"

                        if disable_btn and disable_model:
                            self.run_wf_model_btn["state"] = "disabled"

                        self.master.update()
                    else:
                        msg = "Invalid Workflow Model"
                        self.retrieve_data_count_label.config(
                            text="", fg="black")
                        self.total_hits_label.config(text=msg, fg="red")
                        self.workflow_select_ent["state"] = "readonly"
                        self.run_wf_model_btn["state"] = "normal"

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def toggleInputField(self, val):
        try:
            self.userent["state"] = val
            self.passent["state"] = val
            self.ipenter["state"] = val
            self.select_file_btn["state"] = val
            self.run_wf_model_btn["state"] = val
            self.workflow_select_ent["state"] = val if val == "disabled" else "readonly"

            self.envent["state"] = val
            self.source_dropdown_ent["state"] = val

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initiate_var()
            self.toggleInputField("normal")
            self.master.excelfile = ""
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.data_tree.delete(*self.data_tree.get_children())
            # self.data_tree["columns"] = ()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)


def initiatewindow(root):
    root.state("zoomed")
    root.deiconify()
    root.update()
    root.design = BulkWorkflowManager(root)
    root.design.maindesign()

def splashscreen(root):
    splash = Toplevel(root)
    root.withdraw()
    splash.screen_width = root.winfo_screenwidth()
    splash.screen_height = root.winfo_screenheight()
    splash.width = 500
    splash.height = 330

    splash.position_x = int((splash.screen_width - splash.width)/2)
    splash.position_y = int((splash.screen_height - splash.height)/2)
    splash.geometry(
        f"{splash.width}x{splash.height}+{splash.position_x}+{splash.position_y}")
    splash.resizable(False, False)
    splash.overrideredirect(True)
    splash.update()

    img_o = Image.open(BACKGROUND_IMAGE_1)
    img_c = img_o.copy()
    img = ImageTk.PhotoImage(img_c)

    bgframe = Frame(splash)
    bgframe.pack(fill="both", expand="yes")

    bgLabel = Label(bgframe, text="", image=img)
    bgLabel.place(x=0, y=0, relx=0.5, rely=0.5, anchor=CENTER)

    frame1 = Frame(bgframe)
    frame1.pack(side="bottom", fill="x", expand="yes",
                padx=20, pady=20, anchor="s")
    prog = ttk.Progressbar(frame1, orient="horizontal",
                           mode="determinate", maximum=5)
    pcounter = 1
    prog.pack(side="bottom", fill="x", expand="yes", anchor="s")

    for i in range(5):
        prog["value"] = pcounter
        # splash.update_idletasks()
        splash.update()
        pcounter += 1
        sleep(1)

    splash.destroy()


def Main():
    try:
        mainwindow = Tk()
        # mainwindow.tk.call("source", os.path.join(BASE_SCRIPT_PATH, "themes", "azure.tcl"))
        # mainwindow.tk.call("set_theme", "light")
        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH = mainwindow.winfo_screenwidth()
        SCREEN_HEIGHT = mainwindow.winfo_screenheight()
        splashscreen(mainwindow)
        initiatewindow(mainwindow)
        mainwindow.style = ttk.Style()
        mainwindow.style.theme_use(SELECTED_THEME)
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Georgia")
        mainwindow.option_add("*Font", default_font)
        mainwindow.mainloop()
    except:
        logger.error("Below Exception occured: ", exc_info=True)

if __name__ == "__main__":
    Main()
