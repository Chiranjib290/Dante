import requests
import xlrd


ip = 'https://dpe-stg.pwc.com'
file = 'unames.xlsx'
newpassword="Password@123"
username="aman.pratiush@in.pwc.com"
password = "Password@123"

def reset_for_one(extuname):    
    requesteduserpath=requests.get(ip+'/bin/querybuilder.json?path=/home/users&1_property=rep:authorizableId&1_property.value='+extuname,auth=(username, password),timeout=120.0)
    val=requesteduserpath.json()
    hits=val["hits"]
    path=[x["path"] for x in hits]
    user_path=path[0]
    post_data={
    "rep:password":newpassword
    }
    if requesteduserpath.status_code==200:
        resetpasswordreq=requests.post(ip+"/"+user_path,data=post_data,auth=(username, password),timeout=120.0)
        if resetpasswordreq.status_code==200:
            print("Password reset Successfull")
        else:
            print(f"Password reset cannot be completed. Error for {extuname}") 


def get_all_unames():
    try:
        output_data = set()
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_index(0)
        numrows = sheet.nrows
        for i in range(1, numrows):
            output_data.add(str(sheet.cell_value(i, 0)))
        return list(output_data)
    except Exception as e:
        print(e)


for extuname in get_all_unames():
    #print(extuname)
    reset_for_one(extuname)    
