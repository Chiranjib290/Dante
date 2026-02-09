import xlrd
import requests
import time
from datetime import datetime
import logging
import json


class RunWorkflow:
    """
        Used to Run Multiple Workflow in DPE.

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
        self.selected_model_id = None

    def opencode(self, file):
        "Open the JSON Files"
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def get_wf_models_list(self):
        try:
            model_list = []
            current_seconds_in_ms = int(time.time() * 1000)
            model_url = self.ip + self.wfoperationdata["wf models link"] + "?_dc=" + str(current_seconds_in_ms)

            output = requests.get(model_url, auth=(self.user, self.passwd), timeout=self.timeout)

            if output.status_code == 200:
                model_list = output.json().get("models",None)
            elif output.status_code == 401:
                model_list = None

            self.logger.debug("Model List")
            self.logger.debug(model_list)

            return model_list

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def sync_wf_models(self):
        try:
            model_list = None
            current_seconds_in_ms = int(time.time() * 1000)
            model_url = self.ip + self.wfoperationdata["wf models link"] + "?_dc=" + str(current_seconds_in_ms)

            output = requests.get(model_url, auth=(self.user, self.passwd), timeout=self.timeout)
            
            if output.status_code == 200:
                output_data = output.json().get("models", None)
                model_list = {}
                for each_models in output_data:
                    model_list[each_models["title"]] = each_models["item"]

                self.logger.debug("Synced Model List")
                self.logger.debug(model_list)
            else:
                model_list = output.status_code

            return model_list

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def excel_to_list(self, file):
        """ Convert the excel data into userfriendly List Data """

        try:
            self.logger.debug("Excel File "+str(file))
            url_list = []
            work_book = xlrd.open_workbook(file)
            work_sheet = work_book.sheet_by_index(0)
            num_rows = work_sheet.nrows
            for i in range(1, num_rows):
                url_list.append([work_sheet.cell_value(i, 0),work_sheet.cell_value(i, 1)])
            self.logger.debug(url_list)
            return url_list
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def set_model(self, model_name):
        try:
            # model_list = self.get_wf_models_list()
            model_list = self.opencode("configfiles\\wf_models.json")
            self.logger.debug("Model List")
            self.logger.debug(model_list)
            status = False
            # if model_list is None:
            #     status = 401
            # else:
            #     self.logger.info("Model Name: "+str(model_name))
            #     for each_model in model_list:
            #         if each_model["title"] == model_name:
            #             self.selected_model_id = each_model["item"]
            #             status = 200

            if model_list is not None:
                self.selected_model_id = model_list[model_name]
                status = True

            self.logger.info("Selected Worfklow: "+str(self.selected_model_id))
            
            return status

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def is_payload_valid(self, payload):   
        try:
            self.logger.debug("Checking for payload validity...")
            _content_root = self.wfoperationdata.get("content root", "/content/pwc")
            _content_root_experience_fragment = self.wfoperationdata.get("content root experience fragment","/content/experience-fragments/pwc")
            _content_root_dam = self.wfoperationdata.get("content dam root", "/content/dam/pwc")
            _form_path = self.wfoperationdata.get("content usergenerated root", "/content/usergenerated/content/pwc")
            _form_archive_path = self.wfoperationdata.get("form archive content path", "/content/usergenerated/archive/content/pwc")
            if payload.lower().startswith(_content_root) or payload.lower().startswith(_content_root_experience_fragment) or payload.lower().startswith(_content_root_dam) or payload.lower().startswith(_form_path) or payload.lower().startswith(_form_archive_path):
                pageinfo=self.ip+"/libs/wcm/core/content/pageinfo.json?path="+payload
                requestedpage=requests.get(pageinfo,auth=(self.user, self.passwd),timeout=self.timeout)
                return requestedpage.status_code  
            else:
                return 404
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999 

    def bulk_run_workflow(self, payload_and_name):
        "Bulk Run Workflow"
        payload = payload_and_name[0]
        title = payload_and_name[1]
        try:
            # data_to_be_deleted = self.excel_to_list(file)
            status = 999
            if self.selected_model_id is not None:
                post_data = {
                            'model':self.selected_model_id,
                            '_charset_':'utf-8',
                            'payload':str(payload),
                            'payloadType':'JCR_PATH',
                            'workflowTitle':title}
                post_url = self.ip + '/var/workflow/instances'
                valid_payload = self.is_payload_valid(payload)
                if valid_payload==200:
                    post_resp_data = requests.post(post_url, data=post_data, auth=(self.user, self.passwd), timeout=self.timeout)
                    time.sleep(self.sleeptime)
                    
                    if post_resp_data.status_code >= 200 and post_resp_data.status_code < 207:
                        self.logger.info("Workflow Ran Successfully: "+str(payload))
                        status = post_resp_data.status_code
                    elif post_resp_data.status_code == 401:
                        self.logger.error("Invalid Username/Password!! - "+str(post_resp_data.status_code))
                        status = post_resp_data.status_code
                    else:
                        self.logger.error("Issue in establishing connection!! - "+str(post_resp_data.status_code))
                        status = post_resp_data.status_code            
                elif valid_payload==401:
                    self.logger.debug("Incorrect UserName/Password")
                    status=valid_payload  
                elif valid_payload==404:
                    status=valid_payload
                    self.logger.debug("Payload Not Found")
            else:
                status = None
                self.logger.error("Invalid Model ID. Please check Logs.")

            return status

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999
    
    def validate_admin_user(self, uname, passwd):
        try:
            _url = self.configdata["production"] + \
                    self.wfoperationdata["password validator"] + ".json"
            self.logger.debug("Authentication Validator: "+_url)
            resp_data = requests.get(_url, auth=(
                    uname.strip(), passwd), timeout=self.configdata["timeout"])
            self.logger.info("Response Data Status: " +
                            str(resp_data.status_code))
            return resp_data.status_code
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False