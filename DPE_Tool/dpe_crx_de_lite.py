import logging
import json
import time
import re
import requests
from bs4 import BeautifulSoup as bsoup

IP_CONFIG = {
    # "production": "http://10.195.132.229:4502",
    "production": "http://10.248.54.68:4502",
    # "stage": "http://10.195.143.84:4502",
    "stage": "http://10.248.50.36:4502",
    # "qa": "http://10.195.4.169:4502"
    "qa": "http://10.248.53.100:4502"
}

def opencode(file):
    """
    Open the Operation Code from designated Files
    """
    with open(file) as fin:
        data = json.loads(fin.read())
    return data

class DPECrxDeLiteApp:
    """docstring for DamAssetReference. """
    logger = logging.getLogger(__name__)
    configdata = opencode("configfiles\\config.json")
    wfoperationdata = opencode("configfiles\\operationcode.json")

    def __init__(self, ip, user, passwd):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        # self.configdata = self.opencode("configfiles\\config.json")
        self.loglevel = self.configdata.get("loglevel", "error").strip()
        self.sleeptime = self.configdata.get("sleeptime", 1.0)
        self.timeout = self.configdata.get("timeout", 5.0)
        log_level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        self.logger.setLevel(log_level[self.loglevel]) if log_level[self.loglevel] <= logging.INFO else self.logger.setLevel(logging.INFO)
        self.logger.debug("Operation data : %s", str(self.wfoperationdata))
        self.logger.debug("Config data : %s", str(self.configdata))
        
    def get_key(self, data, value):
        try:
            for key_, value_ in data.items():
                if value_ == value:
                    self.logger.debug("Key for Value %s is %s.", key_, value)
                    return key_
            self.logger.warning("No match found for Value %s.", value)
            return None
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def check_json_data(self, response):
        try:
            out = response.json()
            return True
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def read_payload(self, payload):
        try:
            current_time_in_secs = int(time.time() * 1000)
            final_payload = self.ip + "/crx/server/crx.default/jcr:root" + payload + ".1.json?_dc="+str(current_time_in_secs)
            self.logger.debug("Payload: %s", final_payload)
            resp_data = requests.get(final_payload, auth=(self.user, self.passwd), timeout=self.timeout)
            out_msg = None
            if resp_data.status_code == 200:
                is_valid_json_resp = self.check_json_data(resp_data)
                self.logger.debug("Valid JSON: %s", is_valid_json_resp)
                if is_valid_json_resp:
                    # out_msg = resp_data.json()
                    out_msg = dict(sorted(resp_data.json().items()))
                else:
                    out_msg = 901
            else:
                out_msg = resp_data.status_code
            
            self.logger.debug(out_msg)
            return out_msg
                
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def fetch_payload_property(self, payload):
        try:
            out_msg = None
            url = self.ip + payload + ".json"
            resp_data = requests.get(url, auth = (self.user, self.passwd), timeout = self.timeout)
            if resp_data.status_code == 200:
                is_valid_json_resp = self.check_json_data(resp_data)
                self.logger.debug("Valid JSON: %s", is_valid_json_resp)
                if is_valid_json_resp:
                    out_msg = resp_data.json()
                else:
                    out_msg = 901
            else:
                out_msg = resp_data.status_code
            
            self.logger.debug(out_msg)
            return out_msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def update_payload_property(self, payload, post_data):
        try:
            out_msg = None
            url = self.ip + payload
            resp_data = requests.post(url, auth = (self.user, self.passwd), data=post_data, timeout = self.timeout)
            log_msg = f"{payload} was updateded with data {post_data} by {self.user} on {time.asctime()}"
            if resp_data.status_code == 200:
                self.logger.info(log_msg)
            out_msg = resp_data.status_code
            # out_msg = 200
            
            self.logger.debug("%s : %s",payload, str(out_msg))
            return out_msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def get_replication_status(self, payload,):
        try:
            out_msg = None
            time_in_ms = int(time.time() * 1000)
            url = self.ip + "/crx/de/replication.jsp?_dc="+str(time_in_ms)+"&path=" + payload
            self.logger.debug("Payload %s",str(payload) )
            resp_data = requests.get(url, auth = (self.user, self.passwd), timeout = self.timeout)
            if resp_data.status_code == 200:
                is_valid_json_resp = self.check_json_data(resp_data)
                self.logger.debug("Valid JSON: %s", is_valid_json_resp)
                if is_valid_json_resp:
                    out_msg = resp_data.json()
                else:
                    out_msg = 901
            else:
                out_msg = resp_data.status_code
            
            self.logger.debug(out_msg)
            return out_msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def replicate_payload(self, payload, status):
        try:
            out_msg = None
            url = self.ip + "/bin/replicate.json"
            post_data = {
                "path":payload,
                "cmd" :status.lower()
            }
            resp_data = requests.post(url, auth = (self.user, self.passwd), data=post_data, timeout = self.timeout)
            out_msg = resp_data.status_code
            log_msg = f"{payload} was {status} by {self.user} on {time.asctime()}"
            if resp_data.status_code == 200:
                self.logger.info(log_msg)
            self.logger.debug(out_msg)
            return out_msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def create(self, parent_payload, filename, type_):
        try:
            out_msg = None
            if type_.lower() == "nt:file":
                url = self.ip + parent_payload
                data = " ".encode("utf-8")
                files = {filename: data}
                resp_data = requests.post(url, auth = (self.user, self.passwd), files=files, timeout = self.timeout)
                log_msg = f"Type: {type_} of {parent_payload} was created {filename} by {self.user} on {time.asctime()}"
                if resp_data.status_code == 200:
                    self.logger.info(log_msg)

                out_msg = resp_data.status_code
                self.logger.debug("File Selected - URL: %s, Type: %s", str(url), str(type_))
                self.logger.debug("FileData: %s", str(files))
            else:
                url = self.ip + parent_payload + "/" + filename
                post_data = {"jcr:primaryType":type_}
                resp_data = requests.post(url, auth = (self.user, self.passwd), data=post_data, timeout = self.timeout)
                out_msg = resp_data.status_code
                log_msg = f"Type: {type_} of {parent_payload} was created {filename} by {self.user} on {time.asctime()}"
                if resp_data.status_code == 200:
                    self.logger.info(log_msg)
                self.logger.debug("URL: %s, Type: %s", str(url), str(type_))
                self.logger.debug("Data: %s", str(post_data))
            # out_msg = 200
            
            self.logger.debug(out_msg)
            return out_msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999
    
    def rename(self, old, new):
        try:
            out_msg = None
            url = self.ip + old
            self.logger.debug("URL: %s", str(url))
            post_data = {':operation': 'move', ':dest': new}
            log_msg = f"{old} was renamed or moved to {new} by {self.user} on {time.asctime()}"
            resp_data = requests.post(url, auth = (self.user, self.passwd), data=post_data, timeout = self.timeout)
            if resp_data.status_code == 200:
                self.logger.info(log_msg)
            out_msg = resp_data.status_code
            
            self.logger.debug(out_msg)
            return out_msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999
    
    def copy_or_move(self, operation, source, target):
        try:
            out_msg = None
            url = self.ip
            self.logger.debug("URL: %s", str(url))
            target = self.remove_trailing_backslash(target)
            if target is not None:
                post_data = {':operation': operation,':applyTo':source, ':dest': target+"/"}
                resp_data = requests.post(url, auth = (self.user, self.passwd), data=post_data, timeout = self.timeout)
                out_msg = resp_data.status_code
                log_msg = f"Operation {operation} was performed from {source} to {target} by {self.user} on {time.asctime()}"
                if resp_data.status_code == 200:
                    self.logger.info(log_msg)
            else:
                out_msg = 999
            self.logger.debug(out_msg)
            return out_msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999
    
    def delete(self, payload):
        """ Delete a DPE Node """
        try:
            pat1 = r"^\/content(\/dam\/|\/)pwc\/\w{2}\/\w{2}\/"
            pat2 = r"^\/content\/usergenerated(\/archive\/|\/)content\/pwc\/(\w{2}\/\w{2}\/|global\/forms\/contactUsForm\/\d{4}\/)"
            pat3 = r"^\/etc\/map\/http\/"
            allowed_pattern_path = [pat1, pat2, pat3]
            out_msg = None
            is_valid_payload = False
            for _pat in allowed_pattern_path:
                if re.match(_pat, payload):
                    is_valid_payload = True
                    break

            if is_valid_payload:
                url = self.ip + payload
                self.logger.debug("URL: %s", str(url))
                url = self.remove_trailing_backslash(url)
                if url is not None:
                    post_data = {":operation": "delete"}
                    resp_data = requests.post(url, auth = (self.user, self.passwd), data=post_data, timeout = self.timeout)
                    out_msg = resp_data.status_code
                    log_msg = f"Operation Delete was performed on {payload} by {self.user} on {time.asctime()}"
                    if resp_data.status_code == 200:
                        self.logger.info(log_msg)
                else:
                    out_msg = 999
            else:
                out_msg = 902
            self.logger.debug(out_msg)
            return out_msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def search_or_query(self, query="", search_key="", path="/content", query_type="sql"):
        try:
            out_msg = None
            time_in_ms = int(time.time() * 1000)
            env_ = self.get_key(self.configdata, self.ip)
            env_ip_ = IP_CONFIG.get(env_)
            url = env_ip_ + "/crx/explorer/ui/search_results.jsp"
            post_data = {
                "Text":search_key,
                "Path": path,
                "Name": "search",
                "FormEncoding":"utf-8",
                "ck":time_in_ms,
                "Lang":query_type,
                "Query":query
            }
            self.logger.debug("URL: %s", url)
            resp_data = requests.post(url, auth = (self.user, self.passwd), data = post_data, timeout = self.timeout)
            self.logger.debug("Status Code: %s", resp_data.status_code)
            
            if resp_data.status_code == 200:
                log_msg = f"Operation Sear was performed for {search_key} on path {path} by {self.user} on {time.asctime()}"
                self.logger.info(log_msg)
                out_msg = []
                soup = bsoup(resp_data.text, "html.parser")
                error = soup.find(class_='error')
                if bool(error):
                    self.logger.error(error.text)
                    out_msg = 990
                else:
                    all_tables = soup.findAll('table')
                    
                    if bool(all_tables):
                        all_table = all_tables[0]
                        all_node = all_table.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['node'])
                        for _atom in all_node:
                            out_msg.append(str(_atom.text).strip())
                    else:
                        out_msg = 999
                        self.logger.error("No Result Table found in the output.")
            else:
                out_msg = resp_data.status_code
            
            self.logger.debug("Final Output message: %s",str(out_msg))
            return out_msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def get_file_data(self, payload):
        try:
            time_in_ms = int(time.time() * 1000)
            url = self.ip + "/crx/server/crx.default/jcr:root" + payload + "/jcr:content/jcr:data?_dc=" + str(time_in_ms)
            self.logger.debug("URL: %s", url)
            resp_data = requests.get(url, auth = (self.user, self.passwd), timeout = self.timeout)
            log_msg = f"Filedata was accessed for {payload} by {self.user} on {time.asctime()}"
            if resp_data.status_code == 200:
                self.logger.info(log_msg)
            return resp_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def save_file_data(self, payload, file_data, file_name):
        try:
            url = self.ip + payload
            files = {file_name: file_data}
            self.logger.debug("URL: %s", url)
            resp_data = requests.post(url, auth = (self.user, self.passwd), files = files, timeout = self.timeout)
            log_msg = f"Filedata was saved for {payload} and filename {file_name} by {self.user} on {time.asctime()}"
            if resp_data.status_code == 200:
                self.logger.info(log_msg)
            return resp_data.status_code
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    def remove_trailing_backslash(self, url):
        try:
            url = url.strip()
            while(url[-1] == "/"):
                url = url[:-1]
            return url
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    @classmethod
    def password_validator(cls, uname, passwd):
        try:
            status = False
            prod_url = cls.configdata.get("qa", "https://dpe-qa.pwc.com")
            pwd_validator = cls.wfoperationdata.get("password validator","/content/pwc/global/referencedata/territories/gx") + ".json"
            passwd_validator = prod_url + pwd_validator
            response = requests.get(passwd_validator, auth=(uname, passwd), timeout=cls.configdata.get("timeout"))
            if response.status_code == 200:
                status = True

            return status
        except:
            cls.logger.error("Below Exception occurred\n", exc_info=True)
            return False