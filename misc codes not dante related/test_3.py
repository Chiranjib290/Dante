# from tkinter import *
# from dpe_crx_search_ui import *
# from dpe_crx_de_lite import *
# import tkinter.font as tkFont
# from logging_screen import ViewpointDataCleaner
# from PIL import Image, ImageTk

import logging
LOG_FILE = "logs\\test_file.log"

# root = Tk()
# root.geometry("+100+200")
# root.minsize(500, 500)
# screen_height = root.winfo_screenheight()
# print(screen_height)
# root.maxsize(500, screen_height)
# def fetch_search_key():
#     crx_de = DPECrxDeLiteApp("https://dpe-stg.pwc.com", "shouvik.d.das@in.pwc.com", "pikachu")
#     out = crx_de.search_or_query(query = "SELECT [jcr:path] FROM [nt:unstructured] AS comp WHERE ISDESCENDANTNODE(comp, '/content/usergenerated/content/pwc') AND [formtoprocess]='true'  AND comp.[status]='Ready for processing' AND comp.[jcr:path] LIKE '%/2020/10/%'")
#     for each in out:
#         l = Label(bn.result_frame.main_frame, text=each, wraplength=500, justify="left", fg="blue", cursor="hand2")
#         l.pack(ipadx=5, ipady=5, padx=5, pady=5, anchor="w", )
#         f = tkFont.Font(l, l.cget("font"))
#         f.configure(underline = True)
#         l.configure(font=f)

# def hepatik():
#     v = tkFont.Font().measure("Lovely lady with low horn")
#     print(v)

# sample_btn = Button(root, text="Ok", command=fetch_search_key)
# # sample_btn.pack(anchor="center", ipadx=10)
# tree = ttk.Treeview(root, show="tree")
# tree.pack(side=LEFT, fill="both", expand="yes")
# bn = SearchDPEorQuery(root, "search")
# bn.pack(side=LEFT, padx=10, pady=10, fill="both",expand="yes", anchor="w")
# bn.result_frame.main_frame.config(bg="red")
# bn.export_btn.config(command=hepatik)

# bm = ViewpointDataCleaner(root, "./logo/logo.png", "debug")
# bm.set_date_time("2017-05-22", (12,23,43,344))
# bm.pack()



# img_x = Image.open(r"images\crxde_icons\calendar_13_2x.png")
# img_c = img_x.resize((16,16))

# spin = Spinbox(root, from_ = 1, to=40, width=3, font=("Georgia", 16, ))
# spin.pack()

# def get_me():
#     print(bm.cal_entry.get())
#     print(spin.get())

# btn = Button(root, text="Get", command=get_me)
# btn.pack()

# img = ImageTk.PhotoImage(img_c)

# btn1 = Button(root, image=img).pack()
# from time import sleep
# for counter in range(30):
#     Label(root, text=f"Hello {counter}").pack()
#     root.update()
#     sleep(1)

# width = root.winfo_width()
# height = root.winfo_height()

# print(width, height, sep=" - ")

# root.mainloop()

from tkinter import *
# from dante_main_app import DPESingleRedirect
from vp_asset_update_ui import ViewpointAssetUpdate

# BRAND_PIC_FILE = 
logger = logging.getLogger()
logging.basicConfig(handlers=[logging.FileHandler(filename=LOG_FILE, mode='a+', encoding='utf-8')],
                            format='%(asctime)s -> %(name)s -> {%(module)s : %(funcName)s} -> %(lineno)d -> %(levelname)s -> %(message)s', level=logging.DEBUG)


root = Tk()
print("Started")
# brandpic = PhotoImage(file=BRAND_PIC_FILE)
def close_popup_window(modal_window, master):
    try:
        master.state('zoomed')
        master.deiconify()
        master.update()
        master.focus_set()
        master.wm_attributes("-disabled", False)
        modal_window.destroy()
        logger.info("Working")
    except:
        logger.error("Below Exception occured: ", exc_info=True)

vp = ViewpointAssetUpdate(root)
print("Running")
vp.config(close_pop_window=close_popup_window)
# vp.state('zoomed')
root.withdraw()
root.mainloop()
