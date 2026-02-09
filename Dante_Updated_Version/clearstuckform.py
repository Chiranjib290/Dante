import xlrd
import requests
import time
from datetime import datetime
import logging
from urllib.parse import quote
import json


class ClearStuckForm:
    """To Clear Stuck Form, Form that are in Ready for processing, Processed due to missing runModes property or incomplete runModes property in the form data.
            Process is to add the runModes and run PwC Form Email workflow again to process the forms."""

    def __init__(self, ip, user, passwd, to_process_from_excel = False):
        self.ip = ip.strip()
        self.user = user.strip()
        self.passwd = passwd.strip()
        self.to_process_from_excel = to_process_from_excel
        self.configdata = self.opencode("configfiles\\config.json")
        # print(loglevel)
        self.loglevel = self.configdata["loglevel"]
        self.sleeptime = float(self.configdata["sleeptime"])
        self.timeout = float(self.configdata["timeout"])
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
        self.wfmodeldata = self.opencode("configfiles\\wf_models.json")
        self.logger.debug("Configuration data : " + str(self.configdata))
        self.logger.debug("Operation data : " + str(self.wfoperationdata))

    def opencode(self, file):
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def retrievedata(self, lowerbound, upperbound, cntry, status):
        try:
            query = ""
            tip_query = ""
            ct = 1
            formpath = self.wfoperationdata.get("form content path", "/content/usergenerated/content/pwc")
            # limitresult = self.wfoperationdata["limit result"]
            path_filter = ""

            if cntry.strip() == "":
                path_filter = formpath
            else:
                path_filter = formpath + "/" + cntry.strip()

            # for st in status:
            #     tip_query = tip_query + "group." + \
            #         str(ct)+"_group.property=status&group." + \
            #         str(ct)+"_group.property.value="+str(st) + "&"
            #     ct += 1

            data = []
            total_results_retrieve = 0

            for each_status in status:
                # status_filter = 'child.[status]="' + each_status + '"'
                initial_path = path_filter
                daterange_prop = "cq%3alastReplicated"
                excluded_path = "%2fcontent%2fusergenerated%2fcontent%2fpwc%2fgx%2fen%2fservices%2fpeople-organisation%2fpublications%2fworkforce-of-the-future%2fquiz"
                filter_data = f"1_daterange.lowerBound={lowerbound}&1_daterange.property={daterange_prop}&2_property=*%2fstatus&2_property.value={str(each_status)}&3_property=formid&3_property.operation=exists&group.1_group.p.not=true&group.1_group.path={excluded_path}&group.1_group.path.self=true&p.limit=-1&path={initial_path}"
                # query = self.ip + self.wfoperationdata["query builder link"] + "?1_property=formType&1_property.value=online&2_daterange.lowerBound=" + \
                #     str(lowerbound)+"&2_daterange.property=cq%3alastReplicated&2_daterange.upperBound="+str(upperbound)+"&" + \
                #     tip_query+"group.p.or=true&p.limit=" + \
                #     str(limitresult)+"&path="+formpath + \
                #     content_root + "%2f"+str(cntry)
                # sql_query = 'SELECT child.* FROM [nt:unstructured] AS parent INNER JOIN [nt:unstructured] as child ON ISCHILDNODE(child,parent) WHERE ISDESCENDANTNODE(parent, "'+path_filter+'") AND child.[formtoprocess]="true" AND parent.[cq:lastReplicated] > CAST("'+str(
                #     lowerbound)+'T00:00:00.000Z" AS DATE) AND parent.[cq:lastReplicated] < CAST("'+str(upperbound)+'T00:00:00.000Z" AS DATE) AND ' + status_filter
                # self.logger.debug("Query: "+str(sql_query))

                # enc_sql_query = quote(sql_query, safe='()')
                # self.logger.debug("Encoded SQL Query: "+str(enc_sql_query))

                # time_in_ms = int(time.time()*1000)

                # query = self.ip + self.wfoperationdata["sql2 query link"] + '?_dc='+str(
                #     time_in_ms)+'&_charset_=utf-8&type=JCR-SQL2&stmt='+enc_sql_query+'&showResults=true'
                query = self.ip + self.wfoperationdata["query builder link"] + "?" + filter_data

                self.logger.debug(query)

                resp_data = requests.get(query, auth=(
                    self.user, self.passwd), timeout=self.timeout)
                time.sleep(self.sleeptime)
                if(resp_data.status_code == 200):
                    if resp_data.json()["success"]:
                        data_t = resp_data.json().get("hits", [])
                        for _excerpt_data in data_t:
                            path = _excerpt_data["path"]
                            name = path.split("/")[-1]
                            suffix_list = name.split("_")
                            suffix = suffix_list[0] if bool(suffix_list) else name
                            new_path = f"{path}/{suffix}"
                            data.append([new_path, each_status])
                        total_results_retrieve = total_results_retrieve + resp_data.json()["total"]
                    else:
                        data.append(
                            ["Exception", resp_data.json()['errorMessage']])
                #data.append("Workign Fine")
                elif(resp_data.status_code == 401):
                    data.append(
                        ["Wrong username and Password - Http status " + str(resp_data.status_code), resp_data.status_code])
                    break
                else:
                    data.append(
                        ["Some Error occured while connecting. Http Status " + str(resp_data.status_code), resp_data.status_code])
                self.logger.debug(data)
                # return data
            self.logger.debug("Total Results Retrieve: "+str(total_results_retrieve))
            data.append(
                ["Total Hits: "+str(total_results_retrieve), total_results_retrieve])
            return data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def monthlyDataRetrieve(self, month, year, contentpath, status):
        try:
            month_num = datetime.strptime(
                "1900-"+str(month).title()+"-01", "%Y-%B-%d").month if month != "" else ""
            data = []
            formpath = quote(self.configdata["formpath"].strip(), safe='')
            contentpath = quote(contentpath)
            limitresult = self.wfoperationdata["limit result"]

            if(month_num != "" and str(year) != ""):
                path = formpath + contentpath + "%2f" + \
                    str(year) + "%2f" + str(month_num)
                tip_query = ""
                ct = 1
                for st in status:
                    tip_query = tip_query + "group." + \
                        str(ct)+"_group.property=status&group." + \
                        str(ct)+"_group.property.value="+str(st) + "&"
                    ct += 1

                query = self.ip + self.wfoperationdata["query builder link"] + "?1_property=formType&1_property.value=online&" + \
                    tip_query+"group.p.or=true&p.limit=" + \
                    str(limitresult)+"&path="+path

                self.logger.debug(query)
                resp_data = requests.get(query, auth=(
                    self.user, self.passwd), timeout=self.timeout)
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
            else:
                data.append("Month and Year Can't be Empty!!")

            self.logger.debug(data)
            return data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def exceltolist(self, file):
        """ Convert the excel data into userfriendly List Data """
        try:
            wb = xlrd.open_workbook(file)
            sh = wb.sheet_by_index(0)
            num_rows = sh.nrows
            url_list = []
            for i in range(1, num_rows):
                url_list.append(sh.cell_value(i, 0))
            self.logger.debug("Data From Files: "+str(url_list))
            return url_list
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def processform(self, uri):
        # Add Runmodes
        msg = ""
        # '/var/workflow/instances'
        inbox_url = self.ip + self.wfoperationdata["workflow instances"]
        #post_data = {'runModes':{'crx3tar','publish','nosamplecontent','crx3','s7connect','prod'}}
        node_available = requests.get(
            self.ip + uri + ".json", auth=(self.user, self.passwd), timeout=self.timeout)
        msg = str(uri) + "   :   "
        if(node_available.status_code == 200):
            if (self.ip.find(self.configdata["stage"]) > -1 or self.ip.find(self.configdata["qa"]) > -1):
                post_data = {'runModes': [
                    'crx3tar', 'publish', 'nosamplecontent', 'crx3', 's7connect', 'staging']}
            else:
                post_data = {'runModes': [
                    'crx3tar', 'publish', 'nosamplecontent', 'crx3', 's7connect', 'prod']}
            post_resp = requests.post(
                self.ip + uri, data=post_data, auth=(self.user, self.passwd), timeout=self.timeout)
            #post_resp = requests.get(self.ip + uri +".json", auth=(self.user, self.passwd))
            status_code = post_resp.status_code

            self.logger.info("Payload: " + str(uri) +
                             " - Status Code: " + str(status_code))

            if status_code == 200:
                send_data = {'model': str(self.wfmodeldata["PwC Form Email"]),
                             '_charset_': 'utf-8', 'payload': uri, 'payloadType': 'JCR_PATH'}
                self.logger.debug('Send Data: ' + str(send_data))
                resp = requests.post(inbox_url, data=send_data, auth=(
                    self.user, self.passwd), timeout=self.timeout)
                # time.sleep(self.sleeptime)
                self.logger.debug('Executed : ' + str(uri) +
                                  ' - \n'+str(resp.text))
                #self.logger.debug('Executed : '+uri+' - \n'+post_resp.text)
                time.sleep(self.sleeptime)
                if resp.status_code >= 200 and resp.status_code <= 205:
                    msg = msg + "Processed(" + str(resp.status_code) + ")" if self.to_process_from_excel else "Processed(" + str(resp.status_code) + ")"
                elif(resp.status_code == 401):
                    msg = "Wrong username and Password - Http status " + \
                        str(resp.status_code)
                else:
                    msg = msg + "Failed(" + str(resp.status_code) + ")"
            elif status_code == 401:
                msg = "Wrong username and Password - Http status " + \
                    str(status_code)
            else:
                msg = msg + "Failed(" + str(status_code) + ")"
        elif node_available.status_code == 401:
            msg = "Wrong username and Password - Http status " + \
                str(node_available.status_code)

        else:
            msg = msg + \
                "Node not Available - Failed(" + \
                str(node_available.status_code) + ")"

        self.logger.debug(msg)
        return msg

    def execute_from_excel(self, file):
        self.logger = logging.getLogger()

        try:
            url_list = self.exceltolist(file)

            if url_list is not None:
                self.logger.info(
                    "Number of URLs that need to be cleared are :" + str(len(url_list)))
                for uri in url_list:
                    msg = self.processform(uri)
                self.logger.info('Form Data has been cleared Successfully')
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def check_form_router(self, uri, env):
        # self.logger = logging.getLogger()

        try:
            router_present = False
            varpath_environment = "varpath"+str(env).lower()
            varpath = quote(
                self.configdata[varpath_environment].strip(), safe='')
            enc_uri = quote(uri, safe='')
            query = self.ip + self.wfoperationdata["query builder link"] + \
                "?1_group.property=status&1_group.property.value=ACTIVE&2_property=contentPath&2_property.value=" + \
                str(enc_uri) + "&path="+str(varpath)
            resp_data = requests.get(query, auth=(
                self.user, self.passwd), timeout=self.timeout)
            if(resp_data.status_code == 200):
                len_of_fetched_router = len(resp_data.json()["hits"])
                if len_of_fetched_router > 0:
                    router_present = True

            return router_present

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def check_run_modes(self, data):
        try:
            is_validated = False
            validator_list = [
                'crx3tar', 'publish', 'nosamplecontent', 'crx3', 's7connect', 'staging', 'prod']
            runmodes_data = data["runModes"]

            if isinstance(runmodes_data, list):
                counter = 0
                for each in runmodes_data:
                    if each in validator_list:
                        counter += 1

                if counter == 6:
                    is_validated = True

            return is_validated

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def run_workflow(self, uri, wf_model):
        try:
            msg = str(uri) + "   :   "
            # '/var/workflow/instances'
            inbox_url = self.ip + self.wfoperationdata["workflow instances"]
            send_data = {'model': str(
                wf_model), '_charset_': 'utf-8', 'payload': uri, 'payloadType': 'JCR_PATH'}
            self.logger.debug('Send Data: ' + str(send_data))
            resp = requests.post(inbox_url, data=send_data, auth=(
                self.user, self.passwd), timeout=self.timeout)
            # time.sleep(self.sleeptime)
            self.logger.debug('Executed : ' + str(uri) +
                              ' - \n'+str(resp.text))
            #self.logger.debug('Executed : '+uri+' - \n'+post_resp.text)
            time.sleep(self.sleeptime)
            if resp.status_code >= 200 and resp.status_code <= 205:
                msg = msg + "Processed(" + str(resp.status_code) + ")" if self.to_process_from_excel else "Processed(" + str(resp.status_code) + ")"
            elif(resp.status_code == 401):
                msg = "Wrong username and Password - Http status " + \
                    str(resp.status_code)
            else:
                msg = msg + "Failed(" + str(resp.status_code) + ")"

            return msg

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception Occurred - 999"

    def run_spam_submission_v2(self, uri):
        try:
            msg = ""
            node_available = requests.get(
                self.ip + uri + ".json", auth=(self.user, self.passwd), timeout=self.timeout)
            msg = str(uri) + "   :   "
            if(node_available.status_code == 200):
                runmodes_present = self.check_run_modes(node_available.json())
                if not(runmodes_present):
                    status = self.post_runmodes(uri)
                    self.logger.info("Post Status: "+str(status))

                self.logger.info("Node Available: " +
                                 str(node_available.status_code))
                spam_submission_wf_model = str(
                    self.wfmodeldata["PwC Form Submission Spam Check v2"])
                self.logger.info("Workflow model: " +
                                 str(spam_submission_wf_model))
                msg = self.run_workflow(uri, spam_submission_wf_model)

            elif node_available.status_code == 401:
                msg = "Wrong username and Password - Http status " + \
                    str(node_available.status_code)

            else:
                msg = msg + \
                    "Node not Available - Failed(" + \
                    str(node_available.status_code) + ")"

            self.logger.debug(msg)
            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception Occurred - 999"

    def post_runmodes(self, uri):
        try:
            if (self.ip.find(self.configdata["stage"]) > -1 or self.ip.find(self.configdata["qa"]) > -1):
                post_data = {'runModes': [
                    'crx3tar', 'publish', 'nosamplecontent', 'crx3', 's7connect', 'staging']}
            else:
                post_data = {'runModes': [
                    'crx3tar', 'publish', 'nosamplecontent', 'crx3', 's7connect', 'prod']}
            post_resp = requests.post(
                self.ip + uri, data=post_data, auth=(self.user, self.passwd), timeout=self.timeout)
            #post_resp = requests.get(self.ip + uri +".json", auth=(self.user, self.passwd))
            status_code = post_resp.status_code

            self.logger.info("Payload: " + str(uri) +
                             " - Status Code: " + str(status_code))
            return status_code
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def run_form_email(self, uri):
        # Add Runmodes
        msg = ""
        node_available = requests.get(
            self.ip + uri + ".json", auth=(self.user, self.passwd), timeout=self.timeout)
        msg = str(uri) + "   :   "
        if(node_available.status_code == 200):
            status_code = self.post_runmodes(uri)

            if status_code == 200:
                wf_form_email_model = str(self.wfmodeldata["PwC Form Email"])
                self.logger.info("Workflow model: "+str(wf_form_email_model))
                msg = self.run_workflow(uri, wf_form_email_model)
            elif status_code == 401:
                msg = "Wrong username and Password - Http status " + \
                    str(status_code)
            else:
                msg = msg + "Failed(" + str(status_code) + ")"
        elif node_available.status_code == 401:
            msg = "Wrong username and Password - Http status " + \
                str(node_available.status_code)

        else:
            msg = msg + \
                "Node not Available - Failed(" + \
                str(node_available.status_code) + ")"

        self.logger.debug(msg)
        return msg

    def process_failed_forms(self, uri, env):
        try:
            is_form_has_router = self.check_form_router(uri, env)
            self.logger.debug("Form has router: "+str(is_form_has_router))
            msg = ""
            if is_form_has_router:
                msg = self.run_form_email(uri)
            else:
                msg = self.run_spam_submission_v2(uri)
            self.logger.debug(msg)
            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception Occurred - 999"

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