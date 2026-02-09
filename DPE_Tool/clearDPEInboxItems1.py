import time
import datetime
import json
import logging
from urllib.parse import quote
import xlrd
import requests
import calendar
import Adder

class ClearDPEInboxItems:
    """Made by Shouvik Das, Date: 10/09/2020.
    Clear the Stuck Items in Inbox from DPE. The list is as below
    1. Email Delivery Failure
    2. MX Lookup failure
    3. Potential Spam Clear
    4. Obscene Language
    """

    def __init__(self, issuetype, ip, user, passwd, to_clear_from_excel = False):
        self.ip = ip.strip()
        self.issuetype = issuetype.strip().lower()
        self.user = user.strip()
        self.passwd = passwd.strip()
        self.to_clear_from_excel = to_clear_from_excel

        self.configdata = self.opencode("configfiles\\config.json")

        self.loglevel = self.configdata["loglevel"].strip()
        self.sleeptime = self.configdata["sleeptime"]
        self.timeout = self.configdata["timeout"]

        frmt_crnt_date = datetime.datetime.now().strftime("%m%d%Y")
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
        self.logger.debug("Operation data : " + str(self.wfoperationdata))
        self.logger.debug("Config data : " + str(self.configdata))

    def opencode(self, file):
        """
        Open the Operation Code from designated Files
        """
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def retrieveList(self, varpath, country, lowerbound, upperbound):
        """
        Pull the data between given timeslot and return it as List.
        """
        try:
            varpath = quote(varpath.strip(), safe='')
            upperbound = (datetime.datetime.now() + datetime.timedelta(days=1)
                          ).strftime("%Y-%m-%d") if upperbound == "" else upperbound
            wfmodelid = quote(self.wfoperationdata[self.issuetype].strip(), safe='')
            query = ""
            country = country if self.issuetype == "delivery failure" else ""
            limitresult = int(self.wfoperationdata["limit result"])
            # print(limitresult)
            # print(self.issuetype)
            # %2fvar%2fworkflow%2fmodels%2fpwc-form-email
            if(country.strip() == ""):
                if(self.issuetype == "delivery failure"):
                    query = self.ip + self.wfoperationdata["query builder link"] + '?1_property=wfModelId&1_property.value='+wfmodelid+'&2_daterange.lowerBound=' + lowerbound.strip() + '&2_daterange.property=startTime&2_daterange.upperBound=' + upperbound.strip(
                    ) + '&group.1_property=status&group.1_property.value=ACTIVE&p.limit='+str(limitresult)+'&path='+varpath+'&3_property=_title&3_property.value='+quote(self.wfoperationdata["email delivery failure title"].strip(), safe='')
                elif(self.issuetype == "archive data failed"):
                    query = self.ip + self.wfoperationdata["query builder link"] + '?1_property=wfModelId&1_property.value='+wfmodelid+'&2_daterange.lowerBound=' + lowerbound.strip() + '&2_daterange.property=startTime&2_daterange.upperBound=' + upperbound.strip(
                    ) + '&group.1_property=status&group.1_property.value=ACTIVE&p.limit='+str(limitresult)+'&path='+varpath+'&3_property=_title&3_property.value='+quote(self.wfoperationdata["archive failure title"].strip(), safe='')
                elif(self.issuetype == "potential spam"):
                    query = self.ip + self.wfoperationdata["query builder link"] + '?1_property=wfModelId&1_property.value='+wfmodelid+'&2_daterange.lowerBound=' + lowerbound.strip() + '&2_daterange.property=startTime&2_daterange.upperBound=' + upperbound.strip(
                    ) + '&group.1_property=status&group.1_property.value=ACTIVE&p.limit='+str(limitresult)+'&path='+varpath+'&3_property=_title&3_property.value='+quote(self.wfoperationdata["potential spam title"].strip(), safe='')
                else:
                    query = self.ip + self.wfoperationdata["query builder link"] + '?1_property=wfModelId&1_property.value='+wfmodelid+'&2_daterange.lowerBound=' + lowerbound.strip() + '&2_daterange.property=startTime&2_daterange.upperBound=' + \
                        upperbound.strip() + '&group.1_property=status&group.1_property.value=ACTIVE&p.limit=' + \
                        str(limitresult)+'&path='+varpath

            elif(country.strip() != "" and self.issuetype == "delivery failure"):

                query = self.ip + self.wfoperationdata["query builder link"] + '?1_property=wfModelId&1_property.value=' + wfmodelid + '&2_daterange.lowerBound='+lowerbound.strip()+'&2_daterange.property=startTime&2_daterange.upperBound='+upperbound.strip()+'&3_property=assignee&3_property.value=' + \
                    country.strip().lower()+'-sitemanagers&group.1_property=status&group.1_property.value=ACTIVE&p.limit='+str(limitresult)+'&path=' + \
                    varpath + '&4_property=_title&4_property.value=' + \
                    quote(
                        self.wfoperationdata["email delivery failure title"].strip(), safe='')

            # pwc-form-submission-spam-check-v2
            # pwc-form-submission-obscene-check-v2'
            # print(query)
            self.logger.debug(query)
            data = []
            resp_data = requests.get(query, auth=(
                self.user, self.passwd), timeout=self.timeout)
            time.sleep(self.sleeptime)

            if(resp_data.status_code == 200):
                if(resp_data.json()['results'] > 0):
                    data_t = resp_data.json()['hits']
                    for dt in data_t:
                        data.append(dt['path'])

                data.append("Total Hits: "+str(resp_data.json()["total"]))

            elif(resp_data.status_code == 401):
                data.append(
                    "Wrong username and Password - Http status " + str(resp_data.status_code))
            else:
                data.append(
                    "Some Error occured while connecting. Http Status " + str(resp_data.status_code))

            self.logger.debug(data)
            return data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def exceltolist(self, file):
        """ Convert the excel data into userfriendly List Data """

        try:
            self.logger.debug("Excel File "+str(file))
            url_list = []
            wb = xlrd.open_workbook(file)
            sh = wb.sheet_by_index(0)
            num_rows = sh.nrows
            for i in range(1, num_rows):
                url_list.append(sh.cell_value(i, 0))
            self.logger.debug(url_list)
            return url_list
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def processfaileditem(self, uri, status):
        """
        Clear the Inbox Items with the status that has been passed as an argument to this function. Uses should be processfaileditem(varurl,status) Where varurl is the URL and spam_status as based on Type
        """
        try:
            msg = ""
            inbox_url = self.ip + '/bin/workflow/inbox'
            item = uri
            resp_data = requests.get(
                self.ip + uri + ".json", auth=(self.user, self.passwd), timeout=self.timeout)
            msg = str(uri) + "   :   "
            if(resp_data.status_code == 200):
                if status.lower() in self.wfoperationdata:
                    post_data = {
                        'cmd': 'advance',
                        '_charset_': 'utf-8',
                        'item': item,
                        'route-'+item: self.wfoperationdata[status.lower()]
                    }
                    self.logger.debug('Send Data: ' + str(post_data))
                    # print(post_data)
                    post_resp = requests.post(inbox_url, data=post_data, auth=(
                        self.user, self.passwd), timeout=self.timeout)
                    status_code = post_resp.status_code
                    #status_code = 201
                    self.logger.debug(
                        'Executed : ' + str(uri) + ' - \n'+str(post_resp.text))
                    time.sleep(self.sleeptime)
                    if status_code >= 200 and status_code <= 205:
                        msg = msg + "Processed("+str(status_code)+")" if self.to_clear_from_excel else "Processed("+str(status_code)+")"
                        # msg = "Processed("+str(status_code)+")"
                    elif(status_code == 401):
                        msg = "Wrong username and Password - Http status " + \
                            str(status_code)
                    else:
                        # msg = msg + "Failed("+str(status_code)+")"
                        msg = "Failed("+str(status_code)+")"
                    self.logger.info("Payload: " + str(uri) +
                                     " - Status Code: " + str(status_code))
                else:
                    msg = "Invalid Clear Status. Status Should be a valid one. You can get the list from operationcode"
            elif(resp_data.status_code == 401):
                msg = "Wrong username and Password - Http status " + \
                    str(resp_data.status_code)
            else:
                # msg = msg + "Failed(Node not available - " + \
                #     str(resp_data.status_code)+")"
                msg = "Failed(Node not available - " + str(resp_data.status_code)+")"

            self.logger.warning(msg)
            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return ""

    def executefromlist(self, data_list, status):
        """
        Execute the bulk URL maintained in Python List and Process the submission as either Status based on time
        """
        # self.logger = logging.getLogger()

        try:
            url_list = data_list

            if url_list is not None:
                self.logger.info(
                    "Number of URLs that need to be cleared are :" + str(len(url_list)))
                for uri in url_list:
                    msg = self.processfaileditem(uri, status)
                    time.sleep(self.sleeptime)
                self.logger.info(
                    'Email Delivery Failure has been cleared Successfully')
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def executefromexcel(self, file, status):
        """
        Execute the bulk URL maintained in a Excel Sheet and Process the submission as
        either Status. Status as based on type
        Note. Data should be in Sheet 1(Position 1) always
        """
        self.logger = logging.getLogger()

        try:
            url_list = self.exceltolist(file)

            if url_list is not None:
                self.logger.info(
                    "Number of URLs that need to be cleared are :" + str(len(url_list)))
                for uri in url_list:
                    msg = self.processfaileditem(uri, status)
                    time.sleep(self.sleeptime)
                self.logger.info(
                    'Email Delivery Failure has been cleared Successfully')
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def retrieve_list(self, issue, lowerbound, upperbound, adder_list, remover_list):
        try:
            # print(time.time())
            data = None
            retrieved_query = self.select_query_url(issue)
            self.logger.debug("Retrieved the query: "+str(retrieved_query))
            if retrieved_query is not None:
                lowerbound_in_sec = int(calendar.timegm(time.strptime(lowerbound, '%Y-%m-%d')) * 1000)
                upperbound_in_sec = int(calendar.timegm(time.strptime(upperbound, '%Y-%m-%d')) * 1000)
                
                self.logger.debug("Lower Bound: "+str(lowerbound) + ", Upper Bound: "+str(upperbound))
                self.logger.debug("Lower Bound in Secs: "+str(lowerbound_in_sec) + ", Upper Bound in Secs: "+str(upperbound_in_sec))

                query_url = self.ip + retrieved_query
                self.logger.debug("Final Query: "+str(query_url))

                resp_data = requests.get(query_url, auth=(self.user, self.passwd), timeout=self.timeout)
                data = []
                # print(time.time())
                if resp_data.status_code == 200:

                    if issue =="obscene language":
                        data_bannedwords=requests.get('https://dpe.pwc.com/content/pwc/global/referencedata/bannedWords.json',auth=(self.user, self.passwd)).json()
                        bannedwords=list(data_bannedwords['bannedWords'])
                        for x in Adder.adder : adder_list.append(x)
                        print(adder_list)
                        print(remover_list)
                        for each_data in resp_data.json()["items"]:
                            self.logger.debug("Single Data: "+ str(each_data))
                            if each_data["startTime"] > lowerbound_in_sec and each_data["startTime"] < upperbound_in_sec:
                                payload_summary = each_data.get("payloadSummary","")
                                descrip = payload_summary.get("description","") if isinstance(payload_summary, dict) else ""
                                _description = [x.strip() for x in descrip.split("<br>") if x.strip()!= ""]
                                _description_data = ", ".join(_description)
                                nodata = ""
                                company=""
                                email=""
                                fullName=""
                                queryDetails=""
                                querysubject=""
                                job_role=""
                                telephone=""
                                searchstring=""
                                formfieldslist=[]
                                url = each_data["payloadPath"]
                                #print(url)
                                get_url='https://dpe.pwc.com'+url+'.json'
                                #print(get_url)
                                r = requests.get(get_url,auth=(self.user, self.passwd))
                                data2=r.json()
                                data1=str(data2)
                                if data2['formType']=='contactUs':  
                                    if 'company' in data2: 
                                        company=data2['company']
                                    if 'email' in data2:
                                        email=data2['email']
                                    if 'fullName' in data2:
                                        fullName=data2['fullName']
                                    if 'queryDetails' in data2:
                                        queryDetails=data2['queryDetails']
                                    if 'querysubject' in data2:
                                        querysubject=data2['querysubject']
                                    if 'job_role' in data2:
                                        job_role=data2['job_role']  
                                    if 'telephone' in data2:
                                        telephone=data2['telephone']

                                    searchstring=company+' '+email+' '+fullName+' '+queryDetails+' '+querysubject+''+job_role+''+telephone
                                
                                
                                elif "pwcFormFieldOrder" in data2 and data2["pwcFormFieldOrder"]!='':
                                    formfields=data2['pwcFormFieldOrder']
                                    formfieldslist=formfields.split(",")
                                    for i in range(len(formfieldslist)):
                                        searchstring+=str(data2[formfieldslist[i]])+' '

                                elif 'g-recaptcha-response' in data2:
                                        grecaptcharesponse=data2['g-recaptcha-response']
                                        refined_data1=data1.replace(str(grecaptcharesponse),'') 
                                        searchstring=str(refined_data1) 
                                else:
                                        searchstring=data1

                                if "/content/pwc/in/en" in url and 'sikkim' in bannedwords:
                                    bannedwords.remove("sikkim") 
                                if "/content/pwc/cn/" in url and 'poon' in bannedwords:
                                    bannedwords.remove("poon")  
                                if "/content/pwc/hk/" in url and 'poon' in bannedwords:
                                    bannedwords.remove("poon")

                                
                                for x in bannedwords:
                                    if '/n' in x:
                                        x1=x.replace('\n','') 
                                    else:
                                        x1=x  
                                    if x1 in adder_list:
                                        x1=' '+x1+' '
                                    a=searchstring.lower().find(str(x1).lower())
                                    if a>0:
                                        data.append([url, _description_data, str(x), "Banned Word Present"])
                                        b=0
                                        break
                                    else:
                                        b=1
                                
                                if b==1:        
                                    data.append([url, _description_data, nodata, "Banned Words Were Not Present"])
                                
                    else:
                        for each_data in resp_data.json()["items"]:
                            # print(each_data["startTime"])
                            self.logger.debug("Single Data: "+ str(each_data))
                            if each_data["startTime"] > lowerbound_in_sec and each_data["startTime"] < upperbound_in_sec:
                                payload_summary = each_data.get("payloadSummary","")
                                descrip = payload_summary.get("description","") if isinstance(payload_summary, dict) else ""
                                _description = [x.strip() for x in descrip.split("<br>") if x.strip()!= ""]
                                _description_data = ", ".join(_description)
                                data.append([each_data.get("payload",""), _description_data, each_data["item"]])
                elif(resp_data.status_code == 401):
                    data.append([
                        "Wrong username and Password - Http status " + str(resp_data.status_code),resp_data.status_code, "Failed"])
                else:
                    print([
                        "Some Error occured while connecting. Http Status " + str(resp_data.status_code),resp_data.status_code,"Failed"])
                # print(time.time())
            self.logger.debug("Final Data Retrieved: "+str(data))
            return data

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def select_query_url(self, issue_type):
        try:
            generated_query = None
            data_model = quote(self.wfoperationdata[issue_type.lower().strip()], safe="-")
            if issue_type.lower().strip() == "potential spam":
                potential_spam_node_filter = self.wfoperationdata["potential spam node"]
                self.logger.debug("Selected Node Filter: "+str(potential_spam_node_filter))
                generated_query = "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                    str(data_model)+"&filter-step=" + str(potential_spam_node_filter)

            elif issue_type.lower().strip() == "delivery failure":
                delivery_fail_node_filter = self.wfoperationdata["email delivery failure node"]
                self.logger.debug("Selected Node Filter: "+str(delivery_fail_node_filter))
                generated_query = "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                    str(data_model)+"&filter-step=" + str(delivery_fail_node_filter)

            elif issue_type.lower().strip() == "mx lookup":
                generated_query = "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                    str(data_model)

            elif issue_type.lower().strip() == "archive data failed":
                archive_node_filter = self.wfoperationdata["archive failure node"]
                generated_query = "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                    str(data_model)+"&filter-step=" + str(archive_node_filter)
                self.logger.debug("Selected Node Filter: "+str(archive_node_filter))

            elif issue_type.lower().strip() == "obscene language":
                generated_query = "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                    str(data_model)
            elif issue_type.lower().strip() == "form data on hold":
                form_data_on_hold_node_filter = self.wfoperationdata["form data on hold node"]
                generated_query = "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                    str(data_model)+"&filter-step=" + str(form_data_on_hold_node_filter)

            self.logger.debug("Generated Query: "+str(generated_query))
            return generated_query
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def fetch_payload_summary(self, payload):
        try:
            _url = self.ip + payload.strip().replace(".html","") + ".json"
            self.logger.info("Fetch URL: %s" % _url)
            _resp_data = requests.get(_url, auth=(self.user, self.passwd), timeout=self.timeout)
            time.sleep(self.sleeptime)
            _resp_list_data = None
            invalid_cols = ["jcr:primaryType","jcr:mixinTypes","longformform","cq:lastReplicationAction",
                    "cq:lastReplicatedBy","formid","formtoprocess","pwcReferrerTitle","pwcFormUrlTitle","cq:lastReplicated",
                    "spam","referenceNumber","formPath","formName","pwcSubmissionDateTitle","sling:resourceType",
                    "_charset_","mandatoryHField","pwcFormFieldOrder"]
            self.logger.info("Fetch Status: %s" % _resp_data.status_code)
            if _resp_data.status_code == 200:
                _resp_list_data = []
                for _each_prop in _resp_data.json():
                    if _each_prop not in invalid_cols:
                        _resp_list_data.append([_each_prop, _resp_data.json()[_each_prop]])

            self.logger.debug(_resp_list_data)
            return _resp_list_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None
