# coding=utf-8
from tkinter import *
from tkinter import ttk, PhotoImage, messagebox, filedialog
import tkinter.font as tkFont
import logging
from datetime import datetime
from editconfig import EditConfig
from terminatewf import TerminateWorkflow
from getdatafromdpe import GetDataFromPayload
from validate_redirect import RedirectValidation
from update_dpe_prop import UpdateDPEProperties
from validate_redirect_content_path import ContentPathValidator
from bulk_node_deletion import BulkNodeDeletion
from predefined_dpe_reports import PreDefinedReports
from form_data_marketing_consent import FormDataMarketingConsent
from logging_screen import LoggingScreen, ViewpointDataCleaner
from dpe_bulk_workflow_manager import RunWorkflow
from dpe_copy_and_users_related import UserAccountsAndCopy
from dpe_page_unlock import UnlockPages
from dpe_crx_search_ui import *
#SearchDPEorQuery, CreateNodeUI, RenameNodeUI, ScrollableFrameWithEntry
# from tkcalendar import Calendar
from PIL import Image, ImageTk
import webbrowser
import os
import xlsxwriter
import threading
from time import sleep
from dpe_validation import GenericFunctions
import sys

# Configdata
SCREEN_WIDTH = 1320
SCREEN_HEIGHT = 768
ADMIN_USERS = ['shouvik.d.das@in.pwc.com', 'shouvik.d.das@pwc.com','debolina.b.dutta@in.pwc.com','debolina.b.dutta@pwc.com']

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    BASE_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
else:
    BASE_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

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

INVALID_PATH_ENCRYPTED_DATA = INVALID_PATH_ENCRYPTED_DATA if INVALID_PATH_ENCRYPTED_DATA else \
    "gAAAAABfv9o2LTKCxvhtDHuZfMOuCpJlG1oBFcToMxba2caFVIJvrR6AcNY-49iLvjBdE5WdqzAE7Rf4PNtWQYcZVW5bHMBv0UI2FkWT75rp0jSzqn_yfcC_tVuSanroeFA-r8qSONegeX1G_9OHO2ITn3h-IgGx7DLVXlraCAZLtxEF221GIss="

# INVALID_PATH_STRING = "/, /content, /var, /var/workflow, /apps/pwc, /bin, /etc"
INVALID_PATH_STRING = ""

edcfg = EditConfig()
basicconfigdata = edcfg.readConfig(BASIC_CONFIG_FILE)
configdata = edcfg.readConfig(CONFIG_FILE)
operationdata = edcfg.readConfig(OPERATION_CODE_FILE)

# Set Logger
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

# Logo
BRAND_PIC_FILE = os.path.join(BASE_SCRIPT_PATH, "logo", "logo.png")
BACKGROUND_IMAGE_1 = os.path.join(BASE_SCRIPT_PATH, "images", "bg.png")
# BACKGROUND_IMAGE_2 = os.path.join(BASE_SCRIPT_PATH,"images","bg1.jpg")
ICON_FOLDER = os.path.join(BASE_SCRIPT_PATH, "images", "crxde_icons")

# Theme
# ['winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative']
SELECTED_THEME = basicconfigdata["selected theme"]
DEFAULT_ENVIRONMENT = "PRODUCTION"

# Font Details
FONT_NAME = "Georgia"
FONT_SIZE = 12
# End Font Details

# Application Name
APPLICATION_NAME = "DanTe"

FORBIDDEN_PATH = GenericFunctions.decrypt_passwd(INVALID_PATH_ENCRYPTED_DATA)
INVALID_PATH_STRING = "/, /content, /content/pwc ,/var, /var/workflow, /apps/pwc, /bin, /etc" \
    if FORBIDDEN_PATH == "" else FORBIDDEN_PATH

ALLOWED_CRX_PATH_FILE = os.path.join(BASE_SCRIPT_PATH, "configfiles", "crx_allowed_path.dat")
ALLOWED_CRX_DE_PATH = edcfg.read_pickle_data(ALLOWED_CRX_PATH_FILE)

VERSION_INFO_FILE = os.path.join(BASE_SCRIPT_PATH, "configfiles", "version_info.yml")
VERSION_INFO = GenericFunctions.read_yaml_file(VERSION_INFO_FILE)


class DPEInboxClearing:
    def __init__(self, master):
        self.master = master
        self.master.state("zoomed")
        self.master.configdata = configdata
        self.master.title(APPLICATION_NAME + " - " +
                          "DPE Dashboard")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.master.iconphoto(False, self.brandpic)
        # self.master.excelfile = None

    def initialize_variable(self):
        try:
            self.varenvdata.set(DEFAULT_ENVIRONMENT)
            selected_env = self.varenvdata.get().lower()
            self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                basicconfigdata.get(str(selected_env)+"_passwd","")) if basicconfigdata.get(str(selected_env)+"_passwd","").strip() != "" else basicconfigdata.get(str(selected_env)+"_passwd","").strip()
            self.varuserent.set(basicconfigdata.get(str(selected_env)+"_username",""))
            self.varpassent.set(self.decrypted_passwd)
            self.varipdata.set("")
            self.varreportolderent.set("1")
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def maindesign(self):
        # String Variable
        self.varuserent = StringVar()
        self.varpassent = StringVar()
        self.varenvdata = StringVar()
        self.varipdata = StringVar()
        self.varreportolderent = StringVar()
        # self.varquery = IntVar()

        # End String Variable
        self.initialize_variable()

        # Validation
        # self.varquery.trace("w", lambda *args: self.updatequerybtn())
        self.varipdata.trace(
            "w", lambda *args: self.checkipdata(self.varipdata))

        # Add Menubar
        self.createmenubar()

        # LabelFrame
        self.labelframecreation()

        # Assigning Elements
        self.assignWidget()

    # Create or Desing Menubar
    def createmenubar(self):
        try:
            self.menubar = Menu(self.master)
            self.dpemenu = Menu(self.menubar, tearoff=0)

            self.dpemenu.add_command(
                label="Terminate Workflow", command=self.terminatewf
            )

            self.menubar.add_cascade(label="DPE", menu=self.dpemenu)

            self.redirect_menu = Menu(self.menubar, tearoff=0)
            self.redirect_menu.add_command(
                label="Place/Remove Redirect", command=self.place_single_redirect)

            self.redirect_menu.add_command(
                label="Validate Redirect", command=self.redirection_check_for_dpe)
            self.menubar.add_cascade(label="Redirect", menu=self.redirect_menu)

            self.reporting_menu = Menu(self.menubar, tearoff=0)
            self.reporting_menu.add_command(
                label="Pre-defined Report", command=self.predefined_report_from_dpe)
            self.reporting_menu.add_command(
                label="Retrieve Data", command=self.retrieve_data_from_dpe)
            # self.reporting_menu.add_command(
            #     label="DAM Assets Reference", command=self.retrieve_dam_reference)
            self.reporting_menu.add_command(
                label="Extract Reports For All Types Of Forms", command=self.form_data_for_marketing_consent)
            self.menubar.add_cascade(
                label="Reporting", menu=self.reporting_menu)

            self.bulk_operation_menu = Menu(self.menubar, tearoff=0)

            self.bulk_operation_menu.add_command(
                label="Bulk Update", command=self.bulk_update_to_dpe)

            self.bulk_operation_menu.add_command(
                label="Delete Node", command=self.bulk_deletion_of_node)

            self.bulk_operation_menu.add_command(
                label="Bulk Workflow Manager", command=self.bulk_workflow_manager)
            self.bulk_operation_menu.add_command(
                label="Enable/Disable Users", command=self.deactivate_dpe_users)
            self.bulk_operation_menu.add_command(
                label="Copy/Move Nodes", command=self.copy_or_move_nodes)
            self.bulk_operation_menu.add_command(
                label="Unlock DPE Pages", command=self.unlock_dpe_pages) 

            self.menubar.add_cascade(
                label="Bulk Operations", menu=self.bulk_operation_menu)

            self.viewpoint_menu = Menu(self.menubar, tearoff=0)
            self.viewpoint_menu.add_command(
                label="MetaData Clean", command=self.metadata_cleanup
            )
            self.menubar.add_cascade(label="Viewpoint", menu=self.viewpoint_menu)

            self.filemenu = Menu(self.menubar, tearoff=0)  # savebasicconfig
            self.filemenu.add_command(
                label="Basic Settings", command=self.savebasicconfig
            )
            self.filemenu.add_command(
                label="Configurations", command=self.savesettings)
            self.filemenu.add_command(
                label="Operations Code", command=self.operationScreen
            )
            self.filemenu.add_command(
                label="Logging", command=self.open_logging_screen
            )
            self.filemenu.add_command(
                label="Forbidden Path", command=self.forbiddenPathScreen
            )
            self.filemenu.add_command(
                label="Sync WF Models", command=self.sync_wf_model_id
            )
            self.menubar.add_cascade(label="Settings", menu=self.filemenu)

            self.aboutmenu = Menu(self.menubar, tearoff=0)
            self.aboutmenu.add_command(
                label="About", command=self.showinformation)
            self.aboutmenu.add_command(
                label="Documentaion", command=self.openMannual)
            self.aboutmenu.add_command(
                label="Link for Mannual", command=self.docLink)
            # self.aboutmenu.add_command(
            #     label="Update", command=self.update_tool)
            self.menubar.add_cascade(label="Help", menu=self.aboutmenu)

            self.master.config(menu=self.menubar)

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    # Create Label Frame
    def labelframecreation(self):
        try:
            self.main_frame = Frame(self.master)
            self.main_frame.pack(fill="both", expand="yes")

            self.main_top_frame = Frame(self.main_frame)
            self.main_top_frame.pack(fill="both", expand="yes")

            self.main_bottom_frame = Frame(self.main_frame)
            self.main_bottom_frame.pack(
                side="bottom", fill="both", expand="yes")

            
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def define_style(self):
        try:
            # Sepcify Style
            self.stylewidget = ttk.Style()

            self.stylewidget.configure(
                "buttondesign.TButton", font=(FONT_NAME, FONT_SIZE)
            )
            self.stylewidget.configure(
                "bigbuttondesign.TButton", font=(FONT_NAME, 36)
            )
            self.stylewidget.configure(
                "smallbuttondesign.TButton", font=(FONT_NAME, 9)
            )
            self.stylewidget.configure(
                "smallbuttondesign_f7.TButton", font=(FONT_NAME, 7)
            )
            # self.stylewidget.configure("welcome.TLabel", font=(FONT_NAME, 72))
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    # Assign New Widget
    def assignWidget(self):
        try:
            self.define_style()

            # Assign widget
            self.welcome_message_lbl = ttk.Label(self.main_top_frame, text="Welcome to DPE Automation tool.", font=(FONT_NAME, 50))
            self.welcome_message_lbl.grid(row=0, column = 0, padx=10, ipadx=10, pady=10, ipady=10)

            l2_text = "This tool is used for reporting, bulk updates and other important work related to DPE. "+\
                "The main use is for reporting, which is based on Query Debugger"

            self.welcome_message_txt_lbl = ttk.Label(self.main_top_frame, text=l2_text, font=(FONT_NAME, 22))
            self.welcome_message_txt_lbl.grid(row=1, column = 0, padx=10, ipadx=10, pady=10, ipady=10)

            self.main_top_frame.grid_columnconfigure(0, weight=1)

            self.button_lframe = LabelFrame(self.main_bottom_frame, text="Quick Links")
            self.button_lframe.pack(fill="both", expand="yes", padx=10, pady=10)

            terminate_wf_btn = ttk.Button(self.button_lframe, text="Terminate WF", command=self.terminatewf, style="bigbuttondesign.TButton")
            terminate_wf_btn.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5, expand="yes")
            predefined_report_btn = ttk.Button(self.button_lframe, text="Predefined Reports", command=self.predefined_report_from_dpe, style="bigbuttondesign.TButton")
            predefined_report_btn.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5, expand="yes")
            bulk_update_to_dpe_btn = ttk.Button(self.button_lframe, text="Bulk Update", command=self.bulk_update_to_dpe, style="bigbuttondesign.TButton")
            bulk_update_to_dpe_btn.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5, expand="yes")
            place_single_redirect_btn = ttk.Button(self.button_lframe, text="Redirect Manager", command=self.place_single_redirect, style="bigbuttondesign.TButton")
            place_single_redirect_btn.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5, expand="yes")
            redirection_check_for_dpe_btn = ttk.Button(self.button_lframe, text="Validate Redirect", command=self.redirection_check_for_dpe, style="bigbuttondesign.TButton")
            redirection_check_for_dpe_btn.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5, expand="yes")
            bulk_workflow_manager_btn = ttk.Button(self.button_lframe, text="Bulk WF Manager", command=self.bulk_workflow_manager, style="bigbuttondesign.TButton")
            bulk_workflow_manager_btn.pack(side="left", padx=5, pady=5, ipadx=5, ipady=5, expand="yes")
            self.welcome_message_txt_lbl.bind("<Configure>", lambda *args: self.resize_window(self.welcome_message_txt_lbl, *args))
            self.welcome_message_lbl.bind("<Configure>", lambda *args: self.resize_window(self.welcome_message_lbl, *args))  

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def resize_window(self, label, *args, **kwargs):
        event = args[0]
        width = event.width
        label.configure(wraplength = width-10)


    # DPE Menu Items #DPE
    def terminatewf(self):
        try:
            TerminateWorkflowUI(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def predefined_report_from_dpe(self):
        try:
            PreDefinedReportsManager(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def retrieve_data_from_dpe(self):
        try:
            RetrieveDataFromDPE(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def form_data_for_marketing_consent(self):
        try:
            # if self.report_generated:
            #     self.reset_all()
            FormDataforMarketingConsent(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)        

    def deactivate_dpe_users(self):
        try:
            # RetrieveDataFromDPE(self.master)
            BulkUserManager(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)
    
    def copy_or_move_nodes(self):
        try:
            BulkCopyOrMoveManager(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def unlock_dpe_pages(self):
        try:
            UnlockDPEPages(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)         

    def bulk_update_to_dpe(self):
        try:
            DPEBulkUpdate(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def place_single_redirect(self):
        try:
            DPESingleRedirect(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def redirection_check_for_dpe(self):
        try:
            DPERedirectionCheck(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def bulk_deletion_of_node(self):
        try:
            BulkDeletionOfDPENode(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def bulk_workflow_manager(self):
        try:
            BulkWorkflowManager(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)


    # DPE Menu Items #Settings
    def savesettings(self):
        try:
            win = ConfigWindow(self.master)
            self.master.wait_window(win.configwin)
            # self.varquery.set(configdata["isquerybuilder"])
            self.master.configdata = configdata
            logger.setLevel(log_level[configdata["loglevel"]])

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def savebasicconfig(self):
        try:
            win = BasicConfigWindow(self.master)
            self.master.wait_window(win.basicconfigwin)
            # self.varquery.set(configdata["isquerybuilder"])
            SELECTED_THEME = basicconfigdata.get("selected theme","")
            self.master.style.theme_use(SELECTED_THEME)
            self.varuserent.set(basicconfigdata.get("username",""))
            self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                basicconfigdata.get("passwd","")) if basicconfigdata.get("passwd","").strip() != "" else basicconfigdata.get("passwd","").strip()
            self.varpassent.set(self.decrypted_passwd)
            # self.master.configdata = configdata
            # logger.setLevel(log_level[configdata["loglevel"]])

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def operationScreen(self):
        try:
            OperationsWindow(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def open_logging_screen(self):
        try:
            LoggingScreen(self.master, APPLICATION_NAME,
                          BRAND_PIC_FILE, LOG_FILE_WITH_DEST)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def forbiddenPathScreen(self):
        try:
            ForbiddenPathWindow(self.master)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def sync_wf_model_id(self):
        try:
            self.sync_wf_models_ui = Toplevel(self.master)
            self.master.wm_attributes("-disabled", True)
            self.sync_wf_models_ui.focus_set()
            self.sync_wf_models_ui.title(
                APPLICATION_NAME + " - " + "Sync WF - Enter Details")
            self.sync_wf_models_ui.geometry("+500+30")
            
            self.sync_wf_models_ui.minsize(300, 400)
            self.sync_wf_models_ui.maxsize(300, SCREEN_HEIGHT)
            self.sync_wf_models_ui.resizable(width=False, height=True)
            self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
            self.sync_wf_models_ui.iconphoto(False, self.brandpic)
            self.sync_wf_models_ui.transient(self.master)
            self.sync_wf_models_ui.protocol(
                "WM_DELETE_WINDOW", lambda *args: self.closethiswindow(self.sync_wf_models_ui))
            # self.sync_wf_models_ui.overrideredirect(True)

            def ip_change(data):
                try:
                    if data.lower() == "ip":
                        self.sync_wf_models_ui.ipent.pack(
                            side="left", fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)
                        # self.frame_1.grid_columnconfigure(4, weight=1)
                        self.varuserent.set("")
                        self.varpassent.set("")
                    else:
                        selected_env = data.lower()
                        if self.sync_wf_models_ui.ipent.winfo_ismapped():
                            self.sync_wf_models_ui.ipent.pack_forget()
                        self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                            basicconfigdata.get(str(selected_env)+"_passwd","")) if basicconfigdata.get(str(selected_env)+"_passwd","").strip() != "" else basicconfigdata.get(str(selected_env)+"_passwd","").strip()
                        self.varuserent.set(
                            basicconfigdata[str(selected_env)+"_username"])
                        self.varpassent.set(self.decrypted_passwd)
                except:
                    logger.error("Below Exception occurred\n", exc_info=True)

            # Validation
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))
            self.varenvdata.trace(
                "w", lambda *args: ip_change(self.varenvdata.get().strip())
            )

            # Functions
            def sync_wf_ids():
                try:
                    global edcfg, WF_MODEL_FILE
                    username = self.varuserent.get().strip()
                    passwd = self.varpassent.get().strip()
                    ip = (
                        self.varipdata.get().strip()
                        if self.varenvdata.get().strip().lower() == "ip"
                        else self.master.configdata[
                            self.varenvdata.get().lower().strip()
                        ]
                    )
                    bn = RunWorkflow(ip, username, passwd)
                    out = bn.sync_wf_models()
                    can_be_closed = False
                    if isinstance(out, dict):
                        outval = edcfg.updateConfig(out, WF_MODEL_FILE)
                        logger.info("Success - Synced Workflow Models")
                        messagebox.showinfo(
                            "Success", "Synced Workflow Models", parent=self.sync_wf_models_ui)
                        can_be_closed = True

                    else:
                        if out == 401:
                            logger.info(
                                "Error Occured - Invalid Username/Password")
                            messagebox.showerror(
                                "Error Occured", "Invalid Username/Password", parent=self.sync_wf_models_ui)
                        else:
                            logger.info(
                                "Error Occured - Error in Connection - "+str(out))
                            messagebox.showerror(
                                "Error Occured", "Error in Connection - "+str(out), parent=self.sync_wf_models_ui)

                    if can_be_closed:
                        self.closethiswindow(self.sync_wf_models_ui)
                except:
                    logger.error("Below Exception occured: ", exc_info=True)

            self.sync_wf_models_ui.main_frame = Frame(
                self.sync_wf_models_ui)
            self.sync_wf_models_ui.main_frame.pack(
                side="top", fill="both", expand="yes")

            self.sync_wf_models_ui.button_frame = Frame(
                self.sync_wf_models_ui)
            self.sync_wf_models_ui.button_frame.pack(
                side="bottom", fill="both", expand="yes")
            
            # Environment
            self.sync_wf_models_ui.environment_labelframe = LabelFrame(
                self.sync_wf_models_ui, text="Environment")
            self.sync_wf_models_ui.environment_labelframe.pack(
                fill="both", expand="yes", padx=10, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            # self.sync_wf_models_ui.environment_data = [
            #     "", "Production", "Stage", "QA", "IP"]
            env_data = configdata.get("environments",[])
            self.sync_wf_models_ui.environment_data = env_data.copy()
            # self.sync_wf_models_ui.environment_data.insert(0,"")

            # self.sync_wf_models_ui.envent = ttk.OptionMenu(
            #     self.sync_wf_models_ui.environment_labelframe, self.varenvdata, *self.sync_wf_models_ui.environment_data)
            self.sync_wf_models_ui.envent = ttk.Combobox(
                self.sync_wf_models_ui.environment_labelframe, textvariable=self.varenvdata, state="readonly", values=self.sync_wf_models_ui.environment_data)
            self.sync_wf_models_ui.envent.pack(
                side="left", fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            self.sync_wf_models_ui.ipent = ttk.Entry(
                self.sync_wf_models_ui.environment_labelframe, textvariable=self.varipdata)

            # Username
            self.sync_wf_models_ui.username_labelframe = LabelFrame(
                self.sync_wf_models_ui, text="DPE Username")
            self.sync_wf_models_ui.username_labelframe.pack(
                fill="both", expand="yes", padx=10, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            self.sync_wf_models_ui.username_entry = ttk.Entry(
                self.sync_wf_models_ui.username_labelframe, textvariable=self.varuserent)
            self.sync_wf_models_ui.username_entry.pack(
                fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            # Password
            self.sync_wf_models_ui.password_labelframe = LabelFrame(
                self.sync_wf_models_ui, text="DPE Password")
            self.sync_wf_models_ui.password_labelframe.pack(
                fill="both", expand="yes", padx=10, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            self.sync_wf_models_ui.password_entry = ttk.Entry(
                self.sync_wf_models_ui.password_labelframe, show="*", textvariable=self.varpassent)
            self.sync_wf_models_ui.password_entry.pack(
                fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            # self.sync_wf_models_ui.ipent.pack(side="left", fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            self.sync_wf_models_ui.button_submit = ttk.Button(
                self.sync_wf_models_ui.button_frame, text="Sync", command=sync_wf_ids)
            self.sync_wf_models_ui.button_submit.pack(
                expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    ## Viewpoint Menu Items
    def metadata_cleanup(self):
        try:
            ViewpointDataCleaner(self.master, BRAND_PIC_FILE, configdata.get("loglevel", "error"))
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    # DPE Menu Items #About
    def showinformation(self):
        try:
            self.informationwin = Toplevel(self.master)
            # mainwindow.wait_window(informationwin)
            version_info_details = f'''App Version: {VERSION_INFO.get("Version", "X.X.X")}
            Creator: Shouvik Das - Manager of PwC India Pvt.Ltd.
            Collaborator: Debolina Dutta, Aman Pratiush - Senior Associate of PwC India Pvt.Ltd, Chiranjib Bhattacharyya - Associate of PwC India Pvt.Ltd
            Created Date: {VERSION_INFO.get("CreatedDate", "10-10-2020")}
            Last Updated: {VERSION_INFO.get("LastUpdatedOn", "10-10-2020")}
            '''
            infoFrame = Frame(self.informationwin)
            infoFrame.pack(
                fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10
            )
            infolabel = Label(
                infoFrame,
                text=version_info_details,
            )
            infolabel.pack(
                fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10
            )
            infobtn = ttk.Button(
                infoFrame, text="Ok", command=lambda *args: self.closethiswindow(self.informationwin)
            )
            infobtn.pack(side="bottom", padx=10, pady=10, ipadx=10, ipady=10)
            self.informationwin.geometry("+200+200")
            self.informationwin.title("About the Application")
            self.informationwin.brandpic = PhotoImage(file=BRAND_PIC_FILE)
            self.informationwin.iconphoto(False, self.informationwin.brandpic)
            self.informationwin.resizable(False, False)
            self.informationwin.transient(self.master)
            self.master.wm_attributes("-disabled", True)
            self.informationwin.focus_set()
            self.informationwin.protocol(
                "WM_DELETE_WINDOW", lambda *args: self.closethiswindow(self.informationwin))
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            # self.loglist.insert(
            #     "end", "There are some errors. Please check log file.")

    def openMannual(self):
        try:
            webbrowser.register(
                "chrome",
                None,
                webbrowser.BackgroundBrowser(
                    "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"
                ),
            )
            chrome = webbrowser.get("chrome")
            chrome.open(
                "https://docs.google.com/document/d/1MM4xEzYwNfujr9pWIlKx_1FU9v3nk_12ixQibdzsCAY/edit?usp=sharing"
            )
        except:
            self.docLink()
            logger.error("Below Exception occurred\n", exc_info=True)

    def docLink(self):
        try:
            self.doclinkwin = Toplevel(self.master)
            infoFrame = Frame(self.doclinkwin)
            infoFrame.pack(
                fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10
            )
            w = Text(infoFrame, height=1, borderwidth=0)
            w.insert(
                1.0,
                "https://docs.google.com/document/d/1MM4xEzYwNfujr9pWIlKx_1FU9v3nk_12ixQibdzsCAY/edit?usp=sharing",
            )
            w.pack(fill="both", expand="yes", padx=10,
                   pady=10, ipadx=10, ipady=10)
            w.configure(state="disabled")
            infobtn = ttk.Button(
                infoFrame, text="Ok", command=lambda *args: self.closethiswindow(self.doclinkwin)
            )
            infobtn.pack(side="bottom", padx=15, pady=5, ipadx=15, ipady=5)
            self.doclinkwin.geometry("400x200+200+200")
            self.doclinkwin.title("Document Link")
            self.doclinkwin.resizable(False, False)
            self.doclinkwin.brandpic = PhotoImage(file=BRAND_PIC_FILE)
            self.doclinkwin.iconphoto(False, self.doclinkwin.brandpic)
            self.doclinkwin.resizable(False, False)
            self.doclinkwin.transient(self.master)
            self.master.wm_attributes("-disabled", True)
            self.doclinkwin.focus_set()
            self.doclinkwin.protocol(
                "WM_DELETE_WINDOW", lambda *args: self.closethiswindow(self.doclinkwin))
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def update_tool(self):
        """ 
        Update the tool with newer version
        """
        # os.system("updater.bat")
        self.master.destroy()
    
    def closethiswindow(self, top):
        try:
            self.master.focus_set()
            self.master.wm_attributes("-disabled", False)
            top.destroy()
        except:
            logger.error("Below Exception occured: ", exc_info=True)

####### END OF DPE DPE Inbox Clearing##########


class BasicConfigWindow:
    def __init__(self, master):
        # self.master = master
        self.master = master
        self.basicconfigwin = Toplevel(master)
        self.master.wm_attributes("-disabled", True)
        self.basicconfigwin.focus_set()
        self.basicconfigwin.title(APPLICATION_NAME + " - " + "Basic Settings")
        self.basicconfigwin.geometry("520x640+10+20")
        self.basicconfigwin.minsize(520, 640)
        self.basicconfigwin.maxsize(520, SCREEN_HEIGHT)
        self.basicconfigwin.resizable(width=False, height=True)
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.basicconfigwin.iconphoto(False, self.brandpic)
        self.basicconfigwin.transient(self.master)
        self.basicconfigwin.protocol("WM_DELETE_WINDOW", self.closethiswindow)
        self.style = ttk.Style()
        self.basicdata = basicconfigdata
        self.basicconfigmaindesign()

    def basicconfigframe(self):
        self.basicframe = LabelFrame(
            self.basicconfigwin, text="Basic Settings")
        self.basicframe.pack(fill="both", padx=10, pady=10, expand="yes")

    def enable_disable_input(self, data):
        try:
            if data == 0:
                self.save_username_entry["state"] = "disabled"
                self.save_password_entry["state"] = "disabled"
                self.env_details_combobox["state"] = "disabled"
            elif data == 1:
                self.save_username_entry["state"] = "normal"
                self.save_password_entry["state"] = "normal"
                self.env_details_combobox["state"] = "readonly"

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def basicconfigmaindesign(self):
        try:
            self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                basicconfigdata.get("production_passwd")) if basicconfigdata.get("production_passwd","").strip() != "" else basicconfigdata.get("production_passwd","").strip()
            self.varthemedata = StringVar()
            self.varthemedata.set(self.basicdata.get("selected theme","Clam").title())
            self.save_user_details_var = IntVar()
            self.save_user_details_var.set(
                int(self.basicdata.get("save_user_details",False)))
            self.var_save_username = StringVar()
            self.var_save_username.set(self.basicdata.get("production_username",""))
            self.var_save_password = StringVar()
            self.var_save_password.set(self.decrypted_passwd)
            self.env_details_var = StringVar()
            self.env_details_var.set("Production")

            # Validation of Checkbox
            self.save_user_details_var.trace(
                "w", lambda *args: self.enable_disable_input(
                    self.save_user_details_var.get())
            )

            self.basic_config_style = ttk.Style()
            self.basic_config_style.configure(
                "BW.TLabel", background="white", disabledforeground="lightgrey", disabledbackground="black")
            self.basic_config_style.configure(
                "BWDanger.TLabel", foreground="red")

            self.basicconfigframe()

            self.frame_1 = Frame(self.basicframe)
            self.frame_1.pack(padx=10, pady=10)

            self.themelabel = ttk.Label(
                self.frame_1,
                text="Select Theme",
                font=(FONT_NAME, FONT_SIZE - 2),
                anchor=CENTER,
            )
            self.themelabel.grid(
                row=0, column=0, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew"
            )
            self.frame_1.grid_columnconfigure(0, weight=1)
            self.themedata = [
                "",
                "Winnative",
                "Clam",
                "Alt",
                "Default",
                "Classic",
                "Vista",
                "XPNative",
            ]
            self.themeentry = ttk.OptionMenu(
                self.frame_1, self.varthemedata, *self.themedata
            )
            self.themeentry.grid(
                row=0, column=1, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew"
            )
            self.frame_1.grid_columnconfigure(1, weight=1)

            self.save_user_details_frame = LabelFrame(
                self.frame_1, text="Save user data")
            self.save_user_details_frame.grid(
                row=1, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")
            self.frame_1.grid_columnconfigure(0, weight=1)

            self.save_user_details_checkbtn = ttk.Checkbutton(
                self.save_user_details_frame, text="Save User Deatils", variable=self.save_user_details_var, onvalue=1, offvalue=0)
            self.save_user_details_checkbtn.grid(
                row=0, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")

            env_values = configdata.get("environments", []).copy()
            self.env_details_combobox = ttk.Combobox(
                self.save_user_details_frame, textvariable=self.env_details_var, state="readonly", values=env_values)
            self.env_details_combobox.grid(
                row=0, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")

            self.save_username_label = ttk.Label(
                self.save_user_details_frame, text="DPE Username", font=(FONT_NAME, FONT_SIZE-2), anchor=CENTER)
            self.save_username_label.grid(
                row=1, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")
            self.save_username_entry = ttk.Entry(
                self.save_user_details_frame, textvariable=self.var_save_username, style="BW.TLabel")
            self.save_username_entry.grid(
                row=1, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")
            self.save_user_details_frame.grid_columnconfigure(1, weight=1)
            self.save_password_label = ttk.Label(
                self.save_user_details_frame, text="DPE Password", font=(FONT_NAME, FONT_SIZE-2), anchor=CENTER)
            self.save_password_label.grid(
                row=2, column=0, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")
            self.save_password_entry = ttk.Entry(
                self.save_user_details_frame, show="*", textvariable=self.var_save_password, style="BW.TLabel")
            self.save_password_entry.grid(
                row=2, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")
            self.save_user_details_frame.grid_columnconfigure(1, weight=1)

            self.enable_disable_input(self.save_user_details_var.get())

            self.erro_show_label = ttk.Label(self.save_user_details_frame, text="", font=(
                FONT_NAME, FONT_SIZE-2), anchor=CENTER, style="BWDanger.TLabel")
            self.erro_show_label.grid(
                row=3, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")

            # Combox Event
            self.env_details_combobox.bind(
                "<<ComboboxSelected>>", self.change_environment)

            # Button
            self.frame_btn = Frame(self.basicconfigwin)
            self.frame_btn.pack(fill="both")
            self.style.configure("btnStyle.TButton", font=(FONT_NAME, 9))

            self.btncancel = ttk.Button(
                self.frame_btn,
                text="Cancel",
                style="btnStyle.TButton",
                command=self.closethiswindow,
            )  # lambda: self.configwin.destroy()
            self.btncancel.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5)
            self.btnsave = ttk.Button(
                self.frame_btn,
                text="Save Settings",
                style="btnStyle.TButton",
                command=self.savesettings,
            )
            self.btnsave.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5)

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def change_environment(self, event):
        try:
            selected_env = self.env_details_var.get().lower()
            self.var_save_username.set(
                self.basicdata.get(selected_env+"_username",""))
            self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                basicconfigdata.get(str(selected_env)+"_passwd","")) if basicconfigdata.get(str(selected_env)+"_passwd","").strip() != "" else basicconfigdata.get(str(selected_env)+"_passwd","").strip()
            self.var_save_password.set(self.decrypted_passwd)

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def closethiswindow(self):
        try:
            self.master.focus_set()
            self.master.wm_attributes("-disabled", False)
            self.basicconfigwin.destroy()
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def savesettings(self):
        try:
            global basicconfigdata
            selected_environment = self.env_details_var.get().lower()
            can_be_closed = False
            env_list = configdata.get("environments",[])
            if(self.save_user_details_var.get() == 0):
                self.basicdata["username"] = ""
                self.basicdata["passwd"] = ""
                for env in env_list:
                    self.basicdata[f"{env.lower()}_username"] = ""
                    self.basicdata[f"{env.lower()}_passwd"] = ""

                # can_be_closed = True

            elif(self.save_user_details_var.get() == 1):
                if(self.var_save_username.get().strip() != "" and self.var_save_password.get().strip() != ""):
                    self.basicdata[str(selected_environment)+"_username"] = self.var_save_username.get(
                    ).strip()
                    self.basicdata[str(selected_environment)+"_passwd"] = GenericFunctions.encrypt_passwd(
                        self.var_save_password.get().strip())
                    # can_be_closed = True
                else:
                    errorfields = []
                    if(self.var_save_username.get().strip() == ""):
                        errorfields.append("DPE Username")
                    if(self.var_save_password.get().strip() == ""):
                        errorfields.append("DPE Password")
                    # messagebox.showerror("Empty Mandatory Fields","Below fields are Mandatory\n"+",".join(errorfields),parent=self.basicconfigwin)
                    self.erro_show_label.config(
                        text="Below fields are Mandatory\n"+",".join(errorfields))

            self.basicdata["save_user_details"] = self.save_user_details_var.get()
            self.basicdata["selected theme"] = self.varthemedata.get(
            ).lower().strip()
            _config_saved = edcfg.updateConfig(
                self.basicdata, BASIC_CONFIG_FILE)
            basicconfigdata = self.basicdata

            can_be_closed = messagebox.askyesnocancel(
                "Please Confirm", "Data has been Saved Successfully.\nDo you want to Close the settings?", parent=self.basicconfigwin)

            if can_be_closed:
                self.closethiswindow()
        except:
            logger.error("Below Exception occured: ", exc_info=True)

####### END OF Basic Config Data ##########


class ConfigWindow:
    def __init__(self, master):
        # self.master = master
        global configdata
        self.master = master
        self.configwin = Toplevel(master)
        self.master.wm_attributes("-disabled", True)
        self.configwin.focus_set()
        self.configwin.title(APPLICATION_NAME + " - " + "Settings")
        self.configwin.geometry("+10+20")
        self.configwin.minsize(520, 520)
        self.configwin.maxsize(520, SCREEN_HEIGHT)
        self.configwin.resizable(width=False, height=True)
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.configwin.iconphoto(False, self.brandpic)
        self.configwin.transient(self.master)
        self.configwin.protocol("WM_DELETE_WINDOW", self.closethiswindow)
        self.style = ttk.Style()
        self.data = configdata
        self.configmaindesign()
        
        self.create_new_env_details = False
        self.edit_env_details = False
        # self.configwin.attributes('-topmost', 'true')

    def configlabelframe(self):
        # Start of Design
        self.envframe = LabelFrame(
            self.configwin, text="Environment Details", padx=10, pady=10
        )
        self.othersframe = LabelFrame(
            self.configwin, text="Other Settings", padx=10, pady=10
        )
        self.envframe.pack(fill="both", padx=5, pady=5)
        # self.varpathframe.pack(fill="both", padx=5, pady=5)
        self.othersframe.pack(fill="both", padx=5, pady=5)

    def define_style(self):
        try:
            self.window_style = ttk.Style()
            self.window_style.configure(
                "smalltableStyle.Treeview", highlightthickness=2, bd=2, font=(FONT_NAME, 9))
            self.window_style.configure(
                "smalltableStyle.Treeview.Heading", font=(FONT_NAME, 9, "bold"))
            self.window_style.configure(
                "treeStyle.Treeview", highlightthickness=2, bd=2, font=(FONT_NAME, FONT_SIZE))
            self.window_style.configure(
                "treeStyle.Treeview.Heading", font=(FONT_NAME, FONT_SIZE, "bold"))
            self.window_style.configure(
                "smallBtn.TButton", font=(FONT_NAME, 8), relief="flat") #smallbuttondesign
            self.window_style.configure(
                "smallbuttondesign.TButton", font=(FONT_NAME, 10))
            self.window_style.configure(
                "mainBtn.TButton", font=(FONT_NAME, FONT_SIZE), relief="raised")
            self.window_style.configure("scrollbarmain.TScrollbar", background="Green", darkcolor="DarkGreen",
                                        lightcolor="LightGreen", troughcolor="gray", bordercolor="blue", arrowcolor="white")
            self.window_style.configure(
                "green.Horizontal.TProgressbar", foreground='green', background='darkgreen')

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def initiate_variables(self):
        try:
            self.varenvironment.set("--ADD NEW--")
            self.varenvironmentname.set("")
            self.varenvironmenturl.set("")
            self.varenvironmentvarpath.set("")
            self.varenvironmentredirectdotcom.set("")
            self.varenvironmentredirectsand.set("")
            self.varloglevel.set(self.data.get("loglevel","error").upper())
            self.varsleeptime.set(self.data.get("sleeptime","1.0"))
            self.vartimeout.set(self.data.get("timeout","20.0"))
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def configmaindesign(self):
        try:
            self.define_style()
            # data = self.data
            self.varenvironment = StringVar()
            self.varenvironmentname = StringVar()
            self.varenvironmenturl = StringVar()
            self.varenvironmentvarpath = StringVar()
            self.varenvironmentredirectsand = StringVar()
            self.varenvironmentredirectdotcom = StringVar()
            self.varloglevel = StringVar()
            self.varsleeptime = StringVar()
            self.vartimeout = StringVar()

            self.initiate_variables()

            # Validation
            self.vartimeout.trace(
                "w", lambda *args: self.validate_input(self.vartimeout))
            self.varsleeptime.trace(
                "w", lambda *args: self.validate_input(self.varsleeptime))
            self.varenvironment.trace("w", lambda *args: self.change_env_dropdown(self.varenvironment))

            # Label Frame
            self.configlabelframe()
            env_data = self.data.get("environments", [])
            # env_data.remove("IP")
            self.envdata = env_data.copy()
            self.envdata.insert(0,"--ADD NEW--")
            # Widget Adding
            self.main_frame = Frame(self.envframe)
            self.main_frame.pack(fill="both")
            self.select_frame = Frame(self.main_frame)
            self.select_frame.pack(fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.env_combobox = ttk.Combobox(self.select_frame, textvariable=self.varenvironment, state="readonly", values=self.envdata)
            self.env_combobox.pack(
                side="left",fill="x", ipadx=5, ipady=5, anchor="center")

            self.edit_or_add_rpt_btn = ttk.Button(self.select_frame, text="Add/Edit", command=self.add_or_edit_env, style="smallBtn.TButton")
            self.edit_or_add_rpt_btn.pack(side="left", padx=5, ipadx=2, ipady=5, anchor="center")

            self.remove_selected = ttk.Button(self.select_frame, text="Remove Selected", command=self.remove_selected_environments, style="smallBtn.TButton")
            self.remove_selected.pack(side="left", padx=5, ipadx=5, ipady=5, anchor="center")

            self.main_edit_frame = LabelFrame(self.main_frame, text="Add or Edit Environment")
            self.main_edit_frame.pack(fill="both", expand="yes", padx=10, pady=5, ipadx=10, ipady=5, anchor="center")

            ## Env Name
            self.new_env_name_frame = Frame(self.main_edit_frame)
            self.new_env_name_frame.pack(fill="x", pady=5)
            self.new_env_name_label = ttk.Label(self.new_env_name_frame, text="Environemnt Name")
            self.new_env_name_label.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)
            self.new_env_name_ent = ttk.Entry(self.new_env_name_frame, state="disabled", textvariable=self.varenvironmentname)
            self.new_env_name_ent.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)
            #Env URL
            self.new_env_url_frame = Frame(self.main_edit_frame)
            self.new_env_url_frame.pack(fill="x", pady=5)
            self.new_env_url_label = ttk.Label(self.new_env_url_frame, text="URL")
            self.new_env_url_label.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)
            self.new_env_url_ent = ttk.Entry(self.new_env_url_frame, state="disabled", textvariable=self.varenvironmenturl)
            self.new_env_url_ent.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)

            #Env Varpath
            self.new_env_varpath_frame = Frame(self.main_edit_frame)
            self.new_env_varpath_frame.pack(fill="x", pady=5)
            self.new_env_varpath_label = ttk.Label(self.new_env_varpath_frame, text="Variable Path")
            self.new_env_varpath_label.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)
            self.new_env_varpath_ent = ttk.Entry(self.new_env_varpath_frame, state="disabled", textvariable=self.varenvironmentvarpath)
            self.new_env_varpath_ent.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)

            #Env Redirectpath .com
            self.new_env_redirect_docom_frame = Frame(self.main_edit_frame)
            self.new_env_redirect_docom_frame.pack(fill="x", pady=5)
            self.new_env_redirect_docom_label = ttk.Label(self.new_env_redirect_docom_frame, text="Redirect Path .com")
            self.new_env_redirect_docom_label.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)
            self.new_env_redirect_docom_ent = ttk.Entry(self.new_env_redirect_docom_frame, state="disabled", textvariable=self.varenvironmentredirectdotcom)
            self.new_env_redirect_docom_ent.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)

            #Env Redirectpath s&
            self.new_env_redirect_sand_frame = Frame(self.main_edit_frame)
            self.new_env_redirect_sand_frame.pack(fill="x", pady=5)
            self.new_env_redirect_sand_label = ttk.Label(self.new_env_redirect_sand_frame, text="Redirect Path s&")
            self.new_env_redirect_sand_label.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)
            self.new_env_redirect_sand_ent = ttk.Entry(self.new_env_redirect_sand_frame, state="disabled", textvariable=self.varenvironmentredirectsand)
            self.new_env_redirect_sand_ent.pack(side="left", fill="x", expand="yes", anchor="w", padx=5)

            self.cancel_btn_frame = Frame(self.main_frame)
            self.cancel_btn_frame.pack(fill="x", expand="yes", padx=10, pady=5, ipadx=10, ipady=5, anchor="center")

            self.cancel_btn = ttk.Button(self.cancel_btn_frame, text="Cancel", state="disabled", command=lambda *args: self.toggle_input_field("disabled"), style="smallBtn.TButton")
            self.cancel_btn.pack(side="right", expand="yes", anchor="e")

            ###########
            self.frame_2 = Frame(self.othersframe)
            self.frame_2.pack(fill="both", expand="yes")
            # loglevel, sleeptime, timeout, isquerybuilder

            # Loglevel
            self.loglabel = LabelFrame(self.frame_2, text="Loglevel")
            logdata = ["", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAl"]
            self.logent = ttk.OptionMenu(
                self.loglabel, self.varloglevel, *logdata)
            self.logent.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.loglabel.grid_columnconfigure(0, weight=1)
            self.loglabel.pack(side="left", expand="yes", fill="both")

            # Sleeptime
            self.sleeptimelabel = LabelFrame(self.frame_2, text="Sleep time")
            # sleeptimedata = [0, 0, 1, 2, 3, 4, 5]
            # self.sleeptimeent = ttk.OptionMenu(
            #     self.sleeptimelabel, self.varsleeptime, *sleeptimedata
            # )
            # self.sleeptimeent.grid(
            #     row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.sleeptimeent = ttk.Entry(
                self.sleeptimelabel, textvariable=self.varsleeptime)
            self.sleeptimeent.grid(
                row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.sleeptimelabel.grid_columnconfigure(0, weight=1)
            self.sleeptimelabel.pack(side="left", expand="yes", fill="both")

            # Timeout
            self.timeoutlabel = LabelFrame(
                self.frame_2, text="Connection timeout")
            # timeoutdata = [0, 0, 5, 10, 20, 30, 40, 50, 60, 90, 120]
            # self.timeoutent = ttk.OptionMenu(
            #     self.timeoutlabel, self.vartimeout, *timeoutdata
            # )
            # self.timeoutent.grid(row=0, column=0, padx=5,
            #                      pady=5, sticky="nsew")
            self.timeoutent = ttk.Entry(
                self.timeoutlabel, textvariable=self.vartimeout)
            self.timeoutent.grid(row=0, column=0, padx=5,
                                 pady=5, sticky="nsew")
            self.timeoutlabel.grid_columnconfigure(0, weight=1)
            self.timeoutlabel.pack(side="left", expand="yes", fill="both")

            # Button
            self.frame_btn = Frame(self.configwin)
            self.frame_btn.pack(fill="both")
            self.style.configure("btnStyle.TButton",
                                 font=(FONT_NAME, FONT_SIZE - 3))

            self.btncancel = ttk.Button(
                self.frame_btn,
                text="Cancel",
                style="btnStyle.TButton",
                command=self.closethiswindow,
            )  # lambda: self.configwin.destroy()
            self.btncancel.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5)
            self.btnsave = ttk.Button(
                self.frame_btn,
                text="Save Settings",
                style="btnStyle.TButton",
                command=self.savesettings,
            )
            self.btnsave.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5)

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def change_env_dropdown(self, varenvironment):
        try:
            cap_env_name = str(varenvironment.get())
            cap_env_name = "" if cap_env_name == "--ADD NEW--" else cap_env_name
            env_name = cap_env_name.lower()
            varpathname = f"varpath{env_name}"
            redirectpathdotcom = f"redirectpathdotcom{env_name}"
            redirectpathsand = f"redirectpathsand{env_name}"
            self.varenvironmentname.set(cap_env_name)
            self.varenvironmenturl.set(self.data.get(env_name,""))
            self.varenvironmentvarpath.set(self.data.get(varpathname,""))
            self.varenvironmentredirectdotcom.set(self.data.get(redirectpathdotcom,""))
            self.varenvironmentredirectsand.set(self.data.get(redirectpathsand,""))
            self.toggle_input_field("disabled")
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def add_or_edit_env(self):
        try:
            selected_env = str(self.varenvironment.get()).lower()
            # self.create_new_env_details
            if selected_env == "--add new--":
                self.create_new_env_details = True
            else:
                self.edit_env_details = True
            self.toggle_input_field("normal",True)
            
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def toggle_input_field(self, state, ip_exception=False):
        try:
            self.new_env_name_ent["state"] = state
            self.new_env_url_ent["state"] = state
            self.new_env_varpath_ent["state"] = state
            self.new_env_redirect_docom_ent["state"] = state
            self.new_env_redirect_sand_ent["state"] = state
            self.cancel_btn["state"] = state
            selected_env = str(self.varenvironment.get()).lower()

            if selected_env != "--add new--":
                self.new_env_name_ent["state"] = "disabled"
                
            if ip_exception:
                env_name = str(self.varenvironment.get()).lower()
                if env_name == "ip":
                    self.new_env_name_ent["state"] = "disabled"
                    self.new_env_url_ent["state"] = "disabled"
            
            if state == "disabled":
                self.create_new_env_details = False
                self.edit_env_details = False

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def closethiswindow(self):
        try:
            self.master.focus_set()
            self.master.wm_attributes("-disabled", False)
            self.configwin.destroy()
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def validate_input(self, text_variable):
        try:
            dt = text_variable.get()
            if dt.strip() != "":
                if dt[-1] == ".":
                    if dt.count(".") > 1:
                        text_variable.set(dt[:-1])
                elif not(dt[-1].isnumeric() or dt[-1] == "."):
                    text_variable.set(dt[:-1])
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def savesettings(self):
        try:
            # global root
            global configdata
            _environments = configdata.get("environments", [])
            _environment = str(self.varenvironment.get()).lower()
            _env_name = str(self.varenvironmentname.get()).upper()
            _env_url = str(self.varenvironmenturl.get())
            _env_varpath = str(self.varenvironmentvarpath.get())
            _env_redirectpathdotcom = str(self.varenvironmentredirectdotcom.get())
            _env_redirectpathsand = str(self.varenvironmentredirectsand.get())

            env_name = GenericFunctions.removetrailingspecialchar(_env_name)
            env_url = GenericFunctions.removetrailingspecialchar(_env_url)
            is_ip_env = GenericFunctions.validateIP(env_url, "ip")
            env_name = f"IP_{env_name}" if is_ip_env else env_name
            lower_env_name = env_name.lower()
            env_varpath = GenericFunctions.removetrailingspecialchar(_env_varpath)
            env_redirectpathdotcom = GenericFunctions.removetrailingspecialchar(_env_redirectpathdotcom)
            env_redirectpathsand = GenericFunctions.removetrailingspecialchar(_env_redirectpathsand)
            logdt = GenericFunctions.removetrailingspecialchar(
                self.varloglevel.get().strip()
            )
            is_new_env = False
            if _environment == "--add new--":
                is_new_env = True
            
            sleepdata = float(self.varsleeptime.get())
            timeoutdt = float(self.vartimeout.get())
            # query = self.varquery.get()
            #validation
            is_not_empty_env_name = True if bool(env_name.strip()) else False
            is_not_empty_env_url = True if env_name.strip().lower() == "ip" else (True if bool(env_url.strip()) else False)
            is_not_empty_env_varpath = True if bool(env_varpath.strip()) else False
            is_not_empty_env_redirectpathdotcom = True if env_name.strip().lower() == "ip" else (True if bool(env_redirectpathdotcom.strip()) else False)
            is_not_empty_env_redirectpathsand = True if env_name.strip().lower() == "ip" else (True if bool(env_redirectpathsand.strip()) else False)
            is_not_empty_logdt = True if bool(logdt.strip()) else False
            is_valid_sleep_data = True if bool(sleepdata) and sleepdata>0 else False
            is_valid_timeoutdt = True if bool(timeoutdt) and timeoutdt>0 else False
            is_valid_varpath = GenericFunctions.is_valid_dpepath(env_varpath, env_name, "/var/workflow/instances")
            is_valid_redirectdotcompath = GenericFunctions.is_valid_dpepath(env_redirectpathdotcom, env_name, "/etc/map/http")
            is_valid_redirectsandpath = GenericFunctions.is_valid_dpepath(env_redirectpathsand, env_name, "/etc/map/http")

            logger.info("Env: %s, URL: %s, Varpath: %s, Loglevel: %s, Sleeptime: %s, Timeout: %s", env_name, env_url, env_varpath, logdt, sleepdata, timeoutdt)
            environment_validation = (is_not_empty_env_name and is_not_empty_env_url and is_not_empty_env_varpath and is_valid_varpath and is_valid_redirectdotcompath and is_valid_redirectsandpath
                    and is_not_empty_env_redirectpathdotcom and is_not_empty_env_redirectpathsand)
            is_env_validated = environment_validation if self.create_new_env_details or self.edit_env_details else True
            if (is_env_validated and is_not_empty_logdt and is_valid_sleep_data and is_valid_timeoutdt):
                
                if self.create_new_env_details:
                    if env_name not in _environments: _environments.append(env_name)
                    else: raise ValueError(f"{env_name} already in the environment list, Please edit.")
                if self.create_new_env_details or self.edit_env_details:
                    configdata[lower_env_name] = env_url
                    configdata[f"varpath{lower_env_name}"] = env_varpath
                    configdata[f"redirectpathdotcom{lower_env_name}"] = env_redirectpathdotcom
                    configdata[f"redirectpathsand{lower_env_name}"] = env_redirectpathsand
                configdata["loglevel"] = logdt.lower()
                configdata["sleeptime"] = sleepdata
                configdata["timeout"] = timeoutdt
                # configdata["isquerybuilder"] = query
                _config_saved = edcfg.updateConfig(configdata, CONFIG_FILE)
                # self.parent.varquery.set(configdata["isquerybuilder"])
                self.closethiswindow()

            else:
                errors = []
                if not is_not_empty_env_name: errors.append("Env name can't be empty")
                if not is_not_empty_env_url: errors.append("Env url can't be empty")
                if not is_not_empty_logdt: errors.append("Select a valid Loglevel")
                if not is_valid_sleep_data: errors.append("Sleep should be more than 0")
                if not is_valid_timeoutdt: errors.append("Timout should be more than 0")
                if not is_valid_varpath: errors.append("Varpath should be nonempty and\n starts with /var/workflow/instances")
                if not is_valid_redirectdotcompath: errors.append(".com Redirectpath should be nonempty and\n starts with /etc/map/http")
                if not is_valid_redirectsandpath: errors.append("s& Redirectpath should be nonempty and\n starts with /etc/map/http")

                msg = "\n".join([f"{i}. {x}" for i,x in enumerate(errors, start=1) if x.strip() != ""])

                messagebox.showerror(
                    "Error in Data",
                    msg,
                    parent=self.configwin,
                )
                logger.warning("Error in Data, %s", ",".join(errors).replace("\n", " "))
        except ValueError as ve:
            messagebox.showerror(
                    "Error in Data",
                    ve,
                    parent=self.configwin,)
            logger.error("Below Exception occurred\n", exc_info=True)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def remove_selected_environments(self):
        try:
            global configdata
            confirm = messagebox.askyesnocancel(
                                title="Please Confirm",
                                message="Do you want to DELETE the selected Env,\nThis is irreversible?",
                                parent=self.configwin
                            )
            if confirm:
                selected_env = str(self.varenvironment.get()).lower()
                u_selected_env = selected_env.upper()

                if selected_env == "--add new--":
                    messagebox.showerror("Failed", "Can't Perform the operation", parent=self.configwin)
                else:
                    environments = configdata.get("environments", [])
                    if u_selected_env in environments:
                        environments.remove(u_selected_env)
                        try:
                            configdata.pop(selected_env)
                        except:
                            logger.error(f"{selected_env} not Present in Config\n", exc_info=True)
                        try:
                            configdata.pop(f"varpath{selected_env}")
                        except:
                            logger.error(f"{selected_env} not Present in Config\n", exc_info=True)
                        try:
                            configdata.pop(f"redirectpathdotcom{selected_env}")
                        except:
                            logger.error(f"{selected_env} not Present in Config\n", exc_info=True)
                        try:
                            configdata.pop(f"redirectpathsand{selected_env}")
                        except:
                            logger.error(f"{selected_env} not Present in Config\n", exc_info=True)
                            
                        _config_saved = edcfg.updateConfig(configdata, CONFIG_FILE)
                        if _config_saved:
                            self.remove_basic_config_data_and_save(selected_env)
                            final_env_data = environments.copy()
                            final_env_data.insert(0, "--ADD NEW--")
                            self.env_combobox['values'] = final_env_data
                            self.initiate_variables()

                    else:
                        raise ValueError("Can't perform the operation, Bad config files.")
        
        except ValueError as ve:
            messagebox.showerror(
                    "Error in Data",
                    ve,
                    parent=self.configwin,)
            logger.error("Below Exception occurred\n", exc_info=True)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def remove_basic_config_data_and_save(self, env_name):
        try:
            global basicconfigdata
            u_name = f"{env_name}_username"
            password = f"{env_name}_passwd"

            try:
                basicconfigdata.pop(u_name)
            except:
                logger.warning("%s is not present in Saved Details", u_name)

            try:
                basicconfigdata.pop(password)
            except:
                logger.warning("%s is not present in Saved Details", password)

            _basicconfig_saved = edcfg.updateConfig(basicconfigdata, BASIC_CONFIG_FILE)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

####### END OF Config Window  ##########


class OperationsWindow:
    def __init__(self, master):
        global operationdata
        self.master = master
        self.operationwin = Toplevel(master)
        self.master.wm_attributes("-disabled", True)
        self.operationwin.focus_set()
        self.operationwin.title(APPLICATION_NAME + " - " + "Operations Code")
        self.operationwin.geometry("+10+20")
        self.operationwin.minsize(520, 640)
        self.operationwin.maxsize(520, SCREEN_HEIGHT)
        self.operationwin.resizable(width=False, height=True)
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.operationwin.iconphoto(False, self.brandpic)
        self.operationwin.transient(self.master)
        self.operationwin.protocol("WM_DELETE_WINDOW", self.closethiswindow)
        self.styleoperationwin = ttk.Style()
        self.data = configdata
        self.operationmaindesign()
        # self.operationwin.attributes('-topmost', 'true')

    def operationlabelframe(self):
        try:
            # Start of Design
            self.titleframe = Frame(self.operationwin)
            self.editframe = LabelFrame(
                self.operationwin, text="Edit the Data", padx=10, pady=10
            )
            self.titleframe.pack(fill="both", padx=5, pady=5)
            self.editframe.pack(fill="both", padx=5, pady=5)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def operationmaindesign(self):
        try:
            localfontsize = FONT_SIZE - 3
            # String Variable
            self.varnewval = StringVar()
            self.varnewval.set("")
            self.enabledisablevar = IntVar()
            self.enabledisablevar.set(2)

            # Validation
            self.enabledisablevar.trace(
                "w", lambda *args: self.enabledisableinput(
                    self.enabledisablevar.get())
            )

            # Label Frame
            self.operationlabelframe()

            # Adding Widgets
            self.frame_1 = Frame(self.titleframe)
            self.frame_1.pack(fill="both", expand="yes")
            self.titlelabel = ttk.Label(
                self.frame_1,
                text="Operations Code",
                anchor=CENTER,
                font=(FONT_NAME, localfontsize + 4, "italic"),
                borderwidth=2,
                relief="groove",
            )
            self.titlelabel.pack(
                fill="x",
                expand="yes",
                padx=5,
                pady=5,
                ipadx=5,
                ipady=5,
                anchor="center",
            )
            self.enableframe = LabelFrame(self.frame_1)
            self.enableradio = ttk.Radiobutton(
                self.enableframe, text="Enable", variable=self.enabledisablevar, value=1
            )
            self.enableradio.grid(row=0, column=0, sticky="nsew")
            self.enableframe.grid_columnconfigure(0, weight=1)
            self.disableradio = ttk.Radiobutton(
                self.enableframe,
                text="Disable",
                variable=self.enabledisablevar,
                value=2,
            )
            self.disableradio.grid(row=0, column=1, sticky="nsew")
            self.enableframe.grid_columnconfigure(1, weight=1)
            self.enableframe.pack(
                fill="both",
                expand="yes",
                padx=5,
                pady=5,
                ipadx=5,
                ipady=5,
                anchor="center",
            )

            # Treeview
            self.treeframe_1 = Frame(self.editframe)
            self.treeframe_1.pack(fill="both", expand="yes")

            self.styleoperationwin.configure(
                "treeStyle.Treeview",
                highlightthickness=2,
                bd=2,
                font=(FONT_NAME, localfontsize),
            )
            self.styleoperationwin.configure(
                "treeStyle.Treeview.Heading", font=(FONT_NAME, localfontsize, "bold")
            )
            self.styleoperationwin.configure(
                "btnStyle.TButton", font=(FONT_NAME, FONT_SIZE - 3)
            )

            self.tree = ttk.Treeview(
                self.treeframe_1,
                column=("No#", "Operation", "Code"),
                style="treeStyle.Treeview",
                show="headings",
                height="10",
                selectmode="browse",
            )

            # Scrollbar
            self.scroll_y = ttk.Scrollbar(
                self.treeframe_1, orient=VERTICAL, command=self.tree.yview
            )
            self.tree.config(yscrollcommand=self.scroll_y.set)
            self.scroll_y.pack(side="right", fill="y")
            self.scroll_x = ttk.Scrollbar(
                self.treeframe_1, orient=HORIZONTAL, command=self.tree.xview
            )
            self.tree.config(xscrollcommand=self.scroll_x.set)
            self.scroll_x.pack(side="bottom", fill="x", expand="yes")
            self.tree.bind("<Double-Button-1>", self.getDataandFill)

            # Tree Column
            self.tree.column("#0", width=1)  # ,minwidth=1
            self.tree.column("No#", width=50)  # ,minwidth=30,
            # ,minwidth=180,stretch=NO
            self.tree.column("Operation", width=180)
            self.tree.column(
                "Code", width=480, minwidth=480, stretch=YES
            )  # ,minwidth=90

            # Tree Heading
            self.tree.heading("#0", anchor=CENTER)
            self.tree.heading("No#", text="No.", anchor=CENTER)
            self.tree.heading("Operation", text="Operations", anchor=CENTER)
            self.tree.heading("Code", text="Code", anchor=NW)

            # Insert Data in Treeview
            self.insertTree()
            self.tree.pack(fill="both", expand="yes", ipadx=10, ipady=10)

            #######################
            self.editframe_1 = Frame(self.editframe)
            self.editframe_1.pack(fill="both", expand="yes", padx=5, pady=5)

            self.operationlabel = ttk.Label(
                self.editframe_1,
                anchor=CENTER,
                text="Operation Title",
                font=(FONT_NAME, localfontsize),
                borderwidth=2,
                relief="groove",
            )
            self.operationlabel.grid(
                row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew"
            )
            self.operationtitlelabel = ttk.Label(
                self.editframe_1,
                anchor=CENTER,
                text="",
                font=(FONT_NAME, localfontsize),
                borderwidth=2,
                relief="groove",
            )
            self.operationtitlelabel.grid(
                row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew"
            )
            self.editframe_1.grid_columnconfigure(1, weight=1)

            self.currlabel = ttk.Label(
                self.editframe_1,
                anchor=CENTER,
                text="Current Value",
                font=(FONT_NAME, localfontsize),
                borderwidth=2,
                relief="groove",
            )
            self.currlabel.grid(
                row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew"
            )
            self.currvaluelabel = ttk.Label(
                self.editframe_1,
                text="",
                font=(FONT_NAME, localfontsize),
                borderwidth=2,
                relief="groove",
                anchor="w",
                justify=LEFT,
                wraplength=330,
            )
            self.currvaluelabel.grid(
                row=1, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew"
            )
            self.editframe_1.grid_columnconfigure(1, weight=1)

            self.newvallabel = ttk.Label(
                self.editframe_1,
                anchor=CENTER,
                text="New Value",
                font=(FONT_NAME, localfontsize),
                borderwidth=2,
                relief="groove",
            )
            self.newvallabel.grid(
                row=2, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew"
            )
            self.newvalent = ttk.Entry(
                self.editframe_1, textvariable=self.varnewval)
            self.newvalent.grid(
                row=2, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew"
            )
            self.editframe_1.grid_columnconfigure(1, weight=1)

            #############
            self.frame_btn = Frame(self.operationwin)
            self.frame_btn.pack(fill="both")

            self.btncancel = ttk.Button(
                self.frame_btn,
                text="Exit",
                style="btnStyle.TButton",
                command=self.closethiswindow,
            )  # lambda:self.operationwin.destroy()
            self.btncancel.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5)
            self.btnreset = ttk.Button(
                self.frame_btn,
                text="Reset",
                style="btnStyle.TButton",
                command=self.resetall,
            )
            self.btnreset.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5)
            self.btnsave = ttk.Button(
                self.frame_btn,
                text="Save Settings",
                style="btnStyle.TButton",
                command=self.savesettings,
            )
            self.btnsave.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5)

            if self.enabledisablevar.get() == 2:
                self.newvalent["state"] = "disabled"
                self.btnsave["state"] = "disabled"
                self.btnreset["state"] = "disabled"

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def closethiswindow(self):
        self.master.focus_set()
        self.master.wm_attributes("-disabled", False)
        self.operationwin.destroy()

    def savesettings(self):
        try:
            global operationdata
            key = self.operationtitlelabel.cget("text").lower()
            if key.strip() != "":
                if self.varnewval.get().strip() != "":
                    logger.debug(
                        "NewVal before removing trailing space: "+str(self.varnewval.get()))
                    data = GenericFunctions.removetrailingspecialchar(
                        self.varnewval.get().strip()
                    )
                    logger.debug(
                        "NewVal after removing trailing space: "+str(data))
                    
                    c_data = int(data) if GenericFunctions.is_signed_numeric(data) else data
                    if key == "crxde max array items" and c_data > 400:
                        messagebox.showerror(
                            "Error in Data",
                            "Maximum Array items that is allowed is 400",
                            parent=self.operationwin,
                            )
                        logger.error("Maximum Array items that is allowed is 400. Entered value is %s", c_data)
                    else:
                        operationdata[key] = c_data
                        _config_saved = edcfg.updateConfig(
                            operationdata, OPERATION_CODE_FILE)
                        self.operationdata = operationdata
                        logger.debug("Form Operations Data: "+str(operationdata))
                        self.insertTree()
                        self.resetall()
                else:
                    messagebox.showerror(
                        "Error in Data",
                        "New Value Can't be blank",
                        parent=self.operationwin,
                    )
                    logger.warning("New Value Can't be blank")
            else:
                messagebox.showerror(
                    "Error in Process",
                    "Please Select a Value to Edit",
                    parent=self.operationwin,
                )
                logger.warning(
                    "Please Select a Value to Edit. Key Field is Empty")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetall(self):
        try:
            self.operationtitlelabel.config(text="")
            self.currvaluelabel.config(text="")
            self.varnewval.set("")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def enabledisableinput(self, val):
        try:
            if val == 1:
                self.newvalent["state"] = "normal"
                self.btnsave["state"] = "normal"
                self.btnreset["state"] = "normal"
            elif val == 2:
                self.newvalent["state"] = "disabled"
                self.btnsave["state"] = "disabled"
                self.btnreset["state"] = "disabled"
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def getDataandFill(self, event):
        try:
            item = self.tree.item(self.tree.focus())
            values = item["values"]
            self.operationtitlelabel.config(text=values[1])
            self.currvaluelabel.config(
                text=GenericFunctions.wrap_text_with_dot(values[2], 50))
            self.varnewval.set(values[2])
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def insertTree(self):
        try:
            self.operationdata = edcfg.readConfig(OPERATION_CODE_FILE)
            operationdata = self.operationdata
            self.tree.delete(*self.tree.get_children())
            treecounter = 0
            for data in self.operationdata:
                t_value = (
                    str(treecounter + 1),
                    data.title(),
                    self.operationdata[data],
                    40,
                )
                self.tree.insert(
                    "", "end", iid=treecounter, text=str(treecounter), values=t_value
                )
                treecounter += 1
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

####### END OF Operations Window  ##########

# Start of Page Unlock
class  UnlockDPEPages:
    def __init__(self, master):
        self.dpe_page_unlock_ui = Toplevel(master)
        self.master = master
        self.dpe_page_unlock_ui.state('zoomed')
        master.withdraw()
        self.dpe_page_unlock_ui.title(
            APPLICATION_NAME + " - " + "Unlock DPE Page(s)"
        )
        self.dpe_page_unlock_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.dpe_page_unlock_ui.iconphoto(False, self.brandpic)
        self.dpe_page_unlock_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.dpe_page_unlock_ui.configdata = configdata
        self.dpe_page_unlock_ui.excelfile = ""
        self.dpe_page_unlock_ops_instances = None
        
        self.create_menu_bar()
        self.main_design()
    
    def create_menu_bar(self):
        try:
            file_url = "https://docs.google.com/spreadsheets/d/1mvZsBt9iylSjnr8Enbw_xBR4Fjohk3djibMXsJKgXP0/export?format=xlsx&gid=0"
            self.main_menu = Menu(self.dpe_page_unlock_ui)
            self.downloadmenu = Menu(self.main_menu, tearoff=0)
            self.downloadmenu.add_command(
                label="Payloads", command=lambda *args: GenericFunctions.download_google_sheet(file_url)
            )
            self.main_menu.add_cascade(
                label="Sample File", menu=self.downloadmenu)
            self.dpe_page_unlock_ui.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state("zoomed")
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.dpe_page_unlock_ui.destroy()
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
            self.var_selected_source.set("Source Data from Excel")
            self.varipdata.set("")
            self.varpassent.set(self.decrypted_passwd)
            self.varexcelfile.set("Browse & Select Excel File")
            self.varuseroperation.set("--SELECT--")
            self.vartounlockpage.set("")
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

    def main_design(self):
        try:
            # Declare String Variable
            self.define_style()

            # String Variable
            self.var_selected_source = StringVar()
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varexcelfile = StringVar()
            self.varuseroperation = StringVar()
            self.vartounlockpage = StringVar()

            # Initiate String Variable
            self.initiate_var()

            # Validation
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))
            self.var_selected_source.trace(
                "w", lambda *args: self.changeoptionbox(self.var_selected_source.get()))

            # Frame Creation
            self.main_frame = Frame(self.dpe_page_unlock_ui)
            self.main_frame.pack(fill="x")

            self.main_btn_frame_sep = ttk.Separator(
                self.dpe_page_unlock_ui)
            self.main_btn_frame_sep.pack(fill="x", padx=5, pady=10)

            self.main_btn_frame = Frame(self.dpe_page_unlock_ui)
            self.main_btn_frame.pack(fill="x")

            self.btn_frame_details_sep = ttk.Separator(
                self.dpe_page_unlock_ui)
            self.btn_frame_details_sep.pack(fill="x", padx=5, pady=10)

            self.main_details_frame = Frame(self.dpe_page_unlock_ui)
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
                self.iplabelframe, textvariable = self.varenvdata, values = self.envdata, state="readonly")
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
                row=1, column=0, columnspan=4, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.source_dropdown_data = [
                "", "Source Data from Excel", "Enter Payload (Comma Seperated)"]  # , "Use Query Builder"
            self.source_dropdown_ent = ttk.OptionMenu(
                self.selectionlabelframe, self.var_selected_source, *self.source_dropdown_data)  # , command=self.changecheckbox
            self.source_dropdown_ent.grid(row=0, column=0, padx=5,
                                          pady=5, sticky="nsew")

            # Query Window or Excel Window
            self.select_file_btn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.select_file_btn.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.selected_file_label = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..", textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),
                                                 )
            self.selected_file_label.grid(
                row=0, column=2, padx=5, pady=5, sticky="nsew")
            self.to_unlock_ent = Entry(self.selectionlabelframe, textvariable=self.vartounlockpage)

            self.selectionlabelframe.grid_columnconfigure(2, weight=1)

            
            # Button
            self.user_start_operation_btn = ttk.Button(
                self.main_btn_frame, text="Unlock Page(s)", style="mainBtn.TButton", command=self.unlock_dpe_pages)  # , command=self.retrvdata
            self.user_start_operation_btn.pack(
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

            self.total_hits_label = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE - 2))
            self.total_hits_label.pack(side="left", padx=5, pady=0, anchor="w")

            self.retrieve_data_count_label = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE-2))
            self.retrieve_data_count_label.pack(
                side="left", padx=5, pady=0, anchor="w")
            
            self.retrieve_data_count_label_error = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE-2))
            self.retrieve_data_count_label_error.pack(
                side="left", padx=5, pady=0, anchor="w")

            # Tree Frame
            self.data_tree_frame = Frame(self.main_details_frame)

            self.data_tree = ttk.Treeview(
                self.data_tree_frame, style="treeStyle.Treeview", show="headings", columns=("1", "2","3"), selectmode="extended", height=20)

            self.data_tree_scroll_y = ttk.Scrollbar(
                self.data_tree_frame, orient="vertical", command=self.data_tree.yview)
            self.data_tree.config(yscrollcommand=self.data_tree_scroll_y.set)
            self.data_tree_scroll_y.pack(side="right", fill="y")

            self.data_tree_scroll_x = ttk.Scrollbar(
                self.data_tree_frame, orient="horizontal", command=self.data_tree.xview)
            self.data_tree.config(xscrollcommand=self.data_tree_scroll_x.set)
            self.data_tree_scroll_x.pack(side="bottom", fill="x")

            self.data_tree.pack(fill="both", expand="yes")

            self.data_tree.bind("<<Copy>>", self.getDataandCopy)
            # self.data_tree.bind('<Double-Button-1>', self.edit_data_popup)

            self.data_tree_frame.pack(
                fill="both", padx=5, pady=10)

            self.dpe_page_unlock_ui.update()

            table_width = self.data_tree.winfo_width()
            _width = int(table_width * 0.5)
            status_width = int(table_width * 0.3)
            status_width_1 = int(table_width * 0.2)

            self.data_tree.column("1", width=_width, stretch="yes")
            self.data_tree.column("2", width=status_width,
                                  stretch="yes", anchor="c")
            self.data_tree.column("3", width=status_width_1,
                                  stretch="yes", anchor="c")

                        
            self.data_tree.heading("1", text="Payload")
            self.data_tree.heading("2", text="Locked By")
            self.data_tree.heading("3", text="Status")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    ### Function / Callback
    def close_this_window(self, wind):
        try:
            self.dpe_page_unlock_ui.focus_set()
            self.dpe_page_unlock_ui.wm_attributes("-disabled", False)
            wind.destroy()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
    
    def getDataandCopy(self, event):
        try:
            self.master.clipboard_clear()  # clear clipboard contents
            for i in self.data_tree.selection():
                logger.debug("Item No: " + str(i))
                item = self.data_tree.item(i)
                values = item["values"]
                self.master.clipboard_append("\t".join(values))
                # append new value to clipbaord
                self.master.clipboard_append("\n")
                logger.debug("Copied to Clipboard: "+str(values))
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

    def changeoptionbox(self, val):
        try:
            self.dpe_page_unlock_ui.excelfile = ""
            self.dpe_page_unlock_ui.user_data = ""
            self.vartounlockpage.set("")
            if val == "Enter Payload (Comma Seperated)":
                if self.selected_file_label.winfo_ismapped():
                    self.selected_file_label.grid_forget()
                if self.select_file_btn.winfo_ismapped():
                    self.select_file_btn.grid_forget()
                self.to_unlock_ent.grid(
                        row=0, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
                self.selectionlabelframe.grid_columnconfigure(1, weight=1)
            elif val == "Source Data from Excel":
                if self.to_unlock_ent.winfo_ismapped():
                    self.to_unlock_ent.grid_forget()
                self.select_file_btn.grid(
                        row=0, column=1, padx=5, pady=5, sticky="nsew")
                self.selected_file_label.grid(
                        row=0, column=2, padx=5, pady=5, sticky="nsew")
                self.selectionlabelframe.grid_columnconfigure(1, weight=0)
                self.selectionlabelframe.grid_columnconfigure(2, weight=1)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def insert_into_table(self, pos, table_values):
        try:
            self.data_tree.insert("", "end", iid=pos,
                                  text=str(pos), values=table_values)
            self.data_tree.yview_moveto(1)
            self.dpe_page_unlock_ui.update()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openexcelfile(self):
        try:
            logger.debug("--Single Redirect--")
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.dpe_page_unlock_ui.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.dpe_page_unlock_ui.excelfile:
                logger.debug("Selected Excel File: " +
                             self.dpe_page_unlock_ui.excelfile)
                self.varexcelfile.set(self.dpe_page_unlock_ui.excelfile)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_inputs(self, uname, passwd, environment, selected_ip, source_data, source_type):
        try:
            #excel_file
            output_status = False
            is_not_empty_uname = bool(uname)
            logger.debug("Username Not Empty: "+str(is_not_empty_uname))

            is_not_empty_passwd = bool(passwd)
            logger.debug("Password Not Empty: "+str(is_not_empty_passwd))

            is_not_empty_ip = bool(selected_ip)
            logger.debug("IP Not Empty: "+str(is_not_empty_ip))

            is_valid_source_data = bool(source_data)
            logger.debug("Valid File: "+str(is_valid_source_data))

            is_a_file = True if (source_type == "Source Data from Excel" and is_valid_source_data) else False

            allowed_file_types = [".xlsx", ".xls", ".xlsm"]
            is_valid_excel_file = False
            
            if is_a_file:
                is_valid_excel_file = GenericFunctions.is_valid_file_types(source_data, allowed_file_types)
            if not(is_a_file) and is_valid_source_data:
                is_valid_excel_file = True
            logger.debug("Valid Excel File: "+str(is_valid_excel_file))

            is_valid_ip = GenericFunctions.validateIP(
                selected_ip, environment) if is_not_empty_ip else False
            logger.debug("Valid IP: "+str(is_valid_ip))

            if is_not_empty_ip and is_not_empty_uname and is_not_empty_passwd and is_valid_source_data and is_valid_excel_file and is_valid_ip:
                output_status = True

            else:
                error_list = []
                if not(is_not_empty_uname):
                    error_list.append("\nUsername Can't be Empty")

                if not(is_not_empty_passwd):
                    error_list.append("\nPassword Can't be Empty")

                if not(is_not_empty_ip):
                    error_list.append("\nIP Can't be Empty")

                if not(is_valid_source_data):
                    error_list.append("\nPlease select a File")


                if not(is_valid_excel_file):
                    error_list.append(
                        "\nInvalid Selected File. Only accepts below\n"+",".join(allowed_file_types))

                if not(is_valid_ip):
                    error_list.append(
                        "\nInvalid IP, Please select/enter correct IP")

                if bool(error_list):
                    messagebox.showerror("Below Error has occurred", "--------Errors---------"+".".join(
                        error_list), parent=self.dpe_page_unlock_ui)
                    logger.error("Below Error has occurred" +
                                 ".".join(error_list))
            logger.info("Data Validation Status: " + str(output_status))
            return output_status

        except:
            logger.error("Below Exception occurred\n", exc_info=True)


    def unlock_dpe_pages(self):
        try:
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.retrieve_data_count_label_error.config(text="", fg="black")
            self.dpe_page_unlock_ui.update()

            uname = self.varuserent.get().strip()
            passwd = self.varpassent.get().strip()

            environment = self.varenvdata.get().lower()
            selected_ip = (self.varipdata.get().lower().strip()
                           if environment == "ip" else configdata[environment])
            source_type = self.var_selected_source.get()
            source_data = self.dpe_page_unlock_ui.excelfile if source_type == "Source Data from Excel" else \
                (self.vartounlockpage.get() if source_type == "Enter Payload (Comma Seperated)" else "")

            run_the_operation = True
            if environment.lower() == "production":
                run_the_operation = messagebox.askyesnocancel(
                    "Please confirm", "Do you want to Run\nthe Operation in Production?", parent=self.dpe_page_unlock_ui)

            if run_the_operation:
                is_validated = self.validate_inputs(
                    uname, passwd, environment, selected_ip, source_data, source_type)
                output=[]
                if is_validated:
                    self.unlock_page_operation=UnlockPages(selected_ip,uname,passwd)
                    payload_for_unlock=[]
                    unlocked=0
                    notunlocked=0
                    #User Input via EntryPoint
                    if self.var_selected_source.get() == "Enter Payload (Comma Seperated)":
                        payload_for_unlock = [[x.strip(),] for x in self.vartounlockpage.get().split(",") if x.strip() != "" ]
                        count_of_payload = len(payload_for_unlock)
                        self.total_hits_label.config(text="Total: "+str(count_of_payload), fg="black")
                        logger.debug("Total Number of Payloads: " +str(count_of_payload))
                        logger.debug(payload_for_unlock)
                        self.dpe_page_unlock_ui.progress_bar = ttk.Progressbar(self.small_btn_frame, orient=HORIZONTAL, maximum=count_of_payload, mode="determinate", style="green.Horizontal.TProgressbar")
                        self.dpe_page_unlock_ui.progress_bar.pack(fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")
                        for i in range(len(payload_for_unlock)):
                          _each_payload=payload_for_unlock[i]
                          lockowner_output=self.unlock_page_operation.get_LockOwner(_each_payload[0])
                          if lockowner_output!="Page Is Not Locked" and lockowner_output!="Page Not Found" and lockowner_output!="Incorrect Page Path" and lockowner_output!="Incorrect UserName/Password" and lockowner_output != 999:
                             output=self.unlock_page_operation.unlock_process(lockowner_output,_each_payload[0])
                             table_values = (_each_payload[0],output[1], output[0])
                             self.insert_into_table(i+1, table_values)
                             if output[0]!="Internal Server Error" and output[0]!="Invalid LockOwner Username/Password" and output[0]!="Page Unlock Cannot Be Completed":
                              unlocked+=1
                             self.retrieve_data_count_label.config(text="Unlocked: "+str(unlocked), fg="green")
                          else:
                             if lockowner_output == 999 : lockowner_output = "Exception Occurred"
                             output=[lockowner_output,"Invalid"]
                             table_values = (_each_payload[0],output[1], output[0])
                             self.insert_into_table(i+1, table_values)
                             notunlocked+=1
                             self.retrieve_data_count_label_error.config(text="Not Unlocked: "+str(notunlocked), fg="red")

                                                    
                          self.dpe_page_unlock_ui.progress_bar["value"] = i+1
                          self.dpe_page_unlock_ui.update()

                        self.dpe_page_unlock_ui.progress_bar.destroy()    
                        self.toggleInputField("disabled")    
                    
                    #User Input via Excel Sheet(.xlsx format supported)
                    if self.var_selected_source.get() == "Source Data from Excel":
                        payload_for_unlock = self.unlock_page_operation.read_data_xlsx(source_data)
                        count_of_payload = len(payload_for_unlock)
                        self.total_hits_label.config(text="Total: "+str(count_of_payload), fg="black")
                        logger.debug("Total Number of Payloads: " +str(count_of_payload))
                        logger.debug(payload_for_unlock)
                        self.dpe_page_unlock_ui.progress_bar = ttk.Progressbar(self.small_btn_frame, orient=HORIZONTAL, maximum=count_of_payload, mode="determinate", style="green.Horizontal.TProgressbar")
                        self.dpe_page_unlock_ui.progress_bar.pack(fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")
                        for i in range(len(payload_for_unlock)):
                          _each_payload=payload_for_unlock[i]
                          lockowner_output=self.unlock_page_operation.get_LockOwner(_each_payload[0])
                          if lockowner_output!="Page Is Not Locked" and lockowner_output!="Page Not Found" and lockowner_output!="Incorrect Page Path" and lockowner_output!="Incorrect UserName/Password" and lockowner_output != 999:
                             output=self.unlock_page_operation.unlock_process(lockowner_output,_each_payload[0])
                             table_values = (_each_payload[0],output[1], output[0])
                             self.insert_into_table(i+1, table_values)
                             if output[0]!="Internal Server Error" and output[0]!="Invalid LockOwner Username/Password" and output[0]!="Page Unlock Cannot Be Completed":
                              unlocked+=1
                             self.retrieve_data_count_label.config(text="Unlocked: "+str(unlocked), fg="green")
                          else:
                             if lockowner_output == 999 : lockowner_output = "Exception Occurred"
                             output=[lockowner_output,"Invalid"]
                             table_values = (_each_payload[0],output[1], output[0])
                             self.insert_into_table(i+1, table_values)
                             notunlocked+=1
                             self.retrieve_data_count_label_error.config(text="Not Unlocked: "+str(notunlocked), fg="red")
                          
                          self.dpe_page_unlock_ui.progress_bar["value"] = i+1
                          self.dpe_page_unlock_ui.update()

                        self.dpe_page_unlock_ui.progress_bar.destroy()    
                        self.toggleInputField("disabled")
                                                           
        except Exception as e:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.total_hits_label.config(
                                    text="Exception Occurred!!", fg="red")
            self.toggleInputField("normal")
            print(e)

    
    def toggleInputField(self, val):
        try:
            self.userent["state"] = val
            self.passent["state"] = val
            self.ipenter["state"] = val
            self.select_file_btn["state"] = val
            self.to_unlock_ent["state"] = val
            self.user_start_operation_btn["state"] = val

            self.envent["state"] = val
            self.source_dropdown_ent["state"] = val


        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initiate_var()
            self.toggleInputField("normal")
            self.dpe_page_unlock_ui.excelfile = ""
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.retrieve_data_count_label_error.config(text="", fg="black")
            self.data_tree.delete(*self.data_tree.get_children())
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# End of Page Unlock

class TerminateWorkflowUI:
    def __init__(self, master):
        self.terminatewf = Toplevel(master)
        self.isDataValidated = False
        self.terminatewf.state("zoomed")
        self.master = master
        master.withdraw()
        self.terminatewf.title(APPLICATION_NAME + " - " +
                               "Terminate Stuck Workflow")
        self.terminatewf.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.terminatewf.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.terminatewf.iconphoto(False, self.brandpic)
        self.styleterminatewin = ttk.Style()
        self.terminatewf.protocol(
            "WM_DELETE_WINDOW", lambda root=master: self.reopenroot(root)
        )
        self.terminatewf.configdata = configdata
        self.terminatewinmaindesign()
        self.isDataValidated = False

    def changeRoot(self, root):
        root.state("zoomed")
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.terminatewf.destroy()
            root.after(1000, self.changeRoot(root))
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def terminatewinlabelframe(self):
        try:
            self.dataframe = LabelFrame(
                self.terminatewf, text="Enter Details", padx=10, pady=10
            )
            self.progressframe = LabelFrame(self.terminatewf, padx=10, pady=10)
            self.logframe = LabelFrame(
                self.terminatewf, text="Log Details", padx=10, pady=10
            )
            self.dataframe.pack(fill="both")
            self.progressframe.pack(fill="both")
            self.logframe.pack(fill="both", expand="yes")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def initializevar(self):
        try:
            self.varenvdata.set(DEFAULT_ENVIRONMENT)
            selected_env = self.varenvdata.get().lower()
            self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                basicconfigdata.get(str(selected_env)+"_passwd","")) if basicconfigdata.get(str(selected_env)+"_passwd","").strip() != "" else basicconfigdata.get(str(selected_env)+"_passwd","").strip()
            self.varuserent.set(basicconfigdata.get(str(selected_env)+"_username",""))
            self.varpassent.set(self.decrypted_passwd)
            self.varipdata.set("")
            self.varcontentpath.set("")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def terminatewinmaindesign(self):
        try:
            # String and Int Variable
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varenvdata = StringVar()
            self.varipdata = StringVar()
            self.varcontentpath = StringVar()

            # Initialize
            self.initializevar()

            # Validation in Progress
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get().strip())
            )

            # Start of Labelframe
            self.terminatewinlabelframe()

            # Start of Design
            self.frame_1 = Frame(self.dataframe)
            self.frame_1.pack(fill="both", expand="yes")

            # Username
            self.userlabelframe = LabelFrame(
                self.frame_1, text="DPE Username*")
            self.userent = ttk.Entry(
                self.userlabelframe,
                textvariable=self.varuserent,
                font=(FONT_NAME, FONT_SIZE),
            )
            self.userent.grid(
                row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew"
            )
            self.userlabelframe.grid_columnconfigure(0, weight=1)
            self.userlabelframe.grid(
                row=0, column=2, padx=10, pady=10, ipadx=5, ipady=5, sticky="nsew"
            )
            self.frame_1.grid_columnconfigure(2, weight=1)

            # Password Entry
            self.passlabelframe = LabelFrame(
                self.frame_1, text="DPE password*")
            self.passent = ttk.Entry(
                self.passlabelframe,
                show="*",
                textvariable=self.varpassent,
                font=(FONT_NAME, FONT_SIZE),
            )
            self.passent.grid(
                row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew"
            )
            self.passlabelframe.grid_columnconfigure(0, weight=1)
            self.passlabelframe.grid(
                row=0, column=3, padx=10, pady=10, ipadx=5, ipady=5, sticky="nsew"
            )
            self.frame_1.grid_columnconfigure(3, weight=1)

            # IP Frame
            self.iplabelframe = LabelFrame(
                self.frame_1,
                text="Select Env or Enter IP(should start with http://)",
                padx=10,
                pady=10,
            )
            # self.envdata = ["", "Stage", "Production", "QA", "IP"]
            env_data = configdata.get("environments",[])
            self.envdata = env_data.copy()
            # self.envdata.insert(0,"")
            # self.envent = ttk.OptionMenu(
            #     self.iplabelframe, self.varenvdata, *self.envdata, command=self.ipchange
            # )
            self.envent = ttk.Combobox(
                self.iplabelframe, textvariable=self.varenvdata, state="readonly", values=self.envdata, #command=self.ipchange
            )
            self.envent.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.iplabelframe.grid_columnconfigure(0, weight=1)
            self.ipenter = ttk.Entry(
                self.iplabelframe,
                textvariable=self.varipdata,
                font=(FONT_NAME, FONT_SIZE - 2),
            )
            self.iplabelframe.grid(
                row=0,
                column=0,
                columnspan=2,
                padx=10,
                pady=10,
                ipadx=5,
                ipady=5,
                sticky="nsew",
            )
            self.frame_1.grid_columnconfigure(0, weight=1)

            # Content path
            self.contentpathlabel = ttk.Label(
                self.frame_1,
                text="Enter content path to terminate workflow\nFor Multiple use comma(,) as seperator",
                font=(FONT_NAME, FONT_SIZE),
                borderwidth=2,
                anchor=CENTER,
            )
            self.contentpathlabel.grid(
                row=1, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="nsew"
            )
            self.contentent = ttk.Entry(
                self.frame_1,
                textvariable=self.varcontentpath,
                font=(FONT_NAME, FONT_SIZE - 2),
            )
            self.contentent.grid(
                row=1, column=1, columnspan=3, padx=10, pady=10, sticky="nsew"
            )
            self.frame_1.grid_columnconfigure(1, weight=1)

            # Button Style and More
            self.styleterminatewin.configure(
                "buttondesign.TButton", font=(FONT_NAME, FONT_SIZE)
            )
            self.styleterminatewin.configure(
                "progressbar.Horizontal.TProgressbar",
                background="green",
                lightcolor="green",
                darkcolor="green",
            )

            # Frame 2
            self.frame_2 = Frame(self.progressframe)
            self.frame_2.pack(fill="both", expand="yes")
            self.submitbtn = ttk.Button(
                self.frame_2,
                text="Terminate Workflow",
                style="buttondesign.TButton",
                command=lambda *args: self.t_processitem(self.processitem),
            )
            self.submitbtn.pack(side="left", expand="yes")
            self.resetallbtn = ttk.Button(
                self.frame_2,
                text="Reset",
                style="buttondesign.TButton",
                command=self.resetall,
            )
            self.resetallbtn.pack(side="left", expand="yes")
            self.exitbtn = ttk.Button(
                self.frame_2,
                text="Exit Window",
                style="buttondesign.TButton",
                command=lambda root=self.master: self.reopenroot(root),
            )
            self.exitbtn.pack(side="right", expand="yes")

            # Frame 3
            self.frame_3 = Frame(self.logframe)
            self.frame_3.pack(fill="both", expand="yes")

            self.progressbarframe = Frame(self.frame_3)
            self.progressbarframe.pack(fill="x")
            self.loglist = Listbox(
                self.frame_3, selectmode=EXTENDED, activestyle=NONE)
            self.scrollbar_y = ttk.Scrollbar(
                self.frame_3, orient=VERTICAL, command=self.loglist.yview
            )
            self.loglist.config(yscrollcommand=self.scrollbar_y.set)
            self.scrollbar_y.pack(side="right", fill="y")
            self.scrollbar_x = ttk.Scrollbar(
                self.frame_3, orient="horizontal", command=self.loglist.xview
            )
            self.loglist.config(xscrollcommand=self.scrollbar_x.set)
            self.scrollbar_x.pack(side="bottom", fill="x")
            self.loglist.pack(fill="both", expand="yes", ipadx=10, ipady=10)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def toggleInputField(self, val):
        try:
            self.userent["state"] = val
            self.passent["state"] = val
            self.contentent["state"] = val
            self.envent["state"] = val
            self.ipenter["state"] = val
            self.submitbtn["state"] = val
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.loglist.insert(
                "end", "There are some errors. Please check log file.")

    def resetall(self):
        try:
            self.initializevar()
            self.toggleInputField("normal")
            self.loglist.delete(0, END)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.loglist.insert(
                "end", "There are some errors. Please check log file.")

    def validationofdata(self, uname, pwd, contentpath, ip, env):
        try:
            self.loglist.delete(0, END)

            if uname != "" and pwd != "" and contentpath != "" and ip != "":
                if ip.count(":") <= 2 and GenericFunctions.validateIP(ip, env):
                    self.isDataValidated = True
                else:
                    self.loglist.insert(
                        0, "Invalid IP Address. Please Enter/Select Correct IP"
                    )
                    logger.warning(
                        "Invalid IP Address. Please Enter/Select Correct IP")
            else:
                self.isDataValidated = False
                if uname == "":
                    self.loglist.insert(
                        0, "Username cannot be left blank. These fields are mandatory."
                    )
                    logger.warning(
                        "Username cannot be left blank. These fields are mandatory."
                    )
                if pwd == "":
                    self.loglist.insert(
                        0, "Password cannot be left blank. These fields are mandatory."
                    )
                    logger.warning(
                        "Password cannot be left blank. These fields are mandatory."
                    )
                if contentpath == "":
                    self.loglist.insert(
                        0,
                        "Contentpath cannot be left blank. These fields are mandatory.",
                    )
                    logger.warning(
                        "Contentpath cannot be left blank. These fields are mandatory."
                    )
                if ip == "":
                    self.loglist.insert(
                        0, "IP cannot be left blank. These fields are mandatory."
                    )
                    logger.warning(
                        "IP cannot be left blank. These fields are mandatory."
                    )
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.loglist.insert(
                "end", "There are some errors. Please check log file.")

    def t_processitem(self, func):
        try:
            _clear_thread = threading.Thread(target=func)
            _clear_thread.daemon = True
            _clear_thread.start()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.loglist.insert("end",
                "There are some errors. Please check logs")

    def processitem(self):
        try:
            # self.toggleInputField("disabled")
            user = self.varuserent.get().strip()
            passwd = self.varpassent.get().strip()
            contentpath = self.varcontentpath.get().strip()
            ip = (
                self.varipdata.get().strip()
                if self.varenvdata.get().strip().lower() == "ip"
                else configdata[self.varenvdata.get().strip().lower()]
            )
            varpath = configdata["varpath" +
                                 self.varenvdata.get().lower().strip()]

            logger.info(
                "Username: "
                + user
                + ", Contentpath: "
                + contentpath
                + ",IP: "
                + ip
                + ",Varpath: "
                + varpath
            )
            self.validationofdata(
                user, passwd, contentpath, ip, self.varenvdata.get().strip().lower()
            )

            if self.isDataValidated:
                if self.varenvdata.get().strip().lower() == "production":
                    confirm = messagebox.askyesnocancel(
                        title="Please Confirm",
                        message="Do you want to continue\nto run the operation on prod?",
                    )
                else:
                    confirm = True

                if confirm:
                    st = False
                    # ip,user,passwd,loglevel,sleeptime,timeout
                    urllist = [x.strip() for x in contentpath.split(",")]
                    self.toggleInputField("disabled")
                    self.progressbar = ttk.Progressbar(
                        self.progressbarframe,
                        style="progressbar.Horizontal.TProgressbar",
                        orient=HORIZONTAL,
                        maximum=len(urllist),
                        mode="determinate",
                    )
                    self.progressbar.pack(
                        side="left", expand="yes", fill="both")
                    progcounter = 1
                    twf = TerminateWorkflow(ip, user, passwd)
                    for url in urllist:
                        if url.count(".html") > 0 or url.count("//") > 0:
                            self.progressbar["value"] = progcounter
                            self.loglist.insert(
                                END,
                                "Invalid URL. Shouldn't contain // or .html - "
                                + str(url),
                            )
                            logger.warning(
                                "Invalid URL. Shouldn't contain // or .html")
                        else:
                            failed_data = twf.retrieveList(varpath, url)
                            logger.debug(failed_data)
                            # failed_data = "/content/pwc/gx/en/services/people-organisation/publications/workforce-of-the-future/quiz"

                            if failed_data is not None:
                                if failed_data.strip() != "" and (
                                    failed_data.strip()
                                    != "Wrong username and Password - Http status 401"
                                    and failed_data.find(
                                        "Some Error occured while connecting. Http Status"
                                    )
                                    < 0
                                ):
                                    msg = twf.processfaileditem(failed_data)
                                    # msg = failed_data
                                    self.loglist.insert(END, msg)
                                    self.progressbar["value"] = progcounter
                                    st = True

                                elif (
                                    failed_data.strip() != ""
                                    and failed_data.strip()
                                    == "Wrong username and Password - Http status 401"
                                ):
                                    self.loglist.insert(
                                        END, str(url) + " - " +
                                        str(failed_data)
                                    )
                                    self.progressbar["value"] = progcounter
                                    st = False
                                    self.toggleInputField("normal")
                                    # self.submitbtn["state"] = "normal"
                                    break

                                else:
                                    failed_data = (
                                        "No Data has been retrieved!!"
                                        if (failed_data.strip() == "")
                                        else failed_data
                                    )
                                    self.loglist.insert(
                                        END, str(url) + " - " +
                                        str(failed_data)
                                    )
                                    self.progressbar["value"] = progcounter
                                    st = False

                            else:
                                self.loglist.insert(
                                    END,
                                    str(url)
                                    + " - Error in fetching data. Datatype of Data is NoneTyp!!",
                                )
                                self.progressbar["value"] = progcounter
                                st = False
                            # sleep(1)

                            # self.progressbarframe.update_idletasks()
                            self.terminatewf.update()
                            # sleep(0.1)
                            progcounter += 1

                    self.progressbar.destroy()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.loglist.insert(
                "end", "There are some errors. Please check log file.")

    def ipchange(self, value):
        try:
            if value.strip().lower() == "ip":
                self.ipenter.grid(
                    row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew"
                )
                self.iplabelframe.grid_columnconfigure(1, weight=1)
                self.varuserent.set("")
                self.varpassent.set("")
            else:
                if self.ipenter.winfo_ismapped():
                    self.ipenter.grid_forget()

                self.iplabelframe.grid_columnconfigure(0, weight=1)
                self.iplabelframe.grid_columnconfigure(1, weight=0)

                selected_env = value.strip().lower()
                self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                    basicconfigdata.get(str(selected_env)+"_passwd","")) if basicconfigdata.get(str(selected_env)+"_passwd","").strip() != "" else basicconfigdata.get(str(selected_env)+"_passwd","").strip()
                self.varuserent.set(
                    basicconfigdata.get(str(selected_env)+"_username",""))
                self.varpassent.set(self.decrypted_passwd)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.loglist.insert(
                "end", "There are some errors. Please check log file.")

    def checkipdata(self, varipdata):
        try:
            if len(varipdata.get()) > 7 and varipdata.get()[0:7] != "http://":
                varipdata.set("")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.loglist.insert(
                "end", "There are some errors. Please check log file.")

####### END OF Terminate Workflow UI  ##########


class RetrieveDataFromDPE:
    def __init__(self, master):
        self.retrieve_data_win = Toplevel(master)
        self.master = master
        self.isDataValidated = False
        self.retrieve_data_win.state("zoomed")
        master.withdraw()
        self.retrieve_data_win.title(
            APPLICATION_NAME + " - " + "Retrieve Data From DPE"
        )
        self.retrieve_data_win.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.retrieve_data_win.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.retrieve_data_win.iconphoto(False, self.brandpic)
        self.styleretrieve_data_win = ttk.Style()
        self.retrieve_data_win.protocol(
            "WM_DELETE_WINDOW", lambda root=master: self.reopenroot(root)
        )
        self.retrieve_data_win.configdata = configdata
        self.retrieve_data_win.excelfile = ""
        self.retrieve_data_win.final_query = ""
        self.retrieve_data_win.bulk_final_query = ""
        self.retrieve_data_win.payload_data = []
        # self.retrieve_data_winmaindesign()selected_excelfile
        self.create_menu_bar()
        self.mainui_design()
    
    def create_menu_bar(self):
        try:
            file_url = "https://docs.google.com/spreadsheets/d/17oqbHMBZ92CtiNPRKcZlYifHXGje9SwpVQjmzOWQCLs/export?format=xlsx&gid=1128585898"
            self.main_menu = Menu(self.retrieve_data_win)
            self.downloadmenu = Menu(self.main_menu, tearoff=0)
            self.downloadmenu.add_command(
                label="Payloads", command=lambda *args: GenericFunctions.download_google_sheet(file_url)
            )
            self.main_menu.add_cascade(
                label="Sample File", menu=self.downloadmenu)
            self.retrieve_data_win.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state("zoomed")
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.retrieve_data_win.destroy()
            root.after(1000, self.changeRoot(root))
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def initialize_variable(self):
        try:
            self.varenvdata.set(DEFAULT_ENVIRONMENT)
            selected_env = self.varenvdata.get().lower()
            # self.decrypted_passwd = GenericFunctions.decrypt_passwd(
            #     basicconfigdata[str(selected_env)+"_passwd"]) if basicconfigdata[str(selected_env)+"_passwd"].strip() != "" else basicconfigdata[str(selected_env)+"_passwd"].strip()
            self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                    basicconfigdata.get(str(selected_env)+"_passwd","")) if basicconfigdata.get(str(selected_env)+"_passwd","").strip() != "" else basicconfigdata.get(str(selected_env)+"_passwd","").strip()
            self.varuserent.set(
                basicconfigdata.get(str(selected_env)+"_username",""))
            self.varquerydata.set("Source Data from Excel")
            self.varipdata.set("")
            # self.varuserent.set(basicconfigdata[str(selected_env)+"_username"])
            self.varpassent.set(self.decrypted_passwd)
            self.varexcelfile.set("Browse & Select Excel File")
            self.varquerydebugent.set("")
            self.varpropertyent.set("")
            self.var_jcr_content.set(0)
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
                "mainBtn.TButton", font=(FONT_NAME, FONT_SIZE), relief="raised")
            self.window_style.configure("scrollbarmain.TScrollbar", background="Green", darkcolor="DarkGreen",
                                        lightcolor="LightGreen", troughcolor="gray", bordercolor="blue", arrowcolor="white")
            self.window_style.configure(
                "green.Horizontal.TProgressbar", foreground='green', background='darkgreen')

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def create_label_frame(self):
        try:
            self.datalabelframe = LabelFrame(
                self.retrieve_data_win, text="Enter Details")
            self.databuttonframe = LabelFrame(self.retrieve_data_win)
            self.data_log_frame = LabelFrame(
                self.retrieve_data_win, text="Logs")
            self.datalabelframe.pack(
                fill="both", padx=10, pady=10, ipadx=10, ipady=10)
            self.databuttonframe.pack(
                fill="both", padx=10, pady=10, ipadx=10, ipady=10)
            self.data_log_frame.pack(
                fill="both", expand="yes", padx=10, pady=10)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def mainui_design(self):
        try:
            self.define_style()

            # String Variable
            self.varquerydata = StringVar()
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varexcelfile = StringVar()
            self.varquerydebugent = StringVar()
            self.varpropertyent = StringVar()
            self.var_jcr_content = IntVar()

            # Initiate Var
            self.initialize_variable()

            # Validation
            self.varquerydata.trace(
                "w", lambda *args: self.changecheckbox(self.varquerydata.get()))
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))

            # Initiate Label Frames
            self.create_label_frame()

            # main Frame
            self.mainframe = Frame(self.datalabelframe)
            self.mainframe.pack(fill="both", expand="yes")

            # User Entry
            self.userlabelframe = LabelFrame(
                self.mainframe, text="DPE Username", padx=5, pady=5)
            self.userlabelframe.grid(
                row=0, column=2, columnspan=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.userent = Entry(self.userlabelframe,
                                 textvariable=self.varuserent)
            self.userent.grid(row=0, column=0, padx=5, pady=5,
                              ipadx=5, ipady=5, sticky="nsew")
            self.userlabelframe.grid_columnconfigure(0, weight=1)
            self.mainframe.grid_columnconfigure(2, weight=1)

            # Password Entry
            self.passlabelframe = LabelFrame(
                self.mainframe, text="DPE Password", padx=5, pady=5)
            self.passlabelframe.grid(
                row=0, column=3, columnspan=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.passent = Entry(self.passlabelframe,
                                 show="*", textvariable=self.varpassent)
            self.passent.grid(row=0, column=0, padx=5, pady=5,
                              ipadx=5, ipady=5, sticky="nsew")
            self.passlabelframe.grid_columnconfigure(0, weight=1)
            self.mainframe.grid_columnconfigure(3, weight=1)

            # Ip Frame
            self.iplabelframe = LabelFrame(
                self.mainframe, text="Select Env or Enter IP(should start with http://)", padx=10, pady=10)
            # self.envdata = ["", "Stage", "Production", "QA", "IP"]
            env_data = configdata.get("environments",[])
            self.envdata = env_data.copy()
            # self.envdata.insert(0,"")
            # self.envent = ttk.OptionMenu(
            #     self.iplabelframe, self.varenvdata, *self.envdata)  # command=ipchange
            self.envent = ttk.Combobox(
                self.iplabelframe, textvariable = self.varenvdata, values=self.envdata, state="readonly")

            self.envent.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.iplabelframe.grid_columnconfigure(0, weight=1)
            self.ipenter = ttk.Entry(
                self.iplabelframe, textvariable=self.varipdata)
            self.iplabelframe.grid(
                row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.mainframe.grid_columnconfigure(0, weight=1)

            # Select label Frame:
            self.selectionlabelframe = LabelFrame(
                self.mainframe, text="Select the source & Enter Details", padx=5, pady=5)
            self.selectionlabelframe.grid(
                row=1, column=0, columnspan=4, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.querydata = [
                "", "Source Data from Excel", "Use Query Builder", "Use Bulk Editor"]
            self.queryent = ttk.OptionMenu(
                self.selectionlabelframe, self.varquerydata, *self.querydata, ) #command=self.changecheckbox
            self.queryent.grid(row=0, column=0, padx=5,
                               pady=5, sticky="nsew")

            # Query Window or Excel Window
            self.excelbtn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.excelquerylabel = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..", textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),
                                             )
            self.excelquerylabel.grid(
                row=0, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

            self.selectionlabelframe.grid_columnconfigure(2, weight=1)
            self.querybuilderbtn = ttk.Button(
                self.selectionlabelframe, text="Open Query Window", command=self.openquerywindow)
            self.bulkeditorbtn = ttk.Button(
                self.selectionlabelframe, text="Open Bulk Editor", command=self.openbulkeditor)

            if self.varquerydata.get().lower().strip() == "source data from excel":
                self.excelbtn.grid(row=0, column=1, padx=5,
                                   pady=5, sticky="nsew")
                self.varexcelfile.set("Browse & Select Excel File..")

            # Property
            self.propertylabel = ttk.Label(self.mainframe, text="Type Property, For multi property\nUse comma(,) as Separator", font=(
                FONT_NAME, FONT_SIZE), anchor=CENTER)
            self.propertyent = ttk.Entry(
                self.mainframe, textvariable=self.varpropertyent)
            self.propertylabel.grid(
                row=3, column=0, padx=5, pady=5, sticky="nsew")
            self.propertyent.grid(
                row=3, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
            self.mainframe.grid_columnconfigure(1, weight=1)

            # JCR:Content
            self.jcr_content_labelframe = LabelFrame(self.mainframe)
            self.jcr_content_labelframe.grid(
                row=3, column=3,  padx=5, pady=5, sticky="nsew")

            self.jcr_content_checkbtn = ttk.Checkbutton(
                self.jcr_content_labelframe, variable=self.var_jcr_content, onvalue=1, offvalue=0, text="Read From JCR:CONTENT")
            self.jcr_content_checkbtn.pack(padx=5, pady=5, anchor=CENTER)

            # Button
            self.buttonFrame = Frame(self.databuttonframe)
            self.buttonFrame.pack(fill="both", expand="yes")
            self.retrvdatabtn = ttk.Button(
                self.buttonFrame, text="Request Data", style="mainBtn.TButton", command=self.retrvdata)
            self.retrvdatabtn.pack(side="left", expand="yes")
            self.resetbtn = ttk.Button(
                self.buttonFrame, text="Reset All", style="mainBtn.TButton", command=self.resetAll)
            self.resetbtn.pack(side="left", expand="yes")
            self.exitbtn = ttk.Button(self.buttonFrame, text="Exit Window", style="mainBtn.TButton",
                                      command=lambda root=self.master: self.reopenroot(root))
            self.exitbtn.pack(side="left", expand="yes")

            # Data View
            self.small_btn_frame = Frame(self.data_log_frame)
            self.small_btn_frame.pack(
                side="top", anchor="nw", fill="x", expand="yes")

            self.export_btn = ttk.Button(
                self.small_btn_frame, text="Export", style="smallBtn.TButton", width=10, command=self.exportData)
            self.export_btn.pack(side="left", padx=5, pady=0, anchor="w")

            self.total_hits_label = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE))
            self.total_hits_label.pack(side="left", padx=5, pady=0, anchor="w")

            self.retrieve_data_count_label = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE))
            self.retrieve_data_count_label.pack(
                side="left", padx=5, pady=0, anchor="w")

            # Tree Frame
            self.data_tree_frame = Frame(self.data_log_frame)

            self.data_tree = ttk.Treeview(
                self.data_tree_frame, style="treeStyle.Treeview", show="headings", selectmode="extended", height=10)

            self.data_tree_scroll_y = ttk.Scrollbar(
                self.data_tree_frame, orient="vertical", command=self.data_tree.yview)
            self.data_tree.config(yscrollcommand=self.data_tree_scroll_y.set)
            self.data_tree_scroll_y.pack(side="right", fill="y")

            self.data_tree_scroll_x = ttk.Scrollbar(
                self.data_tree_frame, orient="horizontal", command=self.data_tree.xview)
            self.data_tree.config(xscrollcommand=self.data_tree_scroll_x.set)
            self.data_tree_scroll_x.pack(side="bottom", fill="x")

            self.data_tree.pack(fill="both", expand="yes")
            self.data_tree.bind("<<Copy>>", self.getDataandCopy)

            self.data_tree_frame.pack(
                fill="both", expand="yes", padx=5, pady=5)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    # Function/Callback
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

    def changecheckbox(self, val):
        try:
            self.retrieve_data_win.excelfile = ""
            self.retrieve_data_win.final_query = ""
            self.retrieve_data_win.bulk_final_query = ""
            if self.varquerydata.get().lower().strip() == "source data from excel":
                if self.querybuilderbtn.winfo_ismapped():
                    self.querybuilderbtn.grid_forget()
                if self.bulkeditorbtn.winfo_ismapped():
                    self.bulkeditorbtn.grid_forget()
                self.excelbtn.grid(row=0, column=1, padx=10,
                                   pady=10, sticky="nsew")
                self.varexcelfile.set("Browse & Select Excel File..")

            elif self.varquerydata.get().lower().strip() == "use query builder":
                if self.excelbtn.winfo_ismapped():
                    self.excelbtn.grid_forget()
                if self.bulkeditorbtn.winfo_ismapped():
                    self.bulkeditorbtn.grid_forget()
                self.querybuilderbtn.grid(
                    row=0, column=1, padx=10, pady=10, sticky="nsew")
                self.varexcelfile.set("")
            elif self.varquerydata.get().lower().strip() == "use bulk editor":
                if self.excelbtn.winfo_ismapped():
                    self.excelbtn.grid_forget()
                if self.querybuilderbtn.winfo_ismapped():
                    self.querybuilderbtn.grid_forget()
                self.bulkeditorbtn.grid(
                    row=0, column=1, padx=10, pady=10, sticky="nsew")
                self.varexcelfile.set("")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openexcelfile(self):
        try:
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.retrieve_data_win.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.retrieve_data_win.excelfile:
                logger.debug("Selected Excel File: " +
                             self.retrieve_data_win.excelfile)
                self.varexcelfile.set(self.retrieve_data_win.excelfile)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openquerywindow(self):
        try:
            def setvalue():
                textlistbylines = None
                textlistbylines = self.querywritewindow.textwizard.get(
                    "1.0", END).splitlines()
                logger.debug("Query List: "+str(textlistbylines))
                textlines = [x.strip() for x in textlistbylines if (
                    x != "" and x.find("p.limit") < 0)]
                textlines_cleaned = list(set(textlines))
                is_path_present = GenericFunctions.is_belong_to_list(
                    "path", textlines_cleaned)
                is_query_present = True if (
                    is_path_present != "" and len(textlines_cleaned) > 1) else False
                logger.debug("Path is Present in Query? %s" % is_path_present)
                if(is_path_present != ""):
                    if is_query_present:
                        splitted_path = [x.strip() for x in is_path_present.split(
                            "=") if x.strip() != ""]
                        logger.debug("Splitted Path: %s" % splitted_path)
                        if(len(splitted_path) != 2):
                            messagebox.showerror(
                                "Error in Query", "Invalid Path Data. Please check.", parent=self.querywritewindow)
                            logger.error(
                                "Invalid Path Data. Please check."+str(splitted_path))
                        else:
                            content_path = splitted_path[1]
                            logger.debug(INVALID_PATH_STRING)
                            invalid_path = [GenericFunctions.removetrailingspecialchar(
                                x.strip()) for x in INVALID_PATH_STRING.split(",") if x.strip() != ""]
                            if(invalid_path.count(content_path) == 0):
                                confirm = True
                                if(content_path.strip() == operationdata["content root"].strip()):
                                    confirm = messagebox.askyesnocancel(
                                        "Do you want to continue?", "You are running the query\nunder /content/pwc", parent=self.querywritewindow)
                                if confirm:
                                    textlines_cleaned.sort()
                                    separator = "&"

                                    self.retrieve_data_win.final_query = separator.join(
                                        textlines_cleaned)
                                    self.varexcelfile.set(
                                        self.retrieve_data_win.final_query)
                                    logger.debug("Final Query in Popup: %s" %
                                                 self.retrieve_data_win.final_query)
                                    closeQueryWindow()
                            else:
                                messagebox.showerror("Forbidden Path(s)", "Can't use the below paths\n"+",".join(
                                    invalid_path), parent=self.querywritewindow)
                                logger.error("Forbidden Path(s), Can't use the paths: "+",".join(
                                    invalid_path))
                    else:
                        messagebox.showerror(
                            "Error in Query", "Query Should have a\nproper filter. Please check.", parent=self.querywritewindow)
                        logger.error(
                            "Query Should have a proper filter. Please check.")
                else:
                    messagebox.showerror(
                        "Error in Query", "Query Should have a\npath filter. Please check.", parent=self.querywritewindow)
                    logger.error(
                        "Query Should have a\npath filter. Please check.")

            def closeQueryWindow():
                self.retrieve_data_win.wm_attributes("-disabled", False)
                self.retrieve_data_win.focus_set()
                self.querywritewindow.destroy()

            self.querywritewindow = Toplevel(self.retrieve_data_win)
            self.retrieve_data_win.wm_attributes("-disabled", True)
            self.querywritewindow.focus_set()
            self.querywritewindow.title("Enter Your Query")
            self.querywritewindow.geometry("480x480+300+20")
            self.querywritewindow.resizable(False, False)
            self.querywritewindow.transient(self.retrieve_data_win)
            self.querywritewindow.protocol(
                "WM_DELETE_WINDOW", closeQueryWindow)
            self.querywritewindow.toplevelbuttonframe = Frame(
                self.querywritewindow)
            self.querywritewindow.toplevelbuttonframe.pack(side="top")
            self.querywritewindow.toplevelmainframe = Frame(
                self.querywritewindow)
            self.querywritewindow.toplevelmainframe.pack(side="top")
            self.querywritewindow.submit_btn = Button(
                self.querywritewindow.toplevelbuttonframe, text="Submit >>", command=setvalue)
            self.querywritewindow.submit_btn.pack(
                side="left", padx=10, pady=10, ipadx=10)
            self.querywritewindow.textwizard = Text(
                self.querywritewindow.toplevelmainframe, undo=True)
            self.querywritewindow.textwizard.pack(
                side="top", fill="both", expand="yes", padx=20, pady=20)

            if (self.retrieve_data_win.final_query.strip() != ""):
                # counter = 1
                for each in self.retrieve_data_win.final_query.split("&"):
                    self.querywritewindow.textwizard.insert(END, each)
                    self.querywritewindow.textwizard.insert(END, "\n")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openbulkeditor(self):
        try:
            def setvalue():
                textlistbylines = None
                textlistbylines = self.bulkeditorwindow.textwizard.get(
                    "1.0", END).splitlines()
                logger.debug("Query List: "+str(textlistbylines))
                textlines = [x.strip()
                             for x in textlistbylines if x.strip() != ""]
                textlines_cleaned = list(set(textlines))
                is_path_present = True if self.bulkeditorwindow.path_entry_var.get().strip() != "" else False
                is_query_present = bool(textlines_cleaned)
                logger.debug("Is Path present: %s", is_path_present)
                if is_path_present:
                    if is_query_present:
                        content_path = self.bulkeditorwindow.path_entry_var.get().strip()
                        logger.debug(INVALID_PATH_STRING)
                        invalid_path = [GenericFunctions.removetrailingspecialchar(x.strip()) for x in INVALID_PATH_STRING.split(
                            ",") if x.strip() != ""]
                        if(invalid_path.count(content_path) == 0):
                            confirm = True
                            if(content_path.strip() == operationdata["content root"].strip()):
                                confirm = messagebox.askyesnocancel(
                                    "Do you want to continue?", "You are running the query\nunder /content/pwc", parent=self.bulkeditorwindow)
                            if confirm:
                                textlines_cleaned.sort()
                                separator = " "

                                self.retrieve_data_win.bulk_final_query = "path:"+str(content_path) + " "+separator.join(
                                    textlines_cleaned)
                                self.varexcelfile.set(
                                    self.retrieve_data_win.bulk_final_query)
                                logger.debug(
                                    self.retrieve_data_win.bulk_final_query)
                                closeQueryWindow()
                        else:
                            messagebox.showerror("Forbidden Path(s)", "Can't use the below paths\n"+",".join(
                                invalid_path), parent=self.bulkeditorwindow)
                            logger.error(
                                "Forbidden Path(s), Can't use the paths: "+",".join(invalid_path))
                    else:
                        messagebox.showerror(
                            "Error in Query", "Query Should have a\nproper filter. Please check.", parent=self.bulkeditorwindow)
                        logger.error(
                            "Query Should have a, proper filter. Please check.")
                else:
                    messagebox.showerror(
                        "Error in Query", "Query Should have a\npath filter. Please check.", parent=self.bulkeditorwindow)
                    logger.error(
                        "Query Should have a, path filter. Please check.")

            def closeQueryWindow():
                self.retrieve_data_win.wm_attributes("-disabled", False)
                self.retrieve_data_win.focus_set()
                self.bulkeditorwindow.destroy()

            self.bulkeditorwindow = Toplevel(self.retrieve_data_win)
            self.bulkeditorwindow.path_entry_var = StringVar()
            self.bulkeditorwindow.path_entry_var.set("")

            self.retrieve_data_win.wm_attributes("-disabled", True)
            self.bulkeditorwindow.focus_set()
            self.bulkeditorwindow.title("Enter Your Query")
            self.bulkeditorwindow.geometry("480x480+300+20")
            self.bulkeditorwindow.resizable(False, False)
            self.bulkeditorwindow.transient(self.retrieve_data_win)
            self.bulkeditorwindow.protocol(
                "WM_DELETE_WINDOW", closeQueryWindow)
            self.bulkeditorwindow.top_path_frame = Frame(
                self.bulkeditorwindow)
            self.bulkeditorwindow.top_path_frame.pack(
                side="top", fill="x", padx=15)
            self.bulkeditorwindow.path_label = ttk.Label(
                self.bulkeditorwindow.top_path_frame, text="Path   ", anchor="e")
            self.bulkeditorwindow.path_label.pack(
                side="left", padx=5, pady=3, ipadx=5, ipady=2)
            self.bulkeditorwindow.path_entry = ttk.Entry(
                self.bulkeditorwindow.top_path_frame, textvariable=self.bulkeditorwindow.path_entry_var)
            self.bulkeditorwindow.path_entry.pack(
                fill="x", expand=True, side="left", padx=5, pady=3, ipadx=5, ipady=2)
            self.bulkeditorwindow.submit_btn = Button(
                self.bulkeditorwindow.top_path_frame, text="Submit >>", command=setvalue)
            self.bulkeditorwindow.submit_btn.pack(
                side="left", padx=10, pady=10, ipadx=20)

            self.bulkeditorwindow.toplevelmainframe = Frame(
                self.bulkeditorwindow)
            self.bulkeditorwindow.toplevelmainframe.pack(side="top")
            self.bulkeditorwindow.textwizard = Text(
                self.bulkeditorwindow.toplevelmainframe, undo=True)
            self.bulkeditorwindow.textwizard.pack(
                side="top", fill="both", expand="yes", padx=20, pady=20)
            # Button(self.bulkeditorwindow, text="Ok", command=setvalue).pack(
            #     side="top", padx=10, pady=10, ipadx=20
            # )
            if (self.retrieve_data_win.bulk_final_query.strip() != ""):
                # counter = 1
                query_splitted = self.retrieve_data_win.bulk_final_query.split(
                    " ")
                path = query_splitted[0].split(":")[1].strip() if len(
                    query_splitted[0].split(":")) == 2 else ""
                self.bulkeditorwindow.path_entry_var.set(path)
                for i in range(1, len(query_splitted)):
                    self.bulkeditorwindow.textwizard.insert(
                        END, query_splitted[i])
                    self.bulkeditorwindow.textwizard.insert(END, "\n")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def toggleInputField(self, val):
        try:
            logger.info("Setting Widget State to: "+str(val))
            self.userent["state"] = val
            self.passent["state"] = val
            self.ipenter["state"] = val
            self.queryent["state"] = val
            self.excelbtn["state"] = val
            self.querybuilderbtn["state"] = val
            self.bulkeditorbtn["state"] = val
            self.propertyent["state"] = val
            self.retrvdatabtn["state"] = val
            self.envent["state"] = val
            self.jcr_content_checkbtn["state"] = val
            if val == "disabled":
                updatedval = "normal"
            elif val == "normal":
                updatedval = "disabled"
            self.export_btn["state"] = updatedval

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initialize_variable()
            self.toggleInputField("normal")
            self.total_hits_label.config(text="")
            self.retrieve_data_count_label.config(text="")
            self.data_tree.delete(*self.data_tree.get_children())
            self.data_tree["columns"] = ()
            self.retrieve_data_win.payload_data = []
            logger.info("Retrieve Data Window has been reset successfully.")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def getDataandCopy(self, event):
        try:
            self.master.clipboard_clear()  # clear clipboard contents
            for i in self.data_tree.selection():
                logger.debug("Item No: " + str(i))
                item = self.data_tree.item(i)
                values = item["values"]
                self.master.clipboard_append(values)
                # append new value to clipbaord
                self.master.clipboard_append("\n")
                logger.debug("Copied to Clipboard: "+str(values))
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def create_table_column(self):
        try:
            propvalue = self.varpropertyent.get()
            proplist = [x.strip() for x in propvalue.split(",")]
            proplist.insert(0, "Payload")
            proptuple = tuple(proplist)
            self.retrieve_data_win.payload_data.append(proplist)
            self.data_tree["columns"] = proptuple
            tree_col_width = int(
                int(self.data_tree.winfo_width()) / (len(proptuple) + 1))
            tree_col_width_updated = 120 if tree_col_width < 120 else tree_col_width

            for val in proptuple:
                if val == "Payload":
                    self.data_tree.column(
                        val, width=tree_col_width_updated * 2, minwidth=120, stretch=YES)
                else:
                    self.data_tree.column(
                        val, width=tree_col_width_updated, minwidth=120, stretch=YES)

                self.data_tree.heading(val, text=val.title(), anchor=CENTER)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def treeview_insert_data(self, pos, data):
        try:
            t_value = tuple(data)
            self.data_tree.insert("", "end", iid=pos,
                                  text=str(pos+1), value=t_value)
            logger.debug(
                str(data) + " - Inserted into Table at Position: "+str(pos))
            self.data_tree.yview_moveto(1)
            # self.retrieve_data_win.update()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validationofdata(self, ip, user, passwd, propvalue, sourcetype, file, environ):
        try:
            isValidated = False
            logger.debug("Source Type: %s", sourcetype)
            file = "" if file is None else file.strip()
            if ip != "" and user != "" and passwd != "" and propvalue.strip() != "":
                if not(GenericFunctions.validateIP(ip, environ)):
                    isValidated = False
                    messagebox.showerror(
                        "URL Error", "IP or URL is not Correct\nPlease Enter or Select Correct one")
                    logger.error(
                        "IP or URL is not Correct. Please Enter or Select Correct one")
                else:
                    if sourcetype.lower() == "source data from excel":
                        if file != "":
                            filename, ext = os.path.splitext(file)
                            if(ext == ".xlsx" or ext == ".xls" or ext == ".xlsm"):
                                isValidated = True
                            else:
                                isValidated = False
                                messagebox.showerror(
                                    "Invalid File Type", "Please Select a Excel File"
                                )
                                logger.error(
                                    "Invalid Filetype, only .xlsx, .xls, xlsm is allowed. Selected: "+str(ext))
                        else:
                            isValidated = False
                            messagebox.showerror(
                                "Select a File", "Please Select the Excel File"
                            )
                            logger.error("Please Select a Excel File.")
                    elif sourcetype.lower() == "use query builder":
                        if self.retrieve_data_win.final_query != "":
                            isValidated = True
                        else:
                            isValidated = False
                            messagebox.showerror(
                                "Query Error", "Query filter can't be empty")
                            logger.error("Query Filter Can't be Empty!")

                    elif sourcetype.lower() == "use bulk editor":
                        if self.retrieve_data_win.bulk_final_query != "":
                            isValidated = True
                        else:
                            isValidated = False
                            messagebox.showerror(
                                "Query Error", "Query filter can't be empty")
                            logger.error("Bulk Query Filter Can't be Empty!")
            else:
                errorcode = []
                if ip == "":
                    errorcode.append("IP")
                if user == "":
                    errorcode.append("Username")
                if passwd == "":
                    errorcode.append("Password")
                if propvalue.strip() == "":
                    errorcode.append("Property Value")

                finalerror = ", ".join(errorcode)
                if len(errorcode) == 1:
                    messagebox.showerror(
                        "Empty Field!!", "Below field is Mandatory\n" + finalerror
                    )
                elif len(errorcode) > 1:
                    messagebox.showerror(
                        "Empty Field!!", "Below fields are Mandatory\n" + finalerror
                    )
                logger.error(
                    "Final Error: Missing Mandatory field(s) - %s", finalerror)

            return isValidated
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def retrvdata(self):
        try:
            self.retrvdatabtn["state"] = "disabled"
            self.resetbtn["state"] = "disabled"
            self.total_hits_label.config(fg="black")
            environment = self.varenvdata.get().lower().strip()
            ip = (self.varipdata.get().lower().strip()
                  if environment == "ip" else configdata[environment])
            user = self.varuserent.get().lower().strip()
            passwd = self.varpassent.get().strip()
            sourcetype = self.varquerydata.get().lower().strip()
            propvalue = self.varpropertyent.get()
            is_jcr_prop = self.var_jcr_content.get()
            logger.info("Environment: "+str(environment)+", IP: "+str(ip) +
                        ", User: "+str(user)+", Source Type: "+str(sourcetype))
            logger.info("Property: "+str(propvalue) +
                        ", JCR Property Checked: "+str(is_jcr_prop))

            continue_the_operation = True

            if environment == "production":
                continue_the_operation = messagebox.askyesnocancel(
                    title="Please Confirm",
                    message="Do you want to continue\nto run the operation on prod?",
                )

            logger.info("Environment: "+str(environment) +
                        ", Continue Operation: "+str(continue_the_operation))

            if continue_the_operation:

                self.isDataValidated = self.validationofdata(
                    ip, user, passwd, propvalue, sourcetype, self.retrieve_data_win.excelfile, environment)

                if self.isDataValidated:
                    get_data_from_payload = GetDataFromPayload(
                        ip, user, passwd)
                    self.create_table_column()
                    maximumval = 0
                    output_json_data = ""
                    output_query_debug_data = None
                    is_allowed_to_continue = True
                    error_info = ""

                    if sourcetype == "source data from excel":
                        logger.info("Source Selected: Excel Data")
                        paylist = get_data_from_payload.exceltolist(
                            self.retrieve_data_win.excelfile)
                        maximumval = len(paylist) if paylist is not None else 0
                        self.total_hits_label.config(
                            text="Total Payload: " + str(maximumval))
                        logger.info(
                            "Output JSON Data Max Value: %s",str(maximumval))

                    elif sourcetype == "use query builder":
                        logger.info("Source Selected: Query Builder")
                        # paylist = get_data_from_payload.retrievePayload(
                        #     self.retrieve_data_win.final_query+"&p.limit="+str(operationdata["limit result"]))
                        final_debug_query = self.retrieve_data_win.final_query + \
                            "&p.limit="+str(operationdata["limit result"])
                        output_query_debug_data = get_data_from_payload.get_json_data(
                            final_debug_query, propvalue, is_jcr_prop)
                        is_allowed_to_continue = True if isinstance(output_query_debug_data, dict) else False
                        if is_allowed_to_continue:
                            maximumval = len(output_query_debug_data["hits"]) - 1
                            maximumval = 0 if maximumval < 0 else maximumval
                            # self.treeview_insert_data(1, [1,2,3,4, 5])
                            logger.info(
                                "Output JSON Data Max Value: "+str(maximumval))
                        else:
                            error_info = output_query_debug_data

                    elif sourcetype == "use bulk editor":
                        logger.info("Source Selected: Bulk Editor")
                        output_json_data = get_data_from_payload.get_bulk_data(
                            self.retrieve_data_win.bulk_final_query, propvalue, is_jcr_prop)
                        is_allowed_to_continue = True if isinstance(output_json_data, dict) else False
                        if is_allowed_to_continue:
                            maximumval = len(output_json_data["hits"]) - 1
                            maximumval = 0 if maximumval < 0 else maximumval
                            logger.info(
                                "Output JSON Data Max Value: "+str(maximumval))
                        else:
                            error_info = output_json_data

                    self.data_tree.delete(*self.data_tree.get_children())
                    if is_allowed_to_continue:
                        treecounter = 0
                        self.data_load_indicator = ttk.Progressbar(
                            self.small_btn_frame, orient=HORIZONTAL, maximum=maximumval, mode="determinate", style="green.Horizontal.TProgressbar")
                        self.data_load_indicator.pack(
                            fill="x", expand="yes", side="left", padx=20)

                        if sourcetype == "source data from excel":
                            logger.debug(
                                "Source Type: URL List, Prop List: " + str(propvalue))
                            for url in paylist:
                                if url.find("Total Hits") > -1:
                                    self.total_hits_label.config(text=url)
                                else:
                                    out = get_data_from_payload.getPropDataURL(
                                        url, propvalue, is_jcr_prop)
                                    self.retrieve_data_win.payload_data.append(out)
                                    self.treeview_insert_data(treecounter, out)
                                    treecounter += 1
                                    self.retrieve_data_count_label.config(
                                        text="Retrieved: " + str(treecounter))
                                    self.data_load_indicator["value"] = treecounter
                                    self.retrieve_data_win.update()
                                    logger.debug(str(treecounter)+". "+str(out))

                        elif sourcetype == "use query builder":
                            if isinstance(output_query_debug_data, dict):
                                if output_query_debug_data["results"] > 0:
                                    self.total_hits_label.config(
                                        text="Total Hits: " + str(output_query_debug_data["results"]))
                                    prop_list_in = [str(x).strip() for x in propvalue.split(
                                        ",") if str(x).strip() != ""]
                                    logger.debug(
                                        "Source Type: Query Builder, Prop List: " + str(prop_list_in))
                                    if is_jcr_prop == 1:
                                        _prop_list_in = prop_list_in.copy()
                                        prop_list_in = [f"jcr:content/{x}" for x in _prop_list_in]
                                    #     self.retrieve_data_win.payload_data = self.format_out_data(output_query_debug_data, prop_list_in)
                                    #     for each in output_query_debug_data["hits"]:
                                    #         outval = []
                                    #         outval.append(each["jcr:path"])
                                    #         for each_key in prop_list_in:
                                    #             if each_key in each["jcr:content"]:
                                    #                 fetched_data = each["jcr:content"][each_key]
                                    #                 if isinstance(fetched_data, list):
                                    #                     outval.append(
                                    #                         ", ".join(fetched_data))
                                    #                 else:
                                    #                     outval.append(fetched_data)
                                    #             else:
                                    #                 outval.append(
                                    #                     "Invalid Property")
                                    #         logger.debug(
                                    #             str(treecounter)+". "+str(outval))
                                    #         self.treeview_insert_data(
                                    #             treecounter, outval)
                                    #         self.retrieve_data_win.payload_data.append(
                                    #             outval)
                                    #         treecounter += 1
                                    #         self.retrieve_data_count_label.config(
                                    #             text="Retrieved: " + str(treecounter))
                                    #         self.data_load_indicator["value"] = treecounter
                                    #         self.retrieve_data_win.update()

                                    # else:
                                    self.retrieve_data_win.payload_data = self.format_out_data(output_query_debug_data, prop_list_in)
                                    for each_row in self.retrieve_data_win.payload_data:
                                        logger.debug(str(treecounter)+". "+str(each_row))
                                        self.treeview_insert_data(treecounter, each_row)
                                        treecounter += 1
                                        self.retrieve_data_count_label.config(text="Retrieved: " + str(treecounter))
                                        self.data_load_indicator["value"] = treecounter
                                        self.retrieve_data_win.update()

                                    props_with_payload = prop_list_in.copy()
                                    props_with_payload.insert(0, "Payload")
                                    self.retrieve_data_win.payload_data.insert(0, props_with_payload)

                        elif sourcetype == "use bulk editor":
                            if isinstance(output_json_data, dict):
                                if output_json_data["results"] > 0:
                                    self.total_hits_label.config(
                                        text="Total Hits: " + str(output_json_data["results"]))
                                    if is_jcr_prop == 1:
                                        prop_list_in = [
                                            "jcr:content/"+str(x).strip() for x in propvalue.split(",") if str(x).strip() != ""]
                                    else:
                                        prop_list_in = [str(x).strip() for x in propvalue.split(
                                            ",") if str(x).strip() != ""]
                                    # prop_list_in = [x.strip() for x in propvalue.split(",") if x.strip() != ""]
                                    prop_list_in.insert(0, "jcr:path")
                                    logger.debug(
                                        "Source Type: Bulk Editor, Prop List: " + str(prop_list_in))

                                    for each in output_json_data["hits"]:
                                        outval = []
                                        for each_key in prop_list_in:
                                            if(each_key in each):
                                                fetched_data = each[each_key]
                                                if isinstance(fetched_data, list):
                                                    outval.append(
                                                        ", ".join(fetched_data))
                                                else:
                                                    outval.append(fetched_data)
                                                # outval.append(each[each_key])
                                            else:
                                                outval.append("Invalid Property")

                                        logger.debug(
                                            str(treecounter)+". "+str(outval))

                                        self.treeview_insert_data(
                                            treecounter, outval)
                                        self.retrieve_data_win.payload_data.append(
                                            outval)
                                        treecounter += 1
                                        self.retrieve_data_count_label.config(
                                            text="Retrieved: " + str(treecounter))
                                        self.data_load_indicator["value"] = treecounter
                                        self.retrieve_data_win.update()

                        self.data_load_indicator.destroy()
                        self.retrieve_data_count_label.config(
                            text="Final: " + str(treecounter))
                        self.toggleInputField("disabled")
                        logger.info("Input Filed has been disabled")

                    else:
                        self.total_hits_label.config(text=error_info, fg="red")
                        self.retrvdatabtn["state"] = "normal"

            self.resetbtn["state"] = "normal"
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.resetbtn["state"] = "normal"

    def format_out_data(self, t_data, _cleaned_cols):
        out_data = []
        # out_data.append(_cleaned_cols)
        for each in t_data["hits"]:
            chunks = []
            chunks.append(each.get("jcr:path", "Invalid Property"))
            for prop in _cleaned_cols:
                if prop != "jcr:path":
                    splt_cols = [_x for _x in prop.split("/")]
                    _each_d = each.copy()
                    for _y in splt_cols:
                        if isinstance(_each_d.get(_y,""), dict):
                            _each_d = _each_d[_y].copy()
                        else:
                            chunks.append(_each_d.get(_y, "Invalid Property"))
            out_data.append(chunks)
        return out_data

    def exportData(self):
        try:
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            save_file = filedialog.asksaveasfilename(
                initialdir=BASE_SCRIPT_PATH, initialfile="data_output.xlsx", title="Save Data", filetypes=types, defaultextension=types
            )
            logger.info("File Name to Export the Data: "+str(save_file))
            if save_file:
                self.exportDataList(
                    save_file, self.retrieve_data_win.payload_data)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def exportDataList(self, filename, payloadData):
        try:
            logger.debug("Exported Data: " + str(payloadData))
            total_rows = len(payloadData) if payloadData is not None else 0
            total_cols = 0 if total_rows <= 0 else (len(payloadData[0]) if payloadData[0] is not None else 0)
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()

            for x in range(total_rows):
                for y in range(total_cols):
                    worksheet.write(x, y, str(payloadData[x][y]))

            workbook.close()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            if workbook is not None: workbook.close()

####### END OF Retrieve Data  ##########


class DPEBulkUpdate:
    def __init__(self, master):
        self.bulk_update_to_dpe_ui = Toplevel(master)
        self.master = master
        self.bulk_update_to_dpe_ui.state('zoomed')
        master.withdraw()
        self.bulk_update_to_dpe_ui.title(
            APPLICATION_NAME + " - " + "Bulk Update DPE Data"
        )
        self.bulk_update_to_dpe_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.bulk_update_to_dpe_ui.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.bulk_update_to_dpe_ui.iconphoto(False, self.brandpic)
        # self.stylebulk_update_to_dpe_ui = ttk.Style()
        self.bulk_update_to_dpe_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.bulk_update_to_dpe_ui.configdata = configdata
        self.bulk_update_to_dpe_ui.excelfile = ""
        self.bulk_update_to_dpe_ui.payload_data = []
        self.update_dpe_prop_inst = None
        self.bulk_update_to_dpe_ui.is_halted = False

        self.create_menu_bar()
        self.mainui_design()

    def changeRoot(self, root):
        root.state('zoomed')
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.bulk_update_to_dpe_ui.is_halted = True
            self.bulk_update_to_dpe_ui.destroy()
            root.after(1000, self.changeRoot(root))
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def initialize_variable(self):
        try:
            self.varenvdata.set(DEFAULT_ENVIRONMENT)
            selected_env = self.varenvdata.get().lower()
            self.decrypted_passwd = GenericFunctions.decrypt_passwd(
                    basicconfigdata.get(str(selected_env)+"_passwd","")) if basicconfigdata.get(str(selected_env)+"_passwd","").strip() != "" else basicconfigdata.get(str(selected_env)+"_passwd","").strip()
            self.varuserent.set(
                basicconfigdata.get(str(selected_env)+"_username",""))
            self.varquerydata.set("Source Data from Excel")
            self.varipdata.set("")
            self.varpassent.set(self.decrypted_passwd)
            self.varexcelfile.set("Browse & Select Excel File")
            self.var_upd_or_create_ent.set("Update")
            self.var_validate_old_data.set(0)
            self.var_append_new_data.set(0)
            # self.varpropertyent.set("")
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

    def create_label_frame(self):
        try:
            self.datalabelframe = LabelFrame(
                self.bulk_update_to_dpe_ui, text="Enter Details")
            self.databuttonframe = LabelFrame(self.bulk_update_to_dpe_ui)
            self.data_log_frame = LabelFrame(
                self.bulk_update_to_dpe_ui, text="Logs")
            self.datalabelframe.pack(
                fill="both", padx=10, pady=10, ipadx=10, ipady=10)
            self.databuttonframe.pack(
                fill="both", padx=10, pady=10, ipadx=10, ipady=10)
            self.data_log_frame.pack(
                fill="both", expand="yes", padx=10, pady=10)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def create_menu_bar(self):
        try:
            self.main_menu = Menu(self.bulk_update_to_dpe_ui)
            self.downloadmenu = Menu(self.main_menu, tearoff=0)
            self.downloadmenu.add_command(
                label="File without Validation", command=lambda validatior=False: self.download_sample_file(validatior)
            )
            self.downloadmenu.add_command(
                label="File with Validation", command=lambda validatior=True: self.download_sample_file(validatior)
            )
            self.main_menu.add_cascade(
                label="Sample File", menu=self.downloadmenu)
            self.bulk_update_to_dpe_ui.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def mainui_design(self):
        try:
            self.define_style()

            # String Variable
            self.varquerydata = StringVar()
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varexcelfile = StringVar()
            self.var_upd_or_create_ent = StringVar()
            self.var_validate_old_data = IntVar()
            self.var_append_new_data = IntVar()
            # self.varpropertyent = StringVar()

            # Initiate Var
            self.initialize_variable()

            # Validation
            # self.varquerydata.trace(
            #     "w", lambda *args: self.changecheckbox(self.varquerydata.get()))
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))
            self.var_validate_old_data.trace(
                "w", lambda *args: self.chechbox_checked())
            # chechbox_checked

            # Initiate Label Frames
            self.create_label_frame()

            # main Frame
            self.mainframe = Frame(self.datalabelframe)
            self.mainframe.pack(fill="both", expand="yes")

            # User Entry
            self.userlabelframe = LabelFrame(
                self.mainframe, text="DPE Username", padx=5, pady=5)
            self.userlabelframe.grid(
                row=0, column=2, columnspan=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.userent = Entry(self.userlabelframe,
                                 textvariable=self.varuserent)
            self.userent.grid(row=0, column=0, padx=5, pady=5,
                              ipadx=5, ipady=5, sticky="nsew")
            self.userlabelframe.grid_columnconfigure(0, weight=1)
            self.mainframe.grid_columnconfigure(2, weight=1)

            # Password Entry
            self.passlabelframe = LabelFrame(
                self.mainframe, text="DPE Password", padx=5, pady=5)
            self.passlabelframe.grid(
                row=0, column=3, columnspan=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.passent = Entry(self.passlabelframe,
                                 show="*", textvariable=self.varpassent)
            self.passent.grid(row=0, column=0, padx=5, pady=5,
                              ipadx=5, ipady=5, sticky="nsew")
            self.passlabelframe.grid_columnconfigure(0, weight=1)
            self.mainframe.grid_columnconfigure(3, weight=1)

            # Ip Frame
            self.iplabelframe = LabelFrame(
                self.mainframe, text="Select Env or Enter IP(should start with http://)", padx=10, pady=10)
            # self.envdata = ["", "Stage", "Production", "QA", "IP"]
            env_data = configdata.get("environments",[])
            self.envdata = env_data.copy()
            # self.envdata.insert(0,"")
            # self.envent = ttk.OptionMenu(
            #     self.iplabelframe, self.varenvdata, *self.envdata)  # command=ipchange
            self.envent = ttk.Combobox(
                self.iplabelframe, textvariable = self.varenvdata, values=self.envdata, state="readonly")  # command=ipchange
            self.envent.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.iplabelframe.grid_columnconfigure(0, weight=1)
            self.ipenter = ttk.Entry(
                self.iplabelframe, textvariable=self.varipdata)
            self.iplabelframe.grid(
                row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.mainframe.grid_columnconfigure(0, weight=1)

            # Select label Frame:
            self.selectionlabelframe = LabelFrame(
                self.mainframe, text="Select the source & Enter Details")
            self.selectionlabelframe.grid(
                row=1, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.querydata = [
                "", "Source Data from Excel"]  # , "Use Query Builder"
            self.queryent = ttk.OptionMenu(
                self.selectionlabelframe, self.varquerydata, *self.querydata)  # , command=self.changecheckbox
            self.queryent.grid(row=0, column=0, padx=5,
                               pady=5, sticky="nsew")

            # Query Window or Excel Window
            self.excelbtn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.excelquerylabel = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..", textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),
                                             )
            self.excelquerylabel.grid(
                row=0, column=2, padx=5, pady=5, sticky="nsew")

            self.selectionlabelframe.grid_columnconfigure(2, weight=1)

            self.validation_frame = Frame(self.mainframe)
            self.validation_frame.grid(
                row=1, column=2, columnspan=2, padx=5, sticky="nsew")
            self.mainframe.grid_columnconfigure(2, weight=1)

            self.validate_old_data_frame = LabelFrame(
                self.validation_frame, text="****")
            self.validate_old_data_frame.pack(
                side="left", fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)

            #ttk.Checkbutton(self.jcr_content_labelframe,variable=self.var_jcr_content, onvalue=1, offvalue=0, text="Read From JCR:CONTENT")
            self.validate_old_data_ent = ttk.Checkbutton(
                self.validate_old_data_frame, variable=self.var_validate_old_data, onvalue=1, offvalue=0, text="Validate Old Data")
            self.validate_old_data_ent.grid(
                row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            # self.validate_old_data_frame.grid_columnconfigure(0, weight=1)

            self.validate_old_data_help_text = Label(
                self.validate_old_data_frame, text="(**Date is Skipped)", font=(FONT_NAME, 8))
            self.validate_old_data_help_text.grid(
                row=1, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nsew")
            self.validate_old_data_frame.grid_columnconfigure(0, weight=1)

            self.append_new_data_frame = LabelFrame(
                self.validation_frame, text="****")
            self.append_new_data_frame.pack(
                side="left", fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)

            #ttk.Checkbutton(self.jcr_content_labelframe,variable=self.var_jcr_content, onvalue=1, offvalue=0, text="Read From JCR:CONTENT")
            self.append_new_data_ent = ttk.Checkbutton(
                self.append_new_data_frame, variable=self.var_append_new_data, onvalue=1, offvalue=0, text="Append to Old Value", )  # state="disabled"
            self.append_new_data_ent.grid(
                row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            # self.append_new_data_frame.grid_columnconfigure(0, weight=1)
            self.append_new_data_help_text = Label(
                self.append_new_data_frame, text="(**Only for Multi Value)", font=(FONT_NAME, 8))
            self.append_new_data_help_text.grid(
                row=1, column=0, padx=0, pady=0, ipadx=0, ipady=0, sticky="nsew")
            self.append_new_data_frame.grid_columnconfigure(0, weight=1)

            self.update_or_create_frame = LabelFrame(
                self.validation_frame, text="Operation")
            self.update_or_create_frame.pack(
                side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
            self.upd_or_create_data = ["", "Update", "Create", "Update/Create"]
            self.operationent = ttk.OptionMenu(
                self.update_or_create_frame, self.var_upd_or_create_ent, *self.upd_or_create_data, command=self.change_dropdown)
            self.operationent.grid(row=0, column=0, padx=5,
                                   pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.update_or_create_frame.grid_columnconfigure(0, weight=1)

            # self.bulkeditorbtn = ttk.Button(
            #     self.selectionlabelframe, text="Open Bulk Editor", command=self.openquerywindow)  # , command=self.openquerywindow

            if self.varquerydata.get().lower().strip() == "source data from excel":
                self.excelbtn.grid(row=0, column=1, padx=5,
                                   pady=5, sticky="nsew")
                self.varexcelfile.set("Browse & Select Excel File..")

            # Property
            # self.propertylabel = ttk.Label(self.mainframe, text="Type Property, For multi property\nUse comma(,) as Separator", font=(
            #     FONT_NAME, FONT_SIZE), anchor=CENTER)
            # self.propertyent = ttk.Entry(
            #     self.mainframe, textvariable=self.varpropertyent)
            # self.propertylabel.grid(
            #     row=3, column=0, padx=5, pady=5, sticky="nsew")
            # self.propertyent.grid(
            #     row=3, column=1, columnspan=3, padx=5, pady=5, sticky="nsew")
            # self.mainframe.grid_columnconfigure(1, weight=1)

            # Button
            self.buttonFrame = Frame(self.databuttonframe)
            self.buttonFrame.pack(fill="both", expand="yes")
            self.retrvdatabtn = ttk.Button(
                self.buttonFrame, text="Import Data", style="mainBtn.TButton", command=self.import_data_in_ui)  # , command=self.retrvdata
            self.retrvdatabtn.pack(side="left", expand="yes")
            self.resetbtn = ttk.Button(
                self.buttonFrame, text="Reset All", style="mainBtn.TButton", command=self.resetAll)  # , command=self.resetAll
            self.resetbtn.pack(side="left", expand="yes")
            self.exitbtn = ttk.Button(self.buttonFrame, text="Exit Window", style="mainBtn.TButton",
                                      command=lambda root=self.master: self.reopenroot(root))
            self.exitbtn.pack(side="left", expand="yes")

            # Data View
            self.small_btn_frame = Frame(self.data_log_frame)
            self.small_btn_frame.pack(
                side="top", anchor="nw", fill="x", expand="yes")

            self.export_btn = ttk.Button(
                self.small_btn_frame, text="Update", state="disabled", style="smallBtn.TButton", command=self.t_update_data_in_dpe)  # , command=self.exportData
            self.export_btn.pack(side="left", padx=5, pady=0, anchor="w")

            self.total_hits_label = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE))
            self.total_hits_label.pack(side="left", padx=5, pady=0, anchor="w")

            self.retrieve_data_count_label = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE))
            self.retrieve_data_count_label.pack(
                side="left", padx=5, pady=0, anchor="w")

            self.failed_count_label = Label(
                self.small_btn_frame, text="", font=(FONT_NAME, FONT_SIZE))
            self.failed_count_label.pack(
                side="left", padx=5, pady=0, anchor="w")

            # Tree Frame
            self.data_tree_frame = Frame(self.data_log_frame)

            self.data_tree = ttk.Treeview(
                self.data_tree_frame, style="treeStyle.Treeview", show="headings", columns=(), selectmode="extended", height=10)

            self.data_tree_scroll_y = ttk.Scrollbar(
                self.data_tree_frame, orient="vertical", command=self.data_tree.yview)
            self.data_tree.config(yscrollcommand=self.data_tree_scroll_y.set)
            self.data_tree_scroll_y.pack(side="right", fill="y")

            self.data_tree_scroll_x = ttk.Scrollbar(
                self.data_tree_frame, orient="horizontal", command=self.data_tree.xview)
            self.data_tree.config(xscrollcommand=self.data_tree_scroll_x.set)
            self.data_tree_scroll_x.pack(side="bottom", fill="x")

            self.data_tree.pack(fill="both", expand="yes")
            self.data_tree.bind("<<Copy>>", self.getDataandCopy)
            self.data_tree.bind('<Double-Button-1>', self.edit_data_popup)

            self.data_tree_frame.pack(
                fill="both", expand="yes", padx=5, pady=5)

            self.bulk_update_to_dpe_ui.update()
            # width = self.data_tree.winfo_width() - 100
            # each_col_width = int(width/4)

            # self.data_tree.column("1",width=each_col_width*2, stretch="yes")
            # self.data_tree.column("2",width=each_col_width, stretch="yes", anchor="c")
            # self.data_tree.column("3",width=each_col_width, stretch="yes", anchor="c")
            # self.data_tree.column("4",width=100, stretch="yes", anchor="c")

            # self.data_tree.heading("1", text="Payload")
            # self.data_tree.heading("2", text="Property")
            # self.data_tree.heading("3", text="Value")
            # self.data_tree.heading("4", text="Status")

            self.chechbox_checked()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    # Function/Callback
    def download_sample_file(self, validator):
        try:
            download_url = None
            if validator:
                download_url = "https://docs.google.com/spreadsheets/d/1-qX9qE6FUOef4koo4_ivQEz8HFt4aVpm/export?format=xlsx&gid=2109943718"
            else:
                download_url = "https://docs.google.com/spreadsheets/d/1AUpeXu0U_dLWbVavVTBQ6QallsmozwhI/export?format=xlsx&gid=26320545"
            webbrowser.register(
                "chrome",
                None,
                webbrowser.BackgroundBrowser(
                    "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"
                ),
            )
            chrome = webbrowser.get("chrome")
            chrome.open(download_url)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def change_dropdown(self, event):
        try:
            oper = self.var_upd_or_create_ent.get().lower()
            if oper == "create" :#or oper == "update/create":
                self.var_validate_old_data.set(0)
                self.var_append_new_data.set(0)
                self.validate_old_data_ent["state"] = "disabled"
                self.append_new_data_ent["state"] = "disabled"
            
            else:
                self.validate_old_data_ent["state"] = "normal"
                self.append_new_data_ent["state"] = "normal"
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def chechbox_checked(self):
        try:
            checked = self.var_validate_old_data.get()
            if checked:
                self.data_tree["columns"] = ("1", "2", "3", "4", "5", "6")
                width = self.data_tree.winfo_width() - 200
                each_col_width = int(width/5)

                self.data_tree.column(
                    "1", width=each_col_width*2, stretch="yes")
                self.data_tree.column(
                    "2", width=each_col_width, stretch="yes", anchor="c")
                self.data_tree.column(
                    "3", width=each_col_width, stretch="yes", anchor="c")
                self.data_tree.column(
                    "4", width=each_col_width, stretch="yes", anchor="c")
                self.data_tree.column(
                    "5", width=100, stretch="yes", anchor="c")
                self.data_tree.column(
                    "6", width=100, stretch="yes", anchor="c")

                self.data_tree.heading("1", text="Payload")
                self.data_tree.heading("2", text="Property")
                self.data_tree.heading("3", text="Old Value")
                self.data_tree.heading("4", text="New Value")
                self.data_tree.heading("5", text="Type")
                self.data_tree.heading("6", text="Status")
            else:
                self.data_tree["columns"] = ("1", "2", "3", "4", "5")
                width = self.data_tree.winfo_width() - 200
                each_col_width = int(width/4)

                self.data_tree.column(
                    "1", width=each_col_width*2, stretch="yes")
                self.data_tree.column(
                    "2", width=each_col_width, stretch="yes", anchor="c")
                self.data_tree.column(
                    "3", width=each_col_width, stretch="yes", anchor="c")
                self.data_tree.column(
                    "4", width=100, stretch="yes", anchor="c")
                self.data_tree.column(
                    "5", width=100, stretch="yes", anchor="c")

                self.data_tree.heading("1", text="Payload")
                self.data_tree.heading("2", text="Property")
                self.data_tree.heading("3", text="Value")
                self.data_tree.heading("4", text="Type")
                self.data_tree.heading("5", text="Status")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def edit_data_popup(self, event):
        try:
            self.bulk_update_to_dpe_ui.wm_attributes("-disabled", True)
            self.bulk_update_to_dpe_ui.edit_popup_modal = Toplevel(
                self.bulk_update_to_dpe_ui)
            self.bulk_update_to_dpe_ui.edit_popup_modal.focus_set()
            self.bulk_update_to_dpe_ui.edit_popup_modal.resizable(False, False)
            self.bulk_update_to_dpe_ui.edit_popup_modal.geometry(
                "350x250+400+300")
            self.bulk_update_to_dpe_ui.edit_popup_modal.brandpic = PhotoImage(
                file=BRAND_PIC_FILE)
            self.bulk_update_to_dpe_ui.edit_popup_modal.iconphoto(
                False, self.bulk_update_to_dpe_ui.edit_popup_modal.brandpic)
            self.bulk_update_to_dpe_ui.edit_popup_modal.title(
                APPLICATION_NAME+" - Edit Property Vallue")
            self.bulk_update_to_dpe_ui.edit_popup_modal.transient(
                self.bulk_update_to_dpe_ui)
            self.bulk_update_to_dpe_ui.edit_popup_modal.protocol(
                "WM_DELETE_WINDOW", self.close_this_window)

            # self.var_validate_old_data.trace("w", lambda *args: check_validation_of_old_data())
            def check_validation_of_old_data():
                if self.var_validate_old_data.get():
                    self.bulk_update_to_dpe_ui.edit_popup_modal.property_old_value_label.config(
                        text="Property Old Value")
                    self.bulk_update_to_dpe_ui.edit_popup_modal.property_value_label.grid(
                        row=2, column=0, padx=10, pady=5, ipadx=5, ipady=5, sticky="nsew")
                    self.bulk_update_to_dpe_ui.edit_popup_modal.property_value_ent.grid(
                        row=2, column=1, padx=10, pady=5, ipadx=5, ipady=5, sticky="nsew")
                    self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame.grid_columnconfigure(
                        1, weight=1)
                else:
                    self.bulk_update_to_dpe_ui.edit_popup_modal.property_old_value_label.config(
                        text="Property Value")
                    self.bulk_update_to_dpe_ui.edit_popup_modal.property_value_label.grid_forget()
                    self.bulk_update_to_dpe_ui.edit_popup_modal.property_value_ent.grid_forget()
                    self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame.grid_columnconfigure(
                        1, weight=0)

            selected_item = self.data_tree.item(
                self.data_tree.focus(), "values")

            logger.debug("Selected Table Data: " + str(selected_item))
            self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_name = StringVar()
            self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_old_value = StringVar()
            self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_value = StringVar()
            self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_type = StringVar()
            self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_name.set(
                selected_item[1])
            self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_old_value.set(
                selected_item[2])

            if self.var_validate_old_data.get():
                self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_value.set(
                    selected_item[3])
                self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_type.set(
                    selected_item[4])
            else:
                self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_type.set(
                    selected_item[3])

            self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame = Frame(
                self.bulk_update_to_dpe_ui.edit_popup_modal)
            self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame.pack(
                fill="both", expand="yes")

            self.bulk_update_to_dpe_ui.edit_popup_modal.btn_frame = Frame(
                self.bulk_update_to_dpe_ui.edit_popup_modal)
            self.bulk_update_to_dpe_ui.edit_popup_modal.btn_frame.pack(
                fill="x", expand="yes")

            self.bulk_update_to_dpe_ui.edit_popup_modal.property_label = ttk.Label(
                self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame, anchor="e", text="Property Name", font=(FONT_NAME, 9))
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_label.grid(
                row=0, column=0, padx=10, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_entry = ttk.Entry(
                self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame, textvariable=self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_name)
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_entry.grid(
                row=0, column=1, padx=10, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame.grid_columnconfigure(
                1, weight=1)

            self.bulk_update_to_dpe_ui.edit_popup_modal.property_old_value_label = ttk.Label(
                self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame, anchor="e", text="Property Value", font=(FONT_NAME, 9))
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_old_value_label.grid(
                row=1, column=0, padx=10, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_old_value_ent = ttk.Entry(
                self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame, textvariable=self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_old_value)
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_old_value_ent.grid(
                row=1, column=1, padx=10, pady=5, ipadx=5, ipady=5, sticky="nsew")

            # self.bulk_update_to_dpe_ui.edit_popup_modal.property_old_value_label.config(text="Property Old Value")
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_value_label = ttk.Label(
                self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame, anchor="e", text="Property New Value", font=(FONT_NAME, 9))
            # self.bulk_update_to_dpe_ui.edit_popup_modal.property_value_label.grid(row=2,column=0,padx=10,pady=5,ipadx=5,ipady=5,sticky="nsew")
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_value_ent = ttk.Entry(
                self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame, textvariable=self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_value)
            # self.bulk_update_to_dpe_ui.edit_popup_modal.property_value_ent.grid(row=2,column=1,padx=10,pady=5,ipadx=5,ipady=5,sticky="nsew")
            self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame.grid_columnconfigure(
                1, weight=1)

            self.bulk_update_to_dpe_ui.edit_popup_modal.property_type_label = ttk.Label(
                self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame, anchor="e", text="Property Type", font=(FONT_NAME, 9))
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_type_label.grid(
                row=3, column=0, padx=10, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_type_data = [
                "", "Multi", "Single"]
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_type_ent = ttk.OptionMenu(
                self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame, self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_type, *self.bulk_update_to_dpe_ui.edit_popup_modal.property_type_data)
            self.bulk_update_to_dpe_ui.edit_popup_modal.property_type_ent.grid(
                row=3, column=1, padx=10, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.bulk_update_to_dpe_ui.edit_popup_modal.main_frame.grid_columnconfigure(
                1, weight=1)

            self.bulk_update_to_dpe_ui.edit_popup_modal.save_btn = ttk.Button(
                self.bulk_update_to_dpe_ui.edit_popup_modal.btn_frame, text="Save", style="smallBtn.TButton", command=self.save_prop_value)
            self.bulk_update_to_dpe_ui.edit_popup_modal.save_btn.pack(
                side="left", expand="yes", anchor=CENTER, padx=10, pady=5, ipadx=5, ipady=5)
            self.bulk_update_to_dpe_ui.edit_popup_modal.exit_btn = ttk.Button(
                self.bulk_update_to_dpe_ui.edit_popup_modal.btn_frame, text="Exit", style="smallBtn.TButton", command=self.close_this_window)
            self.bulk_update_to_dpe_ui.edit_popup_modal.exit_btn.pack(
                side="left", expand="yes", anchor=CENTER, padx=10, pady=5, ipadx=5, ipady=5)
            check_validation_of_old_data()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def save_prop_value(self):
        try:
            updated_property_name = self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_name.get().strip()
            updated_property_old_value = self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_old_value.get().strip()
            updated_property_type = self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_type.get().strip()
            updated_property_value = None
            if self.var_validate_old_data.get():
                updated_property_value = self.bulk_update_to_dpe_ui.edit_popup_modal.var_prop_value.get().strip()

            all_tab_data = self.data_tree.get_children()
            index = all_tab_data.index(self.data_tree.focus())

            _values = list(self.data_tree.item(
                self.data_tree.focus(), "values"))
            logger.debug("Value Poped up for Edit: "+str(_values))
            _values[1] = updated_property_name
            _values[2] = updated_property_old_value
            if self.var_validate_old_data.get():
                _values[3] = updated_property_value
                _values[4] = updated_property_type
            else:
                _values[3] = updated_property_type

            updated_val = tuple(_values)

            self.data_tree.item(self.data_tree.focus(),
                                text=str(index+1), values=updated_val)
            if updated_property_type.lower() == 'multi':
                _updated_property_old_value = [
                    x.strip() for x in updated_property_old_value.split(",") if x.strip() != ""]
                if self.var_validate_old_data.get():
                    _updated_property_value = [
                        x.strip() for x in updated_property_value.split(",") if x.strip() != ""]
            else:
                _updated_property_old_value = updated_property_old_value
                _updated_property_value = updated_property_value

            self.bulk_update_to_dpe_ui.payload_data[index][1] = updated_property_name
            self.bulk_update_to_dpe_ui.payload_data[index][2] = _updated_property_old_value
            if self.var_validate_old_data.get():
                self.bulk_update_to_dpe_ui.payload_data[index][3] = _updated_property_value
                self.bulk_update_to_dpe_ui.payload_data[index][4] = updated_property_type
            else:
                self.bulk_update_to_dpe_ui.payload_data[index][3] = updated_property_type

            logger.debug("Updated Data")
            logger.debug(self.bulk_update_to_dpe_ui.payload_data)
            self.close_this_window()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def close_this_window(self):
        try:
            self.bulk_update_to_dpe_ui.focus_set()
            self.bulk_update_to_dpe_ui.wm_attributes("-disabled", False)
            self.bulk_update_to_dpe_ui.edit_popup_modal.destroy()
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def getDataandCopy(self, event):
        try:
            self.master.clipboard_clear()  # clear clipboard contents
            for i in self.data_tree.selection():
                logger.debug("Appended in Clipboard")
                item = self.data_tree.item(i)
                values = item["values"]
                self.master.clipboard_append(values)
                logger.debug(values)
                self.master.clipboard_append("\n")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_data(self, excel_file, environment, ip, user, passwd):
        try:
            data_validated = False
            is_file_not_empty = bool(excel_file)
            is_valid_file = False
            valid_ext = [".xlsx", ".xls", ".xlsm"]
            if is_file_not_empty:
                file_name, fileext = os.path.splitext(excel_file)
                if fileext in valid_ext:
                    is_valid_file = True

            is_ip_not_empty = bool(ip)
            is_user_not_empty = bool(user)
            is_passwd_not_empty = bool(passwd)
            is_valid_ip = False
            if is_ip_not_empty:
                is_valid_ip = GenericFunctions.validateIP(ip, environment)

            if is_file_not_empty and is_ip_not_empty and is_user_not_empty and is_passwd_not_empty and is_valid_file:
                data_validated = True
            else:
                error_list = []
                if not(is_file_not_empty):
                    error_list.append("\nSelect a File")
                if not(is_valid_file):
                    error_list.append(
                        "\nInvalid Filetypes, allowed XLSX, XLS, XLSM")
                if not(is_ip_not_empty):
                    error_list.append("\nIP or Env Can't be empty")
                if not(is_valid_ip):
                    error_list.append("\nInvalid IP format")
                if not(is_user_not_empty):
                    error_list.append("\nUsername Can't be empty")
                if not(is_passwd_not_empty):
                    error_list.append("\Password Can't be empty")

                messagebox.showerror("Error Occured!", "Below Error Occured" +
                                     ".".join(error_list), parent=self.bulk_update_to_dpe_ui)
                logger.error("Below Error Occured"+".".join(error_list))

            return data_validated

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_excel_data(self, excel_data, validate_old_data):
        try:
            logger.debug("Validate Old Data: "+str(validate_old_data) +
                         ", ExcelData From Validate Excel Func: "+str(excel_data))
            valid_data = True
            if validate_old_data:
                for each in excel_data:
                    if len(each) != 5:
                        valid_data = False
                        break
            else:
                for each in excel_data:
                    if len(each) != 4:
                        valid_data = False
                        break

            return valid_data
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def convert_list_to_str(self, data):
        try:
            logger.debug("Data: " + str(data))
            out = ",".join(data)
            logger.debug("Out Data: " + str(out))
            return out
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return ""

    def import_data_in_ui(self):
        try:
            environment = self.varenvdata.get().lower().strip()
            excel_file = self.bulk_update_to_dpe_ui.excelfile
            selected_ip = (self.varipdata.get().lower().strip()
                           if environment == "ip" else configdata[environment])
            user = self.varuserent.get().lower().strip()
            passwd = self.varpassent.get().strip()
            validate_old_data = True if self.var_validate_old_data.get() == 1 else False

            continue_the_operation = True

            if environment == "prod":
                continue_the_operation = messagebox.askyesnocancel(
                    title="Please Confirm",
                    message="Do you want to continue\nto run the operation on prod?",
                )

            if continue_the_operation:

                is_data_valid = self.validate_data(
                    excel_file, environment, selected_ip, user, passwd)
                logger.info("IS Valid Data: "+str(is_data_valid))
                if is_data_valid:
                    # please_proceed = False
                    self.update_dpe_prop_inst = UpdateDPEProperties(
                        selected_ip, user, passwd)
                    self.bulk_update_to_dpe_ui.payload_data = self.update_dpe_prop_inst.sorted_excel_to_list(
                        excel_file, validate_old_data, 0)
                    logger.debug(self.bulk_update_to_dpe_ui.payload_data)
                    is_valid_excel_data = self.validate_excel_data(
                        self.bulk_update_to_dpe_ui.payload_data, validate_old_data)
                    logger.info("Is Valid Excel Data: " +
                                str(is_valid_excel_data))
                    if is_valid_excel_data:
                        self.total_hits_label.config(
                            text="Total Payload: "+str(len(self.bulk_update_to_dpe_ui.payload_data)), fg="black")

                        for i, each in enumerate(self.bulk_update_to_dpe_ui.payload_data):
                            logger.debug("Data Type Speified: " +
                                         str(each[-1]).lower())
                            # table_value = []
                            _values = None
                            if str(each[-1]).lower() == "multi":
                                table_value = []
                                if validate_old_data:
                                    old_data = each[2]
                                    logger.debug(
                                        "To Be Validated, Old Data: "+str(old_data))
                                    new_data = each[3]
                                    logger.debug(
                                        "To Be Validated, New Data: "+str(new_data))
                                    table_value.append(each[0])
                                    table_value.append(each[1])
                                    table_value.append(
                                        self.convert_list_to_str(old_data))
                                    logger.debug(
                                        "To Be Validated, Converted Old Data: "+str(table_value[2]))
                                    table_value.append(
                                        self.convert_list_to_str(new_data))
                                    logger.debug(
                                        "To Be Validated, Converted New Data: "+str(table_value[3]))
                                    table_value.append(each[4])
                                else:
                                    table_value.append(each[0])
                                    table_value.append(each[1])
                                    new_data = each[2]
                                    logger.debug(
                                        "Not Validated, New Data: "+str(new_data))
                                    table_value.append(
                                        self.convert_list_to_str(new_data))
                                    logger.debug(
                                        "Not Validated, Converted New Data: "+str(table_value[2]))
                                    table_value.append(each[3])
                                table_value.append("")
                                _values = tuple(table_value)
                            else:
                                each.append("")
                                _values = tuple(each)

                            self.data_tree.insert(
                                "", "end", iid=i, text=str(i+1), values=_values)

                        self.toggleInputField("disabled")
                    else:
                        self.data_tree.delete(*self.data_tree.get_children())
                        self.total_hits_label.config(
                            text="Invalid Excel Data.", fg="red")

                    ouuou = self.data_tree.get_children()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def get_data_in_type(self, data):
        try:
            output = data
            if isinstance(data, str):
                output = data.strip()

            return output

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def run_update_for_data(self, func):
        try:
            disable_btn = True
            self.completed_count = 0
            self.failed_count = 0
            is_valid_old_data = True if self.var_validate_old_data.get() == 1 else False
            is_append_new_data = True if self.var_append_new_data.get() == 1 else False
            all_table_data = self.data_tree.get_children()
            maximumval = len(self.bulk_update_to_dpe_ui.payload_data)
            move_fraction = 1/maximumval
            move_to_bottom = 0
            self.total_hits_label.config(
                text="Total Payload: "+str(maximumval), fg="black")
            self.bulk_update_to_dpe_ui.progress_bar = ttk.Progressbar(
                self.small_btn_frame, orient=HORIZONTAL, maximum=maximumval, mode="determinate", style="green.Horizontal.TProgressbar")
            self.bulk_update_to_dpe_ui.progress_bar.pack(
                fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")
            msg = ""
            for i, each in enumerate(self.bulk_update_to_dpe_ui.payload_data, 1):
                logger.debug(each)
                _type_value = each[4].lower().strip(
                ) if is_valid_old_data else each[3].lower().strip()
                post_data = [] if is_append_new_data and _type_value == "multi" else {}
                old_prop_data = {}
                if not(self.bulk_update_to_dpe_ui.is_halted):
                    if is_valid_old_data:
                        if is_append_new_data and each[4].lower().strip() == "multi":
                            for prop_data in each[3]:
                                chunk = {}
                                chunk[each[1]+"@Patch"] = 'true'
                                chunk[each[1]] = "+" + prop_data
                                post_data.append(chunk)
                            logger.debug(post_data)
                        else:
                            post_data[str(each[1]).strip()
                                      ] = self.get_data_in_type(each[3])
                            post_data[str(each[1]).strip(
                            ) + "@TypeHint"] = "String[]" if each[4].lower().strip() == "multi" else each[4].strip()

                        old_prop_data[str(each[1]).strip()
                                      ] = self.get_data_in_type(each[2])
                        logger.debug("Old Prop Data: "+str(old_prop_data))
                    else:
                        if is_append_new_data and each[3].lower().strip() == "multi":
                            for prop_data in each[2]:
                                chunk = {}
                                chunk[each[1]+"@Patch"] = 'true'
                                chunk[each[1]] = "+" + prop_data
                                post_data.append(chunk)
                            logger.debug(post_data)
                        else:
                            post_data[str(each[1]).strip()
                                      ] = self.get_data_in_type(each[2])
                            post_data[str(each[1]).strip(
                            ) + "@TypeHint"] = "String[]" if each[3].lower().strip() == "multi" else each[3].strip()

                    uri = each[0].strip()
                    logger.debug(str(i)+". URI: "+uri +
                                 ", PostData: "+str(post_data))
                    msg = func(uri, post_data,
                               is_valid_old_data, old_prop_data)
                    logger.debug(msg)

                    if msg == "Wrong username and Password - Http status 401":
                        self.total_hits_label.config(text=msg, fg="red")
                        self.userent["state"] = "normal"
                        self.passent["state"] = "normal"
                        self.export_btn["state"] = "normal"
                        disable_btn = False
                        break
                    else:
                        self.retrieve_data_count_label.config(
                            text="Running: "+str(i), fg="green")
                        msg_split = msg.split("-") if msg is not None else [uri, "Exception", "990"]
                        status = msg_split[-1].strip()
                        logger.debug(all_table_data)
                        if status == '200':
                            old_data = self.data_tree.item(
                                all_table_data[i-1])["values"]
                            if is_valid_old_data:
                                old_data[5] = "Completed"
                            else:
                                old_data[4] = "Completed"

                            updated_data = tuple(old_data)
                            logger.debug("Updated Data: "+str(updated_data))
                            self.data_tree.item(
                                all_table_data[i-1], text=str(i-1), values=updated_data)
                            # self.retrieve_data_count_label.config(text="Completed: "+str(i), fg="black")
                            self.completed_count += 1
                        else:
                            old_data = self.data_tree.item(
                                all_table_data[i-1])["values"]
                            if is_valid_old_data:
                                if status.strip() == '999':
                                    old_data[5] = "Mis Match"
                                elif status.strip() == "Not Avail":
                                    old_data[5] = "Not Avail"
                                elif status.strip() == "Available":
                                    old_data[5] = "Available"
                                else:
                                    old_data[5] = "Failed-"+str(status)
                            else:
                                if status.strip() == "Not Avail":
                                    old_data[4] = "Not Avail"
                                elif status.strip() == "Available":
                                    old_data[4] = "Available"
                                else:
                                    old_data[4] = "Failed-"+str(status)

                            updated_data = tuple(old_data)
                            self.data_tree.item(
                                all_table_data[i-1], text=str(i-1), values=tuple(updated_data))
                            # self.retrieve_data_count_label.config(text="Failed: "+str(i), fg="red")
                            self.failed_count += 1
                        if i > 2:
                            move_to_bottom = move_to_bottom + move_fraction
                        # current_pos = float("{:.1f}".format(move_to_bottom))
                        self.data_tree.yview_moveto(move_to_bottom)

                    self.bulk_update_to_dpe_ui.progress_bar["value"] = i
                    self.bulk_update_to_dpe_ui.update()
                else:
                    break

            self.bulk_update_to_dpe_ui.progress_bar.destroy()

            if disable_btn:
                self.export_btn["state"] = "disabled"
                self.retrieve_data_count_label.config(
                    text="Completed: "+str(self.completed_count), fg="black")
                self.failed_count_label.config(
                    text="Failed: "+str(self.failed_count), fg="red")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def t_update_data_in_dpe(self):
        try:
            update_thread = threading.Thread(target=self.update_data_in_dpe)
            update_thread.daemon = True
            update_thread.start()
            # update_thread.join()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def update_data_in_dpe(self):
        try:
            self.userent["state"] = "disabled"
            self.passent["state"] = "disabled"
            self.export_btn["state"] = "disabled"
            self.bulk_update_to_dpe_ui.update()

            current_username = self.varuserent.get().strip()
            current_passwd = self.varpassent.get().strip()

            self.update_dpe_prop_inst.set_uname_pass(
                current_username, current_passwd)

            selected_operation = self.var_upd_or_create_ent.get().strip().lower()
            logger.info("Selected Operation: "+str(selected_operation))

            if selected_operation == "update":
                self.run_update_for_data(
                    self.update_dpe_prop_inst.update_property_value)
            elif selected_operation == "create":
                self.run_update_for_data(
                    self.update_dpe_prop_inst.create_property_value)
            elif selected_operation == "update/create":
                self.run_update_for_data(
                    self.update_dpe_prop_inst.update_or_create_property_value)

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

    def openexcelfile(self):
        try:
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.bulk_update_to_dpe_ui.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.bulk_update_to_dpe_ui.excelfile:
                logger.debug("Selected Excel File: " +
                             self.bulk_update_to_dpe_ui.excelfile)
                self.varexcelfile.set(GenericFunctions.wrap_text_with_dot(
                    self.bulk_update_to_dpe_ui.excelfile, 50))

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def toggleInputField(self, val):
        try:
            self.userent["state"] = val
            self.passent["state"] = val
            self.ipenter["state"] = val
            self.queryent["state"] = val
            self.excelbtn["state"] = val
            self.operationent["state"] = val
            # self.querybuilderbtn["state"] = val
            # self.propertyent["state"] = val
            self.retrvdatabtn["state"] = val
            self.validate_old_data_ent["state"] = val
            self.append_new_data_ent["state"] = val
            self.envent["state"] = val
            if val == "disabled":
                updatedval = "normal"
            elif val == "normal":
                updatedval = "disabled"
            self.export_btn["state"] = updatedval

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initialize_variable()
            self.toggleInputField("normal")
            self.total_hits_label.config(text="")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.failed_count_label.config(text="", fg="black")
            self.data_tree.delete(*self.data_tree.get_children())
            # self.data_tree["columns"] = ()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# End of DPE Bulk Update

# Start of Placing the redirect


class DPESingleRedirect:
    def __init__(self, master):
        self.single_redirect__modal_ui = Toplevel(master)
        self.master = master
        self.single_redirect__modal_ui.state('zoomed')
        master.withdraw()
        self.single_redirect__modal_ui.title(
            APPLICATION_NAME + " - " + "Place Redirect"
        )
        self.single_redirect__modal_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.single_redirect__modal_ui.brandpic = PhotoImage(
            file=BRAND_PIC_FILE)
        self.single_redirect__modal_ui.iconphoto(False, self.brandpic)
        # self.stylesingle_redirect__modal_ui = ttk.Style()
        self.single_redirect__modal_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.single_redirect__modal_ui.configdata = configdata
        self.single_redirect__modal_ui.excelfile = ""
        self.single_redirect__modal_ui.payload_data = []
        self.redirect_dpe_prop_inst = None
        self.single_redirect__modal_ui.initial_redirect_validated = False

        # self.single_redirect__modal_uimaindesign()selected_excelfile
        self.create_menu_bar()
        self.main_design()

    def create_menu_bar(self):
        try:
            file_url = "https://docs.google.com/spreadsheets/d/17oqbHMBZ92CtiNPRKcZlYifHXGje9SwpVQjmzOWQCLs/export?format=xlsx&gid=0"
            self.main_menu = Menu(self.single_redirect__modal_ui)
            self.downloadmenu = Menu(self.main_menu, tearoff=0)
            self.downloadmenu.add_command(
                label="Redirection File", command=lambda *args: GenericFunctions.download_google_sheet(file_url)
            )
            self.main_menu.add_cascade(
                label="Sample File", menu=self.downloadmenu)
            self.configmenu = Menu(self.main_menu, tearoff=0)
            self.configmenu.add_command(
                label = "Set Path for IP", command=lambda *args: self.open_ip_path_config_modal()
            )
            self.main_menu.add_cascade(
                label="Configuration", menu=self.configmenu)
            self.single_redirect__modal_ui.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state('zoomed')
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            # self.single_redirect__modal_ui.
            self.single_redirect__modal_ui.destroy()
            # sleep(0.5)
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
            self.var_selected_source.set("Source Data from Excel")
            self.varipdata.set("")
            self.varpassent.set(self.decrypted_passwd)
            self.varexcelfile.set("Browse & Select Excel File")
            self.var_validate_data.set(1)
            self.var_selected_operation.set("Place Redirect")
            self.varredirect_payload.set("")
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

    def main_design(self):
        try:
            # Declare String Variable
            self.define_style()

            # String Variable
            self.var_selected_source = StringVar()
            self.var_selected_operation = StringVar()
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varexcelfile = StringVar()
            self.varredirect_payload = StringVar()
            self.var_validate_data = IntVar()

            # Initiate String Variable
            self.initiate_var()

            # Frame Creation
            self.main_frame = Frame(self.single_redirect__modal_ui)
            self.main_frame.pack(fill="x")

            self.main_btn_frame_sep = ttk.Separator(
                self.single_redirect__modal_ui)
            self.main_btn_frame_sep.pack(fill="x", padx=5, pady=10)

            self.main_btn_frame = Frame(self.single_redirect__modal_ui)
            self.main_btn_frame.pack(fill="x")

            self.btn_frame_details_sep = ttk.Separator(
                self.single_redirect__modal_ui)
            self.btn_frame_details_sep.pack(fill="x", padx=5, pady=10)

            self.main_details_frame = Frame(self.single_redirect__modal_ui)
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
                self.iplabelframe, textvariable = self.varenvdata, values = self.envdata, state="readonly")  # command=ipchange
            self.envent.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.iplabelframe.grid_columnconfigure(0, weight=1)
            self.ipenter = ttk.Entry(
                self.iplabelframe, textvariable=self.varipdata)
            # self.iplabelframe.grid(
            #     row=0, column=2, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.iplabelframe.grid(
                row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.main_frame.grid_columnconfigure(0, weight=1)

            # Validate Button
            self.validate_data_frame = LabelFrame(self.main_frame, text="")
            self.validate_data_frame.grid(
                row=1, column=0, padx=5, pady=(13, 7), sticky="nsew")

            self.validate_data_ent = ttk.Checkbutton(
                self.validate_data_frame, variable=self.var_validate_data, onvalue=1, offvalue=0, text="Validate Data")
            self.validate_data_ent.grid(
                row=0, column=0, padx=5, pady=10, ipadx=5, ipady=5, sticky="nsew")
            self.validate_data_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_columnconfigure(3, weight=1)

            # Redirect Remove/Place Button
            self.operation_type_dropdown_data = [
                "", "Place Redirect", "Remove Redirect"]  # , "Use Query Builder"
            self.operation_type_dropdown_ent = ttk.OptionMenu(
                self.validate_data_frame, self.var_selected_operation, *self.operation_type_dropdown_data)  # , command=self.changecheckbox
            self.operation_type_dropdown_ent.grid(row=0, column=1, padx=5,
                                          pady=5, sticky="nsew")
            self.validate_data_frame.grid_columnconfigure(1, weight=1)

            # Select label Frame:
            self.selectionlabelframe = LabelFrame(
                self.main_frame, text="Select the source & Enter Details", padx=5, pady=5)
            self.selectionlabelframe.grid(
                row=1, column=1, columnspan=3, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.source_dropdown_data = [
                "", "Source Data from Excel"]  # , "Use Query Builder"
            self.source_dropdown_ent = ttk.Combobox(
                self.selectionlabelframe, textvariable=self.var_selected_source, state="readonly", values=self.source_dropdown_data)
            # self.source_dropdown_ent = ttk.OptionMenu(
            #     self.selectionlabelframe, self.var_selected_source, *self.source_dropdown_data)  # , command=self.changecheckbox
            self.source_dropdown_ent["state"] = "disabled"
            self.source_dropdown_ent.grid(row=0, column=0, padx=5,
                                          pady=5, sticky="nsew")

            # Query Window or Excel Window
            self.select_file_btn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.select_file_btn.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.select_file_btn["state"] = "disabled"
            self.selected_file_label = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..", textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),
                                                 )
            self.selected_file_label.grid(
                row=0, column=2, padx=5, pady=5, sticky="nsew")
            self.redirec_payload_ent = ttk.Entry(self.selectionlabelframe, textvariable=self.varredirect_payload)

            self.selectionlabelframe.grid_columnconfigure(2, weight=1)
            # Button
            self.retrv_and_place_btn = ttk.Button(
                self.main_btn_frame, text="Place Redirect", style="mainBtn.TButton", command=self.t_validate_and_place_redirect)  # , command=self.validate_and_place_redirect
            self.retrv_and_place_btn.pack(
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

            self.export_btn = ttk.Button(
                self.small_btn_frame, text="Export",state="disabled", style="smallBtn.TButton", command=self.export_status_report)  # , command=self.exportData
            self.export_btn.pack(side="left", padx=5, pady=0, anchor="w")

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
                self.data_tree_frame, style="treeStyle.Treeview", show="headings", selectmode="extended", height=20)

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

            self.single_redirect__modal_ui.update()

            self.table_effective_width = self.data_tree.winfo_width() - 310
            
            self.create_table_column(self.table_effective_width, self.var_selected_operation)

            self.check_operation(self.var_selected_operation)
            self.update_operation_type()
            # Validation
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))
            self.var_selected_operation.trace(
                "w", lambda *args: self.check_operation(self.var_selected_operation)
            )
            self.var_selected_source.trace(
                "w", lambda *args: self.update_operation_type()
            )

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    ### Function / Callback

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

    def check_operation(self, varoperation):
        try:
            operation = str(varoperation.get()).lower()
            logger.info("Operation: %s", operation)
            if operation == "--select--":
                logger.info("--SELECT-- Selected")
                self.source_dropdown_ent["state"] = "disabled"
                self.retrv_and_place_btn["text"] = "Select Operation"
            elif operation == "place redirect":
                logger.info("Place Redirect Selected")
                options = ["Source Data from Excel"]
                self.source_dropdown_ent["state"] = "readonly"
                self.source_dropdown_ent["values"] = options
                self.retrv_and_place_btn["text"] = "Place Redirect"
                self.create_table_column(self.table_effective_width, varoperation)
                # ["value"] = options
                # self.add_to_option_menu(self.source_dropdown_ent, options)

            elif operation == "remove redirect":
                logger.info("Remove Redirect Selected")
                options = ["Source Data from Excel","Enter Payload"]
                self.source_dropdown_ent["state"] = "readonly"
                self.source_dropdown_ent["values"] = options
                self.retrv_and_place_btn["text"] = "Remove Redirect"
                self.create_table_column(self.table_effective_width, varoperation)
                # self.add_to_option_menu(self.source_dropdown_ent, options)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def update_operation_type(self):
        try:
            btn_text = self.var_selected_source.get()
            if btn_text == "Source Data from Excel":
                self.select_file_btn["state"] = "normal"
                if not self.select_file_btn.winfo_ismapped():
                    self.redirec_payload_ent.grid_forget()
                    self.select_file_btn.grid(
                            row=0, column=1, padx=5, pady=5, sticky="nsew")
                    self.selected_file_label.grid(
                        row=0, column=2, padx=5, pady=5, sticky="nsew")
            elif btn_text == "Enter Payload":
                self.select_file_btn["state"] = "disabled"
                if self.select_file_btn.winfo_ismapped():
                    self.select_file_btn.grid_forget()
                    self.selected_file_label.grid_forget()
                    self.redirec_payload_ent.grid(
                            row=0, column=1,columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")


        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def create_table_column(self, table_width, varoperation):
        try:
            operation = str(varoperation.get()).lower()
            if operation == "place redirect":
                self.data_tree["columns"] = ("1", "2", "3", "4")
                each_col_width = int(table_width/4)
                self.data_tree.column("1", width=each_col_width*2, stretch="yes")
                self.data_tree.column("2", width=each_col_width*2, stretch="yes")
                self.data_tree.column("3", width=60, stretch="yes", anchor="c")
                self.data_tree.column("4", width=250, stretch="yes", anchor="c")

                self.data_tree.heading("1", text="Source Path")
                self.data_tree.heading("2", text="Target URL")
                self.data_tree.heading("3", text="Type")
                self.data_tree.heading("4", text="Status")
            else:
                self.data_tree["columns"] = ("1", "2")
                self.data_tree.column("1", width=table_width, stretch="yes")
                self.data_tree.column("2", width=310, stretch="yes")

                self.data_tree.heading("1", text="Payload")
                self.data_tree.heading("2", text="Status")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
        
    def insert_into_table(self, pos, table_values):
        try:
            self.data_tree.insert("", "end", iid=pos,
                                  text=str(pos), values=table_values)
            self.data_tree.yview_moveto(1)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openexcelfile(self):
        try:
            logger.debug("--Single Redirect--")
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.single_redirect__modal_ui.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.single_redirect__modal_ui.excelfile:
                logger.debug("Selected Excel File: " +
                             self.single_redirect__modal_ui.excelfile)
                self.varexcelfile.set(self.single_redirect__modal_ui.excelfile)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_inputs(self, uname, passwd, environment, selected_ip, excel_file):
        try:
            output_status = False
            is_not_empty_uname = bool(uname)
            logger.debug("Username Not Empty: "+str(is_not_empty_uname))

            is_not_empty_passwd = bool(passwd)
            logger.debug("Password Not Empty: "+str(is_not_empty_passwd))

            is_not_empty_ip = bool(selected_ip)
            logger.debug("IP Not Empty: "+str(is_not_empty_ip))

            allowed_file_types = [".xlsx", ".xls", ".xlsm"]
            is_valid_file = False
            is_valid_input = False
            is_valid_excel_file = False
            operation_type = self.var_selected_source.get()
            if operation_type == "Source Data from Excel":
                if excel_file != "" and excel_file is not None:
                    is_valid_file = True
                    is_valid_input = True
                    is_valid_excel_file = GenericFunctions.is_valid_file_types(
                            excel_file, allowed_file_types)
                else:
                    is_valid_file = False
                    is_valid_input = True
                    is_valid_excel_file = False
            elif operation_type == "Enter Payload":
                entry_data = self.varredirect_payload.get().strip()
                if bool(entry_data):
                    is_valid_input = True
                    is_valid_file = True
                    is_valid_excel_file = True
                else:
                    is_valid_input = False
                    is_valid_file = True
                    is_valid_excel_file = True


            logger.debug("Valid File: "+str(is_valid_file))
            logger.debug("Valid Input: "+str(is_valid_input))
            
            logger.debug("Valid Excel File: "+str(is_valid_excel_file))

            is_valid_ip = GenericFunctions.validateIP(
                selected_ip, environment) if is_not_empty_ip else False
            logger.debug("Valid IP: "+str(is_valid_ip))

            if is_not_empty_ip and is_not_empty_uname and is_not_empty_passwd and is_valid_input and is_valid_file and is_valid_excel_file and is_valid_ip:
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

                if operation_type == "Source Data from Excel" and not(is_valid_excel_file):
                    error_list.append(
                        "\nInvalid Selected File. Only accepts below\n"+",".join(allowed_file_types))
                if operation_type == "Enter Payload" and not(is_valid_input):
                    error_list.append(
                        "\nInvalid input for Payloads")
                if not(is_valid_ip):
                    error_list.append(
                        "\nInvalid IP, Please select/enter correct IP")

                if bool(error_list):
                    messagebox.showerror("Below Error has occurred", "Please see the below list"+".".join(
                        error_list), parent=self.single_redirect__modal_ui)
                    logger.error("Below Error has occurred" +
                                 ".".join(error_list))

            logger.info("Data Validation Status: " + str(output_status))
            return output_status

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def redirect_validation(self, excel_list):
        try:
            # initial_validation = False
            over_all_error = {}
            duplicate_list = []
            is_not_empty_list = False
            if bool(excel_list):
                if bool(excel_list[0]):
                    is_not_empty_list = True

            is_list_valid = self.redirect_dpe_prop_inst.validate_data(
                excel_list) if is_not_empty_list else False
            if is_list_valid:
                old_urls = [x[0].strip() for x in excel_list]
                duplicate_list = self.redirect_dpe_prop_inst.get_duplicate_old_url(
                    old_urls)

            is_not_duplicate_old_url = not(bool(duplicate_list))

            available_blank_data = self.redirect_dpe_prop_inst.get_empty_url(
                excel_list) if is_list_valid else []

            is_not_blank_data = not(bool(available_blank_data))

            if is_not_empty_list and is_list_valid and is_not_duplicate_old_url and is_not_blank_data:
                self.single_redirect__modal_ui.initial_redirect_validated = True
            else:
                self.single_redirect__modal_ui.initial_redirect_validated = False
                if not(is_not_empty_list):
                    over_all_error["empty list"] = "Selected Excel File Doesn't have any data. Please select a valid one."
                if not(is_list_valid):
                    over_all_error["invalid data"] = "Selected Excel File have invalid data. Please select a valid one."
                if not(is_not_duplicate_old_url):
                    over_all_error["duplicate old url"] = duplicate_list
                if not(is_not_blank_data):
                    over_all_error["blank urls"] = available_blank_data

                logger.error(over_all_error)

                # pop_up_modal = Toplevel(self.single_redirect__modal_ui)
                self.open_popup_modal(over_all_error)

            # return initial_validation
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def export_status_report(self):
        try:
            ## Select the File
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            save_file = filedialog.asksaveasfilename(
                initialdir=BASE_SCRIPT_PATH, initialfile="data_output.xlsx", title="Save Data", filetypes=types, defaultextension=types
            )
            logger.info("File Name to Export the Data: "+str(save_file))
            if save_file:
                all_table_row_id = self.data_tree.get_children()
                all_table_data = []
                if bool(all_table_row_id):
                    all_table_data.append(["Source Path","Target URL","Type","Status"])
                    for each_row_id in all_table_row_id:
                        all_table_data.append(self.data_tree.item(each_row_id)["values"])

                    logger.debug("Exported Data: " + str(all_table_data))
                    _workbook = xlsxwriter.Workbook(save_file)
                    _worksheet = _workbook.add_worksheet()

                    for x in range(len(all_table_data)):
                        for y in range(len(all_table_data[x])):
                            _worksheet.write(x, y, str(all_table_data[x][y]))

                    _workbook.close()
                    messagebox.showinfo("Success!!!","Exported Successfully", parent=self.single_redirect__modal_ui)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.total_hits_label.config(
                            text="Some Error occurred. Check Logs", fg="red")
            self.retrieve_data_count_label.config(
                            text="", fg="black")

    def open_ip_path_config_modal(self):
        try:
            self.ipconfig_pop_up_modal = Toplevel(self.single_redirect__modal_ui)
            self.single_redirect__modal_ui.wm_attributes("-disabled", True)
            
            def closethiswindow():
                try:
                    self.single_redirect__modal_ui.focus_set()
                    self.single_redirect__modal_ui.wm_attributes(
                        "-disabled", False)
                    self.ipconfig_pop_up_modal.destroy()
                except:
                    logger.error("Below Exception occured: ", exc_info=True)
                
            def save_config():
                global configdata
                dotcom_path = self.ipconfig_pop_up_modal.dotcompath_ent.get().strip()
                sand_path = self.ipconfig_pop_up_modal.sandpath_ent.get().strip()
                is_valid_dotcom_path = True if bool(dotcom_path) and GenericFunctions.is_valid_dpepath(dotcom_path, "ip", "/etc/map/http") else False
                is_valid_sand_path = True if bool(sand_path) and GenericFunctions.is_valid_dpepath(sand_path, "ip", "/etc/map/http") else False

                if is_valid_dotcom_path and is_valid_sand_path:
                    configdata["redirectpathdotcomip"] = dotcom_path
                    configdata["redirectpathsandip"] = sand_path

                    _config_saved = edcfg.updateConfig(configdata, CONFIG_FILE)

                    if _config_saved:
                        logger.info("Configuration Saved: %s", _config_saved)
                        closethiswindow()
                    else:
                        messagebox.showerror("Error Occurred!","Couldn't Save data, Check logs", parent=self.ipconfig_pop_up_modal)
                else:
                    messagebox.showerror("Error Occurred!","Invalid or empty value,\n Check logs for more info", parent=self.ipconfig_pop_up_modal)

            self.ipconfig_pop_up_modal.focus_set()
            self.ipconfig_pop_up_modal.title(
                APPLICATION_NAME + " - " + "Change IP Redirectpath")
            self.ipconfig_pop_up_modal.geometry("+100+20")
            self.ipconfig_pop_up_modal.minsize(400, 200)
            self.ipconfig_pop_up_modal.maxsize(520, SCREEN_HEIGHT)
            self.ipconfig_pop_up_modal.iconphoto(False, self.brandpic)
            self.ipconfig_pop_up_modal.resizable(False, False)
            self.ipconfig_pop_up_modal.transient(self.single_redirect__modal_ui)
            self.ipconfig_pop_up_modal.protocol(
                "WM_DELETE_WINDOW", closethiswindow)

            dotcom_redirect_path = configdata.get("redirectpathdotcomip","")
            sand_redirect_path = configdata.get("redirectpathsandip","")

            self.ipconfig_pop_up_modal.main_frame = Frame(
                self.ipconfig_pop_up_modal)
            self.ipconfig_pop_up_modal.main_frame.pack(
                fill="x", padx=10, pady=10, anchor=CENTER)

            self.ipconfig_pop_up_modal.main_label = ttk.Label(self.ipconfig_pop_up_modal.main_frame, text="**This setting is for Environment IP**")
            self.ipconfig_pop_up_modal.main_label.pack(
                fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            self.ipconfig_pop_up_modal.dotcompath_lframe = LabelFrame(
                self.ipconfig_pop_up_modal.main_frame, text="Enter .com Path", padx=5, pady=5)
            self.ipconfig_pop_up_modal.dotcompath_lframe.pack(
                fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            self.ipconfig_pop_up_modal.dotcompath_ent = Entry(self.ipconfig_pop_up_modal.dotcompath_lframe)
            self.ipconfig_pop_up_modal.dotcompath_ent.pack(fill="x", padx=5, pady=5,
                              ipadx=5, ipady=5, anchor=CENTER)
            
            self.ipconfig_pop_up_modal.dotcompath_ent.insert(0, dotcom_redirect_path)
            
            self.ipconfig_pop_up_modal.sandpath_lframe = LabelFrame(
                self.ipconfig_pop_up_modal.main_frame, text="Enter s& Path", padx=5, pady=5)
            self.ipconfig_pop_up_modal.sandpath_lframe.pack(
                fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            self.ipconfig_pop_up_modal.sandpath_ent = Entry(self.ipconfig_pop_up_modal.sandpath_lframe)
            self.ipconfig_pop_up_modal.sandpath_ent.pack(fill="x", padx=5, pady=5,
                              ipadx=5, ipady=5, anchor=CENTER)
            self.ipconfig_pop_up_modal.sandpath_ent.insert(0, sand_redirect_path)
            
            self.ipconfig_pop_up_modal.cancel_btn = ttk.Button(
                self.ipconfig_pop_up_modal.main_frame, text="Cancel", style="smallBtn.TButton", command=closethiswindow)  # , command=self.exportData
            self.ipconfig_pop_up_modal.cancel_btn.pack(side="right", padx=5, pady=0, anchor="w")

            self.ipconfig_pop_up_modal.save_btn = ttk.Button(
                self.ipconfig_pop_up_modal.main_frame, text="Save", style="smallBtn.TButton", command=save_config)  # , command=self.exportData
            self.ipconfig_pop_up_modal.save_btn.pack(side="right", padx=5, pady=0, anchor="w")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def open_popup_modal(self, error_data):
        try:
            self.error_pop_up_modal = Toplevel(self.single_redirect__modal_ui)
            
            def closethiswindow():
                try:
                    self.single_redirect__modal_ui.focus_set()
                    self.single_redirect__modal_ui.wm_attributes(
                        "-disabled", False)
                    self.error_pop_up_modal.destroy()
                except:
                    logger.error("Below Exception occured: ", exc_info=True)

            self.single_redirect__modal_ui.wm_attributes("-disabled", True)
            self.error_pop_up_modal.focus_set()
            self.error_pop_up_modal.title(
                APPLICATION_NAME + " - " + "Initial Error in Redirection")
            self.error_pop_up_modal.geometry("720x640+100+20")
            self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
            self.error_pop_up_modal.iconphoto(False, self.brandpic)
            self.error_pop_up_modal.resizable(False, False)
            self.error_pop_up_modal.transient(self.single_redirect__modal_ui)
            self.error_pop_up_modal.protocol(
                "WM_DELETE_WINDOW", closethiswindow)
            self.error_pop_up_modal.error_data = error_data

            self.error_pop_up_modal.title_frame = Frame(
                self.error_pop_up_modal)
            self.error_pop_up_modal.title_frame.pack(
                fill="x", padx=10, pady=10, anchor=CENTER)

            self.error_pop_up_modal.title_label = ttk.Label(
                self.error_pop_up_modal.title_frame, text="Initial Error that was detected in the data", anchor=CENTER, font=(FONT_NAME, 16))
            self.error_pop_up_modal.title_label.pack(fill="x")

            self.error_pop_up_modal.error_list_frame = Frame(
                self.error_pop_up_modal)
            self.error_pop_up_modal.error_list_frame.pack(
                fill="both", expand="yes", padx=10, pady=10, anchor=CENTER)

            self.error_pop_up_modal.error_list = Listbox(
                self.error_pop_up_modal.error_list_frame, selectmode="extended", activestyle=NONE)

            self.error_pop_up_modal.scroll_y = Scrollbar(
                self.error_pop_up_modal.error_list_frame, orient=VERTICAL, command=self.error_pop_up_modal.error_list.yview)
            self.error_pop_up_modal.error_list.config(
                yscrollcommand=self.error_pop_up_modal.scroll_y.set)
            self.error_pop_up_modal.scroll_y.pack(side="right", fill="y")

            self.error_pop_up_modal.error_list.pack(fill="both", expand="yes")

            for key in self.error_pop_up_modal.error_data:
                self.error_pop_up_modal.error_list.insert(
                    "end", "-"*50 + key.title()+"-"*50)
                if isinstance(self.error_pop_up_modal.error_data[key], list):
                    for each in self.error_pop_up_modal.error_data[key]:
                        self.error_pop_up_modal.error_list.insert("end", each)
                else:
                    self.error_pop_up_modal.error_list.insert(
                        "end", self.error_pop_up_modal.error_data[key])

            self.single_redirect__modal_ui.wait_window(self.error_pop_up_modal)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def t_validate_and_place_redirect(self):
        try:
            _running_thread = threading.Thread(target=self.validate_and_place_redirect)
            _running_thread.daemon = True
            _running_thread.start()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_and_place_redirect(self):
        try:
            self.total_hits_label.config(text="", fg="black")
            self.resetbtn["state"] = "disabled"
            self.single_redirect__modal_ui.update()

            uname = self.varuserent.get().strip()
            passwd = self.varpassent.get().strip()

            environment = self.varenvdata.get().lower()
            selected_ip = (self.varipdata.get().lower().strip()
                           if environment == "ip" else configdata[environment])
            excel_file = self.single_redirect__modal_ui.excelfile
            run_the_operation = True
            if environment.lower() == "production":
                run_the_operation = messagebox.askyesnocancel(
                    "Please confirm", "Do you want to Run\nthe Operation in Production?", parent=self.single_redirect__modal_ui)

            if run_the_operation:
                is_validated = self.validate_inputs(
                    uname, passwd, environment, selected_ip, excel_file)

                if is_validated:
                    self.toggleInputField("disabled")
                    self.redirect_dpe_prop_inst = ContentPathValidator(
                            uname, passwd)
                    is_user_authenticated = self.redirect_dpe_prop_inst.is_authenticated(
                            selected_ip)
                    if is_user_authenticated:
                        operation_type = str(self.var_selected_operation.get()).lower()
                        if operation_type == "place redirect":
                            self.single_redirect__modal_ui.update()

                            # self.redirect_dpe_prop_inst = ContentPathValidator(
                            #     uname, passwd)
                            # is_user_authenticated = self.redirect_dpe_prop_inst.is_authenticated(
                            #     selected_ip)
                            excel_to_list = self.redirect_dpe_prop_inst.sorted_excel_to_list(
                                excel_file, 0)
                            need_validation = self.var_validate_data.get()
                            self.single_redirect__modal_ui.initial_redirect_validated = True

                            # if is_user_authenticated:
                            if need_validation:
                                self.redirect_validation(excel_to_list)

                            if self.single_redirect__modal_ui.initial_redirect_validated:
                                i = 0
                                logger.debug("Excel File Data START")
                                logger.debug(excel_to_list)
                                logger.debug("Excel File Data END")
                                maximumval = len(excel_to_list)
                                self.total_hits_label.config(
                                    text="Total Payload: "+str(maximumval))
                                self.single_redirect__modal_ui.progress_bar = ttk.Progressbar(
                                    self.small_btn_frame, orient=HORIZONTAL, maximum=maximumval, mode="determinate", style="green.Horizontal.TProgressbar")
                                self.single_redirect__modal_ui.progress_bar.pack(
                                    fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")

                                for each_row in excel_to_list:
                                    logger.debug("Each Row: "+str(i+1))
                                    logger.debug(each_row)
                                    old_content_path = each_row[0]
                                    target_url = each_row[1]
                                    redirection_type = 301
                                    if len(each_row) == 3:
                                        if bool(str(each_row[2]).strip()):
                                            redirection_type = int(float(str(each_row[2]).strip()))
                                    each_row[2] = redirection_type
                                    logger.debug("Source URL: %s, Target URL: %s, Type: %s", old_content_path, target_url, str(redirection_type))
                                    if need_validation:
                                        if redirection_type in (301, 302):
                                            old_content_path = self.redirect_dpe_prop_inst.add_dollar_to_the_end(
                                                old_content_path)
                                            if self.redirect_dpe_prop_inst.valid_source_path(old_content_path):
                                                if self.redirect_dpe_prop_inst.no_redirect_on_target(target_url):
                                                    if self.redirect_dpe_prop_inst.source_not_same_as_target(old_content_path, target_url, environment):
                                                        if self.redirect_dpe_prop_inst.valid_source_url_without_spcl_chars(old_content_path):
                                                            if self.redirect_dpe_prop_inst.valid_target_url_without_spcl_chars(target_url):
                                                                # each_row.append
                                                                redirect_status = self.redirect_dpe_prop_inst.place_redirect(
                                                                    selected_ip, old_content_path, target_url, redirection_type)
                                                                if redirect_status == "Wrong username and password - HTTP Status Code 401":
                                                                    self.total_hits_label.config(
                                                                        text="Wrong Username and Password", fg="red")
                                                                    break
                                                                else:
                                                                    each_row.append(
                                                                        redirect_status)
                                                            else:
                                                                each_row.append(
                                                                    "Target have special chars")
                                                        else:
                                                            each_row.append(
                                                                "Source have special chars")

                                                    else:
                                                        each_row.append(
                                                            "Source and Target same")
                                                else:
                                                    each_row.append(
                                                        "Target has redirect")
                                            else:
                                                each_row.append(
                                                    "Invalid Source Path")
                                        else:
                                            each_row.append("Invalid Redir Status")
                                    else:
                                        redirect_status = self.redirect_dpe_prop_inst.place_redirect(
                                            selected_ip, old_content_path, target_url, redirection_type)
                                        if redirect_status == "Wrong username and password - HTTP Status Code 401":
                                            self.total_hits_label.config(
                                                text="Wrong Username and Password", fg="red")
                                            break
                                        else:
                                            each_row.append(redirect_status)

                                    self.insert_into_table(i, tuple(each_row))

                                    i += 1
                                    self.single_redirect__modal_ui.progress_bar["value"] = i
                                    self.retrieve_data_count_label.config(
                                        text="Current: "+str(i))
                                    self.single_redirect__modal_ui.update()
                                    sleep(configdata["sleeptime"])

                                self.single_redirect__modal_ui.progress_bar.destroy()
                                self.export_btn["state"] = "normal"
                                self.resetbtn["state"] = "normal"
                            else:
                                self.toggleInputField("normal") 
                        elif operation_type == "remove redirect":
                            self.remove_redirect(self.redirect_dpe_prop_inst, excel_file, environment, selected_ip)
                            self.export_btn["state"] = "normal"
                            self.resetbtn["state"] = "normal"

                    else:
                        self.total_hits_label.config(
                            text="Wrong Username and Password", fg="red")
                        self.userent["state"] = "normal"
                        self.passent["state"] = "normal"

                        self.retrv_and_place_btn["state"] = "normal"
                        self.resetbtn["state"] = "normal"
                else:
                    self.resetbtn["state"] = "normal"
            else:
                self.resetbtn["state"] = "normal"
 
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.total_hits_label.config(
                            text="Some Error occurred. Check Logs", fg="red")
            self.retrieve_data_count_label.config(
                            text="", fg="black")
            self.resetbtn["state"] = "normal"

    def remove_redirect(self, redirect_obj, file, environment, selected_ip):
        try:
            self.single_redirect__modal_ui.update()
            selected_source = self.var_selected_source.get()
            payloads = []
            valid_operation = False
            if selected_source == "Source Data from Excel":
                valid_operation = True
                payloads = redirect_obj.sorted_excel_to_list(file)
            elif selected_source == "Enter Payload":
                valid_operation = True
                data = self.varredirect_payload.get()
                payloads = [[x.strip(),] for x in data.split(",") if x.strip() != "" ]
            else:
                messagebox.showerror("Error!!", "Please select a valid operation", parent=self.single_redirect__modal_ui)

            if valid_operation:
                global operationdata
                content_root = operationdata.get("content root", "/content/pwc")
                content_dam_root = operationdata.get("content dam root", "/content/dam/pwc")
                maximumval = len(payloads)
                self.total_hits_label.config(
                                    text="Total Payload: "+str(maximumval))
                self.single_redirect__modal_ui.progress_bar = ttk.Progressbar(
                    self.small_btn_frame, orient=HORIZONTAL, maximum=maximumval, mode="determinate", style="green.Horizontal.TProgressbar")
                self.single_redirect__modal_ui.progress_bar.pack(
                    fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")
                for counter, payload_row in enumerate(payloads) :
                    pwc_com = True
                    payload = payload_row[0]
                    # territory = payload.replace(content_root,"").replace(content_dam_root,"")
                    territory_path = payload.replace(content_root,"").replace(content_dam_root,"")
                    territory = territory_path[1:3] if territory_path[0] == "/" else territory_path[0:2] 
                    if territory.isnumeric():
                        pwc_com = False
                    logger.debug("Payload: %s, Territory: %s, PwC_COM: %s", payload, territory, pwc_com)
                    remove_redirect_status = redirect_obj.remove_redirect(payload, selected_ip, environment, pwc_com)
                    # print(remove_redirect_status)
                    _message = remove_redirect_status.get("msg", "No message found")
                    _status = remove_redirect_status.get("status", "Exception")
                    if _status == 401:
                        self.total_hits_label.config(
                            text="Wrong Username and Password", fg="red")
                        break
                    elif _status == 403:
                        self.total_hits_label.config(
                            text="Forbidden to access", fg="red")
                        break
                    else:
                        payload_row.append(f"{_status} - {_message}")

                    self.insert_into_table(counter+1, tuple(payload_row))
                    self.single_redirect__modal_ui.progress_bar["value"] = counter+1
                    self.retrieve_data_count_label.config(
                        text="Current: "+str(counter+1))
                    self.single_redirect__modal_ui.update()
                    sleep(configdata["sleeptime"])

                self.single_redirect__modal_ui.progress_bar.destroy()
                    
                    
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def toggleInputField(self, val):
        try:
            self.userent["state"] = val
            self.passent["state"] = val
            self.ipenter["state"] = val
            self.select_file_btn["state"] = val
            self.retrv_and_place_btn["state"] = val
            self.validate_data_ent["state"] = val
            self.operation_type_dropdown_ent["state"] = val
            self.envent["state"] = val
            self.source_dropdown_ent["state"] = val if val=="disabled" else "readonly"
            self.redirec_payload_ent["state"] = val
            if val == "disabled":
                updatedval = "normal"
            elif val == "normal":
                updatedval = "disabled"
            self.export_btn["state"] = updatedval

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initiate_var()
            self.toggleInputField("normal")
            self.single_redirect__modal_ui.excelfile = ""
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.data_tree.delete(*self.data_tree.get_children())
            # self.data_tree["columns"] = ()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# End of placing the redirect

# Start of DPE Redirection


class DPERedirectionCheck:
    def __init__(self, master):
        self.redirection_check_window = Toplevel(master)
        self.master = master
        self.redirection_check_window.state("zoomed")
        master.withdraw()
        self.redirection_check_window.title(
            APPLICATION_NAME + " - " + "DPE Redirection Check"
        )
        self.redirection_check_window.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.redirection_check_window.brandpic = PhotoImage(
            file=BRAND_PIC_FILE)
        self.redirection_check_window.iconphoto(False, self.brandpic)
        self.styleredirection_check_window = ttk.Style()
        self.redirection_check_window.protocol(
            "WM_DELETE_WINDOW", lambda root=master: self.reopenroot(root)
        )
        self.redirection_check_window.configdata = configdata
        self.redirection_check_window.excelfile = ""
        self.redirection_check_window.payload_data = []
        # self.redirection_check_windowmaindesign()selected_excelfile
        self.check_redirect_instance = RedirectValidation()
        self.create_menu_bar()
        self.mainui_design()

    def create_menu_bar(self):
        try:
            file_url = "https://docs.google.com/spreadsheets/d/17oqbHMBZ92CtiNPRKcZlYifHXGje9SwpVQjmzOWQCLs/export?format=xlsx&gid=1889758099"
            self.main_menu = Menu(self.redirection_check_window)
            self.downloadmenu = Menu(self.main_menu, tearoff=0)
            self.downloadmenu.add_command(
                label="Validate Redirect", command=lambda *args: GenericFunctions.download_google_sheet(file_url)
            )
            self.main_menu.add_cascade(
                label="Sample File", menu=self.downloadmenu)
            self.redirection_check_window.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state("zoomed")
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.redirection_check_window.destroy()
            root.after(1000, self.changeRoot(root))
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def initialize_variable(self):
        try:
            self.varexcelfile.set("Browse & Select Excel File")
            self.varoperation.set("Validate Redirect")
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

            self.window_style.configure(
                "titleLabel.TLabel", font=(FONT_NAME, 16, "bold"))

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def create_label_frame(self):
        try:
            self.datalabelframe = LabelFrame(
                self.redirection_check_window, text="Enter Details")
            self.databuttonframe = LabelFrame(self.redirection_check_window)
            self.data_log_frame = LabelFrame(
                self.redirection_check_window, text="Logs")
            self.datalabelframe.pack(
                fill="x", padx=10, pady=10, ipadx=10, ipady=10)
            self.databuttonframe.pack(
                fill="x", padx=10, pady=10, ipadx=10, ipady=10)
            self.data_log_frame.pack(
                fill="both", expand="yes", padx=10, pady=10)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def mainui_design(self):
        try:
            self.define_style()

            # String Variable
            self.varexcelfile = StringVar()
            self.varoperation = StringVar()

            # Initiate Var
            self.initialize_variable()

            # Trace data variables
            self.varoperation.trace(
                "w", lambda *args: self.create_data_column()
            )

            # Initiate Label Frames
            self.create_label_frame()

            # main Frame
            self.mainframe = Frame(self.datalabelframe)
            self.mainframe.pack(fill="x", expand="yes")

            self.title_label = ttk.Label(
                self.mainframe, text="Validate Placed Redirect in DPE or other System", anchor=CENTER, style="titleLabel.TLabel", font=(FONT_NAME, 16, "bold"))
            self.title_label.grid(
                row=0, column=0, columnspan=4, padx=5, pady=5, ipadx=15, ipady=15, sticky="nsew")
            self.mainframe.grid_columnconfigure(0, weight=1)

            # Select label Frame:
            self.selectionlabelframe = LabelFrame(
                self.mainframe, text="Select the source & Enter Details", padx=5, pady=5)
            self.selectionlabelframe.grid(
                row=1, column=0, columnspan=4, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.mainframe.grid_columnconfigure(0, weight=1)
            # Excel Window
            operation = ["Validate Redirect", "URL Status Check"]
            self.operation_option_menu = ttk.Combobox(
                self.selectionlabelframe, textvariable = self.varoperation, values = operation, state="readonly")
            self.operation_option_menu.grid(
                row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.excelbtn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.excelbtn.grid(
                row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.excelquerylabel = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..",
                                             textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),)
            self.excelquerylabel.grid(
                row=0, column=2, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.selectionlabelframe.grid_columnconfigure(2, weight=1)

            # Button
            self.buttonFrame = Frame(self.databuttonframe)
            self.buttonFrame.pack(fill="both", expand="yes")
            self.retrvdatabtn = ttk.Button(
                self.buttonFrame, text="Start", style="mainBtn.TButton", command=self.perform_selected_operation)  # , command=self.retrvdata
            self.retrvdatabtn.pack(side="left", expand="yes")
            self.resetbtn = ttk.Button(
                self.buttonFrame, text="Reset All", style="mainBtn.TButton", command=self.resetAll)  # , command=self.resetAll
            self.resetbtn.pack(side="left", expand="yes")
            self.exitbtn = ttk.Button(self.buttonFrame, text="Exit Window", style="mainBtn.TButton",
                                      command=lambda root=self.master: self.reopenroot(root))
            self.exitbtn.pack(side="left", expand="yes")

            # Tree Frame
            self.progress_bar_frame = Frame(self.data_log_frame)
            self.progress_bar_frame.pack(
                fill="x", expand="yes", padx=5, pady=5)
            self.data_tree_frame = Frame(self.data_log_frame)

            self.small_btn_frame = Frame(self.progress_bar_frame)
            self.small_btn_frame.pack(
                side="left", anchor="nw")

            self.export_btn = ttk.Button(
                self.small_btn_frame, text="Export",state="disabled", style="smallBtn.TButton", command=self.export_status_report)  # , command=self.exportData
            self.export_btn.pack(side="left", padx=5, pady=0, anchor="w")

            self.data_tree = ttk.Treeview(
                self.data_tree_frame, style="treeStyle.Treeview", show="headings", columns=("1", "2", "3"), selectmode="extended", height=10)

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

            self.data_tree_frame.pack(
                fill="both", expand="yes", padx=5, pady=5)

            self.redirection_check_window.update()
            tree_width = self.data_tree.winfo_width()
            each_column_width = int(tree_width/5)
            if self.varoperation.get().lower() == "validate redirect":
                self.data_tree.column("1", stretch="yes",
                                    width=each_column_width*2, anchor="c")
                self.data_tree.column("2", stretch="yes",
                                    width=each_column_width*2, anchor="c")
                self.data_tree.column("3", stretch="yes",
                                    width=each_column_width, anchor="c")

                self.data_tree.heading("1", text='Source URL')
                self.data_tree.heading("2", text='Target URL')
                self.data_tree.heading("3", text='Status')
            else:
                self.data_tree.column("1", stretch="yes",
                                    width=each_column_width*4, anchor="c")
                self.data_tree.column("2", stretch="yes",
                                    width=each_column_width, anchor="c")

                self.data_tree.heading("1", text='Source URL')
                self.data_tree.heading("2", text='Status')

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    # Function/Callback

    def validation_of_data(self, file, urllist, operation):
        try:
            is_valid_urllist = False
            is_valid_operation = bool(operation)
            is_redirect_operation = True if operation.lower() == "validate redirect" else False
            is_valid_file = True if(
                file.strip() != "" and file is not None) else False
            is_file_opened = False
            if is_valid_file:
                try:
                    t = open(file, "r+")
                except PermissionError:
                    is_file_opened = True
                    logger.error("File is already opened.", exc_info=True)
                else:
                    t.close()

            logger.debug("Is Valid File? "+str(is_valid_file))
            logger.debug("File is already Opened? "+str(is_file_opened))
            not_empty = bool(urllist)
            is_a_list = isinstance(urllist, list)
            logger.debug("List Not Empty? "+str(not_empty))
            any_exception = True if (
                urllist == "Please close the file." or urllist == "Invalid File Type.") else False

            if not_empty and is_a_list and not(is_file_opened) and is_valid_operation:
                is_list = isinstance(urllist[0], list)
                logger.debug("Element of URL List is a List? %s", str(is_list))
                if is_list:
                    counter = 0
                    for each in urllist:
                        if is_redirect_operation:
                            if len(each) >= 2:
                                counter += 1
                        else:
                            if len(each) >= 1:
                                counter += 1
                    if counter == len(urllist):
                        is_valid_urllist = True
                    logger.debug("Valid URL List? "+str(is_valid_urllist) +
                                 ", Counter: "+str(counter)+", Length: "+str(len(urllist)))

            error_list = []
            if not(is_valid_file):
                error_list.append("\nPlease select a file!")
            if not(is_valid_urllist):
                error_list.append("\nPlease select a file with Valid Data!")
            if is_file_opened:
                error_list.append(
                    "\nPlease close the file or Permission Error!")
            if any_exception:
                error_list.append("\n"+str(urllist))

            if bool(error_list):
                messagebox.showerror("Below Error has occured!", "Errors are as following:" +
                                     ".".join(error_list), parent=self.redirection_check_window)
            final_output = is_valid_urllist and is_valid_file

            return final_output
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def perform_selected_operation(self):
        try:

            # self.check_redirect_instance = RedirectValidation()
            excel_to_list = self.check_redirect_instance.excel_to_list(
                self.redirection_check_window.excelfile) if self.redirection_check_window.excelfile.strip() != "" else []
            # operation = operation = ["Validate Redirect", "URL Status Check"]
            operation = self.varoperation.get()
            is_redirect_operation = True if operation.lower() == "validate redirect" else False
            valid_data = self.validation_of_data(
                self.redirection_check_window.excelfile, excel_to_list, operation)

            if valid_data:
                maximum_val = len(excel_to_list)
                status_list = []
                prog_bar = ttk.Progressbar(self.progress_bar_frame, orient="horizontal",
                                           mode="determinate", maximum=maximum_val)
                prog_bar.pack(fill="x")
                headers = ["Source", "Target", "Status"] if is_redirect_operation else ["Source", "Status"]
                self.redirection_check_window.payload_data.append(headers)

                for i, each in enumerate(excel_to_list, 0):
                    src = each[0]
                    target = each[1] if is_redirect_operation else ""
                    chunks = []
                    if GenericFunctions.validate_input_url(src):
                        if is_redirect_operation:
                            current_status = self.check_redirect_instance.check_redirect(
                                src, target)
                            chunks = [src, target, current_status]
                        else:
                            _current_status = self.check_redirect_instance.get_url_status(
                                src)
                            current_status = _current_status.get("message", "999 - Invalid Key Exception")
                            chunks = [src, current_status]
                    else:
                        current_status = "False"
                        chunks = [src, target, current_status] if is_redirect_operation else [src, current_status]
                    status_list.append(current_status)
                    self.redirection_check_window.payload_data.append(chunks)
                    if is_redirect_operation:
                        self.data_tree.insert(
                            "", "end", iid=i+1, text=str(i+1), values=(src, target, current_status))
                    else:
                        self.data_tree.insert(
                            "", "end", iid=i+1, text=str(i+1), values=(src, current_status))
                    self.data_tree.yview_moveto(1)
                    prog_bar["value"] = i+1
                    self.redirection_check_window.update()

                prog_bar.destroy()
                self.toggleInputField("disabled")
                output = self.check_redirect_instance.write_to_excel(
                    self.redirection_check_window.excelfile, status_list, is_redirect_operation)
                if output != "Successfully Saved the Data.":
                    messagebox.showerror(
                        "Some Erorr Occured!", output, parent=self.redirection_check_window)
                else:
                    messagebox.showinfo("Success!", output,
                                        parent=self.redirection_check_window)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openexcelfile(self):
        try:
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.redirection_check_window.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.redirection_check_window.excelfile:
                logger.debug("Selected Excel File: " +
                             self.redirection_check_window.excelfile)
                self.varexcelfile.set(self.redirection_check_window.excelfile)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def create_data_column(self):
        try:
            operation = self.varoperation.get()
            if operation.lower() == "redirect check":
                self.data_tree["columns"] = ("1", "2", "3")
                width = self.data_tree.winfo_width()
                each_col_width = int(width/5)

                self.data_tree.column("1", stretch="yes",
                                    width=each_col_width*2, anchor="c")
                self.data_tree.column("2", stretch="yes",
                                    width=each_col_width*2, anchor="c")
                self.data_tree.column("3", stretch="yes",
                                    width=each_col_width, anchor="c")

                self.data_tree.heading("1", text='Source URL')
                self.data_tree.heading("2", text='Target URL')
                self.data_tree.heading("3", text='Status')
            else:
                self.data_tree["columns"] = ("1", "2")
                width = self.data_tree.winfo_width()
                each_col_width = int(width/4)

                self.data_tree.column(
                    "1", width=each_col_width*3, stretch="yes")
                self.data_tree.column(
                    "2", width=each_col_width, stretch="yes", anchor="c")

                self.data_tree.heading("1", text="Source")
                self.data_tree.heading("2", text="Status")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def export_status_report(self):
        try:
            ## Select the File
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            save_file = filedialog.asksaveasfilename(
                initialdir=BASE_SCRIPT_PATH, initialfile="data_output.xlsx", title="Save Data", filetypes=types, defaultextension=types
            )
            logger.info("File Name to Export the Data: "+str(save_file))
            if save_file:
                all_table_row_id = self.data_tree.get_children()
                all_table_data = []

                logger.debug("Exported Data: " + str(self.redirection_check_window.payload_data))
                _workbook = xlsxwriter.Workbook(save_file)
                _worksheet = _workbook.add_worksheet()

                for x, row in enumerate(self.redirection_check_window.payload_data):
                    for y, column in enumerate(row):
                        _worksheet.write(x, y, column)

                _workbook.close()
                messagebox.showinfo("Success!!!","Exported Successfully", parent=self.single_redirect__modal_ui)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def toggleInputField(self, val):
        try:
            self.excelbtn["state"] = val
            self.retrvdatabtn["state"] = val
            if val == "disabled":
                updatedval = "normal"
            elif val == "normal":
                updatedval = "disabled"
            self.export_btn["state"] = updatedval

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initialize_variable()
            self.toggleInputField("normal")
            self.data_tree.delete(*self.data_tree.get_children())
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# END of DPE Redirection

# Start of BULK Deletion


class BulkDeletionOfDPENode:
    def __init__(self, master):
        self.bulk_deletion_node_ui = Toplevel(master)
        self.master = master
        self.bulk_deletion_node_ui.state('zoomed')
        master.withdraw()
        self.bulk_deletion_node_ui.title(
            APPLICATION_NAME + " - " + "Bulk Deletion of DPE Node"
        )
        self.bulk_deletion_node_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.bulk_deletion_node_ui.brandpic = PhotoImage(
            file=BRAND_PIC_FILE)
        self.bulk_deletion_node_ui.iconphoto(False, self.brandpic)
        # self.stylebulk_deletion_node_ui = ttk.Style()
        self.bulk_deletion_node_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.bulk_deletion_node_ui.configdata = configdata
        self.bulk_deletion_node_ui.excelfile = ""
        self.bulk_deletion_node_ui.payload_data = []
        self.redirect_dpe_prop_inst = None
        self.bulk_deletion_node_ui.initial_redirect_validated = False

        # self.bulk_deletion_node_uimaindesign()selected_excelfile
        self.create_menu_bar()
        self.main_design()

    def create_menu_bar(self):
        try:
            file_url = "https://docs.google.com/spreadsheets/d/17oqbHMBZ92CtiNPRKcZlYifHXGje9SwpVQjmzOWQCLs/export?format=xlsx&gid=1193038397"
            self.main_menu = Menu(self.bulk_deletion_node_ui)
            self.downloadmenu = Menu(self.main_menu, tearoff=0)
            self.downloadmenu.add_command(
                label="Delete Payloads", command=lambda *args: GenericFunctions.download_google_sheet(file_url)
            )
            self.main_menu.add_cascade(
                label="Sample File", menu=self.downloadmenu)
            self.bulk_deletion_node_ui.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state('zoomed')
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            # self.bulk_deletion_node_ui.
            self.bulk_deletion_node_ui.destroy()
            # sleep(0.5)
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
            self.var_selected_source.set("Source Data from Excel")
            self.varipdata.set("")
            self.varpassent.set(self.decrypted_passwd)
            self.varexcelfile.set("Browse & Select Excel File")
            self.varthreadcount.set(10)
            self.var_validate_payload.set(1)
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

    def main_design(self):
        try:
            # Declare String Variable
            self.define_style()

            # String Variable
            self.var_selected_source = StringVar()
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varexcelfile = StringVar()
            self.varthreadcount = StringVar()
            self.var_validate_payload = IntVar()

            # Initiate String Variable
            self.initiate_var()

            # Validation
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))
            self.varthreadcount.trace(
                "w", lambda *args: self.checkthreadcount(self.varthreadcount))

            # Frame Creation
            self.main_frame = Frame(self.bulk_deletion_node_ui)
            self.main_frame.pack(fill="x")

            self.main_btn_frame_sep = ttk.Separator(
                self.bulk_deletion_node_ui)
            self.main_btn_frame_sep.pack(fill="x", padx=5, pady=10)

            self.main_btn_frame = Frame(self.bulk_deletion_node_ui)
            self.main_btn_frame.pack(fill="x")

            self.btn_frame_details_sep = ttk.Separator(
                self.bulk_deletion_node_ui)
            self.btn_frame_details_sep.pack(fill="x", padx=5, pady=10)

            self.main_details_frame = Frame(self.bulk_deletion_node_ui)
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
                self.iplabelframe, textvariable = self.varenvdata, values = self.envdata, state="readonly")
            self.envent.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.iplabelframe.grid_columnconfigure(0, weight=1)
            self.ipenter = ttk.Entry(
                self.iplabelframe, textvariable=self.varipdata)
            self.iplabelframe.grid(
                row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.main_frame.grid_columnconfigure(0, weight=1)

            # Thread count Frame
            self.thread_count_labelframe = LabelFrame(
                self.main_frame, text="Enter number of Thread (Max. 30)", padx=10, pady=10)
            self.thread_count_ent = ttk.Entry(
                self.thread_count_labelframe, textvariable=self.varthreadcount)  # command=ipchange
            self.thread_count_ent.grid(
                row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.thread_count_labelframe.grid_columnconfigure(0, weight=1)
            self.thread_count_labelframe.grid(
                row=0, column=4, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.main_frame.grid_columnconfigure(4, weight=1)

            # Select label Frame:
            self.selectionlabelframe = LabelFrame(
                self.main_frame, text="Select the source & Enter Details", padx=5, pady=5)
            self.selectionlabelframe.grid(
                row=1, column=0, columnspan=5, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.source_dropdown_data = [
                "", "Source Data from Excel"]  # , "Use Query Builder"
            self.source_dropdown_ent = ttk.OptionMenu(
                self.selectionlabelframe, self.var_selected_source, *self.source_dropdown_data)  # , command=self.changecheckbox
            self.source_dropdown_ent.grid(row=0, column=0, padx=5,
                                          pady=5, sticky="nsew")

            # Query Window or Excel Window
            self.select_file_btn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.select_file_btn.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.selected_file_label = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..", textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),
                                                 )
            self.selected_file_label.grid(
                row=0, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")
            self.validate_payload_ent = ttk.Checkbutton(
                self.selectionlabelframe, variable=self.var_validate_payload, onvalue=1, offvalue=0, text="Validate Payload(s)")
            self.validate_payload_ent.grid(
                row=0, column=4, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.selectionlabelframe.grid_columnconfigure(2, weight=1)

            # Button
            self.retrv_and_place_btn = ttk.Button(
                self.main_btn_frame, text="Delete Node", style="mainBtn.TButton", command=self.validate_and_delete_node)  # , command=self.retrvdata
            self.retrv_and_place_btn.pack(
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

            self.export_btn = ttk.Button(
                self.small_btn_frame, text="Export",state="disabled", style="smallBtn.TButton", command=self.exportData)  # , command=self.exportData
            self.export_btn.pack(side="left", padx=5, pady=0, anchor="w")

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
                self.data_tree_frame, style="treeStyle.Treeview", show="headings", columns=("1", "2"), selectmode="extended", height=20)

            self.data_tree_scroll_y = ttk.Scrollbar(
                self.data_tree_frame, orient="vertical", command=self.data_tree.yview)
            self.data_tree.config(yscrollcommand=self.data_tree_scroll_y.set)
            self.data_tree_scroll_y.pack(side="right", fill="y")

            self.data_tree_scroll_x = ttk.Scrollbar(
                self.data_tree_frame, orient="horizontal", command=self.data_tree.xview)
            self.data_tree.config(xscrollcommand=self.data_tree_scroll_x.set)
            self.data_tree_scroll_x.pack(side="bottom", fill="x")

            self.data_tree.pack(fill="both", expand="yes")
            self.data_tree.bind("<<Copy>>", self.getDataandCopy)
            self.data_tree.bind('<Control-a>', lambda *args: self.data_tree.selection_set(self.data_tree.get_children()))
            self.data_tree.bind('<Control-z>', lambda *args: self.data_tree.selection_remove(self.data_tree.selection()))

            # self.data_tree.bind('<Double-Button-1>', self.edit_data_popup)

            self.data_tree_frame.pack(
                fill="both", padx=5, pady=10)

            self.bulk_deletion_node_ui.update()

            table_width = self.data_tree.winfo_width()
            _width = int(table_width * 0.8)
            status_width = int(table_width * 0.2)

            self.data_tree.column("1", width=_width, stretch="yes")
            self.data_tree.column("2", width=status_width,
                                  stretch="yes", anchor="c")

            self.data_tree.heading("1", text="Payload")
            self.data_tree.heading("2", text="Status")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    ### Function / Callback
    def getDataandCopy(self, event):
        try:
            self.master.clipboard_clear()  # clear clipboard contents
            for i in self.data_tree.selection():
                logger.debug("Item No: " + str(i))
                item = self.data_tree.item(i)
                values = item["values"]
                self.master.clipboard_append("\t".join(values))
                # append new value to clipbaord
                self.master.clipboard_append("\n")
                logger.debug("Copied to Clipboard: "+str(values))
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

    def checkthreadcount(self, varthreadcount):
        try:
            dt = varthreadcount.get()
            if dt.strip() != "":
                if not(dt[-1].isnumeric()) or len(dt) > 2:
                    varthreadcount.set(dt[:-1])
                if int(dt) > 30:
                    varthreadcount.set("")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def insert_into_table(self, pos, table_values):
        try:
            self.data_tree.insert("", "end", iid=pos,
                                  text=str(pos), values=table_values)
            self.data_tree.yview_moveto(1)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openexcelfile(self):
        try:
            logger.debug("--Single Redirect--")
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.bulk_deletion_node_ui.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.bulk_deletion_node_ui.excelfile:
                logger.debug("Selected Excel File: " +
                             self.bulk_deletion_node_ui.excelfile)
                self.varexcelfile.set(self.bulk_deletion_node_ui.excelfile)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_inputs(self, uname, passwd, environment, selected_ip, excel_file):
        try:
            output_status = False
            is_not_empty_uname = bool(uname)
            logger.debug("Username Not Empty: "+str(is_not_empty_uname))

            is_not_empty_passwd = bool(passwd)
            logger.debug("Password Not Empty: "+str(is_not_empty_passwd))

            is_not_empty_ip = bool(selected_ip)
            logger.debug("IP Not Empty: "+str(is_not_empty_ip))

            is_valid_file = True if excel_file != "" and excel_file is not None else False
            logger.debug("Valid File: "+str(is_valid_file))

            allowed_file_types = [".xlsx", ".xls", ".xlsm"]
            is_valid_excel_file = GenericFunctions.is_valid_file_types(
                excel_file, allowed_file_types) if is_valid_file else False
            logger.debug("Valid Excel File: "+str(is_valid_excel_file))

            is_valid_ip = GenericFunctions.validateIP(
                selected_ip, environment) if is_not_empty_ip else False
            logger.debug("Valid IP: "+str(is_valid_ip))

            if is_not_empty_ip and is_not_empty_uname and is_not_empty_passwd and is_valid_file and is_valid_excel_file and is_valid_ip:
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

                if not(is_valid_excel_file):
                    error_list.append(
                        "\nInvalid Selected File. Only accepts below\n"+",".join(allowed_file_types))

                if not(is_valid_ip):
                    error_list.append(
                        "\nInvalid IP, Please select/enter correct IP")

                if bool(error_list):
                    messagebox.showerror("Below Error has occurred", "Please see the below list"+".".join(
                        error_list), parent=self.bulk_deletion_node_ui)
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

    def delete_payloads(self, delete_function, payloads):
        try:
            for _payload in payloads:
                _output = delete_function(_payload)
                # _output = 200
                _payload_end = _payload.split("/")[-1]
                _table_iid = str(GenericFunctions.random_number_gen(100000)) +"_"+ _payload_end
                self.bulk_deletion_node_ui.payload_data.remove(_payload)
                sleep(1)
                if _output == 200:
                    _table_insert_values = (_payload, "Completed",)
                else:
                    _table_insert_values = (_payload, "Failed",)
                self.insert_into_table(_table_iid, _table_insert_values)
            if not(bool(self.bulk_deletion_node_ui.payload_data)):
                self.bulk_deletion_node_ui.progress_bar.destroy()
                self.resetbtn["state"] = "normal"

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_and_delete_node(self):
        try:
            disable_btn = True
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.resetbtn["state"] = "disabled"
            self.bulk_deletion_node_ui.update()

            uname = self.varuserent.get().strip()
            passwd = self.varpassent.get().strip()

            environment = self.varenvdata.get().lower()
            selected_ip = (self.varipdata.get().lower().strip()
                           if environment == "ip" else configdata[environment])
            excel_file = self.bulk_deletion_node_ui.excelfile
            thread_count = GenericFunctions.get_int_value(
                self.varthreadcount.get(), 10)
            run_the_operation = True
            if environment.lower() == "production":
                run_the_operation = messagebox.askyesnocancel(
                    "Please confirm", "Do you want to Run\nthe Operation in Production?", parent=self.bulk_deletion_node_ui)

            if run_the_operation:
                is_validated = self.validate_inputs(
                    uname, passwd, environment, selected_ip, excel_file)

                if is_validated:
                    self.toggleInputField("disabled")
                    self.bulk_deletion_node_ui.update()

                    self.delete_node_instances = BulkNodeDeletion(
                        selected_ip, uname, passwd)
                    _valid_uname_pass = self.delete_node_instances.password_validator()

                    if _valid_uname_pass == 200:
                        _validate_payloads = self.var_validate_payload.get()
                        self.bulk_deletion_node_ui.payload_data = self.delete_node_instances.excel_to_list(
                            excel_file, _validate_payloads)
                        all_payloads = self.bulk_deletion_node_ui.payload_data.copy()
                        count_of_payloads = len(all_payloads)
                        self.total_hits_label.config(
                            text="Total: "+str(count_of_payloads), fg="black")

                        logger.debug("Data To Be Deleted: " +
                                     str(count_of_payloads))
                        logger.debug(all_payloads)

                        if bool(all_payloads):
                            self.bulk_deletion_node_ui.progress_bar = ttk.Progressbar(
                                self.small_btn_frame, orient=HORIZONTAL, mode="indeterminate", style="green.Horizontal.TProgressbar")
                            self.bulk_deletion_node_ui.progress_bar.pack(
                                fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")

                            url_slices = []
                            for cnt in range(thread_count - 1):
                                url_slices.append(all_payloads[int(
                                    len(all_payloads)/thread_count)*cnt:int(len(all_payloads)/thread_count)*(cnt+1)])
                            url_slices.append(all_payloads[int(
                                len(all_payloads)/thread_count)*(thread_count - 1):len(all_payloads)])
                            self.bulk_deletion_node_ui.progress_bar.start()
                            for _cur_thread in range(thread_count):
                                _running_thread = threading.Thread(target=self.delete_payloads, args=(
                                    self.delete_node_instances.delete_dpe_node, url_slices[_cur_thread]))
                                _running_thread.daemon = True
                                _running_thread.start()
                        else:
                            messagebox.showwarning("Warning!!!","There are not valid payloads to delete", 
                                    parent=self.bulk_deletion_node_ui)
                            self.resetbtn["state"] = "normal"

                    elif _valid_uname_pass == 401:
                        msg = "Invalid UserName and Password"
                        self.retrieve_data_count_label.config(
                            text="", fg="black")
                        self.total_hits_label.config(text=msg, fg="red")
                        self.userent["state"] = "normal"
                        self.passent["state"] = "normal"
                        self.retrv_and_place_btn["state"] = "normal"
                        self.resetbtn["state"] = "normal"
                        disable_btn = False
                    elif _valid_uname_pass == 999:
                        self.retrieve_data_count_label.config(
                            text="Exception Occurred: "+str(_valid_uname_pass), fg="red")
                        self.resetbtn["state"] = "normal"
                    else:
                        self.retrieve_data_count_label.config(
                            text="Connection Status: "+str(_valid_uname_pass), fg="black")
                        self.resetbtn["state"] = "normal"

                    if disable_btn:
                        self.userent["state"] = "disabled"
                        self.passent["state"] = "disabled"
                        self.retrv_and_place_btn["state"] = "disabled"
                        # self.export_btn["state"] = "disabled"
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            if self.bulk_deletion_node_ui.progress_bar.winfo_exists():
                self.bulk_deletion_node_ui.progress_bar.destroy()
                self.resetbtn["state"] = "normal"

    def toggleInputField(self, val):
        try:
            self.userent["state"] = val
            self.passent["state"] = val
            self.ipenter["state"] = val
            self.select_file_btn["state"] = val
            self.retrv_and_place_btn["state"] = val
            # self.validate_data_ent["state"] = val
            self.envent["state"] = val
            self.source_dropdown_ent["state"] = val
            self.validate_payload_ent["state"] = val
            if val == "disabled":
                updatedval = "normal"
            elif val == "normal":
                updatedval = "disabled"
            self.export_btn["state"] = updatedval

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initiate_var()
            self.toggleInputField("normal")
            self.bulk_deletion_node_ui.excelfile = ""
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.data_tree.delete(*self.data_tree.get_children())
            # self.data_tree["columns"] = ()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def exportData(self):
        try:
            if bool(self.data_tree.get_children()):
                types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                        ("All Files", "*.*"))
                save_file = filedialog.asksaveasfilename(
                    initialdir=BASE_SCRIPT_PATH, initialfile="data_output.xlsx", title="Save Data", filetypes=types, defaultextension=types
                )
                logger.info("File Name to Export the Data: "+str(save_file))
                if save_file:
                    self.exportDataList(save_file)
            else:
                messagebox.showwarning("Warning!!", "No Data to Export!!!", parent=self.bulk_deletion_node_ui)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def exportDataList(self, filename):
        try:
            table_value = self.data_tree.get_children()
            logger.info("Table IID " + str(table_value))
            table_columns = ["Paylodas", "Status", ]
            logger.info("Columns Name: " + str(table_columns))
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()
            worksheet.write_row(0,0,list(table_columns))
            for i, _each_row_iid in enumerate(table_value):
                _row_values = list(self.data_tree.item(_each_row_iid, "values"))
                logger.debug("Row Values: " + str(_row_values))
                worksheet.write_row((i+1), 0, _row_values)
            
            workbook.close()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# End of Bulk Deletion

# Start of Bulk Workflow Manager


class BulkWorkflowManager:
    def __init__(self, master):
        self.bulk_workflow_manager_ui = Toplevel(master)
        self.master = master
        self.bulk_workflow_manager_ui.state('zoomed')
        master.withdraw()
        self.bulk_workflow_manager_ui.title(
            APPLICATION_NAME + " - " + "Bulk Workflow Manager"
        )
        self.bulk_workflow_manager_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.bulk_workflow_manager_ui.brandpic = PhotoImage(
            file=BRAND_PIC_FILE)
        self.bulk_workflow_manager_ui.iconphoto(False, self.brandpic)
        # self.stylebulk_workflow_manager_ui = ttk.Style()
        self.bulk_workflow_manager_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.bulk_workflow_manager_ui.configdata = configdata
        self.bulk_workflow_manager_ui.excelfile = ""
        self.bulk_workflow_manager_ui.payload_data = []
        self.redirect_dpe_prop_inst = None
        self.bulk_workflow_manager_ui.initial_redirect_validated = False
        self.workflow_model_data = [
            x.strip() for x in operationdata["workflow models"].split(",") if x.strip() != ""]

        # self.bulk_workflow_manager_uimaindesign()selected_excelfile
        self.create_menu_bar()
        self.main_design()
    
    def create_menu_bar(self):
        try:
            file_url = "https://docs.google.com/spreadsheets/d/17oqbHMBZ92CtiNPRKcZlYifHXGje9SwpVQjmzOWQCLs/export?format=xlsx&gid=861142537"
            self.main_menu = Menu(self.bulk_workflow_manager_ui)
            self.downloadmenu = Menu(self.main_menu, tearoff=0)
            self.downloadmenu.add_command(
                label="Payloads", command=lambda *args: GenericFunctions.download_google_sheet(file_url)
            )
            self.main_menu.add_cascade(
                label="Sample File", menu=self.downloadmenu)
            self.add_wf_menu = Menu(self.main_menu, tearoff=0)
            self.add_wf_menu.add_command(
                label="Add/Remove", command=self.select_add_workflow)
            self.main_menu.add_cascade(
                label="Edit Workflow List", menu=self.add_wf_menu)
            self.bulk_workflow_manager_ui.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state("zoomed")
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.bulk_workflow_manager_ui.destroy()
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
            self.var_selected_source.set("Source Data from Excel")
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

    def main_design(self):
        try:
            # Declare String Variable
            self.define_style()

            # String Variable
            self.var_selected_source = StringVar()
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varexcelfile = StringVar()
            self.var_selected_wf_model = StringVar()

            # Initiate String Variable
            self.initiate_var()

            # Validation
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))

            # Frame Creation
            self.main_frame = Frame(self.bulk_workflow_manager_ui)
            self.main_frame.pack(fill="x")

            self.main_btn_frame_sep = ttk.Separator(
                self.bulk_workflow_manager_ui)
            self.main_btn_frame_sep.pack(fill="x", padx=5, pady=10)

            self.main_btn_frame = Frame(self.bulk_workflow_manager_ui)
            self.main_btn_frame.pack(fill="x")

            self.btn_frame_details_sep = ttk.Separator(
                self.bulk_workflow_manager_ui)
            self.btn_frame_details_sep.pack(fill="x", padx=5, pady=10)

            self.main_details_frame = Frame(self.bulk_workflow_manager_ui)
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
                self.iplabelframe, textvariable = self.varenvdata, values = self.envdata, state="readonly")
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

            self.source_dropdown_data = [
                "", "Source Data from Excel"]  # , "Use Query Builder"
            self.source_dropdown_ent = ttk.OptionMenu(
                self.selectionlabelframe, self.var_selected_source, *self.source_dropdown_data)  # , command=self.changecheckbox
            self.source_dropdown_ent.grid(row=0, column=0, padx=5,
                                          pady=5, sticky="nsew")

            # Query Window or Excel Window
            self.select_file_btn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.select_file_btn.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.selected_file_label = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..", textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),
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

            self.bulk_workflow_manager_ui.update()

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
            self.bulk_workflow_manager_ui.select_and_add_wf_modal = Toplevel(
                self.bulk_workflow_manager_ui)
            self.bulk_workflow_manager_ui.wm_attributes("-disabled", True)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.focus_set()
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.iconphoto(False, self.brandpic)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.geometry("+300+100")
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.minsize(650, 450)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.maxsize(650, SCREEN_HEIGHT)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.resizable(width=False, height=True)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.title(
                APPLICATION_NAME + " - Workflow List")
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.transient(
                self.bulk_workflow_manager_ui)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.protocol(
                "WM_DELETE_WINDOW", lambda *args: self.close_this_window(self.bulk_workflow_manager_ui.select_and_add_wf_modal))

            def add_wf_model():
                try:
                    selected_wf = self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.selection()
                    logger.debug("Selected Left WF: "+str(selected_wf))
                    if bool(selected_wf):
                        for _each_select in selected_wf:
                            _item = self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.item(_each_select)
                            _values = _item["values"]
                            logger.debug("Selected Left table Values: "+str(_values))
                            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.insert("","end",iid=self.last_item_iid_of_sel_wf + 1, values= _values)
                            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.delete(_each_select)
                            self.last_item_iid_of_sel_wf += 1
                    else:
                        messagebox.showwarning("Warning!!", "Please Select a Workflow", parent=self.bulk_workflow_manager_ui.select_and_add_wf_modal)
                except:
                    logger.error("Below Exception occurred\n", exc_info=True)
            
            def remove_wf_model():
                try:
                    selected_wf = self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.selection()
                    logger.debug("Selected Right WF: "+str(selected_wf))
                    if bool(selected_wf):
                        for _each_select in selected_wf:
                            _item = self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.item(_each_select)
                            _values = _item["values"]
                            logger.debug("Selected Right Tables Values: "+str(_values))
                            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.insert("","end",iid=self.last_item_iid_of_all_wf + 1, values= _values)
                            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.delete(_each_select)
                            self.last_item_iid_of_all_wf += 1
                    else:
                        messagebox.showwarning("Warning!!", "Please Select a Workflow", parent=self.bulk_workflow_manager_ui.select_and_add_wf_modal)
                except:
                    logger.error("Below Exception occurred\n", exc_info=True)

            def save_wf_model():
                try:
                    global operationdata
                    self.workflow_model_data = []
                    all_wf = self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.get_children()
                    for _each_child in all_wf:
                        _val = self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.item(_each_child, "values")
                        self.workflow_model_data.append(_val[0])

                    self.workflow_model_data.sort()
                    logger.debug("ALL Selected WFs: "+str(self.workflow_model_data))
                    operationdata["workflow models"] = ",".join(self.workflow_model_data)
                    status = edcfg.updateConfig(operationdata, OPERATION_CODE_FILE)
                    if status:
                        self.workflow_select_ent.config(values=self.workflow_model_data)
                        messagebox.showinfo("Success!!","Data has been saved succefully.")
                        self.close_this_window(self.bulk_workflow_manager_ui.select_and_add_wf_modal)
                    else:
                        messagebox.showerror("Error!!","Failed to Save Data. Please check logs")

                except:
                    logger.error("Below Exception occurred\n", exc_info=True)
            
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.label_frame = Frame(self.bulk_workflow_manager_ui.select_and_add_wf_modal)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.label_frame.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.tree_frame = Frame(self.bulk_workflow_manager_ui.select_and_add_wf_modal)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.tree_frame.pack(fill="both", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.btn_frame = Frame(self.bulk_workflow_manager_ui.select_and_add_wf_modal)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.btn_frame.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree_frame = Frame(self.bulk_workflow_manager_ui.select_and_add_wf_modal.tree_frame)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree_frame.pack(side="left", fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.middle_btn_frame = Frame(self.bulk_workflow_manager_ui.select_and_add_wf_modal.tree_frame)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.middle_btn_frame.pack(side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree_frame = Frame(self.bulk_workflow_manager_ui.select_and_add_wf_modal.tree_frame)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree_frame.pack(side="left", fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.title_label = Label(self.bulk_workflow_manager_ui.select_and_add_wf_modal.label_frame, text="Select and Add Workflow", anchor="center", font=("Georgia", 12, "bold"))
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.title_label.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.title_label = Label(self.bulk_workflow_manager_ui.select_and_add_wf_modal.label_frame, text="Workflow(s)\t\t\t\tSelected Workflow", font=("Georgia", 10, "bold"))
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.title_label.pack(fill="x", padx=5, ipadx=5)

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree = ttk.Treeview(self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree_frame, show="headings", column=("Workflow"), height=12,)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree_scroll_y = ttk.Scrollbar(self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree_frame, command=self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.yview)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.config(yscrollcommand=self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree_scroll_y.set)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree_scroll_y.pack(side="right", fill="y")
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.pack(fill="both", expand="yes")
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.column("Workflow", minwidth=150, stretch=YES)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.heading("Workflow", text="Workflow", anchor=CENTER)

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.middle_add_btn = ttk.Button(self.bulk_workflow_manager_ui.select_and_add_wf_modal.middle_btn_frame, text=">>", style="smallBtn.TButton", command=add_wf_model)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.middle_add_btn.pack(padx=5,pady=5, ipadx=1, ipady=1, anchor="center")
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.middle_remove_btn = ttk.Button(self.bulk_workflow_manager_ui.select_and_add_wf_modal.middle_btn_frame, text="<<", style="smallBtn.TButton", command=remove_wf_model)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.middle_remove_btn.pack(padx=5,pady=5, ipadx=1, ipady=1, anchor="center")

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree = ttk.Treeview(self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree_frame, show="headings", column=("Selected_Workflow"), height=12,)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree_scroll_y = ttk.Scrollbar(self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree_frame, command=self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.yview)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.config(yscrollcommand=self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree_scroll_y.set)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree_scroll_y.pack(side="right", fill="y")
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.pack(fill="both", expand="yes")
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.column("Selected_Workflow", minwidth=150, stretch=YES)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.heading("Selected_Workflow", text="Selected Workflow", anchor=CENTER)

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.save_btn = ttk.Button(self.bulk_workflow_manager_ui.select_and_add_wf_modal.btn_frame, text="Save", command=save_wf_model)
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.save_btn.pack(side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.bulk_workflow_manager_ui.select_and_add_wf_modal.exit_btn = ttk.Button(self.bulk_workflow_manager_ui.select_and_add_wf_modal.btn_frame, text="Exit", command=lambda *args: self.close_this_window(self.bulk_workflow_manager_ui.select_and_add_wf_modal))
            self.bulk_workflow_manager_ui.select_and_add_wf_modal.exit_btn.pack(side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            for _id, _each_selected_wf in enumerate(self.workflow_model_data):
                self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.insert("","end", iid=_id+1, values=(_each_selected_wf,))

            all_workflows = edcfg.readConfig(WF_MODEL_FILE)
            for _id, _each_all_wf in enumerate(all_workflows):
                if _each_all_wf not in self.workflow_model_data:
                    self.bulk_workflow_manager_ui.select_and_add_wf_modal.left_tree.insert("","end", iid=_id+1, values=(_each_all_wf,))

            self.last_item_iid_of_sel_wf = len(self.bulk_workflow_manager_ui.select_and_add_wf_modal.right_tree.get_children())
            self.last_item_iid_of_all_wf = len(all_workflows)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def close_this_window(self, wind):
        try:
            self.bulk_workflow_manager_ui.focus_set()
            self.bulk_workflow_manager_ui.wm_attributes("-disabled", False)
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
            self.bulk_workflow_manager_ui.update()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openexcelfile(self):
        try:
            logger.debug("--Single Redirect--")
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.bulk_workflow_manager_ui.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.bulk_workflow_manager_ui.excelfile:
                logger.debug("Selected Excel File: " +
                             self.bulk_workflow_manager_ui.excelfile)
                self.varexcelfile.set(self.bulk_workflow_manager_ui.excelfile)
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
                        error_list), parent=self.bulk_workflow_manager_ui)
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
            self.bulk_workflow_manager_ui.update()

            uname = self.varuserent.get().strip()
            passwd = self.varpassent.get().strip()

            environment = self.varenvdata.get().lower()
            selected_ip = (self.varipdata.get().lower().strip()
                           if environment == "ip" else configdata[environment])
            excel_file = self.bulk_workflow_manager_ui.excelfile
            selected_wf = self.var_selected_wf_model.get()
            run_the_operation = True
            if environment.lower() == "production":
                run_the_operation = messagebox.askyesnocancel(
                    "Please confirm", "Do you want to Run\nthe Operation in Production?", parent=self.bulk_workflow_manager_ui)

            if run_the_operation:
                is_validated = self.validate_inputs(
                    uname, passwd, environment, selected_ip, selected_wf, excel_file)

                if is_validated:
                    self.toggleInputField("disabled")
                    self.bulk_workflow_manager_ui.update()

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

                        self.bulk_workflow_manager_ui.progress_bar = ttk.Progressbar(
                            self.small_btn_frame, orient=HORIZONTAL, maximum=count_of_payloads, mode="determinate", style="green.Horizontal.TProgressbar")
                        self.bulk_workflow_manager_ui.progress_bar.pack(
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

                            self.bulk_workflow_manager_ui.update()

                            self.bulk_workflow_manager_ui.progress_bar["value"] = i+1
                            self.bulk_workflow_manager_ui.update()
                            sleep(configdata["sleeptime"])

                        self.bulk_workflow_manager_ui.progress_bar.destroy()

                        if disable_btn:
                            self.userent["state"] = "disabled"
                            self.passent["state"] = "disabled"

                        if disable_model:
                            self.workflow_select_ent["state"] = "disabled"

                        if disable_btn and disable_model:
                            self.run_wf_model_btn["state"] = "disabled"

                        self.bulk_workflow_manager_ui.update()
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
            self.bulk_workflow_manager_ui.excelfile = ""
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.data_tree.delete(*self.data_tree.get_children())
            # self.data_tree["columns"] = ()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# End of Bulk Workflow Manager

# Start of Bulk Deactivate/Activate User Manager

class BulkUserManager:
    def __init__(self, master):
        self.bulk_user_manager_ui = Toplevel(master)
        self.master = master
        self.bulk_user_manager_ui.state('zoomed')
        master.withdraw()
        self.bulk_user_manager_ui.title(
            APPLICATION_NAME + " - " + "Bulk User Manager"
        )
        self.bulk_user_manager_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.bulk_user_manager_ui.iconphoto(False, self.brandpic)
        self.bulk_user_manager_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.bulk_user_manager_ui.configdata = configdata
        self.bulk_user_manager_ui.excelfile = ""
        self.bulk_user_manager_ops_instances = None
        
        self.create_menu_bar()
        self.main_design()
    
    def create_menu_bar(self):
        try:
            file_url = "https://docs.google.com/spreadsheets/d/17oqbHMBZ92CtiNPRKcZlYifHXGje9SwpVQjmzOWQCLs/export?format=xlsx&gid=2092399760"
            self.main_menu = Menu(self.bulk_user_manager_ui)
            self.downloadmenu = Menu(self.main_menu, tearoff=0)
            self.downloadmenu.add_command(
                label="Payloads", command=lambda *args: GenericFunctions.download_google_sheet(file_url)
            )
            self.main_menu.add_cascade(
                label="Sample File", menu=self.downloadmenu)
            self.bulk_user_manager_ui.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state("zoomed")
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.bulk_user_manager_ui.destroy()
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
            self.var_selected_source.set("Source Data from Excel")
            self.varipdata.set("")
            self.varpassent.set(self.decrypted_passwd)
            self.varexcelfile.set("Browse & Select Excel File")
            self.varuseroperation.set("--SELECT--")
            self.vartobedeletedusers.set("")
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

    def main_design(self):
        try:
            # Declare String Variable
            self.define_style()

            # String Variable
            self.var_selected_source = StringVar()
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varexcelfile = StringVar()
            self.varuseroperation = StringVar()
            self.vartobedeletedusers = StringVar()

            # Initiate String Variable
            self.initiate_var()

            # Validation
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))
            self.var_selected_source.trace(
                "w", lambda *args: self.changeoptionbox(self.var_selected_source.get()))

            # Frame Creation
            self.main_frame = Frame(self.bulk_user_manager_ui)
            self.main_frame.pack(fill="x")

            self.main_btn_frame_sep = ttk.Separator(
                self.bulk_user_manager_ui)
            self.main_btn_frame_sep.pack(fill="x", padx=5, pady=10)

            self.main_btn_frame = Frame(self.bulk_user_manager_ui)
            self.main_btn_frame.pack(fill="x")

            self.btn_frame_details_sep = ttk.Separator(
                self.bulk_user_manager_ui)
            self.btn_frame_details_sep.pack(fill="x", padx=5, pady=10)

            self.main_details_frame = Frame(self.bulk_user_manager_ui)
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
                self.iplabelframe, textvariable = self.varenvdata, values = self.envdata, state="readonly")
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

            self.source_dropdown_data = [
                "", "Source Data from Excel", "Enter Username(Comma Seperated)"]  # , "Use Query Builder"
            self.source_dropdown_ent = ttk.OptionMenu(
                self.selectionlabelframe, self.var_selected_source, *self.source_dropdown_data)  # , command=self.changecheckbox
            self.source_dropdown_ent.grid(row=0, column=0, padx=5,
                                          pady=5, sticky="nsew")

            # Query Window or Excel Window
            self.select_file_btn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.select_file_btn.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.selected_file_label = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..", textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),
                                                 )
            self.selected_file_label.grid(
                row=0, column=2, padx=5, pady=5, sticky="nsew")
            self.to_be_deleted_users_ent = Entry(self.selectionlabelframe, textvariable=self.vartobedeletedusers)

            self.selectionlabelframe.grid_columnconfigure(2, weight=1)

            # # User Operation
            self.user_operation_frame = LabelFrame(
                self.main_frame, text="Select Operation")
            self.user_operation_frame.grid(
                row=1, column=3, padx=5, pady=(13, 7), sticky="nsew")

            self.user_operation_data = ["--SELECT--","Disable","Enable"]

            self.user_operation_select_ent = ttk.Combobox(
                self.user_operation_frame, textvariable=self.varuseroperation, state="readonly", values=self.user_operation_data)
            self.user_operation_select_ent.grid(
                row=0, column=0, padx=5, pady=10, ipadx=5, ipady=5, sticky="nsew")
            self.user_operation_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_columnconfigure(3, weight=1)

            # Button
            self.user_start_operation_btn = ttk.Button(
                self.main_btn_frame, text="Start Operation", style="mainBtn.TButton", command=self.validate_and_run_user_operation)  # , command=self.retrvdata
            self.user_start_operation_btn.pack(
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

            self.export_btn = ttk.Button(
                self.small_btn_frame, text="Export",state="disabled", style="smallBtn.TButton", command=self.export_status_report)  # , command=self.exportData
            self.export_btn.pack(side="left", padx=5, pady=0, anchor="w")

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
                self.data_tree_frame, style="treeStyle.Treeview", show="headings", columns=("1", "2"), selectmode="extended", height=20)

            self.data_tree_scroll_y = ttk.Scrollbar(
                self.data_tree_frame, orient="vertical", command=self.data_tree.yview)
            self.data_tree.config(yscrollcommand=self.data_tree_scroll_y.set)
            self.data_tree_scroll_y.pack(side="right", fill="y")

            self.data_tree_scroll_x = ttk.Scrollbar(
                self.data_tree_frame, orient="horizontal", command=self.data_tree.xview)
            self.data_tree.config(xscrollcommand=self.data_tree_scroll_x.set)
            self.data_tree_scroll_x.pack(side="bottom", fill="x")

            self.data_tree.pack(fill="both", expand="yes")

            self.data_tree.bind("<<Copy>>", self.getDataandCopy)
            # self.data_tree.bind('<Double-Button-1>', self.edit_data_popup)

            self.data_tree_frame.pack(
                fill="both", padx=5, pady=10)

            self.bulk_user_manager_ui.update()

            table_width = self.data_tree.winfo_width()
            _width = int(table_width * 0.8)
            status_width = int(table_width * 0.2)

            self.data_tree.column("1", width=_width, stretch="yes")
            self.data_tree.column("2", width=status_width,
                                  stretch="yes", anchor="c")

            self.data_tree.heading("1", text="User Email ID")
            self.data_tree.heading("2", text="Status")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    ### Function / Callback
    def close_this_window(self, wind):
        try:
            self.bulk_user_manager_ui.focus_set()
            self.bulk_user_manager_ui.wm_attributes("-disabled", False)
            wind.destroy()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
    
    def getDataandCopy(self, event):
        try:
            self.master.clipboard_clear()  # clear clipboard contents
            for i in self.data_tree.selection():
                logger.debug("Item No: " + str(i))
                item = self.data_tree.item(i)
                values = item["values"]
                self.master.clipboard_append("\t".join(values))
                # append new value to clipbaord
                self.master.clipboard_append("\n")
                logger.debug("Copied to Clipboard: "+str(values))
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

    def changeoptionbox(self, val):
        try:
            self.bulk_user_manager_ui.excelfile = ""
            self.bulk_user_manager_ui.user_data = ""
            self.vartobedeletedusers.set("")
            if val == "Enter Username(Comma Seperated)":
                if self.selected_file_label.winfo_ismapped():
                    self.selected_file_label.grid_forget()
                if self.select_file_btn.winfo_ismapped():
                    self.select_file_btn.grid_forget()
                self.to_be_deleted_users_ent.grid(
                        row=0, column=1, columnspan=2, padx=5, pady=5, sticky="nsew")
                self.selectionlabelframe.grid_columnconfigure(1, weight=1)
            elif val == "Source Data from Excel":
                if self.to_be_deleted_users_ent.winfo_ismapped():
                    self.to_be_deleted_users_ent.grid_forget()
                self.select_file_btn.grid(
                        row=0, column=1, padx=5, pady=5, sticky="nsew")
                self.selected_file_label.grid(
                        row=0, column=2, padx=5, pady=5, sticky="nsew")
                self.selectionlabelframe.grid_columnconfigure(1, weight=0)
                self.selectionlabelframe.grid_columnconfigure(2, weight=1)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def insert_into_table(self, pos, table_values):
        try:
            self.data_tree.insert("", "end", iid=pos,
                                  text=str(pos), values=table_values)
            self.data_tree.yview_moveto(1)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openexcelfile(self):
        try:
            logger.debug("--Single Redirect--")
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.bulk_user_manager_ui.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.bulk_user_manager_ui.excelfile:
                logger.debug("Selected Excel File: " +
                             self.bulk_user_manager_ui.excelfile)
                self.varexcelfile.set(self.bulk_user_manager_ui.excelfile)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_inputs(self, uname, passwd, environment, selected_ip, selected_operation, source_data, source_type):
        try:
            #excel_file
            output_status = False
            is_not_empty_uname = bool(uname)
            logger.debug("Username Not Empty: "+str(is_not_empty_uname))

            is_not_empty_passwd = bool(passwd)
            logger.debug("Password Not Empty: "+str(is_not_empty_passwd))

            is_not_empty_ip = bool(selected_ip)
            logger.debug("IP Not Empty: "+str(is_not_empty_ip))

            is_not_empty_operation = bool(selected_operation)
            logger.debug("WF Not Empty: "+str(is_not_empty_operation))

            is_valid_source_data = bool(source_data)
            logger.debug("Valid File: "+str(is_valid_source_data))

            is_a_file = True if (source_type == "Source Data from Excel" and is_valid_source_data) else False

            allowed_file_types = [".xlsx", ".xls", ".xlsm"]
            is_valid_excel_file = False
            
            if is_a_file:
                is_valid_excel_file = GenericFunctions.is_valid_file_types(source_data, allowed_file_types)
            if not(is_a_file) and is_valid_source_data:
                is_valid_excel_file = True
            logger.debug("Valid Excel File: "+str(is_valid_excel_file))

            is_valid_ip = GenericFunctions.validateIP(
                selected_ip, environment) if is_not_empty_ip else False
            logger.debug("Valid IP: "+str(is_valid_ip))

            is_valid_operaion = True if selected_operation != "--SELECT--" else False
            logger.debug("Valid Workflow: "+str(is_valid_operaion))

            if is_not_empty_ip and is_not_empty_uname and is_not_empty_passwd and is_valid_source_data and is_valid_excel_file and is_valid_ip and is_valid_operaion and is_not_empty_operation:
                output_status = True

            else:
                error_list = []
                if not(is_not_empty_uname):
                    error_list.append("\nUsername Can't be Empty")

                if not(is_not_empty_passwd):
                    error_list.append("\nPassword Can't be Empty")

                if not(is_not_empty_ip):
                    error_list.append("\nIP Can't be Empty")

                if not(is_valid_source_data):
                    error_list.append("\nPlease select a File")

                if not(is_valid_operaion):
                    error_list.append("\nPlease select a Valid Operation")

                if not(is_not_empty_operation):
                    error_list.append("\nOperation can't be empty")

                if not(is_valid_excel_file):
                    error_list.append(
                        "\nInvalid Selected File. Only accepts below\n"+",".join(allowed_file_types))

                if not(is_valid_ip):
                    error_list.append(
                        "\nInvalid IP, Please select/enter correct IP")

                if bool(error_list):
                    messagebox.showerror("Below Error has occurred", "--------Errors---------"+".".join(
                        error_list), parent=self.bulk_user_manager_ui)
                    logger.error("Below Error has occurred" +
                                 ".".join(error_list))

            logger.info("Data Validation Status: " + str(output_status))
            return output_status

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_and_run_user_operation(self):
        try:
            enable_field = True
            enable_input_field = False
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.bulk_user_manager_ui.update()

            uname = self.varuserent.get().strip()
            passwd = self.varpassent.get().strip()

            environment = self.varenvdata.get().lower()
            selected_ip = (self.varipdata.get().lower().strip()
                           if environment == "ip" else configdata[environment])
            source_type = self.var_selected_source.get()
            source_data = self.bulk_user_manager_ui.excelfile if source_type == "Source Data from Excel" else \
                (self.vartobedeletedusers.get() if source_type == "Enter Username(Comma Seperated)" else "")
            selected_operation = self.varuseroperation.get()
            run_the_operation = True
            if environment.lower() == "production":
                run_the_operation = messagebox.askyesnocancel(
                    "Please confirm", "Do you want to Run\nthe Operation in Production?", parent=self.bulk_user_manager_ui)

            if run_the_operation:
                is_validated = self.validate_inputs(
                    uname, passwd, environment, selected_ip, selected_operation, source_data, source_type)

                if is_validated:
                    self.bulk_user_manager_ops_instances = UserAccountsAndCopy(selected_ip,uname,passwd)
                    all_users = []
                    if self.var_selected_source.get() == "Enter Username(Comma Seperated)":
                        all_users = [[x.strip(),] for x in self.vartobedeletedusers.get().split(",") if x.strip() != "" ]
                    elif self.var_selected_source.get() == "Source Data from Excel":
                        all_users = self.bulk_user_manager_ops_instances.read_data(
                            source_data)
                    
                    if bool(all_users):
                        count_of_users = len(all_users)
                        self.total_hits_label.config(
                            text="Total: "+str(count_of_users), fg="black")

                        logger.debug("Total Number of Payloads: " +
                                    str(count_of_users))
                        logger.debug(all_users)

                        status_proc = {
                            "200" : "Completed",
                            "401" : "Wrong Username and Password",
                            "400" : "Bad Request",
                            "403" : "Forbidden",
                            "404" : "Page not found",
                            "405" : "Method Not Allowed",
                            "406" : "Not Acceptable",
                            "500" : "Internal Server Error",
                            "501" : "Not Implemented",
                            "502" : "Bad Gateway",
                            "503" : "Service Unavailable",
                            "901" : "No User Present",
                            "999" : "Exception"
                        }
                        self.bulk_user_manager_ui.progress_bar = ttk.Progressbar(
                            self.small_btn_frame, orient=HORIZONTAL, maximum=count_of_users, mode="determinate", style="green.Horizontal.TProgressbar")
                        self.bulk_user_manager_ui.progress_bar.pack(
                            fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")
                        for user_id, _each_user in enumerate(all_users):
                            _uname_toggle_status = self.bulk_user_manager_ops_instances.toggle_user_status(_each_user[0], selected_operation)
                            st_htnk = status_proc.get(str(_uname_toggle_status).strip(), "Failed")
                            if _uname_toggle_status == 200 or _uname_toggle_status == 901:
                                self.insert_into_table(user_id + 1, (_each_user[0], st_htnk,))
                                self.retrieve_data_count_label.config(text="Current: "+str(user_id + 1), fg="black")
                            elif _uname_toggle_status == 401:
                                self.total_hits_label.config(
                                        text=st_htnk, fg="red")
                                enable_input_field = True
                                enable_field = False
                                break
                            elif _uname_toggle_status >= 500 and _uname_toggle_status <= 510:
                                self.total_hits_label.config(
                                        text=st_htnk, fg="red")
                                enable_field = False
                                break
                            else:
                                self.total_hits_label.config(
                                        text=st_htnk, fg="red")
                                self.insert_into_table(user_id + 1, (_each_user[0], st_htnk,))
                                self.retrieve_data_count_label.config(text="Current: "+str(user_id + 1), fg="black")
                            
                            self.bulk_user_manager_ui.progress_bar["value"] = user_id+1
                            self.bulk_user_manager_ui.update()

                        self.bulk_user_manager_ui.progress_bar.destroy()
                        self.toggleInputField("disabled")

                        if enable_field:
                            self.export_btn["state"] = "normal"
                            
                        if enable_input_field:
                            self.userent["state"] = "normal"
                            self.passent["state"] = "normal"
                            self.user_start_operation_btn["state"] = "normal"
                            self.export_btn["state"] = "disabled"
                    else:
                        self.total_hits_label.config(
                                    text="Empty Users", fg="red")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.total_hits_label.config(
                                    text="Exception Occurred!!", fg="red")
            self.toggleInputField("normal")

    def export_status_report(self):
        try:
            all_table_row_id = self.data_tree.get_children()
            if bool(all_table_row_id):
                ## Select the File
                types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                        ("All Files", "*.*"))
                save_file = filedialog.asksaveasfilename(
                    initialdir=BASE_SCRIPT_PATH, initialfile="data_output.xlsx", title="Save Data", filetypes=types, defaultextension=types
                )
                logger.info("File Name to Export the Data: "+str(save_file))
                if save_file:
                    all_table_data = []
                    # if bool(all_table_row_id):
                    all_table_data.append(["User ID","Status"])
                    for each_row_id in all_table_row_id:
                        all_table_data.append(self.data_tree.item(each_row_id)["values"])

                    logger.debug("Exported Data: " + str(all_table_data))
                    _workbook = xlsxwriter.Workbook(save_file)
                    _worksheet = _workbook.add_worksheet()

                    for x in range(len(all_table_data)):
                        for y in range(len(all_table_data[x])):
                            _worksheet.write(x, y, str(all_table_data[x][y]))

                    _workbook.close()
                    messagebox.showinfo("Success!!!","Exported Successfully", parent=self.bulk_user_manager_ui)
            else:
                messagebox.showwarning("No Data Warning!!!","No Data to Export!!!", parent=self.bulk_user_manager_ui)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.total_hits_label.config(
                            text="Some Error occurred. Check Logs", fg="red")
            self.retrieve_data_count_label.config(
                            text="", fg="black")

    def toggleInputField(self, val):
        try:
            self.userent["state"] = val
            self.passent["state"] = val
            self.ipenter["state"] = val
            self.select_file_btn["state"] = val
            self.to_be_deleted_users_ent["state"] = val
            self.user_start_operation_btn["state"] = val
            self.user_operation_select_ent["state"] = val if val == "disabled" else "readonly"

            self.envent["state"] = val
            self.source_dropdown_ent["state"] = val

            self.export_btn["state"] = "disabled" if val == "normal" else "normal"

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initiate_var()
            self.toggleInputField("normal")
            self.bulk_user_manager_ui.excelfile = ""
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.data_tree.delete(*self.data_tree.get_children())
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# End of Bulk Deactivate/Activate User Manager

# Start of Bulk Copy/Move Node

class BulkCopyOrMoveManager:
    def __init__(self, master):
        self.bulk_copy_move_ui = Toplevel(master)
        self.master = master
        self.bulk_copy_move_ui.state('zoomed')
        master.withdraw()
        self.bulk_copy_move_ui.title(
            APPLICATION_NAME + " - " + "Copy or Move Node/Page(s)"
        )
        self.bulk_copy_move_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.bulk_copy_move_ui.iconphoto(False, self.brandpic)
        self.bulk_copy_move_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.bulk_copy_move_ui.configdata = configdata
        self.bulk_copy_move_ui.excelfile = ""
        self.bulk_copy_move_instances = None
        
        self.create_menu_bar()
        self.main_design()
    
    def create_menu_bar(self):
        try:
            file_url = "https://docs.google.com/spreadsheets/d/17oqbHMBZ92CtiNPRKcZlYifHXGje9SwpVQjmzOWQCLs/export?format=xlsx&gid=2037198470"
            self.main_menu = Menu(self.bulk_copy_move_ui)
            self.downloadmenu = Menu(self.main_menu, tearoff=0)
            self.downloadmenu.add_command(
                label="Payloads", command=lambda *args: GenericFunctions.download_google_sheet(file_url)
            )
            self.main_menu.add_cascade(
                label="Sample File", menu=self.downloadmenu)
            self.bulk_copy_move_ui.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state("zoomed")
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.bulk_copy_move_ui.destroy()
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
                    basicconfigdata.get(str(selected_env)+"_username",""))# self.var_selected_source.set("Source Data from Excel")
            self.varipdata.set("")
            self.varpassent.set(self.decrypted_passwd)
            self.varexcelfile.set("Browse & Select Excel File")
            self.varuseroperation.set("--SELECT--")
            self.varcreateparent.set(0)
            self.varpublishedpage.set(0)
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

    def main_design(self):
        try:
            # Declare String Variable
            self.define_style()

            # String Variable
            # self.var_selected_source = StringVar()
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varexcelfile = StringVar()
            self.varuseroperation = StringVar()
            self.varcreateparent = IntVar()
            self.varpublishedpage = IntVar()

            # Initiate String Variable
            self.initiate_var()

            # Validation
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))

            # Frame Creation
            self.main_frame = Frame(self.bulk_copy_move_ui)
            self.main_frame.pack(fill="x")

            self.main_btn_frame_sep = ttk.Separator(
                self.bulk_copy_move_ui)
            self.main_btn_frame_sep.pack(fill="x", padx=5, pady=10)

            self.main_btn_frame = Frame(self.bulk_copy_move_ui)
            self.main_btn_frame.pack(fill="x")

            self.btn_frame_details_sep = ttk.Separator(
                self.bulk_copy_move_ui)
            self.btn_frame_details_sep.pack(fill="x", padx=5, pady=10)

            self.main_details_frame = Frame(self.bulk_copy_move_ui)
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
                self.iplabelframe, textvariable = self.varenvdata, values=self.envdata, state="readonly")
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
                row=1, column=2, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            # self.source_dropdown_data = ["Source Data from Excel"]  # , "Use Query Builder"
            # self.source_dropdown_ent = ttk.OptionMenu(
            #     self.selectionlabelframe, self.var_selected_source, *self.source_dropdown_data)  # , command=self.changecheckbox
            # self.source_dropdown_ent.grid(row=0, column=0, padx=5,
            #                               pady=5, sticky="nsew")

            # Query Window or Excel Window
            self.select_file_btn = ttk.Button(
                self.selectionlabelframe, text="Select Excel File", command=self.openexcelfile)
            self.select_file_btn.grid(
                row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.selected_file_label = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..", textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),)
            self.selected_file_label.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")

            self.selectionlabelframe.grid_columnconfigure(1, weight=1)

            # # User Operation
            self.user_operation_frame = LabelFrame(
                self.main_frame, text="Select Operation")
            self.user_operation_frame.grid(
                row=1, column=0, columnspan = 2, padx=5, pady=(13, 7), sticky="nsew")

            self.published_page_checkbox = ttk.Checkbutton(
                self.user_operation_frame, variable=self.varpublishedpage, onvalue=1, offvalue=0, text="Copy/Move Published Page")
            self.published_page_checkbox.pack(side="left", expand="yes", padx=5, pady=10, ipadx=5, ipady=5, anchor="center")
            # .grid(row=0, column=0, padx=5, pady=10, ipadx=5, ipady=5, sticky="nsew")

            self.create_parent_checkbox = ttk.Checkbutton(
                self.user_operation_frame, variable=self.varcreateparent, onvalue=1, offvalue=0, text="Create Parent Folder")
            self.create_parent_checkbox.pack(side="left", expand="yes", pady=10, ipadx=5, ipady=5, anchor="center")
            # .grid(row=0, column=1, padx=5, pady=10, ipadx=5, ipady=5, sticky="nsew")

            # self.user_operation_frame.grid_columnconfigure(0, weight=1)
            self.user_operation_data = ["--SELECT--","Copy","Move"]

            self.user_operation_select_ent = ttk.Combobox(
                self.user_operation_frame, textvariable=self.varuseroperation, state="readonly", values=self.user_operation_data)
            self.user_operation_select_ent.pack(side="left", expand="yes", padx=5, pady=10, ipadx=5, ipady=5, anchor="center")
            # .grid(row=0, column=2, padx=5, pady=10, ipadx=5, ipady=5, sticky="nsew")
            self.main_frame.grid_columnconfigure(2, weight=1)

            # Button
            self.user_start_operation_btn = ttk.Button(
                self.main_btn_frame, text="Start Operation", style="mainBtn.TButton", command=self.validate_and_run_user_operation)  # , command=self.retrvdata
            self.user_start_operation_btn.pack(
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

            self.export_btn = ttk.Button(
                self.small_btn_frame, text="Export",state="disabled", style="smallBtn.TButton", command=self.export_status_report)  # , command=self.exportData
            self.export_btn.pack(side="left", padx=5, pady=0, anchor="w")

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

            self.data_tree.bind("<<Copy>>", self.getDataandCopy)
            # self.data_tree.bind('<Double-Button-1>', self.edit_data_popup)

            self.data_tree_frame.pack(
                fill="both", padx=5, pady=10)

            self.bulk_copy_move_ui.update()

            table_width = self.data_tree.winfo_width()
            _width = int(table_width * 0.4)
            status_width = int(table_width * 0.2)

            self.data_tree.column("1", width=_width, stretch="yes")
            self.data_tree.column("2", width=_width, stretch="yes")
            self.data_tree.column("3", width=status_width,
                                  stretch="yes", anchor="c")

            self.data_tree.heading("1", text="Source Path")
            self.data_tree.heading("2", text="Target Path")
            self.data_tree.heading("3", text="Status")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    ### Function / Callback
    def close_this_window(self, wind):
        try:
            self.bulk_copy_move_ui.focus_set()
            self.bulk_copy_move_ui.wm_attributes("-disabled", False)
            wind.destroy()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
    
    def getDataandCopy(self, event):
        try:
            self.master.clipboard_clear()  # clear clipboard contents
            for i in self.data_tree.selection():
                logger.debug("Item No: " + str(i))
                item = self.data_tree.item(i)
                values = item["values"]
                self.master.clipboard_append("\t".join(values))
                # append new value to clipbaord
                self.master.clipboard_append("\n")
                logger.debug("Copied to Clipboard: "+str(values))
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def ipchange(self, value):
        try:
            if value.lower() == "ip":
                self.ipenter.grid(row=0, column=1, padx=10,
                                  pady=10, ipadx=5, ipady=5, sticky="nsew")
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
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def openexcelfile(self):
        try:
            logger.debug("--Single Redirect--")
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.bulk_copy_move_ui.excelfile = excelfile = filedialog.askopenfilename(
                initialdir=BASE_SCRIPT_PATH, title="Select Excel File", filetypes=types
            )
            if self.bulk_copy_move_ui.excelfile:
                logger.debug("Selected Excel File: " +
                             self.bulk_copy_move_ui.excelfile)
                self.varexcelfile.set(self.bulk_copy_move_ui.excelfile)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def validate_inputs(self, uname, passwd, environment, selected_ip, selected_operation, source_data, source_type):
        try:
            #excel_file
            output_status = False
            is_not_empty_uname = bool(uname)
            logger.debug("Username Not Empty: "+str(is_not_empty_uname))

            is_not_empty_passwd = bool(passwd)
            logger.debug("Password Not Empty: "+str(is_not_empty_passwd))

            is_not_empty_ip = bool(selected_ip)
            logger.debug("IP Not Empty: "+str(is_not_empty_ip))

            is_not_empty_operation = bool(selected_operation)
            logger.debug("WF Not Empty: "+str(is_not_empty_operation))

            is_valid_source_data = bool(source_data)
            logger.debug("Valid File: "+str(is_valid_source_data))

            is_a_file = True if (source_type == "Source Data from Excel" and is_valid_source_data) else False

            allowed_file_types = [".xlsx", ".xls", ".xlsm"]
            is_valid_excel_file = False
            
            if is_a_file:
                is_valid_excel_file = GenericFunctions.is_valid_file_types(source_data, allowed_file_types)
            if not(is_a_file) and is_valid_source_data:
                is_valid_excel_file = True
            logger.debug("Valid Excel File: "+str(is_valid_excel_file))

            is_valid_ip = GenericFunctions.validateIP(
                selected_ip, environment) if is_not_empty_ip else False
            logger.debug("Valid IP: "+str(is_valid_ip))

            is_valid_operaion = True if selected_operation != "--SELECT--" else False
            logger.debug("Valid Workflow: "+str(is_valid_operaion))

            if is_not_empty_ip and is_not_empty_uname and is_not_empty_passwd and is_valid_source_data and is_valid_excel_file and is_valid_ip and is_valid_operaion and is_not_empty_operation:
                output_status = True

            else:
                error_list = []
                if not(is_not_empty_uname):
                    error_list.append("\nUsername Can't be Empty")

                if not(is_not_empty_passwd):
                    error_list.append("\nPassword Can't be Empty")

                if not(is_not_empty_ip):
                    error_list.append("\nIP Can't be Empty")

                if not(is_valid_source_data):
                    error_list.append("\nPlease select a File")

                if not(is_valid_operaion):
                    error_list.append("\nPlease select a Valid Operation")

                if not(is_not_empty_operation):
                    error_list.append("\nOperation can't be empty")

                if not(is_valid_excel_file):
                    error_list.append(
                        "\nInvalid Selected File. Only accepts below\n"+",".join(allowed_file_types))

                if not(is_valid_ip):
                    error_list.append(
                        "\nInvalid IP, Please select/enter correct IP")

                if bool(error_list):
                    messagebox.showerror("Below Error has occurred", "--------Errors---------"+".".join(
                        error_list), parent=self.bulk_copy_move_ui)
                    logger.error("Below Error has occurred" +
                                 ".".join(error_list))

            logger.info("Data Validation Status: " + str(output_status))
            return output_status

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def remove_invalid_data(self, excel_data):
        try:
            for _each_row in excel_data:
                n_cols = len(_each_row)
                if n_cols != 2:
                    excel_data.remove(_each_row)
                    logger.info("Removed Invalid Row: "+str(_each_row))

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def validate_and_run_user_operation(self):
        try:
            enable_field = False
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.bulk_copy_move_ui.update()

            uname = self.varuserent.get().strip()
            passwd = self.varpassent.get().strip()

            environment = self.varenvdata.get().lower()
            selected_ip = (self.varipdata.get().lower().strip()
                           if environment == "ip" else configdata[environment])
            source_type = "Source Data from Excel" #self.var_selected_source.get()
            source_data = self.bulk_copy_move_ui.excelfile if source_type == "Source Data from Excel" else ""
            selected_operation = self.varuseroperation.get()
            copy_published_page = True if self.varpublishedpage.get() else False
            create_parent = True if self.varcreateparent.get() else False
            run_the_operation = True
            if environment.lower() == "production":
                run_the_operation = messagebox.askyesnocancel(
                    "Please confirm", "Do you want to Run\nthe Operation in Production?", parent=self.bulk_copy_move_ui)

            if run_the_operation:
                is_validated = self.validate_inputs(
                    uname, passwd, environment, selected_ip, selected_operation, source_data, source_type)

                if is_validated:
                    status_proc = {
                        "200" : "Completed",
                        "401" : "Wrong Username and Password",
                        "400" : "Bad Request",
                        "403" : "Forbidden",
                        "404" : "Page not found",
                        "405" : "Method Not Allowed",
                        "406" : "Not Acceptable",
                        "500" : "Internal Server Error",
                        "501" : "Not Implemented",
                        "502" : "Bad Gateway",
                        "503" : "Service Unavailable",
                        "901" : "No User Present",
                        "902" : "Aborted, Not Published",
                        "904" : "Can't Create folder",
                        "905" : "Not a Page",
                        "999" : "Exception"
                        }
                    self.bulk_copy_move_instances = UserAccountsAndCopy(selected_ip, uname, passwd)
                    all_data = self.bulk_copy_move_instances.read_data(source_data)
                    self.remove_invalid_data(all_data)
                    count_of_payloads = len(all_data)

                    logger.debug("Count of Payloads: "+str(count_of_payloads))
                    self.bulk_copy_move_ui.progress_bar = ttk.Progressbar(
                            self.small_btn_frame, orient=HORIZONTAL, maximum=count_of_payloads, mode="determinate", style="green.Horizontal.TProgressbar")
                    self.bulk_copy_move_ui.progress_bar.pack(
                            fill="x", expand="yes", side="left", padx=10, pady=0, anchor="w")
                    valid_paths = [
                            operationdata.get("content root","/content/pwc"),
                            operationdata.get("content dam root","/content/dam/pwc"),
                            operationdata.get("form content path","/content/usergenerated/content/pwc"),
                            operationdata.get("form archive content path","/content/usergenerated/archive/content/pwc"),
                        ]
                    self.total_hits_label.config(
                                    text="Total: "+str(count_of_payloads), fg="black")
                    for row_id, _each_row in enumerate(all_data):
                        source_path = _each_row[0]
                        target_path = _each_row[1]
                        status = GenericFunctions.validate_source_with_target(source_path, target_path, valid_paths)

                        if status == "Valid":
                            copy_status = self.bulk_copy_move_instances.copy_move_node(source_path, target_path, selected_operation.lower(), copy_published_page, create_parent)

                            if copy_status == 401:
                                enable_field = True
                                self.total_hits_label.config(
                                    text="Wrong Username and Password", fg="red")
                                break
                            elif copy_status == 200:
                                self.insert_into_table(row_id+1, [source_path, target_path, "Completed"])
                            else:
                                status = status_proc.get(str(copy_status),"Failed - "+str(copy_status))
                                self.insert_into_table(row_id+1, [source_path, target_path, status])
                                
                        else:
                            self.insert_into_table(row_id+1, [source_path, target_path, status])

                        self.bulk_copy_move_ui.progress_bar["value"] = row_id+1
                        self.retrieve_data_count_label.config(text="Current: "+str(row_id+1), fg="black")
                        self.bulk_copy_move_ui.update()

                    self.bulk_copy_move_ui.progress_bar.destroy()
                    self.toggleInputField("disabled")
                    if enable_field:
                        self.userent["state"] = "normal"
                        self.passent["state"] = "normal"
                        self.user_start_operation_btn["state"] = "normal"
                        self.export_btn["state"] = "disabled"


        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.total_hits_label.config(
                                    text="Exception Occurred!!", fg="red")
            if self.bulk_copy_move_ui.progress_bar.winfo_ismapped():
                self.bulk_copy_move_ui.progress_bar.destroy()
            self.toggleInputField("normal")

    def export_status_report(self):
        try:
            all_table_row_id = self.data_tree.get_children()
            if bool(all_table_row_id):
                ## Select the File
                types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                        ("All Files", "*.*"))
                save_file = filedialog.asksaveasfilename(
                    initialdir=BASE_SCRIPT_PATH, initialfile="data_output.xlsx", title="Save Data", filetypes=types, defaultextension=types
                )
                logger.info("File Name to Export the Data: "+str(save_file))
                if save_file:
                    all_table_data = []
                    # if bool(all_table_row_id):
                    all_table_data.append(["Source Path","Target Path", "Status"])
                    for each_row_id in all_table_row_id:
                        all_table_data.append(self.data_tree.item(each_row_id)["values"])

                    logger.debug("Exported Data: " + str(all_table_data))
                    _workbook = xlsxwriter.Workbook(save_file)
                    _worksheet = _workbook.add_worksheet()

                    for x in range(len(all_table_data)):
                        for y in range(len(all_table_data[x])):
                            _worksheet.write(x, y, str(all_table_data[x][y]))

                    _workbook.close()
                    messagebox.showinfo("Success!!!","Exported Successfully", parent=self.bulk_copy_move_ui)
            else:
                messagebox.showwarning("No Data Warning!!!","No Data to Export!!!", parent=self.bulk_copy_move_ui)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.total_hits_label.config(
                            text="Some Error occurred. Check Logs", fg="red")
            self.retrieve_data_count_label.config(
                            text="", fg="black")

    def toggleInputField(self, val):
        try:
            self.userent["state"] = val
            self.passent["state"] = val
            self.ipenter["state"] = val
            self.select_file_btn["state"] = val
            self.create_parent_checkbox["state"] = val
            self.published_page_checkbox["state"] = val
            self.user_start_operation_btn["state"] = val
            self.user_operation_select_ent["state"] = val if val == "disabled" else "readonly"

            self.envent["state"] = val

            self.export_btn["state"] = "disabled" if val == "normal" else "normal"

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initiate_var()
            self.toggleInputField("normal")
            self.bulk_copy_move_ui.excelfile = ""
            self.total_hits_label.config(text="", fg="black")
            self.retrieve_data_count_label.config(text="", fg="black")
            self.data_tree.delete(*self.data_tree.get_children())
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# End of Bulk Copy/Move

# Start of Pre-defined Manager


class PreDefinedReportsManager:
    def __init__(self, master):
        global configdata
        self.predefined_report_ui = Toplevel(master)
        self.master = master
        self.predefined_report_ui.state('zoomed')
        master.withdraw()
        self.predefined_report_ui.title(
            APPLICATION_NAME + " - " + "Generate and Export DPE Report"
        )
        self.predefined_report_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.predefined_report_ui.brandpic = PhotoImage(
            file=BRAND_PIC_FILE)
        self.predefined_report_ui.iconphoto(False, self.brandpic)
        self.predefined_report_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.predefined_report_instance = None
        self.predefined_report_ui.configdata = configdata
        self.predefined_report_ui.fetched_data = None
        self.predefined_report_ui.user_variable_entered_data = None
        self.predefined_report_ui.fetched_data_count = 0
        self.predefined_report_ui.total_data_count = 0
        self.predefined_report_ui.resource_type_data = edcfg.readConfig(RESOURCE_TYPE_FILE)

        self.create_menu_bar()
        self.main_design()

    def changeRoot(self, root):
        root.state('zoomed')
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.predefined_report_ui.destroy()
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
            self.varipdata.set("")
            self.varpassent.set(self.decrypted_passwd)
            self.varreportname.set("--SELECT--")
            self.varterritoryname.set("--SELECT--")
            self.varterritorynameent.set("")
            self.varpropertyname.set("")
            self.varquerydata.set("+ Add Property from List +")
            self.vardate.set("--DAY--")
            self.varmonth.set("--MONTH--")
            self.varyear.set("--YEAR--")
            self.varuserdefvar.set("")
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
            self.window_style.configure(
                "mainBigBtn.TButton", font=(FONT_NAME, FONT_SIZE * 4), relief="flat")
            self.window_style.configure("scrollbarmain.TScrollbar", background="Green", darkcolor="DarkGreen",
                                        lightcolor="LightGreen", troughcolor="gray", bordercolor="blue", arrowcolor="white")
            self.window_style.configure(
                "green.Horizontal.TProgressbar", foreground='green', background='darkgreen')

            self.window_style.configure(
                "labelent.TLabel", font=(FONT_NAME, FONT_SIZE + 4, "bold"))
            self.window_style.configure(
                "labelent.TEntry", font=(FONT_NAME, FONT_SIZE + 4, "bold"))

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def create_menu_bar(self):
        try:
            self.main_menu = Menu(self.predefined_report_ui)
            self.add_report = Menu(self.main_menu, tearoff=0)
            self.add_report.add_command(
                label="Add/Edit Report", command=self.open_user_def_report
            )
            self.main_menu.add_cascade(
                label="Create New Reports", menu=self.add_report)
            self.settings_menu = Menu(self.main_menu, tearoff=0)
            self.settings_menu.add_command(
                label="Edit Value", command=self.change_limit_of_data
            )
            self.settings_menu.add_command(
                label="Import Old Reports", command=self.import_old_report
            )
            self.settings_menu.add_command(
                label="Add Component", command=self.add_component_resource
            )
            self.main_menu.add_cascade(
                label="Settings", menu=self.settings_menu)
            self.predefined_report_ui.config(menu=self.main_menu)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def main_design(self):
        try:
            # Declare String Variable
            self.define_style()

            # String Variable
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varreportname = StringVar()
            self.varterritoryname = StringVar()
            self.varterritorynameent = StringVar()
            self.varpropertyname = StringVar()
            self.varquerydata = StringVar()
            self.vardate = StringVar()
            self.varmonth = StringVar()
            self.varyear = StringVar()
            self.varuserdefvar = StringVar()

            # Initiate String Variable
            self.initiate_var()

            # Validation
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))
            self.varreportname.trace(
                "w", lambda *args: self.report_name_change(self.varreportname.get()))
            self.varterritoryname.trace(
                "w", lambda *args: self.territory_change(self.varterritoryname.get()))
            self.varquerydata.trace(
                "w", lambda *args: self.select_operation())

            # Frame Creation
            self.main_frame = Frame(self.predefined_report_ui)
            self.main_frame.pack(fill="x", padx=5)

            self.main_upper_frame = Frame(self.main_frame)
            self.main_upper_frame.pack(fill="x", padx=5)

            self.main_lower_frame = Frame(self.main_frame)
            self.main_lower_frame.pack(fill="x", padx=5)

            self.main_btn_frame_sep = ttk.Separator(
                self.predefined_report_ui)
            self.main_btn_frame_sep.pack(fill="x", padx=5, pady=10)

            self.main_btn_frame = Frame(self.predefined_report_ui)
            self.main_btn_frame.pack(fill="x")

            self.btn_frame_details_sep = ttk.Separator(
                self.predefined_report_ui)
            self.btn_frame_details_sep.pack(fill="x", padx=5, pady=10)

            self.main_details_frame = Frame(self.predefined_report_ui)
            self.main_details_frame.pack(fill="both")

            # Environment Frame
            self.environment_frame = LabelFrame(
                self.main_upper_frame, text="Select Environment")
            self.environment_frame.pack(
                side="left", fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10)

            ## Username & Password
            self.username_and_password_frame = LabelFrame(
                self.main_upper_frame, text="Login Details")
            self.username_and_password_frame.pack(
                side="left", fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10)
            # self.username_and_password_frame.grid_columnconfigure(0, weight=1)

            self.username_label = ttk.Label(
                self.username_and_password_frame, text="Username", style="labelent.TLabel")
            self.username_label.grid(
                row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.username_ent = ttk.Entry(
                self.username_and_password_frame, textvariable=self.varuserent, style="labelent.TEntry")
            self.username_ent.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.username_and_password_frame.grid_columnconfigure(1, weight=1)

            self.passwd_label = ttk.Label(
                self.username_and_password_frame, text="Password", style="labelent.TLabel")
            self.passwd_label.grid(
                row=1, column=0, padx=5, pady=5, sticky="nsew")
            self.passwd_ent = ttk.Entry(
                self.username_and_password_frame, show="*", textvariable=self.varpassent, style="labelent.TEntry")
            self.passwd_ent.grid(row=1, column=1, padx=5,
                                 pady=5, sticky="nsew")
            self.username_and_password_frame.grid_columnconfigure(1, weight=1)

            # # Environment Frame
            # self.environment_frame = LabelFrame(
            #     self.main_upper_frame, text="Select Environment")
            # self.environment_frame.pack(
            #     side="left", fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10)
            # self.environment_frame.grid_columnconfigure(1, weight=1)

            self.environment_label = ttk.Label(
                self.environment_frame, text="Environment", style="labelent.TLabel")
            self.environment_label.grid(
                row=0, column=0, padx=5, pady=5, sticky="nsew")
            # self.env_dropdown_data = ["Production", "Stage", "QA", "IP"]
            env_data = configdata.get("environments",[])
            # env_data.insert(0,"")
            self.env_dropdown_data = env_data.copy()
            self.environment_ent = ttk.Combobox(
                self.environment_frame, textvariable=self.varenvdata, state="readonly", values=self.env_dropdown_data)
            #ttk.Optionmenu(self.environment_frame, textvariable=self.varuserent)
            self.environment_ent.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.environment_frame.grid_columnconfigure(1, weight=1)

            self.environment_ip_ent = ttk.Entry(
                self.environment_frame, textvariable=self.varipdata, state="disabled", style="labelent.TEntry")
            self.environment_ip_ent.grid(
                row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
            self.environment_frame.grid_columnconfigure(1, weight=1)

            # Report Frame
            self.report_frame = LabelFrame(
                self.main_upper_frame, text="Report & Territory Selection")
            self.report_frame.pack(
                side="left", fill="both", expand="yes", padx=10, pady=10)
            # self.report_frame.grid_columnconfigure(2, weight=1)

            self.report_label_frame = LabelFrame(
                self.report_frame, text="Select Report")
            self.report_label_frame.grid(
                row=0, column=0, padx=5, pady=0, sticky="nsew")

            # self.report_list = ["--SELECT--", "Page Report","Published Page Report", "Contactus Arch Form Report",
            #                 "Contactus Form Report", "Online Archive Form Report", "Online Form Report",
            #                 "DAM Asset Report", "Contact Page Report"]
            global USER_DEF_FILE
            self.user_def_report_json = edcfg.readConfig(USER_DEF_FILE)
            self.report_list = []
            for _rep in self.user_def_report_json.get("report_list", []):
                self.report_list.append(_rep)
            self.report_list.insert(0, "--SELECT--")

            self.report_list_combobox = ttk.Combobox(
                self.report_label_frame, textvariable=self.varreportname, state="readonly", values=self.report_list, width=25)
            self.report_list_combobox.grid(
                row=0, column=0, padx=0, pady=0, ipadx=5, ipady=5, sticky="nsew")
            self.report_label_frame.grid_columnconfigure(0, weight=1)

            self.territory_label_frame = LabelFrame(
                self.report_frame, text="Select/Type Territory or Path")
            self.territory_label_frame.grid(
                row=0, column=1, columnspan=2, padx=5, pady=0, sticky="nsew")
            self.user_def_sep_var_label = ttk.Label(
                self.report_frame, text="***********************", anchor="c")
            self.user_def_var_popup = ttk.Button(
                self.report_frame, text="Enter Variable(s)", command=lambda *args: print("Popup Opened"))

            self.all_territory_mappings = GenericFunctions.read_country_name(
                TERRITORY_FILE)
            
            self.territory_list = []
            for _map_ter in self.all_territory_mappings:
                self.territory_list.append(str(self.all_territory_mappings[_map_ter]).title())

            self.territory_list.sort()
            self.territory_list.insert(0, "MULTI")
            self.territory_list.insert(0, "--SELECT--")
            self.territory_list_combobox = ttk.Combobox(
                self.territory_label_frame, textvariable=self.varterritoryname, state="disabled", values=self.territory_list, width=15)
            self.territory_list_combobox.grid(
                row=0, column=0, padx=5, pady=0, ipadx=5, ipady=5, sticky="nsew")
            self.territory_label_frame.grid_columnconfigure(0, weight=1)

            self.territory_name_ent = ttk.Entry(
                self.territory_label_frame, textvariable=self.varterritorynameent, state="disabled", style="labelent.TEntry")
            self.territory_name_ent.grid(
                row=0, column=1, padx=5, pady=0, sticky="nsew")
            self.territory_change(self.varterritoryname.get())
            self.territory_label_frame.grid_columnconfigure(1, weight=1)

            # self.report_frame.grid_columnconfigure(1, weight=1)
            # self.user_def_var_v_label = ttk.Label(self.report_frame, text='Type values with ";" Separator', anchor="e")
            # self.user_def_var_ent = ttk.Entry(self.report_frame, textvariable=self.varuserdefvar, style="labelent.TEntry")
            self.user_def_var_label = ttk.Label(
                self.report_frame, text="", anchor="c")

            self.year_value = GenericFunctions.generate_five_years_past()
            self.year_value.insert(0, "--YEAR--")
            self.year_combobox = ttk.Combobox(
                self.report_frame, textvariable=self.varyear, state="disabled", values=self.year_value)
            self.year_combobox.grid(
                row=1, column=0, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")

            self.month_list = ['--MONTH--', 'January', 'February', 'March', 'April', 'May',
                               'June', 'July', 'August', 'September', 'October', 'November', 'December']
            self.month_combobox = ttk.Combobox(
                self.report_frame, textvariable=self.varmonth, state="disabled", values=self.month_list, width=12)
            self.month_combobox.grid(
                row=1, column=1, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")

            self.date_list = [(x+1) for x in range(31)]
            self.date_list.insert(0, '--DAY--')
            self.day_combobox = ttk.Combobox(
                self.report_frame, textvariable=self.vardate, state="disabled", values=self.date_list)
            self.day_combobox.grid(
                row=1, column=2, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")

            self.type_of_property_writer = [
                "", "+ Add Property from List +", "+ Type JCR Property in the box +", "Both"]
            self.type_of_property_writer_ent = ttk.OptionMenu(
                self.main_lower_frame, self.varquerydata, *self.type_of_property_writer)
            self.type_of_property_writer_ent.grid(row=0, column=0, padx=5,
                                                  pady=5, sticky="nsew")

            self.property_btn = ttk.Button(
                self.main_lower_frame, text="SELECT >>", command=self.open_property_addition)
            self.property_btn.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")

            self.property_name_ent = ttk.Entry(
                self.main_lower_frame, textvariable=self.varpropertyname, style="labelent.TEntry")
            self.property_name_ent.grid(
                row=0, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

            self.main_lower_frame.grid_columnconfigure(2, weight=1)
            self.select_operation()

            # Button Frame
            self.fetch_data = ttk.Button(
                self.main_btn_frame, text="Retrieve Data", command=self.retreive_data)
            self.fetch_data.pack(side="left", expand="yes",
                                 padx=5, pady=5, anchor=CENTER)

            self.reset_btn = ttk.Button(
                self.main_btn_frame, text="Reset All", command=self.reset_all)
            self.reset_btn.pack(side="left", expand="yes",
                                padx=5, pady=5, anchor=CENTER)

            self.exit_window = ttk.Button(
                self.main_btn_frame, text="Exit Window", command=lambda root=self.master: self.reopenroot(root))
            self.exit_window.pack(side="left", expand="yes",
                                  padx=5, pady=5, anchor=CENTER)

            # Details Frame
            self.retrieved_data_frame = LabelFrame(
                self.main_details_frame, text="********")
            self.retrieved_data_frame.pack(
                side="left", fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)

            self.small_btn_frame = Frame(self.retrieved_data_frame)
            self.small_btn_frame.pack(
                fill="x", padx=2, pady=0, ipadx=2, ipady=2)

            self.data_table_frame = Frame(self.retrieved_data_frame)
            self.data_table_frame.pack(
                fill="both", expand="yes", padx=2, pady=2, ipadx=2, ipady=2)

            # Small Button
            self.export_btn = ttk.Button(self.small_btn_frame, text="Export",
                                         command=self.exportData, style="smallBtn.TButton", state="disabled")
            self.export_btn.pack(side="left", padx=2, pady=2, anchor="w")

            self.results_label = Label(self.small_btn_frame, text="")
            self.results_label.pack(side="left", padx=2, pady=2, anchor="w")

            self.total_label = Label(self.small_btn_frame, text="")
            self.total_label.pack(side="left", padx=2, pady=2, anchor="w")

            # Treeview Table
            self.data_table_holder = ttk.Treeview(
                self.data_table_frame, show="headings", selectmode="extended", height=25)
            self.data_table_holder_scroll_y = ttk.Scrollbar(
                self.data_table_frame, orient="vertical", command=self.data_table_holder.yview)
            self.data_table_holder.config(
                yscrollcommand=self.data_table_holder_scroll_y.set)
            self.data_table_holder_scroll_y.pack(side="right", fill="y")

            self.data_table_holder_scroll_x = ttk.Scrollbar(
                self.data_table_frame, orient="horizontal", command=self.data_table_holder.xview)
            self.data_table_holder.config(
                xscrollcommand=self.data_table_holder_scroll_x.set)
            self.data_table_holder_scroll_x.pack(side="bottom", fill="x")

            self.data_table_holder.pack(
                padx=5, pady=5, anchor="c", fill="both")

            self.predefined_report_ui.update()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    ### Function / Callback
    def add_component_resource(self):
        from ui_component import EditComponentResource
        try:
            self.predefined_report_ui.edit_add_resourcetype = EditComponentResource(self.predefined_report_ui)
            self.predefined_report_ui.edit_add_resourcetype.config(application_name = "DanTe", brandpic=self.brandpic, close_pop_window=self.close_popup_window, datafile=RESOURCE_TYPE_FILE)
            self.predefined_report_ui.edit_add_resourcetype.main()
            self.predefined_report_ui.wait_window(self.predefined_report_ui.edit_add_resourcetype)
            self.predefined_report_ui.resource_type_data = self.predefined_report_ui.edit_add_resourcetype.data
            logger.debug(self.predefined_report_ui.resource_type_data)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def import_old_report(self):
        try:
            #.asksaveasfilename(initialdir=BASE_SCRIPT_PATH, initialfile="data_output.xlsx", title="Save Data", filetypes=types, defaultextension=types)
            old_tool_save_dir = filedialog.askdirectory(title="Select the config directory of Old tool")
            if old_tool_save_dir:
                logger.debug("Old Directory: %s", old_tool_save_dir)
                old_user_def_file = os.path.join(old_tool_save_dir, "user_defined_reports.json")
                ## Old data
                read_data = edcfg.readConfig(old_user_def_file)
                logger.debug("Old Data: "+str(read_data))
                saved_queries = read_data.get("query list", {})
                
                current_id_in_ = self.user_def_report_json.get("current", 1)
                current_user_report_prefix = self.user_def_report_json.get("prefix","User-Def")
                current_report_list = self.user_def_report_json.get("report_list",[])
                current_user_def_query_list = self.user_def_report_json.get("query list",{})
                logger.debug("Current ID: %s, Current User report Prefix: %s", current_id_in_, current_user_report_prefix)
                logger.debug("Current Report List: %s",str(current_report_list))
                logger.debug("Current Query List: %s",str(current_user_def_query_list))
                for _saved_query, _saved_query_det in saved_queries.items():
                    old_report_name = _saved_query_det.get("name","")
                    old_id = _saved_query_det.get("id","")
                    old_query = _saved_query_det.get("query","")
                    old_type = _saved_query_det.get("type","")
                    old_variables = _saved_query_det.get("variables","")
                    new_id = current_id_in_ + 1
                    current_id_in_ = new_id
                    new_report_key = current_user_report_prefix + "-" + str(new_id) + "-" + str(old_report_name)
                    updated_report_dict = {
                        "id": new_id, "name": old_report_name,"query": old_query,
                        "type": old_type,
                        "variables": old_variables
                    }
                    current_report_list.append(new_report_key)
                    current_user_def_query_list[new_report_key] = updated_report_dict
                self.user_def_report_json["current"] = current_id_in_
                self.report_list_combobox.config(values=self.user_def_report_json["report_list"])
                logger.debug("Updated Report: "+str(self.user_def_report_json))
                status = edcfg.updateConfig(self.user_def_report_json, USER_DEF_FILE)
                if status:
                    messagebox.showinfo("Success!!!", "Imported Successfully.", parent=self.predefined_report_ui)
                else:
                    messagebox.showerror("Failed!!!", "Failed to Import.", parent=self.predefined_report_ui)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def select_operation(self):
        try:
            _selected_data = self.varquerydata.get().strip()  # + Add Property from List +
            logger.debug("SELECTED DATA: "+str(_selected_data))
            if _selected_data == "+ Add Property from List +":
                self.property_btn["state"] = "normal"
                self.property_name_ent["state"] = "disabled"
                self.property_btn.config(text="SELECT >>")

            elif _selected_data == "+ Type JCR Property in the box +":
                self.property_btn["state"] = "disabled"
                self.property_name_ent["state"] = "normal"
                self.property_btn.config(text="Type Propertyname")

            elif _selected_data == "Both":
                self.property_btn["state"] = "normal"
                self.property_name_ent["state"] = "normal"
                self.property_btn.config(text="SELECT >>")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def closepopupwindow(self):
        try:
            self.predefined_report_ui.focus_set()
            self.predefined_report_ui.wm_attributes("-disabled", False)
            self.predefined_report_ui.create_ui.destroy()
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def close_popup_window(self, modal_window):
        try:
            self.predefined_report_ui.focus_set()
            self.predefined_report_ui.wm_attributes("-disabled", False)
            modal_window.destroy()
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def change_limit_of_data(self):
        try:
            self.predefined_report_ui.change_limit_modal = Toplevel(
                self.predefined_report_ui)
            self.predefined_report_ui.wm_attributes("-disabled", True)
            self.predefined_report_ui.change_limit_modal.focus_set()
            self.predefined_report_ui.change_limit_modal.title(
                APPLICATION_NAME + " - " + "Edit Limis Results")
            self.predefined_report_ui.change_limit_modal.geometry("250x150+300+20")
            self.predefined_report_ui.change_limit_modal.minsize(250, 150)
            self.predefined_report_ui.change_limit_modal.maxsize(250, 300)
            self.predefined_report_ui.change_limit_modal.resizable(width=False, height=True)
            self.predefined_report_ui.change_limit_modal.iconphoto(False, self.brandpic)
            self.predefined_report_ui.change_limit_modal.transient(
                self.predefined_report_ui)
            self.predefined_report_ui.change_limit_modal.protocol(
                "WM_DELETE_WINDOW", lambda *args: self.close_popup_window(self.predefined_report_ui.change_limit_modal))

            varlimit = StringVar()
            stored_limit = 0 if operationdata.get("limit result", 0) < 0 else operationdata.get("limit result", 0)
            varlimit.set(str(stored_limit))
            varlimit.trace(
                "w", lambda *args: check_limit_data(varlimit.get()))

            def check_limit_data(input_data):
                try:
                    if not(input_data[-1].isnumeric()):
                        varlimit.set(input_data[:-1])
                except:
                    logger.error("Below Exception occured: ", exc_info=True)

            def save_data():
                try:
                    global operationdata
                    _limit_data = varlimit.get().strip()
                    operationdata["limit result"] = int(_limit_data) if _limit_data != "0" else -1
                    save_status = edcfg.updateConfig(operationdata, OPERATION_CODE_FILE)
                    if save_status:
                        if self.predefined_report_instance is not None:
                            self.predefined_report_instance.wfoperationdata["limit result"] = int(varlimit.get().strip())
                        messagebox.showinfo("Success!!","Data has been saved successfully",parent=self.predefined_report_ui.change_limit_modal)
                        self.close_popup_window(self.predefined_report_ui.change_limit_modal)
                    else:
                        messagebox.showerror("Error!!","Error While saving the data",parent=self.predefined_report_ui.change_limit_modal)
                except:
                    logger.error("Below Exception occured: ", exc_info=True)

            label_frame = Frame(self.predefined_report_ui.change_limit_modal)
            label_frame.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
            button_frame = Frame(self.predefined_report_ui.change_limit_modal)
            button_frame.pack(fill="x",padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
            limit_label = ttk.Label(label_frame, text="Existing Limit")
            limit_label.grid(row=0, column=0,padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            limit_entry = ttk.Entry(label_frame, textvariable=varlimit)
            limit_entry.grid(row=0, column=1,padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            label_frame.grid_columnconfigure(1, weight=1)
            limit_info_label = ttk.Label(label_frame, text="(*Type 0 for Unlimited)")
            limit_info_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            label_frame.grid_rowconfigure(1, weight=1)
            save_btn = ttk.Button(button_frame, text="Save", command=save_data)
            save_btn.pack(expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def open_user_def_report(self):
        try:
            self.predefined_report_ui.create_ui = Toplevel(
                self.predefined_report_ui)
            self.predefined_report_ui.wm_attributes("-disabled", True)
            self.predefined_report_ui.create_ui.focus_set()
            self.predefined_report_ui.create_ui.title(
                APPLICATION_NAME + " - " + "Add/Edit Reports")
            self.predefined_report_ui.create_ui.geometry("+300+20") #450x605
            self.predefined_report_ui.create_ui.minsize(450, 605)
            self.predefined_report_ui.create_ui.maxsize(450, SCREEN_HEIGHT)
            self.predefined_report_ui.create_ui.resizable(width=False, height=True)
            # self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
            self.predefined_report_ui.create_ui.iconphoto(False, self.brandpic)
            self.predefined_report_ui.create_ui.transient(
                self.predefined_report_ui)
            self.predefined_report_ui.create_ui.protocol(
                "WM_DELETE_WINDOW", self.closepopupwindow)

            # String Var
            self.predefined_report_ui.varuserdefreport = StringVar()
            self.predefined_report_ui.varuserdefquerytype = StringVar()
            self.predefined_report_ui.varreportname = StringVar()
            self.predefined_report_ui.varneedvariable = IntVar()

            # Set Stringvar
            self.predefined_report_ui.varuserdefreport.set("--ADD NEW--")
            self.predefined_report_ui.varuserdefquerytype.set("--SELECT--")
            self.predefined_report_ui.varreportname.set("")
            self.predefined_report_ui.varneedvariable.set(0)

            self.predefined_report_ui.varuserdefquerytype.trace(
                "w", lambda *args: select_sample_query(self.predefined_report_ui.varuserdefquerytype))

            # Callback/Func
            def select_sample_query(varquerytype):
                try:
                    sample_query = "*Sample:Please Select type to view sample\n\n\n\n\n**************"
                    if varquerytype.get() == "Query Builder":
                        sample_query = "*Sample: This variable can be entered in the mainwindow\n\npath={pathvar}\ntype={typevar}\nproperty=cq:modifiedDate\nproperty.value={varmoddate}"
                    elif varquerytype.get() == "Bulk Editor":
                        sample_query = "*Sample: This variable can be entered in the mainwindow\n\npath:{pathvar}\ntype:{typevar}\n\"previewStatus\":'In Publish'\n"
                    
                    self.predefined_report_ui.query_label_sample.config(text=sample_query)
                except:
                    logger.error("Below Exception occured: ", exc_info=True)

            def add_user_def_report():
                try:
                    self.predefined_report_ui.query_type_cmbobox["state"] = "readonly"
                    self.predefined_report_ui.query_editor["state"] = "normal"
                    self.predefined_report_ui.query_name_ent["state"] = "normal"
                    report_name = self.predefined_report_ui.varuserdefreport.get()
                    self.predefined_report_ui.query_editor.delete("1.0", "end")

                    if report_name.lower() == "--add new--":
                        self.predefined_report_ui.varreportname.set("")
                        self.predefined_report_ui.varuserdefquerytype.set(
                            "--SELECT--")
                        self.predefined_report_ui.varneedvariable.set(0)
                    else:
                        data = self.user_def_report_json["query list"][self.predefined_report_ui.varuserdefreport.get(
                        ).strip()]
                        self.predefined_report_ui.varreportname.set(
                            data["name"])
                        self.predefined_report_ui.varuserdefquerytype.set(
                            data["type"].title())
                        if bool(data["variables"].strip()):
                            self.predefined_report_ui.varneedvariable.set(1)
                        else:
                            self.predefined_report_ui.varneedvariable.set(0)

                        if data["type"].strip() == "query builder":
                            # query_data = [x.strip() for x in data["query"].split("&") if x.strip() != ""]
                            for _query_x in data["query"].split("&"):
                                if _query_x.strip() != "":
                                    self.predefined_report_ui.query_editor.insert(
                                        "end", _query_x.strip()+"\n")

                        else:
                            # query_data = [x.strip() for x in data["query"].split(" ") if x.strip() != ""]
                            for _query_x in data["query"].split(" "):
                                if _query_x.strip() != "":
                                    self.predefined_report_ui.query_editor.insert(
                                        "end", _query_x.strip()+"\n")

                except:
                    logger.error("Below Exception occurred\n", exc_info=True)

            def remove_selected_report():
                try:
                    report_to_be_removed = self.predefined_report_ui.varuserdefreport.get()
                    if report_to_be_removed.lower() != "--add new--":
                        self.user_def_report_json["report_list"].remove(
                            report_to_be_removed)
                        poped_up_val = self.user_def_report_json["query list"].pop(
                            report_to_be_removed)
                        _saved_success = edcfg.updateConfig(
                            self.user_def_report_json, USER_DEF_FILE)
                        self.predefined_report_ui.query_editor.delete(
                            "1.0", "end")
                        self.predefined_report_ui.varuserdefquerytype.set(
                            "--SELECT--")
                        self.predefined_report_ui.varneedvariable.set(0)
                        self.predefined_report_ui.varuserdefreport.set(
                            "--ADD NEW--")
                        self.predefined_report_ui.varreportname.set("")
                        self.predefined_report_ui.query_type_cmbobox["state"] = "disabled"
                        self.predefined_report_ui.query_editor["state"] = "disabled"
                        self.predefined_report_ui.query_name_ent["state"] = "disabled"
                        _report_list = []
                        for _each_report in self.user_def_report_json.get("report_list", []):
                            if _each_report.startswith(self.user_def_report_json["prefix"]):
                                _report_list.append(_each_report)

                        _report_list.insert(0, "--ADD NEW--")
                        self.predefined_report_ui.report_cmbobox.config(
                            values=_report_list)
                        messagebox.showinfo(
                            "Success!!!", report_to_be_removed+" Removed Successfully.", parent=self.predefined_report_ui.create_ui)
                    else:
                        messagebox.showerror(
                            "Failed!!!", "Please Select a report.", parent=self.predefined_report_ui.create_ui)
                except:
                    logger.error("Below Exception occurred\n", exc_info=True)
                    messagebox.showerror(
                        "Failed!!!", "Please check the Logs.", parent=self.predefined_report_ui.create_ui)

            def save_user_report():
                try:
                    _query_type = self.predefined_report_ui.varuserdefquerytype.get().strip().lower()
                    _forbidden_path = [
                        x.strip() for x in INVALID_PATH_STRING.split(",") if x.strip() != ""]
                    textlistbylines = self.predefined_report_ui.query_editor.get(
                        "1.0", END).splitlines()
                    logger.debug("Query List: "+str(textlistbylines))
                    textlines_cleaned = []
                    [textlines_cleaned.append(x.strip()) for x in textlistbylines if x.strip(
                        ) != "" and x.strip() not in textlines_cleaned and x.strip().find("p.limit") < 0 and not(x.strip().startswith("limit"))]
                    logger.debug("After Cleaning: "+str(textlines_cleaned))
                    is_valid_query, query_error_list = GenericFunctions.validate_query(
                        textlines_cleaned, _query_type, _forbidden_path)

                    if is_valid_query:
                        run_query = True
                        if query_error_list.count("Content Root selected.") > 0:
                            run_query = messagebox.askyesnocancel("Please confirm to Run Query","Do you want to Run query on /content/pwc?", parent=self.predefined_report_ui.create_ui)
                        
                        if run_query:
                            # messagebox.showinfo("Working....","Pikabu", parent=self.predefined_report_ui.create_ui)
                            selected_report_name = self.predefined_report_ui.varuserdefreport.get()
                            saved_report_name = self.predefined_report_ui.varreportname.get().strip()
                            _report_name = saved_report_name if bool(
                                saved_report_name) else "Saved Report"
                            current_id = self.user_def_report_json["current"]
                            _updated_query = None
                            if _query_type == "bulk editor":
                                _updated_query = " ".join(textlines_cleaned)
                            elif _query_type == "query builder":
                                _updated_query = "&".join(textlines_cleaned)
                            logger.debug("Updated Query: %s" % _updated_query)
                            _variables_list = GenericFunctions.find_with_regex(
                                "\{\w+\}", _updated_query)
                            _cl_var_list = ",".join(_variables_list).replace(
                                "{", "").replace("}", "")

                            need_variable = self.predefined_report_ui.varneedvariable.get()
                            if not(need_variable) and bool(_variables_list):
                                messagebox.showerror("Please check the variable required checkbox",
                                                    "You have used variable but didn't checked\nthe varibale required checkbox.", parent=self.predefined_report_ui.create_ui)
                            else:

                                if selected_report_name.lower() == "--add new--":
                                    new_id = current_id + 1
                                    new_report_name = self.user_def_report_json["prefix"]+"-"+str(
                                        new_id) + "-" + _report_name
                                    self.user_def_report_json["report_list"].append(
                                        new_report_name)
                                    self.user_def_report_json["current"] = new_id

                                    new_report_prop = {}
                                    new_report_prop["id"] = new_id
                                    new_report_prop["name"] = _report_name
                                    new_report_prop["type"] = _query_type
                                    new_report_prop["query"] = _updated_query
                                    new_report_prop["variables"] = _cl_var_list

                                    self.user_def_report_json["query list"][new_report_name] = new_report_prop
                                else:
                                    new_report_name = self.user_def_report_json["prefix"]+"-"+str(
                                        current_id) + "-" + _report_name
                                    report_idx = self.user_def_report_json["report_list"].index(
                                        selected_report_name)
                                    self.user_def_report_json["query list"][selected_report_name]["name"] = _report_name
                                    self.user_def_report_json["query list"][selected_report_name]["type"] = _query_type
                                    self.user_def_report_json["query list"][selected_report_name]["query"] = _updated_query
                                    self.user_def_report_json["query list"][selected_report_name]["variables"] = _cl_var_list
                                    self.user_def_report_json["report_list"].remove(
                                        selected_report_name)
                                    self.user_def_report_json["report_list"].insert(
                                        report_idx, new_report_name)
                                    self.user_def_report_json["query list"][new_report_name] = self.user_def_report_json["query list"].pop(
                                        selected_report_name)

                                _config_saved = edcfg.updateConfig(
                                    self.user_def_report_json, USER_DEF_FILE)
                                if _config_saved:
                                    self.predefined_report_ui.query_editor.delete(
                                        "1.0", "end")
                                    self.predefined_report_ui.varuserdefquerytype.set(
                                        "--SELECT--")
                                    self.predefined_report_ui.varneedvariable.set(
                                        0)
                                    self.predefined_report_ui.varuserdefreport.set(
                                        "--ADD NEW--")
                                    self.predefined_report_ui.varreportname.set("")
                                    self.predefined_report_ui.query_type_cmbobox["state"] = "disabled"
                                    self.predefined_report_ui.query_editor["state"] = "disabled"
                                    self.predefined_report_ui.query_name_ent["state"] = "disabled"
                                    self.report_list_combobox.config(
                                        values=self.user_def_report_json["report_list"])
                                    messagebox.showinfo(
                                        "Success!!!", "Saved Successfully.", parent=self.predefined_report_ui.create_ui)
                                    self.closepopupwindow()
                                else:
                                    messagebox.showerror(
                                        "Failed!!!", "Failed to Save. Check Log", parent=self.predefined_report_ui.create_ui)

                    else:
                        messagebox.showerror(
                            "Invalid Query", "Below error occurred.\n"+"\n".join(query_error_list), parent=self.predefined_report_ui.create_ui)
                except:
                    logger.error("Below Exception occurred\n", exc_info=True)

            # End Callback

            report_list = []
            for each_report in self.user_def_report_json.get("report_list", []):
                if each_report.startswith(self.user_def_report_json["prefix"]):
                    report_list.append(each_report)

            report_list.insert(0, "--ADD NEW--")
            self.predefined_report_ui.main_frame = Frame(
                self.predefined_report_ui.create_ui)
            self.predefined_report_ui.main_frame.pack(fill="both")
            self.predefined_report_ui.select_frame = Frame(
                self.predefined_report_ui.main_frame)
            self.predefined_report_ui.select_frame.pack(
                fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            self.predefined_report_ui.report_cmbobox = ttk.Combobox(self.predefined_report_ui.select_frame,
                                                                    textvariable=self.predefined_report_ui.varuserdefreport, state="readonly", values=report_list)
            self.predefined_report_ui.report_cmbobox.pack(
                side="left",fill="x", ipadx=5, ipady=5, anchor="center")

            self.predefined_report_ui.edit_or_add_rpt_btn = ttk.Button(self.predefined_report_ui.select_frame,
                                                                       text="Add/Edit", command=add_user_def_report, style="smallBtn.TButton")
            self.predefined_report_ui.edit_or_add_rpt_btn.pack(
                side="left", padx=5, ipadx=2, ipady=5, anchor="center")
            self.predefined_report_ui.remove_selected = ttk.Button(self.predefined_report_ui.select_frame,
                                                              text="Remove Selected", command=remove_selected_report, style="smallBtn.TButton")
            self.predefined_report_ui.remove_selected.pack(
                side="left", padx=5, ipadx=5, ipady=5, anchor="center")

            self.predefined_report_ui.main_edit_frame = LabelFrame(
                self.predefined_report_ui.main_frame, text="Add or Edit reports")
            self.predefined_report_ui.main_edit_frame.pack(
                fill="both", expand="yes", padx=10, pady=5, ipadx=10, ipady=5, anchor="center")

            self.predefined_report_ui.query_name_frame = Frame(
                self.predefined_report_ui.main_edit_frame)
            self.predefined_report_ui.query_name_frame.pack(fill="x", pady=5)
            self.predefined_report_ui.query_name_label = ttk.Label(
                self.predefined_report_ui.query_name_frame, text="Report Name")
            self.predefined_report_ui.query_name_label.pack(
                side="left", fill="x", expand="yes", anchor="w", padx=5)
            self.predefined_report_ui.query_name_ent = ttk.Entry(
                self.predefined_report_ui.query_name_frame, state="disabled", textvariable=self.predefined_report_ui.varreportname)
            self.predefined_report_ui.query_name_ent.pack(
                side="left", fill="x", expand="yes", anchor="w", padx=5)

            self.predefined_report_ui.query_type_frame = Frame(
                self.predefined_report_ui.main_edit_frame)
            self.predefined_report_ui.query_type_frame.pack(fill="x", pady=5)
            self.predefined_report_ui.query_label = ttk.Label(
                self.predefined_report_ui.query_type_frame, text="Query Selector")
            self.predefined_report_ui.query_label.pack(
                side="left", fill="x", expand="yes", anchor="w", padx=5)
            self.predefined_report_ui.query_type_cmbobox = ttk.Combobox(self.predefined_report_ui.query_type_frame,
                                                                        textvariable=self.predefined_report_ui.varuserdefquerytype, state="disabled", values=["--SELECT--", "Bulk Editor", "Query Builder"])
            self.predefined_report_ui.query_type_cmbobox.pack(
                side="left", fill="x", expand="yes", padx=5)  # , padx=5, ipadx=5, ipady=5, anchor="center"

            self.predefined_report_ui.variable_checkbox = ttk.Checkbutton(
                self.predefined_report_ui.main_edit_frame, variable=self.predefined_report_ui.varneedvariable, onvalue=1, offvalue=0, text="Contains Variable data? Put the variable inside '{}'")
            self.predefined_report_ui.variable_checkbox.pack(fill="x", pady=5)
            
            sample_query = "*Sample:Please Select type to view sample\n\n\n\n\n**************"
            self.predefined_report_ui.query_label_sample = ttk.Label(
                self.predefined_report_ui.main_edit_frame, text=sample_query)
            self.predefined_report_ui.query_label_sample.pack(fill="x", anchor="w")

            self.predefined_report_ui.query_label = ttk.Label(
                self.predefined_report_ui.main_edit_frame, text="Query Window")
            self.predefined_report_ui.query_label.pack(
                fill="x", pady=5, anchor="center")

            self.predefined_report_ui.query_editor_frame = Frame(
                self.predefined_report_ui.main_edit_frame)
            self.predefined_report_ui.query_editor_frame.pack(fill="both")
            self.predefined_report_ui.query_editor = Text(
                self.predefined_report_ui.query_editor_frame, undo=True, height=15, state="disabled")
            self.predefined_report_ui.query_editor_scroll_y = ttk.Scrollbar(
                self.predefined_report_ui.query_editor_frame, orient="vertical", command=self.predefined_report_ui.query_editor.yview)
            self.predefined_report_ui.query_editor['yscrollcommand'] = self.predefined_report_ui.query_editor_scroll_y.set
            self.predefined_report_ui.query_editor_scroll_y.pack(
                side="right", fill="y")
            self.predefined_report_ui.query_editor.pack(fill="both")

            self.predefined_report_ui.main_btn_frame = Frame(
                self.predefined_report_ui.main_frame)
            self.predefined_report_ui.main_btn_frame.pack(
                fill="x", expand="yes", padx=10, pady=5, ipadx=10, ipady=5, anchor="center")

            self.predefined_report_ui.submit_btn = ttk.Button(self.predefined_report_ui.main_btn_frame,
                                                              text="Save", command=save_user_report, style="smallBtn.TButton")
            self.predefined_report_ui.submit_btn.pack(
                side="left", expand="yes")

            self.predefined_report_ui.exit_btn = ttk.Button(self.predefined_report_ui.main_btn_frame,
                                                              text="Exit", command=self.closepopupwindow, style="smallBtn.TButton")
            self.predefined_report_ui.exit_btn.pack(
                side="left", expand="yes")

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def ipchange(self, value):
        try:
            if value.lower() == "ip":
                self.environment_ip_ent["state"] = "normal"
                self.varuserent.set("")
                self.varpassent.set("")

            else:
                self.varipdata.set("")
                self.environment_ip_ent["state"] = "disabled"
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

    def report_name_change(self, value):
        try:
            # "Contactus Arch Form Report",
            #  "Contactus Form Report", "Online Archive Form Report", "Online Form Report"
            _territory = self.varterritoryname.get()
            if value == "--SELECT--":
                self.user_def_var_label.grid_forget()
                self.user_def_sep_var_label.grid_forget()
                self.user_def_var_popup.config(
                    command=lambda *args: print("Popup"))
                self.user_def_var_popup.grid_forget()

                self.territory_label_frame.grid(
                    row=0, column=1, columnspan=2, padx=5, pady=0, sticky="nsew")
                self.year_combobox.grid(
                    row=1, column=0, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")
                self.month_combobox.grid(
                    row=1, column=1, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")
                self.day_combobox.grid(
                    row=1, column=2, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")
                self.territory_list_combobox["state"] = "disabled"
                self.year_combobox["state"] = "disabled"
                self.month_combobox["state"] = "disabled"
                self.day_combobox["state"] = "disabled"
                self.varyear.set("--YEAR--")
                self.varterritoryname.set("--SELECT--")
                self.territory_name_ent["state"] = "disabled"
            else:
                if value.lower() == "contact fragment reference":
                    self.varpropertyname.set("pagereference, cq:lastReplicationAction, cq:lastReplicatedBy, cq:lastReplicated")
                    self.property_btn["state"] = "disabled"
                    self.type_of_property_writer_ent["state"]  = "disabled"
                else:
                    self.varpropertyname.set("")
                    self.property_btn["state"] = "normal"
                    self.type_of_property_writer_ent["state"]  = "normal"
                self.varterritoryname.set("--SELECT--")
                self.territory_list_combobox["state"] = "readonly"

                if(value.find(self.user_def_report_json["prefix"]) > -1):
                    if not(bool(self.user_def_report_json["query list"][value]["variables"])):
                        self.user_def_var_popup["state"] = "disabled"
                    else:
                        self.user_def_var_popup["state"] = "normal"
                    self.user_def_var_popup.config(
                        command=lambda *args: self.open_variable_entry_popup(value))
                    self.territory_label_frame.grid_forget()
                    self.year_combobox.grid_forget()
                    self.month_combobox.grid_forget()
                    self.day_combobox.grid_forget()
                    self.user_def_var_label.grid(
                        row=1, column=0, columnspan=3, padx=5, pady=2, ipadx=3, ipady=5, sticky="nsew")
                    self.user_def_var_label.config(
                        text="Variables Present in Query: "+self.user_def_report_json["query list"][value]["variables"])
                    # self.user_def_var_v_label.grid(row=1, column=0, padx=5, pady=2, ipadx=2, ipady=5, sticky="nsew")
                    # self.user_def_var_ent.grid(row=1, column=1, columnspan=2, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")
                    self.user_def_sep_var_label.grid(
                        row=0, column=1, padx=5, pady=2, ipadx=2, sticky="nsew")
                    self.user_def_var_popup.grid(
                        row=0, column=2, padx=5, pady=2, ipadx=2, sticky="nsew")
                    self.report_frame.grid_columnconfigure(1, weight=1)
                else:
                    self.user_def_var_label.grid_forget()
                    self.user_def_sep_var_label.grid_forget()
                    self.user_def_var_popup.config(
                        command=lambda *args: print("Popup"))
                    # self.user_def_var_v_label.grid_forget()
                    # self.user_def_var_ent.grid_forget()
                    self.user_def_var_popup.grid_forget()
                    self.territory_label_frame.grid(
                        row=0, column=1, columnspan=2, padx=5, pady=0, sticky="nsew")
                    self.year_combobox.grid(
                        row=1, column=0, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")
                    self.month_combobox.grid(
                        row=1, column=1, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")
                    self.day_combobox.grid(
                        row=1, column=2, padx=5, pady=2, ipadx=5, ipady=5, sticky="nsew")

                    if value.lower().find("form report") > -1 or value.lower().find("form field order") > -1:
                        self.year_combobox.config(values=self.year_value)
                        self.varyear.set("--YEAR--")
                        self.year_combobox["state"] = "readonly"
                        self.month_combobox["state"] = "readonly"
                        self.day_combobox["state"] = "readonly"
                        if value.lower() == "online archive form report" or value.lower() == "online form report":
                            self.territory_list_combobox["state"] = "disabled"
                    elif value.lower().find("dam assets report") > -1:
                        self.month_combobox["state"] = "disabled"
                        self.day_combobox["state"] = "disabled"
                        self.year_combobox["state"] = "readonly"
                        self.year_combobox.config(
                            values=["--SELECT TYPE--", "Video", "PDF", "Image"])
                        self.varyear.set("--SELECT TYPE--")
                    elif value.lower().find("component usage report") > -1:
                        self.month_combobox["state"] = "disabled"
                        self.day_combobox["state"] = "disabled"
                        self.year_combobox["state"] = "readonly"
                        resource_type = list(self.predefined_report_ui.resource_type_data.keys())
                        resource_type.insert(0,"isection-xf-header")
                        resource_type.insert(0,"isection-xf-footer")
                        resource_type.insert(0,"isection-xf-contact-us")
                        resource_type.insert(0,"isection-xf-follow-us")
                        resource_type.insert(0,"isection-xf-bottom-kick")
                        resource_type.insert(0,"--SELECT TYPE--")
                        self.year_combobox.config(
                            values=resource_type)
                        self.varyear.set("--SELECT TYPE--")
                    else:
                        self.year_combobox.config(values=self.year_value)
                        self.varyear.set("--YEAR--")
                        self.year_combobox["state"] = "disabled"
                        self.month_combobox["state"] = "disabled"
                        self.day_combobox["state"] = "disabled"

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def territory_change(self, value):
        try:
            _report_selected = self.varreportname.get().strip().lower()
            if (value.lower() == "--select--" or value.lower() == "multi") and _report_selected != "--select--":
                self.territory_name_ent["state"] = "normal"
            else:
                self.territory_name_ent["state"] = "disabled"
                self.varterritorynameent.set("")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def closethiswindow(self, top_windown, child_window):
        try:
            top_windown.focus_set()
            top_windown.wm_attributes("-disabled", False)
            child_window.destroy()
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def open_variable_entry_popup(self, s_report):
        try:
            self.variable_addition_popup_window = Toplevel(
                self.predefined_report_ui)
            self.predefined_report_ui.wm_attributes("-disabled", True)
            self.variable_addition_popup_window.focus_set()
            self.variable_addition_popup_window.title(
                APPLICATION_NAME + " - " + "Select Property")
            self.variable_addition_popup_window.geometry("420x500+10+20")
            self.variable_addition_popup_window.iconphoto(False, self.brandpic)
            self.variable_addition_popup_window.resizable(False, False)
            self.variable_addition_popup_window.transient(
                self.predefined_report_ui)
            self.variable_addition_popup_window.protocol("WM_DELETE_WINDOW", lambda *args: self.closethiswindow(
                self.predefined_report_ui, self.variable_addition_popup_window))

            # Functions/Callback
            def save_submit(_abd):
                try:
                    _can_be_exit = False
                    incrementar = 0
                    self.predefined_report_ui.user_variable_entered_data = {}
                    _error_list = []
                    for _io in _abd:
                        for _key_val in _io:
                            _entered_val = _io[_key_val].get()
                            logger.debug("Entered Value for Key %s is: %s" % (
                                _key_val, _entered_val))
                            if not(bool(_entered_val.strip())):
                                _error_list.append(str(_key_val)+" is Empty")
                                logger.error(str(_key_val)+" is Empty")
                            else:
                                logger.debug("Entered value has been saved!!")
                                self.predefined_report_ui.user_variable_entered_data[
                                    _key_val] = _entered_val
                                incrementar += 1

                    if incrementar == len(_abd):
                        logger.debug(
                            self.predefined_report_ui.user_variable_entered_data)
                        self.closethiswindow(
                            self.predefined_report_ui, self.variable_addition_popup_window)
                    else:
                        logger.error(_error_list)
                        messagebox.showerror("Error occurred!!", ".\n".join(
                            _error_list), parent=self.variable_addition_popup_window)
                except:
                    logger.error("Below Exception occured: ", exc_info=True)

            _distorted_query = self.user_def_report_json["query list"][s_report]["query"].replace(
                "&", "\n")
            self.variable_addition_popup_window.query_frame = Frame(
                self.variable_addition_popup_window)
            self.variable_addition_popup_window.query_frame.pack(fill="x")
            self.variable_addition_popup_window.variable_frame = Frame(
                self.variable_addition_popup_window)
            self.variable_addition_popup_window.variable_frame.pack(
                fill="both")
            self.variable_addition_popup_window.btn_frame = Frame(
                self.variable_addition_popup_window)
            self.variable_addition_popup_window.btn_frame.pack(
                fill="x", pady=10)
            self.variable_addition_popup_window.query_win_label = ttk.Label(
                self.variable_addition_popup_window.query_frame, text="Your Saved Query", anchor="c")
            self.variable_addition_popup_window.query_win_label.pack(
                fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
            self.variable_addition_popup_window.query_win = ttk.Label(
                self.variable_addition_popup_window.query_frame, text=_distorted_query)
            self.variable_addition_popup_window.query_win.pack(
                fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="w")

            # Create Scrollable window
            _canvas_win = Canvas(
                self.variable_addition_popup_window.variable_frame)
            self.variable_addition_popup_window.variable_main_frame = Frame(
                _canvas_win)

            scroll_x_canv = Scrollbar(
                self.variable_addition_popup_window.variable_frame, orient="vertical", command=_canvas_win.yview)
            _canvas_win.configure(yscrollcommand=scroll_x_canv.set)
            scroll_x_canv.pack(side="right", fill="y")
            _canvas_win.pack(side="left", fill="both")
            _canvas_win.create_window(
                (0, 0), window=self.variable_addition_popup_window.variable_main_frame, anchor="nw")
            self.variable_addition_popup_window.variable_main_frame.bind(
                "<Configure>", lambda *args: _canvas_win.configure(scrollregion=_canvas_win.bbox("all")))
            # self.predefined_report_ui.user_variable_entered_data = []
            _all_box_data = []
            for _each_var in self.user_def_report_json["query list"][s_report]["variables"].split(","):
                ch = {}
                _frame_in_region = Frame(
                    self.variable_addition_popup_window.variable_main_frame)
                _frame_in_region.pack()
                _var_label_name = ttk.Label(
                    _frame_in_region, text=_each_var.strip(), anchor="e")
                _var_entry_box = ttk.Entry(_frame_in_region)
                ch[_each_var.strip()] = _var_entry_box
                # self.predefined_report_ui.user_variable_entered_data.append(ch)
                _all_box_data.append(ch)
                _var_label_name.pack(
                    side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="e")
                _var_entry_box.pack(
                    side="left", fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="w")

            # End
            self.variable_addition_popup_window.submit_btn = ttk.Button(
                self.variable_addition_popup_window.btn_frame, text="Submit", command=lambda *args: save_submit(_all_box_data))
            self.variable_addition_popup_window.submit_btn.pack(
                side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
            self.variable_addition_popup_window.exit_btn = ttk.Button(self.variable_addition_popup_window.btn_frame, text="Exit",
                                                                      command=lambda *args: self.closethiswindow(self.predefined_report_ui, self.variable_addition_popup_window))
            self.variable_addition_popup_window.exit_btn.pack(
                side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
        except:
            logger.error("Below Exception occured: ", exc_info=True)

    def open_property_addition(self):
        try:
            self.add_property_win = Toplevel(self.predefined_report_ui)
            self.predefined_report_ui.wm_attributes("-disabled", True)
            self.add_property_win.focus_set()
            self.add_property_win.title(
                APPLICATION_NAME + " - " + "Select Property")
            self.add_property_win.geometry("520x640+10+20")
            self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
            self.add_property_win.iconphoto(False, self.brandpic)
            self.add_property_win.resizable(False, False)
            self.add_property_win.transient(self.predefined_report_ui)
            self.add_property_win.protocol("WM_DELETE_WINDOW", lambda *args: self.closethiswindow(
                self.predefined_report_ui, self.add_property_win))
            # self.style = ttk.Style()
            self.config_data = configdata
            property_path = os.path.join(
                BASE_SCRIPT_PATH, "configfiles", "property_list.json")
            self.property_data = edcfg.readConfig(property_path)
            self.all_parent = []

            self.add_property_win.btn_frame = Frame(self.add_property_win)
            self.add_property_win.btn_frame.pack(padx=5, pady=5)

            self.add_property_win.btn_ok = ttk.Button(
                self.add_property_win.btn_frame, text="Select >>", command=self.select_props)
            self.add_property_win.btn_ok.pack(padx=5, pady=5, side="left")

            self.add_property_win.property_tree_frame = Frame(
                self.add_property_win)
            self.add_property_win.property_tree_frame.pack(padx=5, pady=5)

            self.add_property_win.property_tree = ttk.Treeview(
                self.add_property_win.property_tree_frame, columns=("Name", "Props"), height=20)

            self.add_property_win.property_tree.column(
                "#0", width=50, stretch="yes", anchor="c")
            self.add_property_win.property_tree.column(
                "#1", width=220, stretch="yes", anchor="c")
            self.add_property_win.property_tree.column(
                "#2", width=220, stretch="yes", anchor="c")

            self.add_property_win.property_tree.heading("#0", text="#")
            self.add_property_win.property_tree.heading("#1", text="Name")
            self.add_property_win.property_tree.heading("#2", text="Property")

            self.add_property_win.data_tree_scroll_y = ttk.Scrollbar(
                self.add_property_win.property_tree_frame, orient="vertical", command=self.add_property_win.property_tree.yview)
            self.add_property_win.property_tree.config(
                yscrollcommand=self.add_property_win.data_tree_scroll_y.set)
            self.add_property_win.data_tree_scroll_y.pack(
                side="right", fill="y")

            self.add_property_win.property_tree.pack(
                padx=5, pady=5, anchor="c", fill="both")

            self.add_property_data_in_table(self.property_data)

            self.add_property_win.property_tree.bind(
                "<ButtonRelease-1>", self.remove_parent_selection)
            self.add_property_win.property_tree.bind(
                "<MouseWheel>", lambda event, arg1=self.add_property_win.property_tree: GenericFunctions.on_mouse_wheel(arg1, event))

            # self.configmaindesign()
        # self.configwin.attributes('-topmost', 'true')
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def remove_parent_selection(self, evnt):
        try:
            if self.add_property_win.property_tree.focus():
                z = self.add_property_win.property_tree.identify_row(evnt.y)
                if z in self.all_parent:
                    self.add_property_win.property_tree.selection_remove(z)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def select_prop_based_on_type(self, type_, prop_):
        try:
            final_prop_ = prop_
            logger.debug("Type: %s", type_)
            if str(type_).lower() == "contact profile page":
                final_prop_ = "contact-profile-par/contact/" + str(final_prop_)

            logger.debug("Final Prop: %s", final_prop_)
            return final_prop_
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def select_props(self):
        try:
            _selected_rows = self.add_property_win.property_tree.selection()
            logger.debug("Selected Props rows: "+str(_selected_rows))
            _selected_props = []
            for each_row in _selected_rows:
                _parent = self.add_property_win.property_tree.parent(each_row)
                _parent_type = self.add_property_win.property_tree.item(_parent)[
                    "values"][0]
                _prop_name = self.add_property_win.property_tree.item(each_row)[
                    "values"][1]
                _final_prop = self.select_prop_based_on_type(_parent_type, _prop_name)
                _selected_props.append(_final_prop)

            logger.debug("Selected Props: "+str(_selected_props))

            final_prop_in_str = ", ".join(_selected_props)
            old_prop = self.varpropertyname.get()
            prop_output = f"{old_prop}, {final_prop_in_str}" if bool(old_prop) else final_prop_in_str
            self.varpropertyname.set(prop_output)
            self.closethiswindow(self.predefined_report_ui,
                                 self.add_property_win)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            self.varpropertyname.set("Exception Occurred")
            self.closethiswindow(self.predefined_report_ui,
                                 self.add_property_win)

    def validate_input(self, uname, passwd, ip_or_url, environment, selected_rep, terr_or_path, props):
        try:
            is_validated = False

            is_not_empty_uname = bool(uname)
            is_not_empty_passwd = bool(passwd)
            is_not_empty_ip_or_url = bool(ip_or_url)
            is_not_empty_environment = bool(environment)
            is_not_empty_selected_rep = bool(selected_rep)
            is_not_empty_terr_or_path = bool(terr_or_path)
            is_not_empty_props = bool(props)

            is_valid_ip_or_url = GenericFunctions.validateIP(
                ip_or_url, environment)
            # is_terr_or_path_starts_with_invalid =
            is_report_selected = True if selected_rep.lower() != "--select--" else False
            # is_report_selected = True if selected_rep.lower() != "--select--" else False

            logger.debug("Is Not Empty Username: %s, Is Not Empty Password: %s, Is Not Empty IP or URL: %s, \
                    Is Not Empty Environment: %s, Is Not Empty Report: %s, Is Not Empty Terr or Path: %s, \
                        Is Not Empty Property: %s, Is Valid IP or URL: %s, Is Selected Report is Valid: %s, "
                         % (is_not_empty_uname, is_not_empty_passwd, is_not_empty_ip_or_url, is_not_empty_environment,
                            is_not_empty_selected_rep, is_not_empty_terr_or_path, is_not_empty_props, is_valid_ip_or_url, is_report_selected))

            error_list = []

            if (is_not_empty_environment and is_not_empty_ip_or_url and is_not_empty_passwd
                and is_not_empty_props and is_not_empty_selected_rep and is_not_empty_terr_or_path
                    and is_not_empty_uname and is_valid_ip_or_url and is_report_selected):

                is_validated = True
            else:
                if not(is_not_empty_environment):
                    error_list.append("\nPlease Select a Environment")
                if not(is_not_empty_ip_or_url):
                    error_list.append("\nPlease Enter the IP/URL")
                if not(is_not_empty_passwd):
                    error_list.append("\nPlease enter a Password")
                if not(is_not_empty_props):
                    error_list.append("\nPlease Enter/Select the Props")
                if not(is_not_empty_selected_rep):
                    error_list.append("\nPlease Select a Report")
                if not(is_not_empty_terr_or_path):
                    error_list.append("\nPlease Select/Enter a Territory")
                if not(is_not_empty_uname):
                    error_list.append("\nPlease Enter a Username")
                if not(is_valid_ip_or_url):
                    error_list.append("\nPlease Enter a valid IP/URL")
                if not(is_report_selected):
                    error_list.append("\nPlease Select a Report")
                if bool(error_list):
                    error_msg = ".".join(error_list)
                    logger.error("Error message: \n %s" % error_msg)
                    messagebox.showerror(
                        "Below Error has been Occurred", error_msg, parent=self.predefined_report_ui)

            logger.debug(
                "All Data Validation Consolidated Report: %s" % is_validated)
            return is_validated

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def check_mandatory_field(self, report_name, v_year):
        try:
            is_present_mandatory_field = True

            if report_name.lower().find("form report") > -1:
                if v_year.lower() == "--year--":
                    is_present_mandatory_field = False
                    messagebox.showerror(
                        "Error Occurred", "Year value is Mandatory\nFor Forms report.", parent=self.predefined_report_ui)
            elif report_name.lower().find("asset report") > -1:
                if v_year.lower() == "--select type--":
                    is_present_mandatory_field = False
                    messagebox.showerror(
                        "Error Occurred", "Select the proper\nasset type for report.", parent=self.predefined_report_ui)

            return is_present_mandatory_field
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def retreive_data(self):
        try:
            self.results_label.config(text="")
            self.total_label.config(text="")
            self.predefined_report_ui.fetched_data = None
            report_ran_by_user = False

            _user_name = self.varuserent.get().strip()
            _password = self.varpassent.get()
            _selected_env = self.varenvdata.get().lower()
            _environment_url = self.varipdata.get().strip() if _selected_env == "ip" \
                else self.predefined_report_ui.configdata[_selected_env]

            _selected_report = self.varreportname.get()
            _is_user_def_report_selected = True if _selected_report.startswith(
                self.user_def_report_json["prefix"]) else False
            _is_form_field_order_data_selected = True if (_selected_report.lower() == "Processed Form Field Order data".lower() or _selected_report.lower() == "In-Progress Form Field Order data".lower()) else False
            _is_multi_selected = True if self.varterritoryname.get().upper() == "MULTI" else False
            # _var_territory_name = str(self.varterritorynameent.get()).strip()
            _territory_or_path = (GenericFunctions.get_key_of_val(self.all_territory_mappings, self.varterritoryname.get().lower()) if  self.varterritoryname.get().upper() != "MULTI" else self.varterritorynameent.get()) \
                if self.varterritoryname.get().upper() != "--SELECT--" else self.varterritorynameent.get().replace("/content/pwc/", "").replace("/content/dam/pwc/", "")

            _territory_or_path = "User-Def" if _is_user_def_report_selected else _territory_or_path
            # _territory_or_path = GenericFunctions.removeleadingspecialchar(
            #     _territory_or_path)
            _territory_or_path = GenericFunctions.removetrailingspecialchar(
                _territory_or_path)
            _property_string = self.property_name_ent.get().strip()
            _selected_property = [
                x.strip() for x in _property_string.split(",") if x.strip() != ""]

            logger.debug("Username: %s, Environment or IP: %s, Selected Report: %s, Territory or Path: %s, Selected Props: %s" % (
                _user_name, _environment_url, _selected_report, _territory_or_path, _selected_property))

            #uname, passwd,ip_or_url, environment, selected_rep, terr_or_path, props
            is_validated_data = self.validate_input(
                _user_name, _password, _environment_url, _selected_env, _selected_report, _territory_or_path, _selected_property)

            logger.debug("Validated Data %s" % is_validated_data)
            if is_validated_data:
                continue_operation = True
                if _selected_env == "production":
                    continue_operation = messagebox.askyesnocancel(
                        "Please confirm", "Do you want to Run\nthe Operation in Production?", parent=self.predefined_report_ui)

                if continue_operation:
                    self.predefined_report_instance = PreDefinedReports(
                        _environment_url, _user_name, _password)
                    if not(_is_multi_selected):
                        if _is_user_def_report_selected:
                            report_ran_by_user = self.get_user_def_report(_selected_report, _selected_property)
                            # result_info = self.predefined_report_ui.fetched_data.copy()
                            result_info = self.predefined_report_ui.fetched_data.pop(0) if self.predefined_report_ui.fetched_data is not None and isinstance(self.predefined_report_ui.fetched_data, (list, tuple)) else []

                        else:
                            report_ran_by_user, result_info = self.run_report_for_selected(_is_form_field_order_data_selected, _selected_report, _territory_or_path, _selected_env, _selected_property, _property_string)
                        
                        if self.predefined_report_ui.fetched_data is not None:# and _is_form_field_order_data_selected:
                            self.toggleInputField("disabled")
                            self.prepare_output_data(_property_string, True, _territory_or_path, result_info)

                            if isinstance(self.predefined_report_ui.fetched_data, str):
                                self.results_label.config(
                                    text=self.predefined_report_ui.fetched_data, foreground="red")
                                if self.predefined_report_ui.fetched_data == "Wrong Username and Password - Http Code - 401":
                                    self.username_ent["state"] = "normal"
                                    self.passwd_ent["state"] = "normal"
                                    self.fetch_data["state"] = "normal"
                                    self.export_btn["state"] = "disabled"
                        elif self.predefined_report_ui.fetched_data is None and report_ran_by_user:
                            self.total_label.config(
                                    text="No Data has been retrieve.", foreground="red")

                    elif _is_multi_selected:
                        _selected_territories_with_duplicates = [ter.lower().strip() for ter in _territory_or_path.split(",") if len(ter.strip()) == 2 ]
                        logger.debug("Selected Territories: %s", str(_selected_territories_with_duplicates))
                        _selected_territories = list(set(_selected_territories_with_duplicates))
                        self.toggleInputField("disabled")
                        columns_to_be_created = True
                        run_into_issues = False

                        for terr in _selected_territories:
                            report_ran_by_user, result_info = self.run_report_for_selected(_is_form_field_order_data_selected, _selected_report, terr, _selected_env, _selected_property, _property_string)
                            if _is_form_field_order_data_selected:
                                _property_string = _property_string + ", PwCFormFieldOrder, PwCFormFieldOrderData"

                            if self.predefined_report_ui.fetched_data is not None: #and not(_is_form_field_order_data_selected):
                                self.prepare_output_data(_property_string, columns_to_be_created, terr, result_info)
                                columns_to_be_created = False

                                if isinstance(self.predefined_report_ui.fetched_data, str):
                                    run_into_issues = True
                                    self.results_label.config(
                                        text=self.predefined_report_ui.fetched_data, foreground="red")
                                    if self.predefined_report_ui.fetched_data == "Wrong Username and Password - Http Code - 401":
                                        self.username_ent["state"] = "normal"
                                        self.passwd_ent["state"] = "normal"
                                        self.fetch_data["state"] = "normal"
                                        self.export_btn["state"] = "disabled"
                                    break
                            elif self.predefined_report_ui.fetched_data is None and report_ran_by_user:
                                self.total_label.config(
                                        text="No Data has been retrieve.", foreground="red")
                                run_into_issues = True

                        if not(run_into_issues):
                            messagebox.showinfo("Success","Data has been successfully fetched", parent=self.predefined_report_ui)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def run_report_for_selected(self, form_field_selected, _selected_report, _territory_or_path, _selected_env, _selected_property, _property_string):
        try:
            report_ran_by_user = False
            if form_field_selected:
                # self.predefined_report_ui.fetched_data = None
                _fetched_data = None
                if _selected_report == "Processed Form Field Order data":
                    _fetched_data = self.predefined_report_instance.pwc_form_field_order_data_v2("Online Arch", _selected_property, _territory_or_path, self.varyear.get(), self.varmonth.get(), self.vardate.get())
                    # self.predefined_report_ui.fetched_data = self.predefined_report_instance.pwc_form_field_order_data_v2("Online Arch", _selected_property, _territory_or_path, self.varyear.get(), self.varmonth.get(), self.vardate.get())
                elif _selected_report == "In-Progress Form Field Order data":
                    _fetched_data = self.predefined_report_instance.pwc_form_field_order_data_v2("Online", _selected_property, _territory_or_path, self.varyear.get(), self.varmonth.get(), self.vardate.get())
                    # self.predefined_report_ui.fetched_data = self.predefined_report_instance.pwc_form_field_order_data_v2("Online", _selected_property, _territory_or_path, self.varyear.get(), self.varmonth.get(), self.vardate.get())

            else:
                is_mandatory_avl = self.check_mandatory_field(
                    _selected_report, self.varyear.get())
                if is_mandatory_avl:
                    _dam_asset_type = self.varyear.get() if _selected_report.lower().find(
                        "dam assets report") > -1 or _selected_report.lower().find(
                        "component usage report") > -1 else ""
                    
                    dam_asset_type = self.predefined_report_ui.resource_type_data.get(_dam_asset_type, _dam_asset_type) if _selected_report.lower().find("component usage report") > -1 else _dam_asset_type.lower()
                    logger.debug("Type of Selected: %s", dam_asset_type)

                    _fetched_data = self.predefined_report_instance.report_selector(report_name=_selected_report, environment= _selected_env,
                                                                                                            territory=_territory_or_path, props=_selected_property, year=self.varyear.get(), month=self.varmonth.get(),
                                                                                                            day=self.vardate.get(), type_of_dam=dam_asset_type)
            
            result_info = []
            result_info = _fetched_data.pop(0) if _fetched_data is not None and isinstance(_fetched_data, (list, tuple)) else []
            logger.debug("Result Info %s,Report Ran by user, %s",result_info, _fetched_data)
            if isinstance(self.predefined_report_ui.fetched_data, (list, tuple)) and type(self.predefined_report_ui.fetched_data)==type(_fetched_data):
                self.predefined_report_ui.fetched_data += _fetched_data
            elif self.predefined_report_ui.fetched_data is None and isinstance(_fetched_data, (list,tuple,dict)):
                if bool(_fetched_data):
                    self.predefined_report_ui.fetched_data = _fetched_data.copy()
            else:
                self.predefined_report_ui.fetched_data = _fetched_data

            report_ran_by_user = True
            
            return report_ran_by_user, result_info
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False
    
    def get_user_def_report(self, _selected_report, _selected_property):
        try:
            report_ran_by_user = False
            _is_var_present = bool(
                    self.user_def_report_json["query list"][_selected_report]["variables"].strip())
            if self.predefined_report_ui.user_variable_entered_data is None and _is_var_present:
                messagebox.showerror(
                    "Error Occurred!!", "Please Enter Variables value", parent=self.predefined_report_ui)
                logger.error("Please Enter Variables value")
            else:
                logger.debug("Generating Query!!")
                logger.debug("Variables Value Entered: %s" %
                                self.predefined_report_ui.user_variable_entered_data)
                _list_of_vars = [x.strip() for x in self.user_def_report_json["query list"]
                                    [_selected_report]["variables"].split(",") if x.strip() != ""]
                _stored_query = self.user_def_report_json["query list"][_selected_report]["query"]
                _stored_query_type = self.user_def_report_json[
                    "query list"][_selected_report]["type"]
                _generated_query = ""
                logger.debug("List of Vars: %s, Stored Query: %s, Stored Querytype: %s" % (
                    _list_of_vars, _stored_query, _stored_query_type))
                _generated_query = _stored_query
                if self.predefined_report_ui.user_variable_entered_data is not None:
                    for _each_stored_var in _list_of_vars:
                        _generated_query = _generated_query.replace(
                            "{"+_each_stored_var+"}", self.predefined_report_ui.user_variable_entered_data[_each_stored_var])

                logger.debug("Generated Query: %s" %
                                _generated_query)
                _splitted_gen_query = _generated_query.split("&") if _stored_query_type.lower(
                    ) == "query builder" else _generated_query.split(" ")
                logger.debug("Splitted Query: " +str(_splitted_gen_query))
                _forbidden_path = [
                    x.strip() for x in INVALID_PATH_STRING.split(",") if x.strip() != ""]
                _is_valid_stored_query, query_error_list = GenericFunctions.validate_query(
                            _splitted_gen_query, _stored_query_type, _forbidden_path)
                if _is_valid_stored_query:
                    run_the_report = True
                    if query_error_list.count("Content Root selected.") > 0:
                        run_the_report = messagebox.askyesnocancel("Please confirm to Run Query","Do you want to Run query on /content/pwc?", parent=self.predefined_report_ui.create_ui)
                    if run_the_report:
                        report_ran_by_user = True
                        self.predefined_report_ui.fetched_data = self.predefined_report_instance.report_selector(report_name=_selected_report,
                                                                                                                query=_generated_query, query_type=_stored_query_type.lower(), props=_selected_property)
                else:
                    messagebox.showerror(
                        "Invalid Query selected!!", "Below error occurred.\n"+"\n".join(query_error_list), parent=self.predefined_report_ui)
            return report_ran_by_user
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def prepare_output_data(self, _property_string, _create_table_column, territory, result_info):
        try:
            # if self.predefined_report_ui.fetched_data is not None and not(form_field_selected):
            if isinstance(self.predefined_report_ui.fetched_data, list):
                if _create_table_column:
                    self.create_table_column(_property_string)
                
                if bool(result_info) and isinstance(result_info, list) and len(result_info) == 2:
                    _total_records = result_info[0] if (
                             result_info[0] > 0 and result_info[1] == 0) else result_info[1]
                    _result = result_info[0]
                    self.predefined_report_ui.fetched_data_count += _result
                    self.predefined_report_ui.total_data_count += _total_records
                    self.results_label.config(
                            text="Result: "+str(self.predefined_report_ui.fetched_data_count), foreground="green")
                    self.total_label.config(
                            text="Total: "+str(self.predefined_report_ui.total_data_count), foreground="green")

                for i, _each_row in enumerate(self.predefined_report_ui.fetched_data):
                    # if i == 0:
                    #     _total_records = _each_row[0] if (
                    #         _each_row[0] > 0 and _each_row[1] == 0) else _each_row[1]
                    #     _result = _each_row[0]
                    #     self.predefined_report_ui.fetched_data_count += _result
                    #     self.predefined_report_ui.total_data_count += _total_records
                    #     self.results_label.config(
                    #         text="Result: "+str(self.predefined_report_ui.fetched_data_count), foreground="green")
                    #     self.total_label.config(
                    #         text="Total: "+str(self.predefined_report_ui.total_data_count), foreground="green")
                    # else:
                    self.data_table_holder.insert(
                        "", "end", iid=territory+ "_" + str(i), values=tuple(_each_row))
                self.export_btn["state"] = "normal"

            self.predefined_report_ui.update()
        except:
            logger.error("Below Exception Occurred.\n", exc_info=True)

    def add_property_data_in_table(self, prop_data):
        try:
            i = 1
            par = 1

            for each_key in prop_data:
                p_iid = "P"+str(par)
                self.all_parent.append(p_iid)
                parent_elem = self.add_property_win.property_tree.insert(
                    "", "end", iid=p_iid, values=(each_key, "-----SELECT-----"), tags=["parent_tag"])
                self.add_property_win.property_tree.item(p_iid, open=True)
                par += 1

                for p_elem in prop_data[each_key]:
                    child_elem = self.add_property_win.property_tree.insert(
                        parent_elem, "end", iid=i, values=(p_elem, prop_data[each_key][p_elem]))
                    i += 1

            self.add_property_win.property_tree.tag_configure(
                "parent_tag", foreground="black", background="light grey")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def create_table_column(self, cols):
        try:
            # create Cols is a List
            cols_prop = [x.strip() for x in cols.split(",") if x.strip() != ""]
            cols_prop.insert(0, "Payload")

            logger.debug("Property as Cols: "+str(cols) +
                         ", Columns: "+str(cols_prop))
            _table_width = self.data_table_holder.winfo_width()
            number_of_cols = len(cols_prop) + 1
            _each_col_width = _table_width//number_of_cols
            logger.debug("Table Width: "+str(_table_width) + ", Number of Cols: " +
                         str(number_of_cols) + ", Calculated cols width: "+str(_each_col_width))

            _each_col_width = 100 if _each_col_width < 100 else _each_col_width
            payload_width = _each_col_width * 2
            self.data_table_holder["columns"] = tuple(cols_prop)
            self.data_table_holder.column(
                "Payload", minwidth=200, width=payload_width, anchor='nw')
            self.data_table_holder.heading("Payload", text="Payload")
            cols_prop.remove("Payload")
            for each_prop in cols_prop:
                self.data_table_holder.column(
                    each_prop, minwidth=100, width=_each_col_width, anchor='nw')

                self.data_table_holder.heading(
                    each_prop, text=each_prop)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def exportData(self):
        try:
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            save_file = filedialog.asksaveasfilename(
                initialdir=BASE_SCRIPT_PATH, initialfile="data_output.xlsx", title="Save Data", filetypes=types, defaultextension=types
            )
            logger.debug("File Name to Export the Data: "+str(save_file))
            if save_file:
                if self.predefined_report_ui.fetched_data is not None:
                    self.exportDataList(
                        save_file, self.predefined_report_ui.fetched_data)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def exportDataList(self, filename, payloadData):
        try:
            # cols_header = [x.strip() for x in self.varpropertyname.get().split(
            #     ",") if x.strip() != ""]
            # cols_header.insert(0, "Payload")
            cols_header = self.data_table_holder["columns"]
            logger.debug("Exported Data: " + str(payloadData))
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()
            
            if payloadData is not None:
                for i, head in enumerate(cols_header):
                    worksheet.write(0, i, str(head))

                for x in range(0, len(payloadData)):
                    for y in range(len(payloadData[x])):
                        worksheet.write(x+1, y, str(payloadData[x][y]))

            workbook.close()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def toggleInputField(self, value):
        try:
            self.username_ent["state"] = value
            self.passwd_ent["state"] = value
            self.type_of_property_writer_ent["state"] = value
            self.property_btn["state"] = value
            self.fetch_data["state"] = value

            if value == "normal":
                updatedval = "disabled"
                self.environment_ent["state"] = "readonly"
                self.report_list_combobox["state"] = "readonly"

            elif value == "disabled":
                updatedval = "normal"
                self.environment_ent["state"] = "disabled"
                self.report_list_combobox["state"] = "disabled"
                self.territory_list_combobox["state"] = "disabled"
                self.territory_name_ent["state"] = "disabled"
                self.environment_ip_ent["state"] = "disabled"
                self.property_name_ent["state"] = value
                self.year_combobox["state"] = value
                self.month_combobox["state"] = value
                self.day_combobox["state"] = value

            self.export_btn["state"] = updatedval

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            # self.loglist.insert(0, "There are some errors. Please check logs")
            self.error_label.config(
                text="There are some errors. Please check logs", fg="red")

    def reset_all(self):
        try:
            self.initiate_var()
            self.toggleInputField("normal")

            self.data_table_holder.delete(
                *self.data_table_holder.get_children())
            self.data_table_holder["columns"] = ()
            self.results_label.config(text="")
            self.total_label.config(text="")
            self.predefined_report_instance = None
            self.predefined_report_ui.fetched_data = None
            self.predefined_report_ui.fetched_data_count = 0
            self.predefined_report_ui.total_data_count = 0
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# End of Pre-defined Manager

# Start of Extract reports for all types of Form 
class FormDataforMarketingConsent:
    def __init__(self, master):
        global configdata
        self.form_data_marketing_consent_ui = Toplevel(master)
        self.master = master
        self.form_data_marketing_consent_ui.state('zoomed')
        master.withdraw()
        self.form_data_marketing_consent_ui.title(
            APPLICATION_NAME + " - " + "Extract Reports For All Types Of Forms"
        )
        self.form_data_marketing_consent_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.form_data_marketing_consent_ui.brandpic = PhotoImage(
            file=BRAND_PIC_FILE)
        self.form_data_marketing_consent_ui.iconphoto(False, self.brandpic)
        self.form_data_marketing_consent_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=self.master: self.reopenroot(root)
        )
        self.form_data_marketing_consent_instance = None
        self.form_data_marketing_consent_ui.configdata = configdata
        self.form_data_marketing_consent_ui.fetched_data = None
        self.form_data_marketing_consent_ui.user_variable_entered_data = None
        self.form_data_marketing_consent_ui.fetched_data_count = 0
        self.form_data_marketing_consent_ui.total_data_count = 0
        self.form_data_marketing_consent_ui.resource_type_data = edcfg.readConfig(RESOURCE_TYPE_FILE)

        self.main_design()

    def changeRoot(self, root):
        root.state('zoomed')
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.form_data_marketing_consent_ui.destroy()
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
            self.varipdata.set("")
            self.varpassent.set(self.decrypted_passwd)
            self.varformname.set("--SELECT--")
            self.varterritoryname.set("--SELECT--")
            self.varterritorynameent.set("")
            self.varpropertyname.set("")
            self.varuserdefvar.set("")
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
            self.window_style.configure(
                "mainBigBtn.TButton", font=(FONT_NAME, FONT_SIZE * 4), relief="flat")
            self.window_style.configure("scrollbarmain.TScrollbar", background="Green", darkcolor="DarkGreen",
                                        lightcolor="LightGreen", troughcolor="gray", bordercolor="blue", arrowcolor="white")
            self.window_style.configure(
                "green.Horizontal.TProgressbar", foreground='green', background='darkgreen')

            self.window_style.configure(
                "labelent.TLabel", font=(FONT_NAME, FONT_SIZE + 4, "bold"))
            self.window_style.configure(
                "labelent.TEntry", font=(FONT_NAME, FONT_SIZE + 4, "bold"))

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    
    def main_design(self):
        try:
            # Declare String Variable
            self.define_style()

            # String Variable
            self.varipdata = StringVar()
            self.varenvdata = StringVar()
            self.varuserent = StringVar()
            self.varpassent = StringVar()
            self.varformname = StringVar()
            self.varterritoryname = StringVar()
            self.varterritorynameent = StringVar()
            self.varpropertyname = StringVar()
            self.varquerydata = StringVar()
            self.vardate = StringVar()
            self.varmonth = StringVar()
            self.varyear = StringVar()
            self.varuserdefvar = StringVar()

            # Initiate String Variable
            self.initiate_var()

            # Validation
            self.varenvdata.trace(
                "w", lambda *args: self.ipchange(self.varenvdata.get()))
            self.varipdata.trace(
                "w", lambda *args: self.checkipdata(self.varipdata))
            self.varformname.trace(
                "w", lambda *args: self.form_name_change(self.varformname.get()))


            # Frame Creation
            self.main_frame = Frame(self.form_data_marketing_consent_ui)
            self.main_frame.pack(fill="x", padx=5)

            self.main_upper_frame = Frame(self.main_frame)
            self.main_upper_frame.pack(fill="x", padx=5)

            self.main_lower_frame = Frame(self.main_frame)
            self.main_lower_frame.pack(fill="x", padx=5)

            self.main_btn_frame_sep = ttk.Separator(
                self.form_data_marketing_consent_ui)
            self.main_btn_frame_sep.pack(fill="x", padx=5, pady=10)

            self.main_btn_frame = Frame(self.form_data_marketing_consent_ui)
            self.main_btn_frame.pack(fill="x")

            self.btn_frame_details_sep = ttk.Separator(
                self.form_data_marketing_consent_ui)
            self.btn_frame_details_sep.pack(fill="x", padx=5, pady=10)

            self.main_details_frame = Frame(self.form_data_marketing_consent_ui)
            self.main_details_frame.pack(fill="both")

            # Environment Frame
            self.environment_frame = LabelFrame(
                self.main_upper_frame, text="Select Environment")
            self.environment_frame.pack(
                side="left", fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10)

            ## Username & Password
            self.username_and_password_frame = LabelFrame(
                self.main_upper_frame, text="Login Details")
            self.username_and_password_frame.pack(
                side="left", fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10)
            # self.username_and_password_frame.grid_columnconfigure(0, weight=1)

            self.username_label = ttk.Label(
                self.username_and_password_frame, text="Username", style="labelent.TLabel")
            self.username_label.grid(
                row=0, column=0, padx=5, pady=5, sticky="nsew")
            self.username_ent = ttk.Entry(
                self.username_and_password_frame, textvariable=self.varuserent, style="labelent.TEntry")
            self.username_ent.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.username_and_password_frame.grid_columnconfigure(1, weight=1)

            self.passwd_label = ttk.Label(
                self.username_and_password_frame, text="Password", style="labelent.TLabel")
            self.passwd_label.grid(
                row=1, column=0, padx=5, pady=5, sticky="nsew")
            self.passwd_ent = ttk.Entry(
                self.username_and_password_frame, show="*", textvariable=self.varpassent, style="labelent.TEntry")
            self.passwd_ent.grid(row=1, column=1, padx=5,
                                 pady=5, sticky="nsew")
            self.username_and_password_frame.grid_columnconfigure(1, weight=1)

            # # Environment Frame
            # self.environment_frame = LabelFrame(
            #     self.main_upper_frame, text="Select Environment")
            # self.environment_frame.pack(
            #     side="left", fill="both", expand="yes", padx=10, pady=10, ipadx=10, ipady=10)
            # self.environment_frame.grid_columnconfigure(1, weight=1)

            self.environment_label = ttk.Label(
                self.environment_frame, text="Environment", style="labelent.TLabel")
            self.environment_label.grid(
                row=0, column=0, padx=5, pady=5, sticky="nsew")
            # self.env_dropdown_data = ["Production", "Stage", "QA", "IP"]
            env_data = configdata.get("environments",[])
            # env_data.insert(0,"")
            self.env_dropdown_data = env_data.copy()
            self.environment_ent = ttk.Combobox(
                self.environment_frame, textvariable=self.varenvdata, state="readonly", values=self.env_dropdown_data)
            #ttk.Optionmenu(self.environment_frame, textvariable=self.varuserent)
            self.environment_ent.grid(
                row=0, column=1, padx=5, pady=5, sticky="nsew")
            self.environment_frame.grid_columnconfigure(1, weight=1)

            self.environment_ip_ent = ttk.Entry(
                self.environment_frame, textvariable=self.varipdata, state="disabled", style="labelent.TEntry")
            self.environment_ip_ent.grid(
                row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
            self.environment_frame.grid_columnconfigure(1, weight=1)

            # Report Frame
            self.report_frame = LabelFrame(
                self.main_upper_frame, text="Types of Form & Territory Selection")
            self.report_frame.pack(
                side="left", fill="both", expand="yes", padx=10, pady=10)
            # self.report_frame.grid_columnconfigure(2, weight=1)

            self.report_label_frame = LabelFrame(
                self.report_frame, text="Select Form Type")
            self.report_label_frame.grid(
                row=0, column=0, padx=20, pady=0, sticky="nsew")

            
            #get list of forms
            global USER_DEF_FILE
            self.user_def_report_json = edcfg.readConfig(USER_DEF_FILE)
            self.form_list = []
            for _rep in self.user_def_report_json.get("form_list", []):
                self.form_list.append(_rep)
            self.form_list.insert(0, "--SELECT--")
            

            self.form_list_combobox = ttk.Combobox(
                self.report_label_frame, textvariable=self.varformname, state="readonly", values=self.form_list, width=25)
            self.form_list_combobox.grid(
                row=0, column=0, padx=5, pady=10, ipadx=5, ipady=5, sticky="nsew")
            self.report_label_frame.grid_columnconfigure(0, weight=1)

            self.territory_label_frame = LabelFrame(
                self.report_frame, text="Select Territory")
            self.territory_label_frame.grid(
                row=0, column=1, columnspan=2, padx=0, pady=0, sticky="nsew")
            

            self.all_territory_mappings = GenericFunctions.read_country_name(
                TERRITORY_FILE)
            
            self.territory_list = []
            for _map_ter in self.all_territory_mappings:
                self.territory_list.append(str(self.all_territory_mappings[_map_ter]).title())

            self.territory_list.sort()
            self.territory_list.insert(0, "--SELECT--")
            self.territory_list_combobox = ttk.Combobox(
                self.territory_label_frame, textvariable=self.varterritoryname, state="disabled", values=self.territory_list, width=15)
            self.territory_list_combobox.grid(
                row=0, column=0, padx=5, pady=10, ipadx=5, ipady=5, sticky="nsew")
            self.territory_label_frame.grid_columnconfigure(0, weight=1)

                                                                
            #Button_type_jcr_property
            self.property_label = ttk.Label(
                self.main_lower_frame, text="Type JCR Property in the box :")
            self.property_label.grid(
                row=0, column=0, padx=5, pady=5, sticky="nsew")
            #self.property_label["state"] = "disabled"
            
            #form property entry
            self.property_name_ent = ttk.Entry(
                self.main_lower_frame, textvariable=self.varpropertyname, style="labelent.TEntry")
            self.property_name_ent.grid(
                row=0, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

            self.main_lower_frame.grid_columnconfigure(2, weight=1)


            # Button Frame
            self.fetch_data = ttk.Button(
                self.main_btn_frame, text="Retrieve Data", command=self.retreive_data)
            self.fetch_data.pack(side="left", expand="yes",
                                 padx=5, pady=5, anchor=CENTER)

            self.reset_btn = ttk.Button(
                self.main_btn_frame, text="Reset All", command=self.reset_all)
            self.reset_btn.pack(side="left", expand="yes",
                                padx=5, pady=5, anchor=CENTER)

            self.exit_window = ttk.Button(
                self.main_btn_frame, text="Exit Window", command=lambda root=self.master: self.reopenroot(root))
            self.exit_window.pack(side="left", expand="yes",
                                  padx=5, pady=5, anchor=CENTER)

            # Details Frame
            self.retrieved_data_frame = LabelFrame(
                self.main_details_frame, text="********")
            self.retrieved_data_frame.pack(
                side="left", fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)

            self.small_btn_frame = Frame(self.retrieved_data_frame)
            self.small_btn_frame.pack(
                fill="x", padx=2, pady=0, ipadx=2, ipady=2)

            self.data_table_frame = Frame(self.retrieved_data_frame)
            self.data_table_frame.pack(
                fill="both", expand="yes", padx=2, pady=2, ipadx=2, ipady=2)

            # Small Button
            self.export_btn = ttk.Button(self.small_btn_frame, text="Export",
                                         command=self.exportData, style="smallBtn.TButton", state="disabled")
            self.export_btn.pack(side="left", padx=2, pady=2, anchor="w")

            self.results_label = Label(self.small_btn_frame, text="")
            self.results_label.pack(side="left", padx=2, pady=2, anchor="w")

            self.total_label = Label(self.small_btn_frame, text="")
            self.total_label.pack(side="left", padx=2, pady=2, anchor="w")

            # Treeview Table
            self.data_table_holder = ttk.Treeview(
                self.data_table_frame, show="headings", selectmode="extended", height=25)
            self.data_table_holder_scroll_y = ttk.Scrollbar(
                self.data_table_frame, orient="vertical", command=self.data_table_holder.yview)
            self.data_table_holder.config(
                yscrollcommand=self.data_table_holder_scroll_y.set)
            self.data_table_holder_scroll_y.pack(side="right", fill="y")

            self.data_table_holder_scroll_x = ttk.Scrollbar(
                self.data_table_frame, orient="horizontal", command=self.data_table_holder.xview)
            self.data_table_holder.config(
                xscrollcommand=self.data_table_holder_scroll_x.set)
            self.data_table_holder_scroll_x.pack(side="bottom", fill="x")

            self.data_table_holder.pack(
                padx=5, pady=5, anchor="c", fill="both")

            self.form_data_marketing_consent_ui.update()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
 
    def ipchange(self, value):
        try:
            if value.lower() == "ip":
                self.environment_ip_ent["state"] = "normal"
                self.varuserent.set("")
                self.varpassent.set("")

            else:
                self.varipdata.set("")
                self.environment_ip_ent["state"] = "disabled"
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
    
    ###Form Selection Change...
    def form_name_change(self, value):
        try:
            _territory = self.varterritoryname.get()
            if value == "--SELECT--":
                
                self.territory_label_frame.grid(
                    row=0, column=1, columnspan=2, padx=5, pady=0, sticky="nsew")
               
                self.territory_list_combobox["state"] = "disabled"
                
                self.varterritoryname.set("--SELECT--")
                #self.property_label["state"] = "disabled"
            else:                
                self.varpropertyname.set("")
                #self.property_label["state"] = "normal"

                self.varterritoryname.set("--SELECT--")
                self.territory_list_combobox["state"] = "readonly"

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
    
    def validate_input(self, uname, passwd, ip_or_url, environment, selected_form, terr_or_path):
        try:
            is_validated = False

            is_not_empty_uname = bool(uname)
            is_not_empty_passwd = bool(passwd)
            is_not_empty_ip_or_url = bool(ip_or_url)
            is_not_empty_environment = bool(environment)
            is_not_empty_selected_form = bool(selected_form)
            is_not_empty_terr_or_path = bool(terr_or_path)

            is_valid_ip_or_url = GenericFunctions.validateIP(
                ip_or_url, environment)
            # is_terr_or_path_starts_with_invalid =
            is_form_selected = True if selected_form.lower() != "--select--" else False

            logger.debug("Is Not Empty Username: %s, Is Not Empty Password: %s, Is Not Empty IP or URL: %s, \
                    Is Not Empty Environment: %s, Is Not Empty Report: %s, Is Not Empty Terr or Path: %s, \
                        Is Not Empty Property: %s, Is Valid IP or URL: %s, "
                         % (is_not_empty_uname, is_not_empty_passwd, is_not_empty_ip_or_url, is_not_empty_environment,
                            is_not_empty_selected_form, is_not_empty_terr_or_path, is_valid_ip_or_url, is_form_selected))

            error_list = []

            if (is_not_empty_environment and is_not_empty_ip_or_url and is_not_empty_passwd
                and is_not_empty_selected_form and is_not_empty_terr_or_path
                    and is_not_empty_uname and is_valid_ip_or_url and is_form_selected):

                is_validated = True
            else:
                if not(is_not_empty_environment):
                    error_list.append("\nPlease Select a Environment")
                if not(is_not_empty_ip_or_url):
                    error_list.append("\nPlease Enter the IP/URL")
                if not(is_not_empty_passwd):
                    error_list.append("\nPlease enter a Password")                
                if not(is_not_empty_terr_or_path):
                    error_list.append("\nPlease Select/Enter a Territory")
                if not(is_not_empty_uname):
                    error_list.append("\nPlease Enter a Username")
                if not(is_valid_ip_or_url):
                    error_list.append("\nPlease Enter a valid IP/URL")
                if not(is_form_selected):
                    error_list.append("\nPlease Select a Form")
                if bool(error_list):
                    error_msg = ".".join(error_list)
                    logger.error("Error message: \n %s" % error_msg)
                    messagebox.showerror(
                        "Below Error has been Occurred", error_msg, parent=self.form_data_marketing_consent_ui)

            logger.debug(
                "All Data Validation Consolidated Report: %s" % is_validated)
            return is_validated
            
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    
    #Fetch Data ...
    def retreive_data(self):
        try:
            self.results_label.config(text="")
            self.total_label.config(text="")
            self.form_data_marketing_consent_ui.fetched_data = None
            report_ran_by_user = False

            _user_name = self.varuserent.get().strip()
            _password = self.varpassent.get()
            _selected_env = self.varenvdata.get().lower()
            _environment_url = self.varipdata.get().strip() if _selected_env == "ip" \
                else self.form_data_marketing_consent_ui.configdata[_selected_env]

            _selected_form = self.varformname.get()

            _territory_or_path = (GenericFunctions.get_key_of_val(self.all_territory_mappings, self.varterritoryname.get().lower()) if  self.varterritoryname.get().upper() != "MULTI" else self.varterritorynameent.get()) \
                if self.varterritoryname.get().upper() != "--SELECT--" else self.varterritorynameent.get().replace("/content/pwc/", "").replace("/content/dam/pwc/", "")

           
            _territory_or_path = GenericFunctions.removetrailingspecialchar(
                _territory_or_path)
            _property_string = self.property_name_ent.get().strip()
            _selected_property = [
                x.strip() for x in _property_string.split(",") if x.strip() != ""]
            
            logger.debug("Username: %s, Environment or IP: %s, Selected Report: %s, Territory or Path: %s, Selected Props: %s" % (
                _user_name, _environment_url, _selected_form, _territory_or_path, _selected_property))

            
            #is_validated_data=True
            
             #uname, passwd,ip_or_url, environment, selected_rep, terr_or_path, props
            is_validated_data = self.validate_input(
                _user_name, _password, _environment_url, _selected_env, _selected_form, _territory_or_path)

            logger.debug("Validated Data %s" % is_validated_data)
            if is_validated_data:
                continue_operation = True
                if _selected_env == "production":
                    continue_operation = messagebox.askyesnocancel(
                        "Please confirm", "Do you want to Run\nthe Operation in Production?", parent=self.form_data_marketing_consent_ui)
                #retrieve
                if continue_operation:
                    self.form_data_marketing_consent_instance = FormDataMarketingConsent(
                        _environment_url, _user_name, _password)
                    #_fetched_data = self.form_data_marketing_consent_instance.form_selector(form_name=_selected_form, environment= _selected_env,territory=_territory_or_path, props=_selected_property)
                    report_ran_by_user, result_info = self.run_report_for_selected(_selected_form, _territory_or_path, _selected_env, _selected_property, _property_string)
                    if self.form_data_marketing_consent_ui.fetched_data is not None:
                        self.toggleInputField("disabled")
                        self.prepare_output_data(_property_string, True, _territory_or_path, result_info)
                        if isinstance(self.form_data_marketing_consent_ui.fetched_data, str):
                                self.results_label.config(
                                    text=self.form_data_marketing_consent_ui.fetched_data, foreground="red")
                                if self.form_data_marketing_consent_ui.fetched_data == "Wrong Username and Password - Http Code - 401":
                                    self.username_ent["state"] = "normal"
                                    self.passwd_ent["state"] = "normal"
                                    self.fetch_data["state"] = "normal"
                                    self.export_btn["state"] = "disabled"
                        elif self.form_data_marketing_consent_ui.fetched_data is None and report_ran_by_user:
                            self.total_label.config(
                                    text="No Data has been retrieve.", foreground="red")
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def run_report_for_selected(self, _selected_form, _territory_or_path, _selected_env, _selected_property, _property_string):
        try:
            report_ran_by_user = False
            _fetched_data = self.form_data_marketing_consent_instance.form_selector(form_name=_selected_form, environment= _selected_env,territory=_territory_or_path, props=_selected_property)
                                                                                                
            
            result_info = []
            result_info = _fetched_data.pop(0) if _fetched_data is not None and isinstance(_fetched_data, (list, tuple)) else []
            logger.debug("Result Info %s,Report Ran by user, %s",result_info, _fetched_data)
            if isinstance(self.form_data_marketing_consent_ui.fetched_data, (list, tuple)) and type(self.form_data_marketing_consent_ui.fetched_data)==type(_fetched_data):
                self.form_data_marketing_consent_ui.fetched_data += _fetched_data
            elif self.form_data_marketing_consent_ui.fetched_data is None and isinstance(_fetched_data, (list,tuple,dict)):
                if bool(_fetched_data):
                    self.form_data_marketing_consent_ui.fetched_data = _fetched_data.copy()
            else:
                self.form_data_marketing_consent_ui.fetched_data = _fetched_data

            report_ran_by_user = True
            
            return report_ran_by_user, result_info
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False    
    
    def prepare_output_data(self, _property_string, _create_table_column, territory, result_info):
        try:
            # if self.form_data_marketing_consent_ui.fetched_data is not None and not(form_field_selected):
            if isinstance(self.form_data_marketing_consent_ui.fetched_data, list):
                if _create_table_column:
                    self.create_table_column(_property_string)
                
                if bool(result_info) and isinstance(result_info, list) and len(result_info) == 2:
                    _total_records = result_info[0] if (
                             result_info[0] > 0 and result_info[1] == 0) else result_info[1]
                    _result = result_info[0]
                    self.form_data_marketing_consent_ui.fetched_data_count += _result
                    self.form_data_marketing_consent_ui.total_data_count += _total_records
                    self.results_label.config(
                            text="Result: "+str(self.form_data_marketing_consent_ui.fetched_data_count), foreground="green")
                    self.total_label.config(
                            text="Total: "+str(self.form_data_marketing_consent_ui.total_data_count), foreground="green")

                for i, _each_row in enumerate(self.form_data_marketing_consent_ui.fetched_data):
                    # if i == 0:
                    #     _total_records = _each_row[0] if (
                    #         _each_row[0] > 0 and _each_row[1] == 0) else _each_row[1]
                    #     _result = _each_row[0]
                    #     self.form_data_marketing_consent_ui.fetched_data_count += _result
                    #     self.form_data_marketing_consent_ui.total_data_count += _total_records
                    #     self.results_label.config(
                    #         text="Result: "+str(self.form_data_marketing_consent_ui.fetched_data_count), foreground="green")
                    #     self.total_label.config(
                    #         text="Total: "+str(self.form_data_marketing_consent_ui.total_data_count), foreground="green")
                    # else:
                    self.data_table_holder.insert(
                        "", "end", iid=territory+ "_" + str(i), values=tuple(_each_row))
                self.export_btn["state"] = "normal"

            self.form_data_marketing_consent_ui.update()
        except:
            logger.error("Below Exception Occurred.\n", exc_info=True)                       
        
    def create_table_column(self, cols):
        try:
            # create Cols is a List
            cols_prop = [x.strip() for x in cols.split(",") if x.strip() != ""]
            cols_prop.insert(0, "Payload")

            logger.debug("Property as Cols: "+str(cols) +
                         ", Columns: "+str(cols_prop))
            _table_width = self.data_table_holder.winfo_width()
            number_of_cols = len(cols_prop) + 1
            _each_col_width = _table_width//number_of_cols
            logger.debug("Table Width: "+str(_table_width) + ", Number of Cols: " +
                         str(number_of_cols) + ", Calculated cols width: "+str(_each_col_width))

            _each_col_width = 100 if _each_col_width < 100 else _each_col_width
            payload_width = _each_col_width * 2
            self.data_table_holder["columns"] = tuple(cols_prop)
            self.data_table_holder.column(
                "Payload", minwidth=200, width=payload_width, anchor='nw')
            self.data_table_holder.heading("Payload", text="Payload")
            cols_prop.remove("Payload")
            for each_prop in cols_prop:
                self.data_table_holder.column(
                    each_prop, minwidth=100, width=_each_col_width, anchor='nw')

                self.data_table_holder.heading(
                    each_prop, text=each_prop)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
    

    def exportData(self):
        try:
            types = (("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            save_file = filedialog.asksaveasfilename(
                initialdir=BASE_SCRIPT_PATH, initialfile="data_output.xlsx", title="Save Data", filetypes=types, defaultextension=types
            )
            logger.debug("File Name to Export the Data: "+str(save_file))
            if save_file:
                if self.form_data_marketing_consent_ui.fetched_data is not None:
                    self.exportDataList(
                        save_file, self.form_data_marketing_consent_ui.fetched_data)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def exportDataList(self, filename, payloadData):
        try:
            # cols_header = [x.strip() for x in self.varpropertyname.get().split(
            #     ",") if x.strip() != ""]
            # cols_header.insert(0, "Payload")
            cols_header = self.data_table_holder["columns"]
            logger.debug("Exported Data: " + str(payloadData))
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()
            
            if payloadData is not None:
                for i, head in enumerate(cols_header):
                    worksheet.write(0, i, str(head))

                for x in range(0, len(payloadData)):
                    for y in range(len(payloadData[x])):
                        worksheet.write(x+1, y, str(payloadData[x][y]))

            workbook.close()

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def toggleInputField(self, value):
        try:
            self.username_ent["state"] = value
            self.passwd_ent["state"] = value
            #self.property_btn["state"] = value
            self.fetch_data["state"] = value

            if value == "normal":
                updatedval = "disabled"
                self.environment_ent["state"] = "readonly"
                self.form_list_combobox["state"] = "readonly"
                self.property_name_ent["state"] = "normal"

            elif value == "disabled":
                updatedval = "normal"
                self.environment_ent["state"] = "disabled"
                self.form_list_combobox["state"] = "disabled"
                self.territory_list_combobox["state"] = "disabled"
                self.environment_ip_ent["state"] = "disabled"
                self.property_name_ent["state"] = value
                #self.property_label["state"] = "disabled"


            self.export_btn["state"] = updatedval

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            # self.loglist.insert(0, "There are some errors. Please check logs")
            self.error_label.config(
                text="There are some errors. Please check logs", fg="red")

    def reset_all(self):
        try:
            self.initiate_var()
            self.toggleInputField("normal")

            self.data_table_holder.delete(
                *self.data_table_holder.get_children())
            self.data_table_holder["columns"] = ()
            self.results_label.config(text="")
            self.total_label.config(text="")
            self.form_data_marketing_consent_instance = None
            self.form_data_marketing_consent_ui.fetched_data = None
            self.form_data_marketing_consent_ui.fetched_data_count = 0
            self.form_data_marketing_consent_ui.total_data_count = 0
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# End of Extract reports for all types of Form ...

# Start of Forbidden Path Edit

class ForbiddenPathWindow:
    def __init__(self, master):
        self.master = master
        self.forbidden_path_win = Toplevel(master)
        self.master.wm_attributes("-disabled", True)
        self.forbidden_path_win.focus_set()
        self.forbidden_path_win.title(
            APPLICATION_NAME + " - " + "Update Forbidden Paths")
        self.forbidden_path_win.geometry("+10+20")
        self.forbidden_path_win.minsize(520, 620)
        self.forbidden_path_win.maxsize(520, SCREEN_HEIGHT)
        self.forbidden_path_win.resizable(width=False, height=True)
        self.brandpic = PhotoImage(file=BRAND_PIC_FILE)
        self.forbidden_path_win.iconphoto(False, self.brandpic)
        self.forbidden_path_win.transient(self.master)
        self.forbidden_path_win.protocol(
            "WM_DELETE_WINDOW", self.closethiswindow)
        self.style_forbidden_path_win = ttk.Style()
        # self.user_name =
        self.forbidden_path_main_design()
        global INVALID_PATH_STRING
        # self.forbidden_path_win.attributes('-topmost', 'true')

    def forbidden_path_label_frame(self):
        try:
            # Start of Design
            self.titleframe = Frame(self.forbidden_path_win)
            self.editframe = LabelFrame(
                self.forbidden_path_win, text="Edit the Data", padx=10, pady=10
            )
            self.titleframe.pack(fill="both", padx=5, pady=5)
            self.editframe.pack(fill="both", padx=5, pady=5)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def forbidden_path_main_design(self):
        try:
            localfontsize = FONT_SIZE - 3
            # String Variable
            self.varnewval = StringVar()
            self.varnewval.set("")
            self.var_user_name = StringVar()
            self.var_user_name.set("")
            self.var_password = StringVar()
            self.var_password.set("")

            # Validation

            # Label Frame
            self.forbidden_path_label_frame()

            # Adding Widgets
            self.frame_1 = Frame(self.titleframe)
            self.frame_1.pack(fill="both", expand="yes")
            self.titlelabel = ttk.Label(
                self.frame_1,
                text="Update Forbidden Path",
                anchor=CENTER,
                font=(FONT_NAME, localfontsize + 4, "italic"),
                borderwidth=2,
                relief="groove",
            )
            self.titlelabel.pack(
                fill="x",
                expand="yes",
                padx=5,
                pady=5,
                ipadx=5,
                ipady=5,
                anchor="center",
            )

            #######################
            self.uname_password_frame = Frame(self.editframe)
            self.uname_password_frame.pack(
                fill="x", expand="yes", padx=5, pady=5)

            self.uname_label_frame = LabelFrame(
                self.uname_password_frame, text="DPE Prod Username")
            self.uname_label_frame.pack(
                side="left", expand="yes", ipadx=5, ipady=5)

            self.uname_entry = ttk.Entry(
                self.uname_label_frame, textvariable=self.var_user_name)
            self.uname_entry.pack(
                fill="x", padx=5, expand="yes", pady=5, ipadx=5, ipady=5)

            self.password_label_frame = LabelFrame(
                self.uname_password_frame, text="DPE Prod Password")
            self.password_label_frame.pack(
                side="left", expand="yes", ipadx=5, ipady=5)

            self.password_entry = ttk.Entry(
                self.password_label_frame, show="*", textvariable=self.var_password)
            self.password_entry.pack(
                fill="x", padx=5, pady=5, ipadx=5, ipady=5)

            self.editframe_1 = Frame(self.editframe)
            self.editframe_1.pack(fill="both", expand="yes", padx=5, pady=5)

            self.textwizard = Text(self.editframe_1, undo=True)
            self.textwizard.pack(fill="both", expand="yes", padx=5, pady=5)

            self.editframe_1.grid_columnconfigure(1, weight=1)

            self.textwizard.insert(END, INVALID_PATH_STRING)

            #############
            self.frame_btn = Frame(self.forbidden_path_win)
            self.frame_btn.pack(fill="both")

            self.btncancel = ttk.Button(
                self.frame_btn,
                text="Exit",
                style="btnStyle.TButton",
                command=self.closethiswindow,
            )  # lambda:self.forbidden_path_win.destroy()
            self.btncancel.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5)

            self.btnsave = ttk.Button(
                self.frame_btn,
                text="Update",
                style="btnStyle.TButton",
                command=self.savesettings,
            )
            self.btnsave.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5)

        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    ## Functions / Callback
    def closethiswindow(self):
        self.master.focus_set()
        self.master.wm_attributes("-disabled", False)
        self.forbidden_path_win.destroy()

    def validate_user(self, username, passwd):
        try:
            valid_user = False
            logger.debug("Username: " + username + ",Password: "+passwd)
            if username.strip().lower() in ADMIN_USERS:
                r_wf_mgr = RunWorkflow("IP","DUMMY","DUMMY")
                resp_data_status = r_wf_mgr.validate_admin_user(username, passwd)
                
                if resp_data_status == 200:
                    valid_user = True

            logger.debug("Valid User: "+str(valid_user))
            return valid_user
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    def savesettings(self):
        try:
            global INVALID_PATH_STRING
            username = self.var_user_name.get()
            passwd = self.var_password.get()

            valid_user = self.validate_user(username, passwd)

            if valid_user:
                textlistbylines = None
                textlistbylines = self.textwizard.get(
                    "1.0", END).splitlines()
                logger.debug("Invalid Paths: "+str(textlistbylines))
                textlines = [x.strip() for x in textlistbylines if x != ""]
                final_save_line = ",".join(textlines)
                INVALID_PATH_STRING = final_save_line
                logger.debug("Updated Paths: "+str(INVALID_PATH_STRING))
                ecrypted_forbidden_path = GenericFunctions.encrypt_passwd(
                    INVALID_PATH_STRING)
                logger.debug("Decrypted Forbidden Paths: " +
                             str(ecrypted_forbidden_path))
                with open(FORBIDDEN_PATH_FILE, "w") as fout:
                    fout.write(ecrypted_forbidden_path)

                messagebox.showinfo(
                    "Success!!", "Data has been saved successfully.", parent=self.forbidden_path_win)
                self.closethiswindow()

            else:
                messagebox.showerror("Error in Saving Data",
                                     "User Must be an Admin users to Edit this.\nOr Mismatch username and password!",
                                     parent=self.forbidden_path_win)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

# END Of Forbidden Path Edit

# Opening Screen/Splash Screen

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


def initiatewindow(root):
    root.state("zoomed")
    root.deiconify()
    root.update()
    root.design = DPEInboxClearing(root)
    root.design.maindesign()


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
