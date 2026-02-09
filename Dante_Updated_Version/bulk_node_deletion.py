import xlrd
import requests
import time
from datetime import datetime
import logging
import json


class BulkNodeDeletion:
    """
        Used to Delete Multiple Node from DPE.

    """
    def __init__(self, ip, user, passwd):
        "Initialize the Class"

        self.ip = ip.strip()
        self.user = user.strip()
        self.passwd = passwd.strip()
        self.configdata = self.opencode("configfiles\\config.json")
        # print(loglevel)
        self.loglevel = self.configdata["loglevel"]
        self.sleeptime = float(self.configdata["sleeptime"])
        self.timeout = float(self.configdata["timeout"])
        # frmt_crnt_date = datetime.now().strftime("%m%d%Y")
        # self.logfile = "logs\\" + "mainlogfile_"+frmt_crnt_date+".log"
        log_level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level[self.loglevel])
        self.wfoperationdata = self.opencode("configfiles\\operationcode.json")
        self.logger.debug("Configuration data : " + str(self.configdata))
        self.logger.debug("Operation data : " + str(self.wfoperationdata))

    def opencode(self, file):
        "Open the JSON Files"
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def validate_payload(self, payload):
        try:
            return_code = False
            _content_root = self.wfoperationdata.get("content root", "/content/pwc")
            _content_dam_root = self.wfoperationdata.get("content dam root", "/content/dam/pwc")
            _form_path = self.wfoperationdata.get("form content path", "/content/usergenerated/content/pwc")
            _form_archive_path = self.wfoperationdata.get("form archive content path", "/content/usergenerated/archive/content/pwc")
            
            if (payload.startswith(_content_root) or payload.startswith(_content_dam_root) 
                    or payload.startswith(_form_path) or payload.startswith(_form_archive_path)):
                if( not(payload.endswith(".html"))):
                    return_code = True
            
            self.logger.info("Payload to be validated: %s, Valid: %s" % (payload, return_code))
            return return_code
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def excel_to_list(self, file, validate_payloads):
        """ Convert the excel data into userfriendly List Data """

        try:
            self.logger.debug("Excel File "+str(file))
            url_list = []
            work_book = xlrd.open_workbook(file)
            work_sheet = work_book.sheet_by_index(0)
            num_rows = work_sheet.nrows
            for i in range(1, num_rows):
                _payload = str(work_sheet.cell_value(i, 0)).strip()
                if validate_payloads:
                    if self.validate_payload(_payload):
                        if _payload not in url_list:
                            url_list.append(_payload)
                else:
                    if _payload not in url_list:
                        url_list.append(_payload)
            self.logger.debug(url_list)
            return url_list
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def password_validator(self):
        try:
            _pass_validator_url = self.ip + self.wfoperationdata["password validator"] + ".json"
            _resp_data = requests.get(_pass_validator_url, auth=(self.user, self.passwd), timeout=self.timeout)
            return _resp_data.status_code
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def delete_dpe_node(self, payload):
        "Delete Node"
        try:
            # data_to_be_deleted = self.excel_to_list(file)
            status = ""
            post_data = {":operation":"delete"}
            post_url = self.ip + payload
            
            post_resp_data = requests.post(post_url, data=post_data, auth=(self.user, self.passwd), timeout=self.timeout)
            time.sleep(self.sleeptime)
            if post_resp_data.status_code == 200:
                self.logger.info("Deleted Successfully: "+str(payload))
                status = post_resp_data.status_code
            elif post_resp_data.status_code == 401:
                self.logger.error("Invalid Username/Password!! - "+str(post_resp_data.status_code))
                status = post_resp_data.status_code
            else:
                self.logger.error("Issue in establishing connection!! - "+str(post_resp_data.status_code))
                status = post_resp_data.status_code
                
            return status

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999