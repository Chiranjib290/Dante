# from dpe_crx_de_lite import DPECrxDeLiteApp
# from predefined_dpe_reports import PreDefinedReports
# from validate_redirect_content_path import ContentPathValidator
# from viewpoint_metadata_clean import MetaDataClean

# b = DPECrxDeLiteApp("https://dpe-stg.pwc.com","shouvik.d.das@in.pwc.com","pikachu")
# query="""/jcr:root/content/pwc/rm/en/shouvik//*
# [
# (@jcr:title = 'l2landing')
# ]
# """
# out = b.search_or_query(query=query)
# print(out)

# pr = PreDefinedReports("https://dpe-qa.pwc.com", "shouvik.d.das@in.pwc.com", "boltaction")
# m = pr.pwc_form_field_order_data_v2("online arch",["formType"], "am", 2019, "october","")
# print(m)

# https://entrepreneurs.pwc.fr/en/legal/privacy-statement.html
# /content/pwc/fr/en/website/services-entrepreneurs_pwc_fr/legal/privacy-statement.html$
# https://www.pkf-arsilon.com/


# b = ContentPathValidator("shouvik","password")
# out = b.source_not_same_as_target("/content/pwc/fr/en/website/services-entrepreneurs_pwc_fr/legal/privacy-statement.html$","https://www.pkf-arsilon.com/","production")
# print(out)

# bn = MetaDataClean("C:\\Users\\shouvikd256\\Desktop\\DPE\\DPE Automation\\Worker\\multi_column.csv","C:\\Users\\shouvikd256\\Desktop\\DPE\\DPE Automation\\Worker")
# out = bn.clean_data()

# from dpe_crx_search_ui import EnableDisableNode
# from dpe_crx_de_lite import DPECrxDeLiteApp
# from tkinter import *
# from tkinter import PhotoImage

# root = Tk()
# BRAND_PIC_FILE = "logo\\logo.png"
# ALLOWED_CRX_DE_PATH = [
#             "/apps/pwc/i18n", "/content/dam",
#             "/content/pwc/", "/content/cq:tags",
#             "/etc/map/http", "/home", "/var/workflow/instances"
#             ]


# def closeme(popup):
#     root.focus_set()
#     root.wm_attributes("-disabled", False)
#     popup.destroy()

# top = EnableDisableNode(root)
# top.config(brandpic = PhotoImage(file=BRAND_PIC_FILE), close_pop_window=closeme)
# top.main()
# for line in ALLOWED_CRX_DE_PATH:
#     top.textwizard_.insert("end",line)
#     top.textwizard_.insert("end","\n")

# resp = DPECrxDeLiteApp.password_validator("shouvik.d.das@in.pwc.com","boltactio")
# print(resp)

# root.mainloop()

# from editconfig import EditConfig
# import pickle

# ALLOWED_CRX_DE_PATH = [
#             "/apps/pwc/i18n", "/content/dam",
#             "/content/pwc/", "/content/cq:tags",
#             "/etc/map/http", "/home", "/var/workflow/instances"
#             ]

# file = "configfiles\\picked_test.dat"

# edcfg = EditConfig()
# out = edcfg.update_pickle_data(ALLOWED_CRX_DE_PATH, file)
# print(out)

# data = edcfg.read_pickle_data(file)
# print(data)

# from dpe_crx_search_ui import ScrollableFrameWithEntry
# from tkinter import *

# root = Tk()
# values_ = '''<!-- OneTrust Cookies Consent Notice start for www.pwc.fr -->

# <script src="https://cdn.cookielaw.org/scripttemplates/otSDKStub.js" data-language="fr-FR" type="text/javascript" charset="UTF-8" data-domain-script="49cc3ef2-a4fc-48e7-9b4f-cc88fac2559c-test" ></script>
# <script type="text/javascript">
# function OptanonWrapper() { }
# </script>
# <!-- OneTrust Cookies Consent Notice end for www.pwc.fr -->'''
# values_ = ["1", "2", "3"]
# values_ = "Shouvik"
# frame = ScrollableFrameWithEntry(root, values_)
# frame.pack(fill=BOTH, expand=YES)
# l1 = Entry(root)
# l1.pack()
# t1 = Text(root, height=10)
# t1.pack()
# def get_data():
#     class_ = frame.entry_w[0].winfo_class()
#     if class_ == "Text":
#         print(class_)
#         val = frame.entry_w[0].get("1.0", END)
#     else:
#         val = frame.entry_w[0].get()
#     print(val)
#     l1.insert(END, val)

# def fetch_data():
#     data = l1.get()
#     t1.insert("1.0", data)

# btn = Button(root, text="Ok",command=get_data)
# btn.pack()
# btn1 = Button(root, text="GET",command=fetch_data)
# btn1.pack()
# root.mainloop()


