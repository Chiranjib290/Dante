# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=bare-except
import logging
import json
import re
from socket import timeout
from time import sleep
import xlrd
import requests


class ContentPathValidator:
    """ Validate the Content Path"""

    def __init__(self, username, password):
        """ Initializing the Class, Usage :  ContentPathValidator(ip,username, password)"""
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)
        self.configdata = self.opencode("configfiles\\config.json")
        self.loglevel = self.configdata["loglevel"]
        self.sleeptime = float(self.configdata["sleeptime"])
        self.timeout = float(self.configdata["timeout"])
        log_level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        self.logger.setLevel(log_level[self.loglevel])
        self.wfoperationdata = self.opencode("configfiles\\operationcode.json")
        self.logger.debug("Configuration data : %s", str(self.configdata))
        self.logger.debug("Operation data : %s", str(self.wfoperationdata))
        self.all_country_mapping = self.sorted_excel_to_list(
            "configfiles\\DPE_url_mapping.xlsx", sort_column=0)

    def opencode(self, file):
        """ Open JSON Settings File """

        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def is_authenticated(self, selected_ip):
        try:
            authenticated = True
            validator_url = self.wfoperationdata["password validator"]
            full_url = selected_ip+validator_url+".json"
            resp = requests.get(full_url, auth=(
                self.username, self.password), timeout=self.timeout)
            if resp.status_code == 401:
                authenticated = False

            return authenticated
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def sorted_excel_to_list(self, file, sort_column=0):
        """ Convert the excel data into userfriendly List Data.
        Usage:  excel_to_list(excel_file) """

        try:
            self.logger.debug("Excel File %s", str(file))
            output_data = []
            work_book = xlrd.open_workbook(file)
            sheet = work_book.sheet_by_index(0)
            nrows = sheet.nrows
            ncols = sheet.ncols
            for row in range(1, nrows):
                chunks = []
                for col in range(ncols):
                    _d = sheet.cell_value(rowx=row, colx=col)
                    if isinstance(_d, str):
                        chunks.append(_d.strip())
                    else:
                        chunks.append(_d)
                output_data.append(chunks)
            # output_data = [sheet.row_values(i) for i in range(sheet.nrows)]
            # headers = output_data[0]
            # output_data = output_data[1:]
            output_data.sort(key=lambda x: x[sort_column])
            self.logger.debug(output_data)
            return output_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def read_country_name(self, file):
        try:
            self.logger.debug("Excel File %s", str(file))
            output_data = []
            work_book = xlrd.open_workbook(file)
            sheet = work_book.sheet_by_index(0)
            numrows = sheet.nrows
            for i in range(0, numrows):
                output_data.append(sheet.cell_value(i, 0))
            return output_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    # Rule 1, Valid Source path, i.e. /content/pwc or /content/dam/pwc
    # Rule 3, assets should be under asset root path
    def valid_source_path(self, source_path):
        try:
            output_status = False
            source_path = source_path.strip(
            ) + "$" if source_path.strip()[-1] != "$" else source_path.strip()
            content_path = self.wfoperationdata["content root"]
            content_dam_path = self.wfoperationdata["content dam root"]

            split_by_slash = source_path.split("/")
            ext = ""
            last_elem = split_by_slash[-1]
            if last_elem.strip() != '$' and last_elem.strip() != '':
                ext_splitted = last_elem.split(".")
                if len(ext_splitted) > 1:
                    ext = ext_splitted[-1]
                else:
                    ext = ""

            if ext in ("", "html$"):
                init_source_path = source_path[:len(content_path)]
                if init_source_path == content_path:
                    output_status = True
            else:
                init_source_path = source_path[:len(content_dam_path)]
                if init_source_path == content_dam_path:
                    output_status = True

            return output_status

        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)

    # Rule 2, Should End with $, if not append a $
    def add_dollar_to_the_end(self, source_path):
        try:
            ending_with = source_path.strip()[-1]
            if ending_with != '$':
                source_path = source_path + '$'

            return source_path

        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)

    # Rule 4, Shouldn't be a Loop in Redirect
    def no_redirect_on_target(self, target):
        try:
            output_status = False
            out = requests.get(target)
            http_status = None
            if bool(out.history):
                http_status = out.history[-1].status_code
            else:
                http_status = out.status_code

            if http_status not in (301, 302, 308):
                output_status = True

            return output_status
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)

    # Rule 5, Source and Target should n't be same URL
    def source_not_same_as_target(self, source, target, env):
        try:
            self.logger.debug(
                "Received Data: Source - %s, Target - %s, Env - %s"
                , str(source), str(target), str(env))
            output_status = False
            content_root = self.wfoperationdata["content root"]
            content_dam_root = self.wfoperationdata["content dam root"]
            modified_source_path = source.replace(content_root, "").replace(
                content_dam_root, "").replace("$", "")
            self.logger.debug("Modified Source Path: %s", modified_source_path)
            # all_country_mapping = self.sorted_excel_to_list(
            #         "configfiles\\DPE_url_mapping.xlsx", sort_column=0)
            country_content_path = ""
            output_url = ""
            # microsite_pat = r'^\/content\/(dam\/)*pwc\/\w{2}\/\w{2}\/website\/([a-zA-Z0-9_\-]+)'
            microsite_pat = r'^\/\w{2}\/\w{2}\/website\/([a-zA-Z0-9_\-]+)'
            _matched_group = re.search(microsite_pat, modified_source_path)
            if _matched_group:
                country_content_path = content_root + _matched_group.group(0)
                self.logger.debug("Line: 187, Country Content Path: %s",
                                  country_content_path)
            else:
                # host = self.wfoperationdata[env.lower().strip()+" live"]
                splitted_country_name = modified_source_path.split(
                    "/")[0] if modified_source_path.split("/")[0] != "" else modified_source_path.split("/")[1]
                self.logger.debug("Line: 193, Country Name: %s", splitted_country_name)
                splitted_country_name= "" if len(splitted_country_name)> 2 else splitted_country_name
                country_content_path = content_root + "/" + splitted_country_name if bool(splitted_country_name) else content_root
                self.logger.debug("Line: 196, Country Content Path: %s",
                                  country_content_path)

            final_host = ""
            for each_country_mapping in self.all_country_mapping:
                if country_content_path in each_country_mapping:
                    self.logger.debug("Matched: %s", str(each_country_mapping))
                    if env == "production":
                        final_host = each_country_mapping[1]
                    elif env == "stage":
                        final_host = each_country_mapping[2]
                    elif env == "qa":
                        final_host = each_country_mapping[3]
                    self.logger.debug("Generated Host: %s", final_host)
                    break

            if final_host == "":
                self.logger.error(
                    "Invalid Source Path!! Mapping is not available in System")
            else:
                if _matched_group:
                    output_url = final_host + \
                        re.sub(microsite_pat, "", modified_source_path)
                else:
                    if bool(splitted_country_name):
                        output_url = final_host + \
                            modified_source_path.replace(
                                "/"+splitted_country_name, "")
                    else:
                        output_url = final_host + modified_source_path
                        
                    self.logger.debug("Generated Output URL: %s", output_url)

                replaced_url_pat = r'^(http\:\/\/|https\:\/\/)*(www\.)*'
                _cleaned_o_url = re.sub(
                    replaced_url_pat, "", output_url, count=0)
                _cleaned_target_url = re.sub(
                    replaced_url_pat, "", target, count=0)
                if _cleaned_o_url != _cleaned_target_url:
                    output_status = True

            return output_status
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)
            return False

    # Rule 6, Source/Target shouldn't have speacial Characters except the valid one
    # Rule 7, Space shouldn't be present in either Source or Target URL
    def valid_source_url_without_spcl_chars(self, source):
        try:
            status = False
            invalid_special_chars = "[@!#%^&*() <>?|}{~:?]"
            output = re.findall(source, invalid_special_chars)

            if len(output) == 0:
                status = True

            return status

        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)

    def valid_target_url_without_spcl_chars(self, target):
        try:
            status = False
            invalid_special_chars = "[@!#$%^&*()<>?|}{~:?]"
            output = re.findall(target, invalid_special_chars)

            if len(output) == 0:
                status = True

            return status

        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)

    def validate_data(self, data):
        try:
            out_status = True
            if len(data) > 1:
                for each in data:
                    if len(each) != 3:
                        out_status = False
                        break
            return out_status
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)

    def get_duplicate_old_url(self, url_list):
        try:
            duplicate_url = []
            for each in url_list:
                if url_list.count(each) > 1:
                    duplicate_url.append(each)

            self.logger.debug("Duplicate URL List: %s", str(duplicate_url))
            return duplicate_url
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)

    def get_empty_url(self, url_list):
        try:
            output_list = []
            for i, each_row in enumerate(url_list, 1):
                if each_row[0].strip() == "":
                    output_list.append("Row: "+str(i)+", Old URL is Empty")
                if each_row[1].strip() == "":
                    output_list.append("Row: "+str(i)+", Target URL is Empty")
                if str(each_row[2]).strip() == "":
                    output_list.append(
                        "Row: "+str(i)+", Redirection type is Empty")

            self.logger.debug(output_list)
            return output_list
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)
            return []

    # curl -d "actype=SAVE&oldurl=/content/pwc/de/de/contacts/c/clemens-frey.html$
    # &newurl=https://www.pwc.de/&status=301"
    # -u shouvik.d.das@in.pwc.com:reset123 -X POST
    # https://dpe.pwc.com/bin/redirectmanager >> Redirect_25062020.html

    def place_redirect(self, dpe_url, source, target, redirect_type):
        try:
            msg = ""
            send_data = {
                "actype": "SAVE",
                "oldurl": source,
                "newurl": target,
                "status": redirect_type
            }
            # dpe_url = self.configdata[env]
            single_redirect_manager_url = dpe_url + \
                self.wfoperationdata.get("single redirect url","/bin/redirectmanager")
            self.logger.debug("Post Data: %s", str(send_data))
            resp_data = requests.post(single_redirect_manager_url, data=send_data, auth=(
                self.username, self.password), timeout=self.timeout)
            sleep(self.sleeptime * 2)

            if resp_data.status_code == 200:
                msg = "Success - "+str(resp_data.status_code)
            elif resp_data.status_code == 401:
                msg = "Wrong username and password - HTTP Status Code " + \
                    str(resp_data.status_code)
            else:
                msg = "Failed - "+str(resp_data.status_code)

            return msg

        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)

    # curl -k -u shouvik.d.das@in.pwc.com:roguepikachu -X POST -F
    # path="/etc/map/http/pwc-az-origin-extpubv2.pwc.com/content/pwc/us/preferencecenter$" -F
    # cmd="activate"
    # https://dpe.pwc.com/bin/replicate.json
    def path_selector(self, environment, pwc_com):
        try:
            com_or_sand = "redirectpathdotcom" if pwc_com else "redirectpathsand"
            # com_or_sand = "pwc_com" if pwc_com else "s_and"
            # print(com_or_sand)
            selector = f"{com_or_sand}{environment.lower()}"
            self.logger.debug(".com or s&? %s - Selector: %s", com_or_sand, selector)
            # redirect_selector = self.wfoperationdata.get(selector)
            redirect_selector = self.configdata.get(selector)
            self.logger.debug("Redirect Selector: %s", redirect_selector)
            return redirect_selector
        except:
            # print(e)
            self.logger.error("Below Exception Occurred!", exc_info=True)
            return None

    def remove_redirect(self, content_path, dpe_url, environment, pwc_com=True):
        try:
            # dpe_url = self.configdata.get(environment)
            if content_path[-1] != "$":
                content_path += "$"
            output = {}
            if dpe_url is not None:
                self.logger.debug(
                    "URL Received: %s,DPE URL: %s, Environment: %s and pwc.com? %s",
                     content_path, dpe_url, environment, pwc_com)
                redirect_selector = self.path_selector(environment, pwc_com)
                final_url = f"{redirect_selector}{content_path}"
                valid_url = f"{dpe_url}{final_url}.json"
                self.logger.debug("Final URL : %s", final_url)
                url_response = requests.get(valid_url, auth=(
                    self.username, self.password), timeout=self.timeout)
                # print(url_response.content)
                if url_response.status_code == 200:
                    data = {"path": final_url, "cmd": "deactivate"}
                    url = dpe_url + "/bin/replicate.json"
                
                    resp_data = requests.post(url, data = data, auth=(
                        self.username, self.password), timeout=self.timeout)

                    if resp_data.status_code >=200 or resp_data.status_code < 208:
                        output["status"] = resp_data.status_code
                        output["payload"] = content_path
                        output["msg"] = "Deactivated Successfully"
                    elif resp_data.status_code == 401:
                        output["status"] = 401
                        output["payload"] = content_path
                        output["msg"] = "Wrong username and Password"
                    else:
                        output["status"] = resp_data.status_code
                        output["payload"] = content_path
                        output["msg"] = "Error Occurred"

                    # print(resp_data.content)

                else:
                    output["status"] = url_response.status_code
                    output["payload"] = content_path
                    output["msg"] = "Error Occurred"
            
            return output
        except:
            self.logger.error("Below Exception Occurred!", exc_info=True)
            return {"status": 999, "payload": content_path, "msg": "Exception Occurred"}
