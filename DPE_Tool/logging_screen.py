from tkinter import *
from tkinter import ttk, PhotoImage, messagebox, filedialog
import logging
import threading
from viewpoint_metadata_clean import MetaDataClean, METADATA_OPERATION

# global FONT_NAME, FONT_SIZE


FONT_NAME = "Georgia"
FONT_SIZE = 12
APPLICATION_NAME = "Dante"
LOGGER_DETAILS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}

class LoggingScreen:
    def __init__(self, master, app_name, brand_pic_file, log_file):
        self.logger = logging.getLogger()
        self.master = master
        self.loggin_screen_window = Toplevel(master)
        self.master.wm_attributes("-disabled", True)
        self.loggin_screen_window.focus_set()
        self.loggin_screen_window.title(app_name + " - " + "Logging")
        self.loggin_screen_window.geometry("940x640+10+20")
        self.brandpic = PhotoImage(file=brand_pic_file)
        self.loggin_screen_window.iconphoto(False, self.brandpic)
        self.loggin_screen_window.resizable(False, False)
        self.loggin_screen_window.transient(self.master)
        self.loggin_screen_window.protocol("WM_DELETE_WINDOW", self.closethiswindow)
        self.main_log_file = log_file #"logs\\mainlogfile_" + datetime.now().strftime("%m%d%Y") + ".log"
        self.selected_log_file = None
        self.create_menu_bar()
        self.mainui_design()

    def design_menu(self):
        self.menubar = Menu(self.loggin_screen_window)
        self.open_menu = Menu(self.menubar, tearoff=0)
        self.open_menu.add_command(
            label="Open Logfile", command=self.select_log_file
        )
        self.menubar.add_cascade(label="Open", menu=self.open_menu)
        self.loggin_screen_window.config(menu=self.menubar)

    def closethiswindow(self):
        try:
            self.master.focus_set()
            self.master.wm_attributes("-disabled", False)
            self.loggin_screen_window.destroy()
        except:
            self.logger.error("Below Exception occured: ", exc_info=True)

    def initialize_variable(self):
        try:
            self.var_log_file.set(self.main_log_file)
            self.filter_data.set("--SELECT--")
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

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
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def create_label_frame(self):
        try:
            self.datalabelframe = LabelFrame(
                self.loggin_screen_window, text="")
            self.datalabelframe.pack(
                fill="x", padx=10, pady=10, ipadx=10, ipady=10)

            self.log_frame = LabelFrame(
                self.loggin_screen_window, text="Logs")
            self.log_frame.pack(
                fill="both", padx=10, pady=10, ipadx=10, ipady=10)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def create_menu_bar(self):
        try:
            self.main_menu = Menu(self.loggin_screen_window)
            self.open_menu = Menu(self.main_menu, tearoff=0)
            self.open_menu.add_command(
                label="Open Log File", command=self.open_log_file
            )
            self.main_menu.add_cascade(label="Open", menu=self.open_menu)
            self.loggin_screen_window.config(menu=self.main_menu)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def mainui_design(self):
        try:
            self.define_style()
            self.design_menu()

            # String Variable
            self.var_log_file = StringVar()
            self.filter_data = StringVar()

            # Initiate Var
            self.initialize_variable()

            # Initiate Label Frames
            self.create_label_frame()

            # main Frame
            self.title_label = ttk.Label(
                self.datalabelframe,
                text="Please see the below logs",
                font=(FONT_NAME, FONT_SIZE),
                borderwidth=2,
                anchor=CENTER,
            )
            self.title_label.pack(fill="x")
            self.filter_frame = Frame(self.log_frame)
            self.filter_frame.pack(fill="x", pady=10, ipadx=5, ipady=5)

            self.main_log_frame = Frame(self.log_frame)
            self.main_log_frame.pack(fill="both")

            self.log_filter = ttk.Combobox(self.filter_frame, state="readonly", textvariable=self.filter_data, values=["--SELECT--","Debug","Info","Warning","ERROR","Critical"])
            self.log_filter.pack(anchor="w", ipadx=5, ipady=5)

            self.log_filter.bind("<<ComboboxSelected>>", lambda *args: self.filter_log_file(self.filter_data.get()))

            # self.archive_data_view_btn = ttk.Button(
            #     self.filter_frame, text="OpenLog", command=self.select_log_file)
            # self.archive_data_view_btn.pack(
            #     side="left", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)

            self.log_list = Text(self.main_log_frame, height=40)
            self.scroll_y = ttk.Scrollbar(
                    self.main_log_frame, orient=VERTICAL, command=self.log_list.yview)
            self.scroll_y.pack(
                side="right", fill="y")
            
            self.log_list.config(
                    yscrollcommand=self.scroll_y.set)
            self.log_list.pack(fill="both")
            # log = self.log_list.get(
            #         "1.0", END).splitlines()
            # textlines = [x.strip() for x in log if x.strip() != ""]
            # print(bool(textlines))

            self.threaded_open_log()
            self.log_list.config(state="disabled")

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    # Function/Callback
    def threaded_open_log(self):
        try:
            open_thread = threading.Thread(target=self.open_log_file)
            open_thread.start()
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def open_main_log_file(self):
        try:
            # print("main_log_file")
            # print(self.main_log_file)
            read_data = None
            with open(self.main_log_file, encoding="utf8") as file:
                read_data = file.readlines()
            # self.logger.debug("Log Data Read: ")
            # self.logger.debug(read_data)
            return read_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def open_log_file(self):
        try:
            # print(self.main_log_file)
            read_data = self.open_main_log_file()
            self.log_list.config(state="normal")
            self.log_list.delete('1.0', END)
            if read_data is not None:
                self.logger.info("Log is set to Editable Mode.")

                for each_line in read_data:
                    line_list = each_line.split("->")
                    len_line_list = len(line_list)
                    # self.logger.debug("Length of the List: %s", str(len_line_list))
                    final_line = ""
                    if len_line_list > 1:
                        final_line = line_list[0] +" - "+line_list[-2] + " - "+line_list[-1]
                    elif len_line_list == 1:
                        final_line = line_list[0]

                    self.log_list.insert(END,str(final_line))
                    # if final_line[-1] != "\n":
                    #     self.logger.debug("Data Inserted: "+str(final_line))
                    # else:
                    #     self.logger.debug("Data Inserted: "+str(final_line[:-1]))

                self.log_list.config(state="disabled")
                self.logger.info("Log is set to Disabled Mode.")
            else:
                self.log_list.insert(END,"Some Exception occured while opening the file.")
                self.logger.error("Some Exception occured while opening the file.")
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def filter_log_file(self, filter_data):
        try:
            read_data = self.open_main_log_file()
            self.log_list.config(state="normal")

            self.log_list.delete('1.0', END)

            got_error = False
            self.logger.info("Filter Data: %s", filter_data)

            for each_line in read_data:
                line_list = each_line.split("->")
                len_line_list = len(line_list)
                final_line = ""
                if len_line_list > 1:
                    if filter_data != "--SELECT--":
                        
                        if line_list[-2].lower().strip() == filter_data.lower():
                            got_error = True if line_list[-2].lower().strip() == "error" else False
                            final_line = line_list[0] +" - "+line_list[-2] + " - "+line_list[-1]
                            # print(got_error)
                    else:
                        got_error = True
                        final_line = line_list[0] +" - "+line_list[-2] + " - "+line_list[-1]
                elif len_line_list == 1:
                    # print("Type: "+str(got_error))
                    if got_error:
                        final_line = line_list[0]

                self.log_list.insert(END,str(final_line))
                # self.logger.debug("Data Inserted: "+str(final_line))

            self.log_list.config(state="disabled")
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)


    def select_log_file(self):
        try:
            types = (("Log Files", "*.log"),)
            self.selected_log_file = filedialog.askopenfilename( title="Select Excel File", filetypes=types)
            self.logger.info("Selected Log File: "+str(self.selected_log_file)+".")

            #self.main_log_file = self.selected_log_file if (self.selected_log_file is not None or self.selected_log_file.strip() != '') else self.main_log_file
            if str(self.selected_log_file) != '':
                self.main_log_file = self.selected_log_file
                self.threaded_open_log()
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

