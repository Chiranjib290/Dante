import requests
import xlrd
import xlsxwriter
from time import sleep

# def read_country_name( file):
#     try:
#         output_data = []
#         wb = xlrd.open_workbook(file)
#         sheet = wb.sheet_by_index(0)
#         numrows = sheet.nrows
#         for i in range(1, numrows):
#             output_data.append(sheet.cell_value(i, 0))
#         return output_data
#     except Exception as e:
#         print("Below Exception occurred\n")
#         print(e)
#         return []

# all_country = read_country_name("configfiles\\all_territories.xlsx")
rowcount=0
country_code = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16',
    '17','18','19','20','21','22','23','24','25','26','27','28','29']
save_file = "configfiles\\strategyand_mapping-stg.xlsx"
workbook = xlsxwriter.Workbook(save_file)
worksheet = workbook.add_worksheet()

worksheet.write(rowcount,0,"Payload")
worksheet.write(rowcount,1,"Prod URL")
worksheet.write(rowcount,2,"Stage URL")
worksheet.write(rowcount,3,"QA URL")

rowcount += 1

for each_country in country_code:
    try:
        host = "https://dpe.pwc.com"
        new_url = host + "/content/pwc/global/referencedata/territories/" + each_country + ".json"

        out = requests.get(new_url, auth=("shouvik.d.das@in.pwc.com","boltaction"), timeout = 10)
        sleep(2)

        output_url_status = out.status_code
        final_url = ""
        final_stg_url = ""
        final_qa_url = ""

        if output_url_status == 200:
            final_url = "https://www.strategyand.pwc.com/" + out.json().get("territoryCode","")
            final_stg_url = "https://www-strategyand-pwc-com-dpe-staging.pwc.com/" + out.json().get("territoryCode","")
            final_qa_url = "https://www-strategyand-pwc-com-dpe-qa.pwc.com/" + out.json().get("territoryCode","")
            rowcount += 1

            print(final_url+" - "+final_stg_url+" - "+final_qa_url)
            worksheet.write(rowcount,0,"/content/pwc/"+str(each_country))
            worksheet.write(rowcount,1,final_url)
            worksheet.write(rowcount,2,final_stg_url)
            worksheet.write(rowcount,3,final_qa_url)
        else:
            print("Error")

    except Exception as e:
        print(e)


workbook.close()
    
# _url = "https://dpe-qa.pwc.com/crx/de/query.jsp?_dc=1619587582701&_charset_=utf-8&type=JCR-SQL2&stmt=SELECT%20%5Bjcr%3Apath%5D%20FROM%20%5Bnt%3Aunstructured%5D%20AS%20comp%20WHERE%20ISDESCENDANTNODE(comp%2C%20%22%2Fcontent%2Fpwc%2Fglobal%2Freferencedata%2Fterritories%22)%20%20AND%20comp.%5Bjcr%3Apath%5D%20LIKE%20%22%25%2Fwebsite%2F%25%22&showResults=true"
# _authen = ("shouvik.d.das@in.pwc.com","reset123")

# data = requests.get(_url, auth=_authen, timeout=10)

# if data.status_code == 200:
#     output = data.json()["results"]
#     for path in output:
#         print(path["path"])
