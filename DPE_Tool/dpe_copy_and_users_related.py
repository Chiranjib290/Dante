import time
import json
import logging
import xlrd
import requests

class UserAccountsAndCopy:
    """Made by Shouvik Das, Date: 22/04/2021.
    DPE User accounts update or Delete Users in Bulk
    """
    def __init__(self, ip, user, passwd):
        """
        Initialize the Constructor
        """
        self.ip = ip.strip()
        self.user = user.strip()
        self.passwd = passwd.strip()

        self.configdata = self.opencode("configfiles\\config.json")

        self.loglevel = self.configdata["loglevel"].strip()
        self.sleeptime = self.configdata["sleeptime"]
        self.timeout = self.configdata["timeout"]

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
        self.logger.debug("Operation data : " + str(self.wfoperationdata))
        self.logger.debug("Config data : " + str(self.configdata))

    def opencode(self, file):
        """
        Open the Operation Code from designated Files
        """
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def read_data(self, file):
        try:
            self.logger.debug("Excel File "+str(file))
            url_list = []
            work_book = xlrd.open_workbook(file)
            work_sheet = work_book.sheet_by_index(0)
            num_rows = work_sheet.nrows
            num_cols = work_sheet.ncols
            for row in range(1, num_rows):
                chunks = []
                for col in range(0, num_cols):
                    if bool(str(work_sheet.cell_value(row, col)).strip()):
                        chunks.append(work_sheet.cell_value(row, col))
                url_list.append(chunks)
            self.logger.debug(url_list)
            return url_list
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def get_user_payload(self, username):
        try:
            return_msg = None
            auth_token = (self.user, self.passwd)
            query_url = self.wfoperationdata["query builder link"]
            query_filter = "path=%2fhome%2fusers&property=rep%3aauthorizableId&property.value="+username
            
            full_url = self.ip + query_url + "?" + query_filter
            self.logger.debug("Query: %s" % full_url)
            output_data = requests.get(full_url, auth=auth_token, timeout=self.timeout)
            
            if output_data.status_code == 200:
                data = output_data.json()
                if data.get("results",0) > 0:
                    self.logger.debug("Response Data: "+str(data))
                    uname_payload = data["hits"][0].get("path", None)
                    return_msg = uname_payload
                else:
                    return_msg = 901
            elif output_data.status_code == 401:
                # return_msg = "Wrong username and password. Http Status Code - 401"
                return_msg = 401
            else:
                # return_msg = "Error Occurred. Http Status Code - "+str(output_data.status_code)
                return_msg = output_data.status_code
            self.logger.debug(return_msg)
            return return_msg
                
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)
            return None

    def assign_everyone_group(self, payload):
        try:
            auth_token = (self.user, self.passwd)
            send_user_data = {'membership':'everyone'}
            user_url = self.ip + payload+ ".rw.html"
            self.logger.debug("User Post URL: %s", user_url)
            self.logger.debug("Send Data: %s", str(send_user_data))
            resp_data = requests.post(user_url, data=send_user_data, auth=auth_token,timeout=self.timeout)
            
            return resp_data.status_code
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)
            return 999

    def s_toggle_user_status(self, payload, operation):
        try:
            auth_token = (self.user, self.passwd)
            # send_user_data = {'_charset_':'utf-8','path':payload, 'cmd':operation}
            # deactivation_url = self.ip + "/bin/replicate.json"
            disable = "inactive" if operation.lower() == "disable" else ""
            send_user_data = {'_charset_':'utf-8', 'disableUser':disable}
            deactivation_url = f"{self.ip}{payload}.rw.html"
            self.logger.debug("Deactivation URL: %s", deactivation_url)
            self.logger.debug("Post Data: %s", str(send_user_data))
            resp_data = requests.post(deactivation_url,data=send_user_data,auth=auth_token,timeout=10)
            time.sleep(self.sleeptime)
            
            return resp_data.status_code
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)
            return 999

    def toggle_user_status(self, username, operation):
        try:
            output_msg = None
            _user_payload = self.get_user_payload(username)
            self.logger.debug("Username %s, User_Payload %s, Operation: %s", username, _user_payload, operation)
            if _user_payload is not None:
                if not(isinstance(_user_payload, int)):
                    if operation.lower() == "disable":
                        _everyone_group_add_status = self.assign_everyone_group(_user_payload)
                    else:
                        _everyone_group_add_status = 200

                    self.logger.debug("Everyone Group added? %s", _everyone_group_add_status)
                    time.sleep(0.5)
                    if _everyone_group_add_status == 200:
                        _user_ops_status = self.s_toggle_user_status(_user_payload, operation)
                        output_msg = _user_ops_status
                        self.logger.debug("Operation %s Status on user %s is %s", operation, username, _user_ops_status)
                    else:
                        output_msg = _everyone_group_add_status
                else:
                    output_msg = _user_payload
            else:
                output_msg = 999

            self.logger.debug("Final Output msg is: %s", output_msg)
            return output_msg

        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)
            return 999
    
    def create_parent_folder(self, target):
        try:
            status_code = 904 # Can't Create folder
            if target.startswith(self.wfoperationdata.get("content dam root", "/content/dam/pwc")):
                self.logger.info("Creating folder: %s", target)
                create_data = {'jcr:primaryType':'sling:OrderedFolder'}
            elif target.startswith(self.wfoperationdata.get("form archive content path", "/content/usergenerated/archive/content/pwc")):
                self.logger.info("Creating Ordered folder: %s", target)
                create_data = {'jcr:primaryType':'sling:Folder'}
            else:
                create_data = {}
            if bool(create_data):
                resp = requests.post(str(self.ip+target) , data=create_data, auth=(self.user, self.passwd))
                self.logger.debug(resp.text)
                status_code = resp.status_code
            return status_code
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)

    def copy_move_node(self, source, target, operation, published_page_copy, create_parent):
        try:
            self.logger.info("Source: "+str(source)+", Target: "+str(target)+", Operation: "+str(operation)+
                    ", Published Page Copy: "+str(published_page_copy)+", Create Parent: "+str(create_parent))
            activated_in_publish = True
            status_code = 902  # Failed
            if published_page_copy:
                if source.startswith(self.wfoperationdata.get("content root", "/content/pwc")):
                    resp = requests.get(self.ip + source +"/jcr:content.json",auth=(self.user, self.passwd), timeout=self.timeout)
                    if resp.status_code == 200:
                        activated_in_publish = resp.json().get("activatedInPublish",False)
                    else:
                        activated_in_publish = False
                else:
                    activated_in_publish = False
                    status_code = 905

            if activated_in_publish:
                creation_status = 200
                if create_parent:
                    creation_status = self.create_parent_folder(target)
                    target = target + "/"
                if creation_status in(200, 201):
                    mov_data = {':operation':operation.lower(),':applyTo':source,':dest':target}
                    self.logger.debug("Move/Copy Data: %s", str(mov_data))
                    resp_data = requests.post(self.ip , data=mov_data, auth=(self.user, self.passwd), timeout=self.timeout)
                    time.sleep(self.sleeptime)
                    self.logger.debug(resp_data.text)
                    status_code = resp_data.status_code
                else:
                    status_code = creation_status

            return status_code
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)
            return 999