### Viewpoint Validator
class ViewpointDataCleaner:
    def __init__(self, master, brand_pic_file, loglevel):
        self.vp_metadata_cleanup_ui = Toplevel(master)
        self.logger = logging.getLogger()
        self.logger.setLevel(LOGGER_DETAILS.get(loglevel, logging.ERROR))
        self.master = master
        self.vp_metadata_cleanup_ui.state("zoomed")
        master.withdraw()
        self.vp_metadata_cleanup_ui.title(
            APPLICATION_NAME + " - " + "Viewpoint Metadata Cleanup"
        )
        self.vp_metadata_cleanup_ui.geometry("900x800+30+30")
        self.brandpic = PhotoImage(file=brand_pic_file)
        self.vp_metadata_cleanup_ui.iconphoto(False, self.brandpic)
        self.stylevp_metadata_cleanup_ui = ttk.Style()
        self.vp_metadata_cleanup_ui.protocol(
            "WM_DELETE_WINDOW", lambda root=master: self.reopenroot(root)
        )
        self.vp_metadata_cleanup_ui.excelfile = ""
        self.meta_data_clear_inst = MetaDataClean()
        self.create_menu_bar()
        self.mainui_design()

    def create_menu_bar(self):
        try:
            self.main_menu = Menu(self.vp_metadata_cleanup_ui)
            self.header_edit_menu = Menu(self.main_menu, tearoff=0)
            self.header_edit_menu.add_command(
                label="Add/Edit", command = self.add_component_resource #command=lambda *args: GenericFunctions.download_google_sheet(file_url)
            )
            self.main_menu.add_cascade(
                label="Allowed Headers", menu=self.header_edit_menu)
            self.vp_metadata_cleanup_ui.config(menu=self.main_menu)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def close_popup_window(self, modal_window):
        try:
            self.vp_metadata_cleanup_ui.focus_set()
            self.vp_metadata_cleanup_ui.wm_attributes("-disabled", False)
            modal_window.destroy()
        except:
            self.logger.error("Below Exception occured: ", exc_info=True)

    def add_component_resource(self):
        from viewpoint_ui import ViewpointHeaderEdit
        try:
            RESOURCE_TYPE_FILE = "configfiles\\header_file.txt"
            self.edit_add_headerdata = ViewpointHeaderEdit(self.vp_metadata_cleanup_ui)
            self.edit_add_headerdata.config(application_name = "DanTe", brandpic=self.brandpic, close_pop_window=self.close_popup_window, datafile=RESOURCE_TYPE_FILE)
            self.edit_add_headerdata.main()
            self.master.wait_window(self.edit_add_headerdata)
            self.resource_type_data = self.edit_add_headerdata.data
            self.logger.debug(self.resource_type_data)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def changeRoot(self, root):
        root.state("zoomed")
        root.deiconify()
        root.update()

    def reopenroot(self, root):
        try:
            self.vp_metadata_cleanup_ui.destroy()
            root.after(1000, self.changeRoot(root))
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def initialize_variable(self):
        try:
            self.varexcelfile.set("Browse & Select Excel File")
            self.varoperationdata.set("--SELECT--")
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

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
                # style = ttk.Style()
            self.window_style.configure('TCombobox', postoffset=(0,0,50,0))

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def create_label_frame(self):
        try:
            self.datalabelframe = LabelFrame(
                self.vp_metadata_cleanup_ui, text="Enter Details")
            self.databuttonframe = LabelFrame(self.vp_metadata_cleanup_ui)
            self.data_log_frame = LabelFrame(
                self.vp_metadata_cleanup_ui, text="Logs")
            self.datalabelframe.pack(
                fill="x", padx=10, pady=10, ipadx=10, ipady=10)
            self.databuttonframe.pack(
                fill="x", padx=10, pady=10, ipadx=10, ipady=10)
            self.data_log_frame.pack(
                fill="both", expand="yes", padx=10, pady=10)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def mainui_design(self):
        try:
            self.define_style()

            # String Variable
            self.varexcelfile = StringVar()
            self.varoperationdata = StringVar()

            # Initiate Var
            self.initialize_variable()

            # Initiate Label Frames
            self.create_label_frame()

            # main Frame
            self.mainframe = Frame(self.datalabelframe)
            self.mainframe.pack(fill="x", expand="yes")

            self.title_label = ttk.Label(
                self.mainframe, text="Cleanup the Meta Data for Viewpoint", anchor=CENTER, style="titleLabel.TLabel", font=(FONT_NAME, 16, "bold"))
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
            self.operation_data = [values_ for _, values_ in METADATA_OPERATION.items()]
            self.operation_combobox = ttk.Combobox(self.selectionlabelframe, textvariable=self.varoperationdata,
                    state="readonly", values=self.operation_data)
            self.operation_combobox.grid(
                row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.file_select_querylabel = ttk.Label(self.selectionlabelframe, text="Browse & Select Excel File..",
                                             textvariable=self.varexcelfile, font=(FONT_NAME, FONT_SIZE - 2),)
            self.file_select_querylabel.grid(
                row=0, column=1, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")
            self.file_select_btn = ttk.Button(
                self.selectionlabelframe, text="Select File", command=self.open_file)
            self.file_select_btn.grid(
                row=0, column=3, padx=5, pady=5, ipadx=5, ipady=5, sticky="nsew")

            self.selectionlabelframe.grid_columnconfigure(2, weight=1)
            # self.selectionlabelframe.grid_columnconfigure(3, weight=1)

            # Button
            self.buttonFrame = Frame(self.databuttonframe)
            self.buttonFrame.pack(fill="both", expand="yes")
            self.retrvdatabtn = ttk.Button(
                self.buttonFrame, text="Start", style="mainBtn.TButton", command=self.run_operation)
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
                fill="x", padx=5, pady=5)
            self.loglist_frame = Frame(self.data_log_frame)
            self.loglist_frame.pack(
                fill="both", expand="yes", padx=5, pady=5)

            self.log_list = Listbox(self.loglist_frame)
            self.log_list.pack(fill=BOTH, expand=YES, padx=5, pady=5, anchor=CENTER)

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    # Function/Callback
    def open_file(self):
        try:
            types = (("CSV Files", "*.csv"),
                    ("Excel Files", "*.xlsx *.xls *.xlsm"),
                     ("All Files", "*.*"))
            self.vp_metadata_cleanup_ui.excelfile = filedialog.askopenfilename(title="Select CSV File", filetypes=types
            )
            if self.vp_metadata_cleanup_ui.excelfile:
                self.logger.debug("Selected Excel File: " +
                             self.vp_metadata_cleanup_ui.excelfile)
                self.varexcelfile.set(self.vp_metadata_cleanup_ui.excelfile)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def run_operation(self):
        try:
            file_ = self.vp_metadata_cleanup_ui.excelfile
            operation_type = self.varoperationdata.get()
            if bool(file_) and operation_type != METADATA_OPERATION["select"]:
                output_file_dir = filedialog.askdirectory(title="Select output file directory")
                if output_file_dir :
                    self.logger.debug("Output directory %s", output_file_dir)
                    self.logger.debug("Input file %s", file_)

                    config_status_ = self.meta_data_clear_inst.config(file_, output_file_dir)
                    
                    if config_status_:
                        self.retrvdatabtn["state"] = "disabled"
                        status = self.meta_data_clear_inst.run(operation_type, self.log_list, self.vp_metadata_cleanup_ui)

                        if status:
                            messagebox.showinfo("Success!!","All Data has been processed!", parent=self.vp_metadata_cleanup_ui)
                        else:
                            messagebox.showerror("Failed!!","Error has been occurred!!", parent=self.vp_metadata_cleanup_ui)
                        # if status.get("code", 999) == 200:
                        #     messages_ = status.get("message",[])
                        #     for msg in messages_:
                        #         for key_, values_ in msg.items():
                        #             self.log_list.insert(END, "Sheetname: %s, Status: %s, Message: %s" % (key_, values_["code"], values_["message"]))
                        # else:
                        #     self.log_list.insert(END, status.get("message","Error in Fetching"))
                    else:
                        self.log_list.insert(END, "Exception Occurred!! Failed to set Output dir and the Input filepath.")
                else:
                    messagebox.showerror("Error Occurred!!", "Please Select the output folder")

            else:
                error = []
                if not bool(file_):
                    error.append( "Please select a file")
                if operation_type == METADATA_OPERATION["select"]:
                    error.append( "Please select a Operation Type")
                
                if bool(error):    
                    messagebox.showerror("Error Occurred!!", "\n".join(error))

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def toggleInputField(self, val):
        try:
            self.file_select_btn["state"] = val
            self.retrvdatabtn["state"] = val

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def resetAll(self):
        try:
            self.initialize_variable()
            self.toggleInputField("normal")
            self.log_list.delete(0, END)
            self.vp_metadata_cleanup_ui.excelfile = ""
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

# END of Viewpoint Validator