# data = [{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/kim-van-cotthem/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"kim van cotthem","cq:lastReplicationAction":"Activate","cq:lastReplicatedBy":"manten.modest.g.deville@be.pwc.com","jcr:lastModifiedBy":"manten.modest.g.deville@be.pwc.com","cq:lastReplicated":"Tue Nov 29 2022 10:11:00 GMT+0000","jcr:description":"","contentFragment":True,"cq:name":"kim-van-cotthem","jcr:lastModified":"Tue Nov 29 2022 10:10:52 GMT+0000","lastFragmentSave":"Tue Nov 29 2022 10:10:52 GMT+0000","cq:parentPath":"/content/dam/pwc/be/en/content-fragments/contacts/k"},{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/kurt-marichal/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"kurt-marichal","cq:lastReplicationAction":"Activate","migrated":True,"cq:lastReplicatedBy":"migration","cq:lastReplicated":"Fri Oct 14 2022 16:15:33 GMT+0000","contentFragment":True,"pagereference_be_en":"/content/pwc/be/en/contacts/k/kurt-marichal"},{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/koen-vermoere/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"koen-vermoere","cq:lastReplicationAction":"Activate","migrated":True,"cq:lastReplicatedBy":"migration","cq:lastReplicated":"Fri Oct 14 2022 16:15:33 GMT+0000","contentFragment":True,"pagereference_be_en":"/content/pwc/be/en/contacts/k/koen-vermoere"},{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/kurt-cappoen/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"kurt-cappoen","cq:lastReplicationAction":"Activate","migrated":True,"cq:lastReplicatedBy":"migration","cq:lastReplicated":"Fri Oct 14 2022 16:15:33 GMT+0000","contentFragment":True,"pagereference_be_en":"/content/pwc/be/en/contacts/k/kurt-cappoen"},{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/koen-hens/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"koen-hens","cq:lastReplicationAction":"Activate","migrated":True,"cq:lastReplicatedBy":"migration","cq:lastReplicated":"Fri Oct 14 2022 16:15:33 GMT+0000","contentFragment":True,"pagereference_be_en":"/content/pwc/be/en/contacts/k/koen-hens"},{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/klaas-neven/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"klaas-neven","cq:lastReplicationAction":"Activate","migrated":True,"cq:lastReplicatedBy":"dpesystem","cq:lastReplicated":"Tue Nov 08 2022 20:25:22 GMT+0000","contentFragment":True,"pagereference_be_en":"/content/pwc/be/en/contacts/k/klaas-neven"},{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/kristin-de-rudder/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"kristin-de-rudder","cq:lastReplicationAction":"Activate","migrated":True,"cq:lastReplicatedBy":"migration","cq:lastReplicated":"Fri Oct 14 2022 16:15:33 GMT+0000","contentFragment":True,"pagereference_be_en":"/content/pwc/be/en/contacts/k/kristin-de-rudder"},{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/koen-cobbaert/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"koen-cobbaert","cq:lastReplicationAction":"Activate","migrated":True,"cq:lastReplicatedBy":"migration","cq:lastReplicated":"Fri Oct 14 2022 16:15:33 GMT+0000","contentFragment":True,"pagereference_be_en":"/content/pwc/be/en/contacts/k/koen-cobbaert"},{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/kristof-vandepoorte/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"kristof-vandepoorte","cq:lastReplicationAction":"Activate","migrated":True,"cq:lastReplicatedBy":"migration","cq:lastReplicated":"Fri Oct 14 2022 16:15:33 GMT+0000","contentFragment":True,"pagereference_be_en":"/content/pwc/be/en/contacts/k/kristof-vandepoorte"},{"jcr:path":"/content/dam/pwc/be/en/content-fragments/contacts/k/koen-de-grave/jcr:content","jcr:primaryType":"dam:AssetContent","jcr:mixinTypes":["cq:ReplicationStatus"],"jcr:title":"koen-de-grave","cq:lastReplicationAction":"Activate","migrated":True,"cq:lastReplicatedBy":"migration","cq:lastReplicated":"Fri Oct 14 2022 16:15:33 GMT+0000","contentFragment":True,"pagereference_be_en":"/content/pwc/be/en/contacts/k/koen-de-grave"}]

# for each in data:
#     for _key, _value in each.items():
#         # print(_key, _value)
#         if _key.startswith("pagereference"):
#             print(_key, _value)

# for each in data:
#     print(each.items())

# from predefined_dpe_reports import PreDefinedReports
# pd = PreDefinedReports("https://dpe-stg.pwc.com", "shouvik.d.das@in.pwc.com", "roguepikachu")

# print(pd.contact_fragment_page_reference_report("be"))


from vp_asset_update_ui import ViewpointAssetUpdate

vp = ViewpointAssetUpdate()
