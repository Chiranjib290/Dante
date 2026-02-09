import json
import logging
import requests
from time import sleep, time
from urllib.parse import quote

class FormDataMarketingConsent:
    def __init__(self,ip,uname, passwd):
        """ Initializing the Class, Usage :  PreDefinedReports(ip,username, password)"""

        self.logger = logging.getLogger(__name__)
        self.ip = ip.strip()
        self.user = uname.strip()
        self.passwd = passwd.strip()
        self.configdata = self.opencode("configfiles\\config.json")
        self.loglevel = self.configdata.get("loglevel","info")
        self.sleeptime = float(self.configdata.get("sleeptime","1.0"))
        self.timeout = float(self.configdata.get("timeout", "20"))
        log_level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        self.logger.setLevel(log_level[self.loglevel])
        self.wfoperationdata = self.opencode("configfiles\\operationcode.json")
        self.logger.debug("Configuration data : " + str(self.configdata))
        self.logger.debug("Operation data : " + str(self.wfoperationdata))

    def set_uname_pass(self,uname,passwd):
        try:
            self.user = uname
            self.passwd = passwd
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def join_list(self, sep, input_):
        try:
            self.logger.debug("Input List: "+str(input_))
            out = ""
            if isinstance(input_, list):
                for count, pr_ in enumerate(input_):
                    if count == len(input_) - 1:
                        out += str(pr_)
                    else:
                        out += str(pr_) + sep
                self.logger.debug("Final: "+out)
                return out
            else:
                return input_

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return input_

    def opencode(self, file):
        """ Open JSON Settings File """

        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def get_dict_data(self, _key, _data):
        try:
            val = None
            if _key in _data:
                val = _data[_key]
            return val
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def reform_data_in_list(self, _data, props):
        try:
            _data_list = _data["hits"]

            out_data = []
            for each in _data_list:
                chunks = []
                for _key in each:
                    if _key == "jcr:content":
                        for props in each[_key]:
                            chunks.append(each[_key][props])
                    else:
                        chunks.append(each[_key])
                out_data.append(chunks)
            return out_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def form_selector(self, **kwargs):
        try:
            form_name = self.get_dict_data("form_name", kwargs)
            territory = self.get_dict_data("territory", kwargs)
            props = self.get_dict_data("props", kwargs)

            report_data = None
            report_data = self.forms_report(form_name,territory, props)
            self.logger.debug("Retrieved Data " +str(report_data))

            return report_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)



    def forms_report(self, form_name,territory, cols):
        try:
            content_root = self.wfoperationdata.get("content root", "/content/pwc")
            query_builder = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
            full_path = content_root + "/" +territory
            enc_path = quote(full_path, safe='')
            cleaned_cols = [x.strip() for x in cols if x.strip() != ""]
            cleaned_cols.insert(0,"jcr:path")
            col_data = "+".join(cleaned_cols)
            outval = None
            msg = None
            if form_name=="BottomKick Form":
                #filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) + "&1_property=onlineFormType&1_property.value=bottomKick&p.hits=selective"
                filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) + "&1_property=onlineFormType&1_property.operation=equals&1_property.value=bottomKick&2_property=type&2_property.operation=unequals&2_property.value=eventForm&p.hits=selective"

            elif form_name=="Event Form":
                #filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) + "&1_property=onlineFormType&1_property.value=simple&2_property=type&2_property.operation=unequals&2_property.value=eventForm&p.hits=selective"
                filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) + "&property=type&property.value=eventForm&p.hits=selective"

            elif form_name=="Online Forms":
                #filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) + "&1_property=type&1_property.value=eventForm&p.hits=selective" 
                filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) + "&1_property=onlineFormType&1_property.operation=equals&1_property.value=simple&2_property=type&2_property.operation=unequals&2_property.value=eventForm&p.hits=selective"

            elif form_name=="All Form Types":
                #filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) +"&group.1_group.property=onlineFormType&group.1_group.property.value=bottomKick&group.2_group.property=type&group.2_group.property.value=eventForm&group.3_group.1_group.property=onlineFormType&group.3_group.1_group.property.value=simple&group.3_group.2_group.property=type&group.3_group.2_group.property.operation=unequals&group.3_group.2_group.property.value=eventForm&group.p.or=true&p.hits=selective"        
                filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) +"&group.1_group.1_group.property=onlineFormType&group.1_group.1_group.property.operation=equals&group.1_group.1_group.property.value=bottomKick&group.1_group.2_group.property=type&group.1_group.2_group.property.operation=unequals&group.1_group.2_group.property.value=eventForm&group.2_group.property=type&group.2_group.property.value=eventForm&group.3_group.1_group.property=onlineFormType&group.3_group.1_group.property.operation=equals&group.3_group.1_group.property.value=simple&group.3_group.2_group.property=type&group.3_group.2_group.property.operation=unequals&group.3_group.2_group.property.value=eventForm&group.p.or=true&p.hits=selective"

            query_data = filter_data + "&p.properties="+ col_data
            self.logger.debug("Fullpath-> "+str(full_path)+", Filter Data -> "+str(filter_data)+", Columns-> "+str(col_data)
                        +", Query Data-> "+str(query_data))
            final_query = self.ip + query_builder + "?" + query_data
            self.logger.debug("Final Query: "+str(final_query))
            resp_data = requests.get(final_query, auth=(self.user, self.passwd), timeout = self.timeout)
            if resp_data.status_code == 200:
                outval = resp_data.json()                
                if(int(outval["results"])==0):
                    msg="No data to report - Http Code - "+str(resp_data.status_code)
                    self.logger.error(msg)
            elif resp_data.status_code == 401:
                msg = "Wrong Username and Password - Http Code - "+str(resp_data.status_code)
                self.logger.error(msg)
            else:
                msg = "Error Occurred - Http Code - "+str(resp_data.status_code)
                self.logger.error(msg)

            if outval and int(outval["results"])!=0:
                msg = []
                results = [outval.get("results",0),outval.get("total",0)]
                msg.append(results)
                for each in outval["hits"]:
                    chunks = []
                    chunks.append(each.get("jcr:path", "Invalid Property"))
                    for prop in cleaned_cols:
                        if prop != "jcr:path":
                            chunks.append(each.get(prop, "Invalid Property"))
                    
                    msg.append(chunks)
            return msg

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    
        