
uname = "chiranjib.bhattacharyya@in.pwc.com"
passwd = "Change@123456"

import requests
url='https://dpe.pwc.com/bin/querybuilder.json?1_property=sling:redirect&1_property.operation=exists&2_property=sling:status&2_property.value=301&p.limit=-1&path=/etc/map/http/pwc-az-origin-extpubv3.pwc.com/content/pwc/ru'
data_in=requests.get(url,auth=(uname, passwd)).json()

#print(data_in)


hits=data_in["hits"]
path=[x["path"] for x in hits]

#print(path)
# for x in data_in:
#     print(x['hits'])

import xlsxwriter

filename='Redirect_RU.xlsx'
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet()
row = 0
for x in path :
    print('adding value')
    worksheet.write(row+1,0,x)
    row = row + 1

workbook.close()