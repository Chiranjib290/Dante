import requests
import time
from datetime import datetime
import logging
from urllib.parse import quote
import xlrd
import json


class TerminateWorkflow:
    """Made by Shouvik Das, Date: 10/09/2020.
    Clear the Stuck Items in Inbox from DPE. The list is as below
    1. Email Delivery Failure
    2. MX Lookup failure
    3. Potential Spam Clear
    4. Obscene Language
    """

    def __init__(self, ip, user, passwd):
        self.ip = ip.strip()
        self.user = user.strip()
        self.passwd = passwd.strip()
        self.configdata = self.opencode("configfiles\\config.json")
        self.loglevel = self.configdata["loglevel"].strip()
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

    def opencode(self, file):
        """
        Open the Operation Code from designated Files
        """
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def retrieveList(self, varpath, contentpath):
        """
        Pull the Workflow data From the Given Content Path.
        """
        try:
            varpath = quote(varpath.strip(), safe='')
            query = ""
            contentpath = quote(contentpath.strip(), safe='')

            query = self.ip + '/bin/querybuilder.json?1_group.property=status&1_group.property.value=ACTIVE&2_property=contentPath&2_property.value='+contentpath+'&path='+varpath

            # print(query)
            self.logger.debug(query)
            data = ""
            resp_data = requests.get(query, auth=(
                self.user, self.passwd), timeout=self.timeout)
            time.sleep(self.sleeptime)
            if(resp_data.status_code == 200):
                if(resp_data.json()['results'] > 0):
                    data_t = resp_data.json()['hits']
                    # for dt in data_t:
                    # data.append(dt['path'])
                    data = data_t[0]['path']
            elif(resp_data.status_code == 401):
                #data.append("Wrong username and Password or Resposnse Status is not 200")
                data = "Wrong username and Password - Http status " + \
                    str(resp_data.status_code)
            else:
                data = "Some Error occured while connecting. Http Status " + \
                    str(resp_data.status_code)
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
            for i in range(0, num_rows):
                url_list.append(sh.cell_value(i, 0))
            self.logger.debug(url_list)
            return url_list
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def processfaileditem(self, uri):
        """
        Terminate the workflow that has been stuck for long time.
        """
        try:
            msg = ""
            #inbox_url = self.ip + '/bin/workflow/inbox'
            item = uri
            failed_work_items = item.split("/workItems/")[0]
            work_flow_id = self.ip + failed_work_items
            msg = ""
            get_status = requests.get(work_flow_id+".json", auth=(
                self.user, self.passwd), timeout=self.timeout)
            if(get_status.status_code == 200):
                aborted = requests.post(work_flow_id, data={'state': 'ABORTED'}, auth=(
                    self.user, self.passwd), timeout=self.timeout)

                #post_resp = requests.post(inbox_url , data=post_data, auth=(self.user, self.passwd),timeout=self.timeout)
                status_code = aborted.status_code
                #status_code = 201
                self.logger.debug('Executed : ' + str(uri) +
                                ' - \n'+str(aborted.text))
                msg = str(uri) + "   :   "

                if status_code >= 200 and status_code <= 205:
                    msg = msg + "Processed("+str(status_code)+")"
                elif(status_code == 401):
                    msg = "Wrong username and Password - Http status " + \
                        str(status_code)
                else:
                    msg = msg + "Failed("+str(status_code)+")"
                self.logger.info("Terminate Workflow: Payload: " +
                                str(uri) + " - Status Code: " + str(status_code))
            elif(status_code == 401):
                msg = "Wrong username and Password - Http status " + \
                        str(status_code)
            else:
                msg = "Some Error occured while connecting. Http Status "+ \
                        str(status_code)

            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def executefromlist(self, data_list):
        """
        Terminate bulk URL maintained in List
        """
        self.logger = logging.getLogger()

        try:
            url_list = data_list

            if url_list is not None:
                self.logger.info(
                    "Number of URLs that need to be cleared are :" + str(len(url_list)))
                for uri in url_list:
                    msg = self.processfaileditem(uri)
                    time.sleep(self.sleeptime)
                self.logger.info('Workflow has been terminated successfully.')
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def executefromexcel(self, file):
        """
        Terminate bulk URL maintained in Excel File
        Note. Data should be in Sheet 1(Position 1) always
        """
        self.logger = logging.getLogger()

        try:
            url_list = self.exceltolist(file)

            if url_list is not None:
                self.logger.info(
                    "Number of URLs that need to be cleared are :" + str(len(url_list)))
                for uri in url_list:
                    msg = self.processfaileditem(uri)
                    time.sleep(self.sleeptime)
                self.logger.info('Workflow has been terminated successfully.')
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
