from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import logging
from datetime import datetime
from tkcalendar import Calendar

def is_invalid_utf8_chars(input_):
    try:
        status = False
        for j in range(len(input_)):
            if ord(input_[j]) > 65536:
                status = True
                break
        
        logging.debug("Input Value: %s, Status: %s", str(input_), str(status))
        return status

    except:
        logging.error("Below Exception occurred\n", exc_info=True)
        return input_

class SearchDPEorQuery(Frame):
    """docstring for SearchDPEorQuery."""
    def __init__(self, parent, ui_type, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.logger = logging.getLogger()
        self.parent = parent
        self.ui_type = ui_type.lower()
        self.main()

    def main(self):
        try:
            ### Style
            stylewidget = ttk.Style()
            stylewidget.configure(
                "smallbuttondesign.TButton", font=("Georgia", 8), relief="flat"
            )

            if self.ui_type != "search":
                self.entry_frame = Frame(self)
                self.entry_frame.pack(fill="x", anchor="center")
                self.search_entry = Text(self.entry_frame, height = 3)
                self.search_entry.pack(fill="x", expand="yes", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

                self.search_btn = ttk.Button(self.entry_frame, text = "Search", style="smallbuttondesign.TButton")
                self.search_btn.pack(padx=5,pady=5, ipadx=5, ipady=5, anchor="e")

                self.separator = ttk.Separator(self.entry_frame, orient='horizontal')
                self.separator.pack(fill="x", padx=20, pady=10)

            
            # self.result_frame = Frame(self)
            self.small_btn_frame = Frame(self)
            self.small_btn_frame.pack(fill="x", anchor="w")
            self.export_btn = ttk.Button(self.small_btn_frame, text="Copy to Clipboard", style="smallbuttondesign.TButton")
            self.export_btn.pack(side="left", padx=5, pady=5, ipadx=3, ipady=3, anchor="w")
            self.clear_btn = ttk.Button(self.small_btn_frame, text="Clear Screen", style="smallbuttondesign.TButton")
            self.clear_btn.pack(side="left", padx=5, pady=5, ipadx=3, ipady=3, anchor="w")
            self.result_frame = ScrollableFrame(self)
            # self.result_frame = Frame(self)
            self.result_frame.pack(fill="both", expand="yes", anchor="w")
            
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
        
class CreateNodeUI(Frame):
    """docstring for CreateNodeUI."""
    def __init__(self, parent, type_values, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.logger = logging.getLogger()
        self.parent = parent
        self.type_values = type_values
        self.varnodename = StringVar()
        self.varnewtype = StringVar()
        self.main()

    def initiate_var(self):
        try:
            self.varnodename.set("")
            self.varnewtype.set(self.type_values[0])
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def main(self):
        try:
            self.initiate_var()
            self.main_frame = Frame(self)
            self.main_frame.pack(fill="both", expand="yes", anchor="center")
            self.btn_frame = Frame(self)
            self.btn_frame.pack(fill="x", expand="yes", anchor="center")

            self.name_frame = LabelFrame(self.main_frame, text="Enter Name")
            self.name_frame.pack(fill="x", expand="yes", anchor="center", padx=5, pady=5, ipadx=5, ipady=5,)
            self.type_frame = LabelFrame(self.main_frame, text="Select Type")
            self.type_frame.pack(fill="x", expand="yes", anchor="center", padx=5, pady=5, ipadx=5, ipady=5,)
            self.name = Entry(self.name_frame, textvariable=self.varnodename)
            self.name.pack(fill="x", expand="yes", anchor="center", ipadx=5, ipady=5,)
            self.type = ttk.Combobox(self.type_frame, values=self.type_values,
                    textvariable=self.varnewtype, state="readonly")
            self.type.pack(fill="x", expand="yes", anchor="center", ipadx=5, ipady=5,)

            self.ok_btn = ttk.Button(self.btn_frame, text="Ok", style="smallBtn.TButton")
            self.ok_btn.pack(expand="yes", padx=5, pady=5, anchor = "center")
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

class RenameNodeUI(Frame):
    """docstring for CreateNodeUI."""
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.logger = logging.getLogger()
        self.parent = parent
        self.varnodename = StringVar()
        self.main()

    def initiate_var(self):
        try:
            self.varnodename.set("")
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def main(self):
        try:
            self.initiate_var()
            self.main_frame = Frame(self)
            self.main_frame.pack(fill="x", expand="yes", anchor="center")
            self.name = Entry(self.main_frame, textvariable=self.varnodename)
            self.name.pack(side="left", fill="x", expand="yes", padx=5, pady=5, anchor="center", ipadx=5, ipady=5,)
            self.ok_btn = ttk.Button(self.main_frame, text="Ok", style="smallBtn.TButton")
            self.ok_btn.pack(side="right", padx=5, pady=5, ipadx=2, ipady=2, anchor = "w")
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

class ScrollableFrameWithEntry(Frame):
    """docstring for ScrollableFrame."""
    def __init__(self, parent, values, limit=300, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.list_limit = limit
        self.values_ = values.copy() if isinstance(values, list) else values
        self.values = self.values_[-self.list_limit:]
        self.logger = logging.getLogger()
        self.entry_w = []
        self.frame_w = []
        o_image = Image.open(r"images\\delete.png")
        a_image = Image.open(r"images\\add.png")
        img_small = o_image.resize((16,16),  Image.ANTIALIAS)
        img_add_small = a_image.resize((16,16),  Image.ANTIALIAS)
        self.delete_img = ImageTk.PhotoImage(img_small)
        self.add_img = ImageTk.PhotoImage(img_add_small)
        self.main()

    def main(self):
        try:
            if isinstance(self.values, list):
                _canvas_win = Canvas(self, )
                self.main_frame = Frame(_canvas_win, )
            else:
                _canvas_win = Canvas(self, height=60)
                self.main_frame = Frame(_canvas_win, height=60)

            scroll_y_canv = Scrollbar(self, orient="vertical", command=_canvas_win.yview)
            _canvas_win.configure(yscrollcommand=scroll_y_canv.set)
            scroll_y_canv.pack(side="right", fill="y")
            _canvas_win.pack(side="left", fill="both", expand=YES)
            self.parent.update()
            main_frame_id = _canvas_win.create_window((0, 0), window=self.main_frame, anchor="nw")
            self.main_frame.bind("<Configure>", lambda *args: _canvas_win.configure(scrollregion=_canvas_win.bbox("all")))
            _canvas_win.bind("<Configure>", lambda event, arg1=main_frame_id, arg2=_canvas_win: self.resize_frame(event, arg1, arg2))

            ### Entry widget
            if isinstance(self.values, list):
                for _val in self.values:
                    is_invalid_chars = is_invalid_utf8_chars(_val)
                    if not(is_invalid_chars):
                        frame_1 = Frame(self.main_frame)
                        frame_1.pack(fill="x", padx=5, pady=5, ipadx= 5, ipady=5, anchor="nw")
                        entry_1 = Entry(frame_1,)
                        entry_1.pack(fill="x", ipadx=5, expand="yes", ipady=5, side="left")
                        entry_1.insert("1", _val)
                        self.entry_w.append(entry_1)
                        button_1 = ttk.Button(frame_1, image=self.delete_img, command=lambda frame=frame_1: self.delete_widget(frame))
                        button_1.pack(side="left", ipady=5, ipadx=5, anchor="w")
                        self.frame_w.append(frame_1)

                add_btn = ttk.Button(self.main_frame, image=self.add_img, )
                add_btn.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5, anchor="e")
                add_btn.config(command=lambda add_btn=add_btn: self.add_entry_box(add_btn))

            else:
                frame_1 = Frame(self.main_frame, height=15)
                frame_1.pack(fill="both", padx=5, pady=5, ipadx= 5, ipady=5, anchor="nw")
                if self.isIterable(self.values):
                    if "\n" in self.values:
                        entry_1 = Text(frame_1, )
                        entry_1.pack(fill="both", ipadx=5, expand="yes", ipady=5, side="left")
                        entry_1.insert("1.0", self.values)
                    else:
                        entry_1 = Entry(frame_1,)
                        entry_1.pack(fill="x", ipadx=5, expand="yes", ipady=5, side="left")
                        entry_1.insert(END, self.values)
                else:
                    entry_1 = Entry(frame_1,)
                    entry_1.pack(fill="x", ipadx=5, expand="yes", ipady=5, side="left")
                    entry_1.insert(END, str(self.values))

                self.entry_w.append(entry_1)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
    
    def resize_frame(self, event, main_frame_id, _canvas_win,):
        try:
            width = event.width
            _canvas_win.itemconfigure(main_frame_id, width=width)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def isIterable(self, iter_data,):
        try:
            out = iter(iter_data)
            return True
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def delete_widget(self, frame):
        try:
            index = self.frame_w.index(frame)
            frame.destroy()
            ent = self.entry_w[index]
            self.entry_w.remove(ent)
            self.frame_w.remove(frame)
            removed = self.values.pop(index)
            self.logger.debug("Frame Removed: %s, Entry: %s, Values: %s", frame, ent, removed)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def add_entry_box(self, bttn):
        try:
            bttn.pack_forget()
            frame_1 = Frame(self.main_frame)
            frame_1.pack(fill="x",padx=5, pady=5, ipadx= 5, ipady=5, anchor="nw")
            entry_1 = Entry(frame_1,)
            entry_1.pack(fill="x", ipadx=5, expand="yes", ipady=5, side="left")
            self.entry_w.append(entry_1)
            button_1 = ttk.Button(frame_1, image=self.delete_img, command=lambda frame=frame_1: self.delete_widget(frame))
            button_1.pack(side="left", ipadx=5, ipady=5, anchor="w")
            self.frame_w.append(frame_1)
            add_btn = ttk.Button(self.main_frame, image=self.add_img, )
            add_btn.pack(side="right", ipadx=5, ipady=5, padx=5, pady=5, anchor="e")
            add_btn.config(command=lambda add_btn=add_btn: self.add_entry_box(add_btn))
            self.values.append(entry_1.get())
            self.logger.debug("New Values: %s", self.values)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

class TextWizard(Frame):
    """docstring for TextWizard."""
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.main()

    def main(self):
        self.texteditor = Text(self, undo=True,)
        self.texteditor.pack(side="left", fill="both", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
        self.texteditor_scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.texteditor.yview)
        self.texteditor['yscrollcommand'] = self.texteditor_scroll_y.set
        self.texteditor_scroll_y.pack(side="right", fill="y")

class ScrollableFrame(Frame):
    """docstring for ScrollableFrame."""
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.logger = logging.getLogger()
        self.main()

    def main(self):
        try:
            _canvas_win = Canvas(self, )
            self.main_frame = Frame(_canvas_win,)

            scroll_y_canv = Scrollbar(self, orient="vertical", command=_canvas_win.yview)
            _canvas_win.configure(yscrollcommand=scroll_y_canv.set)
            scroll_y_canv.pack(side="right", fill="y")
            _canvas_win.pack(side="left", fill="both",expand="yes", padx=10, pady=10)
            self.parent.update()
            main_frame_id = _canvas_win.create_window((0, 0), window=self.main_frame, anchor="nw")
            self.main_frame.bind("<Configure>", lambda *args: _canvas_win.configure(scrollregion=_canvas_win.bbox("all")))
            _canvas_win.bind("<Configure>", lambda event, arg1=main_frame_id, arg2=_canvas_win: self.resize_frame(event, arg1, arg2))
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def resize_frame(self, event, main_frame_id, _canvas_win,):
        try:
            width = event.width
            _canvas_win.itemconfigure(main_frame_id, width=width)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

class EnableDisableNode(Toplevel):
    """docstring for ScrollableFrame."""
    def __init__(self, parent, *args, **kwargs):
        Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.varuname = StringVar()
        self.varpasswd = StringVar()
        self.close_window = None
        self.logger = logging.getLogger()
        
    def config(self,application_name="DanTe", brandpic = None, close_pop_window =  None, width=400, height=410, x_pos=200, y_pos=100):
        self.close_window = close_pop_window
        self.iconphoto(False, brandpic)
        self.title(application_name + " - Enable Disable Node")
        self.geometry(f'{width}x{height}+{x_pos}+{y_pos}')
        self.parent.wm_attributes("-disabled", True)
        self.focus_set()
        self.transient(self.parent)
        self.protocol("WM_DELETE_WINDOW", lambda *args: close_pop_window(self))

    def main(self):
        try:
            self.varuname.set("")
            self.varpasswd.set("")
            user_pass_lblframe = LabelFrame(self, text="Username/Password")
            user_pass_lblframe.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
            text_lblframe = LabelFrame(self, text="List of Allowed Node(s)")
            text_lblframe.pack(fill="both", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
            btn_frame = LabelFrame(self, text="********")
            btn_frame.pack(fill="x", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

            username_lbl = ttk.Label(user_pass_lblframe, text="Prod Username", anchor="w")
            username_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
            username_ent = ttk.Entry(user_pass_lblframe, textvariable=self.varuname)
            username_ent.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

            password_lbl = ttk.Label(user_pass_lblframe, text="Prod Password", anchor="w")
            password_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
            password_ent = ttk.Entry(user_pass_lblframe, textvariable=self.varpasswd, show="*")
            password_ent.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

            user_pass_lblframe.columnconfigure(1, weight=1)

            self.textwizard_ = Text(text_lblframe, undo=True, height=10, wrap="none")
            self.textwizard_scroll_y = ttk.Scrollbar(
                    text_lblframe, orient=VERTICAL, command=self.textwizard_.yview)
            self.textwizard_scroll_y.pack(
                side="right", fill="y")
            self.textwizard_scroll_x = ttk.Scrollbar(
                text_lblframe, orient=HORIZONTAL, command=self.textwizard_.xview)
            self.textwizard_scroll_x.pack(
                side="bottom", fill="x")
            self.textwizard_.config(
                    yscrollcommand=self.textwizard_scroll_y.set)
            self.textwizard_.config(
                    xscrollcommand=self.textwizard_scroll_x.set)
            self.textwizard_.pack(fill="both", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
            
            
            self.exit_btn = ttk.Button(btn_frame, text="Exit", command=lambda *args: self.close_window(self))
            self.exit_btn.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")
            self.submit_btn = ttk.Button(btn_frame, text="Save")
            self.submit_btn.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5, anchor="center")

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

class DateTimeFrame(Frame):
    """docstring for ScrollableFrame."""
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.logger = logging.getLogger()
        self.calendar_image_file = r"images\crxde_icons\calendar_13_2x.png"
        img_opened = Image.open(self.calendar_image_file)
        resize = img_opened.resize((22, 22))
        self.calendar_image = ImageTk.PhotoImage(resize)
        self.main()

    def main(self):
        try:
            style = ttk.Style(self)
            style.configure(
                "boldLabel.TLabel", font=("Georgia", 14, "bold")
            )
            style.configure("largeText.TEntry",  font=("Georgia", 16, ))
            self.main_frame = Frame(self,)
            self.main_frame.pack(side=LEFT, padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)
            self.date_frame = Frame(self.main_frame)
            self.date_frame.pack(side=LEFT, padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)

            self.cal_entry = ttk.Entry(self.date_frame, justify=RIGHT, font=("Georgia", 12, ), width=10)
            self.cal_entry.pack(side=LEFT, padx=0, pady=5, ipadx=5, ipady=5, anchor=CENTER)
            self.cal_btn = ttk.Button(self.date_frame, image=self.calendar_image, command=self.select_date)
            self.cal_btn.pack(side=LEFT, padx=0, pady=5, ipadx=0, ipady=0, anchor=CENTER)

            self.time_frame = Frame(self.main_frame)
            self.time_frame.pack(side=LEFT, padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER)
            self.cal_hour_entry = ttk.Entry(self.time_frame, width=2)
            self.cal_hour_entry.pack(side=LEFT, padx=0, pady=5, ipadx=5, ipady=5, anchor=CENTER)
            self.colon_label1 = ttk.Label(self.time_frame,text=":", style="boldLabel.TLabel", anchor=CENTER)
            self.colon_label1.pack(side=LEFT, padx=0, pady=5, ipadx=5, ipady=5, anchor=CENTER)
            self.cal_min_entry = ttk.Entry(self.time_frame,  width=2)
            self.cal_min_entry.pack(side=LEFT, padx=0, pady=5, ipadx=5, ipady=5, anchor=CENTER)
            self.colon_label2 = ttk.Label(self.time_frame,text=":", style="boldLabel.TLabel", anchor=CENTER)
            self.colon_label2.pack(side=LEFT, padx=0, pady=5, ipadx=5, ipady=5, anchor=CENTER)
            self.cal_sec_entry = ttk.Entry(self.time_frame,  width=2)
            self.cal_sec_entry.pack(side=LEFT, padx=0, pady=5, ipadx=5, ipady=5, anchor=CENTER)
            self.dot_label = ttk.Label(self.time_frame,text=".", style="boldLabel.TLabel", anchor=CENTER)
            self.dot_label.pack(side=LEFT, padx=0, pady=5, ipadx=5, ipady=5, anchor=CENTER)
            self.cal_microsec_entry = ttk.Entry(self.time_frame, width=3 )
            self.cal_microsec_entry.pack(side=LEFT, padx=0, pady=5, ipadx=5, ipady=5, anchor=CENTER)
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def select_date(self):
        try:

            def setlowerbound():
                self.cal_entry["state"] = "normal"
                self.cal_entry.delete(0, END)
                self.cal_entry.insert("end", cal.selection_get())
                caltop.destroy()
                self.cal_entry["state"] = "disabled"

            btn_x = self.cal_btn.winfo_rootx()
            btn_y = self.cal_btn.winfo_rooty()

            caltop = Toplevel(self.parent)
            caltop.geometry("300x300+{}+{}".format(btn_x, btn_y))
            caltop.title("Select Date")
            # caltop.iconphoto(False, self.brandpic)
            caltop.transient(self.parent)
            t_day = datetime.now().day
            t_month = datetime.now().month
            t_year = datetime.now().year
            cal = Calendar(
                caltop,
                font="Georgia",
                selectmode="day",
                cursor="arrow",
                year=t_year,
                month=t_month,
                day=t_day,
            )
            cal.pack(fill="both", expand="yes")
            Button(caltop, text="Ok", width=10, command=setlowerbound).pack()
            # Button(caltop, text="Cancel", width=10, command=lambda *args: caltop.destroy()).pack()
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def set_date_time(self, date_, time_):
        try:
            self.cal_entry.delete(0, END)
            self.cal_hour_entry.delete(0, END)
            self.cal_min_entry.delete(0, END)
            self.cal_sec_entry.delete(0, END)
            self.cal_microsec_entry.delete(0, END)

            self.cal_entry.insert(END, date_)
            self.cal_hour_entry.insert(END, time_[0])
            self.cal_min_entry.insert(END, time_[1])
            self.cal_sec_entry.insert(END, time_[2])
            self.cal_microsec_entry.insert(END, time_[3])

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

class PopUpWithTreeViewData(Toplevel):
    def __init__(self, parent, data, brandpic, revert_prop, *args, **kwargs): #brandpic
        Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.logger = logging.getLogger()
        self.data = data.copy() if isinstance(data, (list, tuple, dict)) else data
        self.actions = {
            "Removed From CACHE": "Delete",
            "Paste": "Paste",
            "Added Property": "Add",
            "Update": "Update"
        }
        self.brandpic = brandpic
        self.revert_prop = revert_prop
        self.main()
    
    def main(self):
        self.title("DanTe" + " - View")
        self.iconphoto(False, self.brandpic)
        self.geometry(f'600x350+300+150')
        self.parent.wm_attributes("-disabled", True)
        self.focus_set()
        self.transient(self.parent)
        self.protocol("WM_DELETE_WINDOW", lambda *args: self.close_pop_window())
        
        ###Style
        style = ttk.Style()
        style.configure("changeFont.Treeview", highlightthickness=0, bd=0, font=('Georgia', 11)) # Modify the font of the body
        style.configure("changeFont.Treeview.Heading", font=('Georgia', 13,'bold')) # Modify the font of the headings
        ##End style

        btn_frame = Frame(self, )
        btn_frame.pack(expand=YES, fill=X, padx=5, pady=5, ipadx=5, ipady=5)

        revert_selected_btn = ttk.Button(btn_frame, text="Revert Selected",)
        revert_selected_btn.pack(side=RIGHT, padx=5, pady=5, ipadx=5, ipady=5, anchor=E)
        
        data_frame = Frame(self, )
        data_frame.pack(expand=YES, fill=BOTH, padx=5, pady=5, ipadx=5, ipady=5)
        tab_data = ttk.Treeview(data_frame, show="headings", column=("Payload", "Property", "Value", "Action"), style="changeFont.Treeview")
        scroll_y = ttk.Scrollbar(data_frame, orient=VERTICAL, command=tab_data.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x = ttk.Scrollbar(data_frame, orient=HORIZONTAL, command=tab_data.xview)
        scroll_x.pack(side="bottom", fill="x")
        tab_data.config(yscrollcommand=scroll_y.set)
        tab_data.config(xscrollcommand=scroll_x.set)
        
        tab_data.column("Payload", minwidth=150,)
        tab_data.column("Property", width=50, anchor=CENTER)
        tab_data.column("Value", width=50, anchor=CENTER)
        tab_data.column("Action", width=50, anchor=CENTER)

        tab_data.heading("Payload", text="Payload",)
        tab_data.heading("Property", text="Property",)
        tab_data.heading("Value", text="Value",)
        tab_data.heading("Action", text="Action",)

        tab_data.pack(fill=BOTH, expand=YES)
        self.insert_into_table(tab_data, self.data)
        revert_selected_btn.config(command=lambda *args: self.revert_main_prop(tab_data))

    
    def close_pop_window(self):
        self.parent.focus_set()
        self.parent.wm_attributes("-disabled", False)
        self.destroy()
       
    def insert_into_table(self, tabdata, datas):
        try:
            for iid, data in enumerate(datas):
                action_ = self.actions.get(data.get("action", "Invalid"),None)
                if action_ is not None:
                    payload_ = data.get("payload", "Invalid")
                    property_ = data.get("property", "Invalid")
                    value_ = data.get("value", "Invalid")
                    to_be_inserted = (payload_, property_, value_, action_, )
                    self.logger.debug("Data inserted: "+ str(to_be_inserted))
                    tabdata.insert("", "end",iid=iid+1, values = to_be_inserted)
            self.logger.debug("Completed!!")   
        except:
            self.logger.error("Below Exception occurred.\n", exc_info=True)

    def revert_main_prop(self, tabledata):
        try:
            selected_items = list(tabledata.selection())
            selected_items.sort(reverse=True)
            actions_performed = []
            for item in selected_items:
                _action = self.data[int(item)-1]
                actions_performed.append(_action)
                self.data.remove(_action)

            self.revert_prop(actions_performed)
            tabledata.delete(*tabledata.get_children())
            self.insert_into_table(tabledata, self.data)

        except:
            self.logger.error("Below Exception occurred.\n", exc_info=True)
