# pylint: disable=bare-except
import time
from datetime import datetime
import json
import logging
from urllib.parse import quote
import requests
import xlrd
import re


class GetDataFromPayload:
    def __init__(self, ip, user, passwd):
        self.ip = ip.strip()
        self.user = user.strip()
        self.passwd = passwd.strip()

        self.configdata = self.opencode("configfiles\\config.json")
        self.loglevel = self.configdata["loglevel"]
        self.sleeptime = self.configdata["sleeptime"]
        self.timeout = self.configdata["timeout"]
        frmt_crnt_date = datetime.now().strftime("%m%d%Y")
        self.logfile = "logs\\" + "mainlogfile_"+frmt_crnt_date+".log"
        log_level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        logging.basicConfig(filename=self.logfile, filemode='a',
                            level=log_level[self.loglevel], format='%(asctime)s - %(name)s - {%(module)s : %(funcName)s} - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level[self.loglevel])
        self.wfoperationdata = self.opencode("configfiles\\operationcode.json")

    def opencode(self, file):
        """
        Open the Operation Code from designated Files
        """
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def removetrailingspecialchar(self, val):
        try:
            val = str(val)
            pat = "^[\$\?\@\#\%\^\&\*\(\)\+\=\~\[\]\:\;\\\/\<\>\,\.]$"
            if(val != ""):
                while(re.match(pat,val[-1])):
                    val = val[0:len(val)-1]

            return val
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return val

    def exceltolist(self, file):
        """ Convert the excel data into userfriendly List Data """

        try:
            self.logger.debug("Excel File %s", str(file))
            url_list = []
            work_book = xlrd.open_workbook(file)
            work_sheet = work_book.sheet_by_index(0)
            num_rows = work_sheet.nrows
            for i in range(1, num_rows):
                url = work_sheet.cell_value(i, 0)
                if url.strip() != "":
                    url_list.append(url)
            self.logger.debug(url_list)
            return url_list
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def retrievePayload(self, query):
        """ Retrieve The Payload from Query """
        try:
            self.logger.debug("Query Received: %s",str(query))
            payloadlist = []

            # querylist = [x.strip() for x in query.split(",")]
            # querylist_cleaned = list(set(querylist))
            # querylist_cleaned.sort()

            # separator = "&"
            # out = separator.join(querylist_cleaned)

            # queryurl = self.ip + "/bin/querybuilder.json?" + query
            queryurl = self.ip + self.wfoperationdata["query builder link"] + "?" + query

            self.logger.debug("Formatted Query: %s", queryurl)
            resp_data = requests.get(queryurl, auth=(
                self.user, self.passwd), timeout=self.timeout)

            if(resp_data.status_code == 200):
                if(resp_data.json()["results"] > 0):
                    data_t = resp_data.json()["hits"]
                    payloadlist.append(
                        "Total Hits: "+str(resp_data.json()["total"]))
                    for dt in data_t:
                        payloadlist.append(dt["path"])
                # payloadlist.append("Total Hits: "+str(resp_data.json()["total"]))
            #data.append("Workign Fine")
            elif(resp_data.status_code == 401):
                payloadlist.append(
                    "Wrong username and Password - Http status " + str(resp_data.status_code))
            else:
                payloadlist.append(
                    "Some Error occured while connecting. Http Status " + str(resp_data.status_code))

            self.logger.debug("Output: %s", str(payloadlist))

            return payloadlist

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def get_json_data(self, query, all_cols, is_jcr_prop):
        try:
            payloadlist = None
            self.logger.debug("Query Received: %s", str(query))
            if is_jcr_prop==1:
                properties_list = ["jcr:content/"+x.strip() for x in all_cols.split(",") if x.strip() != ""]
            else:
                properties_list = [x.strip() for x in all_cols.split(",") if x.strip() != ""]
            properties_list.insert(0,"jcr:path")
            properties = "+".join(properties_list)

            # queryurl = self.ip + "/bin/querybuilder.json?" + query + "&p.hits=selective&p.properties="+properties
            # self.wfoperationdata["query builder link"]
            queryurl = self.ip + self.wfoperationdata["query builder link"] + "?" + query + "&p.hits=selective&p.properties="+properties
            self.logger.debug("Formatted Query: "+str(queryurl))

            resp_data = requests.get(queryurl, auth=(
                self.user, self.passwd), timeout=self.timeout)

            if(resp_data.status_code == 200):
                if(resp_data.json()["results"] > 0):
                    payloadlist = resp_data.json()
                else:
                    payloadlist = f"No Data has been retrieved - Http status {resp_data.status_code}"
            elif(resp_data.status_code == 401):
                payloadlist = "Wrong username and Password - Http status " + str(resp_data.status_code)
            else:
                payloadlist = "Some Error occured while connecting. Http Status " + str(resp_data.status_code)

            self.logger.debug("Output: "+str(payloadlist))

            return payloadlist

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def getPropDataURL(self, payload, prop, is_jcr_prop):
        """ Retrieve The Property from URL """
        try:

            key_rt = [pro.strip() for pro in prop.split(",")]
            output_data = []
            payload = self.removetrailingspecialchar(payload)
            output_data.append(payload)
            url = ""
            if is_jcr_prop == 1:
                url = self.ip + payload + "/jcr:content.json"
            else:
                url = self.ip + payload + ".json"

            response = requests.get(url, auth=(
                self.user, self.passwd), timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()

                for k in key_rt:
                    if k in data:
                        if k.strip() == "pwcFormFieldOrder":
                            pwc_form_field_order_data = data[k]
                            other_prop = [x.strip() for x in pwc_form_field_order_data.split(",") if x.strip() != ""]
                            out_pwc_form_data = ""
                            counter = 0
                            for each in other_prop:
                                if each in data:
                                    out_pwc_form_data = out_pwc_form_data + str(each)+": "+ str(data[each])
                                counter += 1
                                if len(other_prop) != counter:
                                    out_pwc_form_data = out_pwc_form_data + ", "

                            output_data.append(str(out_pwc_form_data))

                        else:
                            _data = data[k]
                            to_be_pushed = None
                            if isinstance(_data, list):
                                to_be_pushed = ",".join(_data)
                            else:
                                to_be_pushed = _data

                            output_data.append(to_be_pushed)
                    else:
                        output_data.append("Invalid Property")
            else:
                for k in key_rt:
                    output_data.append(f"Error - {response.status_code}")

            time.sleep(self.sleeptime/2)
            return output_data

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def getPropDataList(self, payloadlist, prop, is_jcr_prop):
        """ Retrieve The Property value from List """
        try:
            # headers = [pro.strip().title() for pro in prop.split(",")]
            # headers.insert(0,"Payload")
            output_data = []
            # output_data.append(headers)

            for payload in payloadlist:
                data = self.getPropDataURL(payload, prop, is_jcr_prop)
                output_data.append(data)

            return output_data

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def get_bulk_data(self,query_data, propvalue, is_jcr_prop):
        try:
            msg = ""
            if is_jcr_prop==1:
                proplist = ["jcr:content/"+str(x).strip() for x in propvalue.split(",") if str(x).strip() != ""]
            else:
                proplist = [str(x).strip() for x in propvalue.split(",") if str(x).strip() != ""]

            # dpe_bulk_query_url = "/etc/importers/bulkeditor/query.json?query="
            dpe_bulk_query_url = self.wfoperationdata["bulk editor link"] + "?query="
            query_data_enc = quote(query_data, safe='')
            current_time_in_ms = int(time.time() * 1000)
            prop = "&tidy=true&cols=" + ",".join(proplist)+"&_dc="+str(current_time_in_ms)
            final_query = query_data_enc+prop
            
            url = self.ip + dpe_bulk_query_url + final_query
            # print(url)

            resp_data = requests.get(url, auth=(self.user, self.passwd), timeout=self.timeout)
            time.sleep(self.sleeptime)

            if resp_data.status_code == 200:
                msg = resp_data.json()
            elif(resp_data.status_code == 401):
                msg = "Wrong username and Password - Http status " + str(resp_data.status_code)
            else:
                msg = "Some Error occured while connecting. Http Status " + str(resp_data.status_code)

            self.logger.debug("Output: %s", str(msg))

            return msg
            
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return ""
