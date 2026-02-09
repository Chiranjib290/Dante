import logging
from datetime import datetime, timedelta
from urllib.parse import quote
import json
from time import sleep, strptime as time_strptime
from calendar import timegm as cal_timegm
import requests

CURRENT_DATE = datetime.now()


class DPEInboxDashboard:
    """To Retrieve the Data"""

    def __init__(self, ip, user, passwd):
        self.ip = ip.strip()
        self.user = user.strip()
        self.passwd = passwd.strip()
        self.configdata = self.opencode("configfiles\\config.json")
        # print(loglevel)
        self.loglevel = self.configdata["loglevel"]
        self.sleeptime = float(self.configdata["sleeptime"])
        self.timeout = float(self.configdata["timeout"])
        self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(log_level[self.loglevel])
        self.wfoperationdata = self.opencode("configfiles\\operationcode.json")
        self.logger.debug("Configuration data : " + str(self.configdata))
        self.logger.debug("Operation data : " + str(self.wfoperationdata))

    def opencode(self, file):
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def get_archive_data(self, report_older = 1):
        data = []
        # lowerbound_in_sec = int(calendar.timegm(time.strptime(lowerbound, '%Y-%m-%d')) * 1000)
        try:
            today = CURRENT_DATE
            older_date = today - timedelta(days=report_older)

            _lowerbound = older_date.strftime("%Y-%m-%d")
            lowerbound_in_msec = int(cal_timegm(time_strptime(_lowerbound, '%Y-%m-%d')) * 1000)
            archive_data_model = quote(
                self.wfoperationdata["archive data failed"], safe='')
            archive_node_filter = self.wfoperationdata["archive failure node"]
            query_url = self.ip + "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                str(archive_data_model)+"&filter-step=" + \
                str(archive_node_filter)
            self.logger.debug(query_url)

            data_response = requests.get(query_url, auth=(
                self.user, self.passwd), timeout=self.timeout)
            sleep(self.sleeptime)
            if(data_response.status_code == 200):
                temp_data = data_response.json().get("items",[])
                for _itered_data in temp_data:
                    starttime = _itered_data.get("startTime", 0)
                    if starttime > lowerbound_in_msec:
                        data.append(_itered_data)
            elif(data_response.status_code == 401):
                data.append(
                    "Wrong username and Password - Http status " + str(data_response.status_code))
            else:
                data.append(
                    "Some Error occured while connecting. Http Status " + str(data_response.status_code))

            self.logger.debug(data)
            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return data

    def get_mxlookup_data(self, report_older = 1):
        data = []
        try:
            today = CURRENT_DATE
            older_date = today - timedelta(days=report_older)

            _lowerbound = older_date.strftime("%Y-%m-%d")
            lowerbound_in_msec = int(cal_timegm(time_strptime(_lowerbound, '%Y-%m-%d')) * 1000)
            mxlookup_data_model = quote(
                self.wfoperationdata["mx lookup"], safe='')

            query_url = self.ip + "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                str(mxlookup_data_model)
            self.logger.debug(query_url)

            data_response = requests.get(query_url, auth=(
                self.user, self.passwd), timeout=self.timeout)
            sleep(self.sleeptime)
            if(data_response.status_code == 200):
                temp_data = data_response.json().get("items",[])
                for _itered_data in temp_data:
                    starttime = _itered_data.get("startTime", 0)
                    if starttime > lowerbound_in_msec:
                        data.append(_itered_data)
            elif(data_response.status_code == 401):
                data.append(
                    "Wrong username and Password - Http status " + str(data_response.status_code))
            else:
                data.append(
                    "Some Error occured while connecting. Http Status " + str(data_response.status_code))

            self.logger.debug(data)
            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return data

    def get_email_delivery_data(self, report_older = 1):
        data = []
        try:
            today = CURRENT_DATE
            older_date = today - timedelta(days=report_older)

            _lowerbound = older_date.strftime("%Y-%m-%d")
            lowerbound_in_msec = int(cal_timegm(time_strptime(_lowerbound, '%Y-%m-%d')) * 1000)
            delivery_fail_data_model = quote(
                self.wfoperationdata["delivery failure"], safe='')
            delivery_fail_node_filter = self.wfoperationdata["email delivery failure node"]
            query_url = self.ip + "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                str(delivery_fail_data_model)+"&filter-step=" + \
                str(delivery_fail_node_filter)
            self.logger.debug(query_url)

            data_response = requests.get(query_url, auth=(
                self.user, self.passwd), timeout=self.timeout)
            sleep(self.sleeptime)
            if(data_response.status_code == 200):
                temp_data = data_response.json().get("items",[])
                for _itered_data in temp_data:
                    starttime = _itered_data.get("startTime", 0)
                    if starttime > lowerbound_in_msec:
                        data.append(_itered_data)
            elif(data_response.status_code == 401):
                data.append(
                    "Wrong username and Password - Http status " + str(data_response.status_code))
            else:
                data.append(
                    "Some Error occured while connecting. Http Status " + str(data_response.status_code))

            self.logger.debug(data)
            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return data

    def get_potential_spam_data(self, report_older = 1):
        data = []
        try:
            today = CURRENT_DATE
            older_date = today - timedelta(days=report_older)

            _lowerbound = older_date.strftime("%Y-%m-%d")
            lowerbound_in_msec = int(cal_timegm(time_strptime(_lowerbound, '%Y-%m-%d')) * 1000)
            potential_spam_data_model = quote(
                self.wfoperationdata["potential spam"], safe='')
            potential_spam_node_filter = self.wfoperationdata["potential spam node"]
            query_url = self.ip + "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                str(potential_spam_data_model)+"&filter-step=" + \
                str(potential_spam_node_filter)
            self.logger.debug(query_url)

            data_response = requests.get(query_url, auth=(
                self.user, self.passwd), timeout=self.timeout)
            sleep(self.sleeptime)
            if(data_response.status_code == 200):
                temp_data = data_response.json().get("items",[])
                for _itered_data in temp_data:
                    starttime = _itered_data.get("startTime", 0)
                    if starttime > lowerbound_in_msec:
                        data.append(_itered_data)
            elif(data_response.status_code == 401):
                data.append(
                    "Wrong username and Password - Http status " + str(data_response.status_code))
            else:
                data.append(
                    "Some Error occured while connecting. Http Status " + str(data_response.status_code))

            self.logger.debug(data)
            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return data

    def get_form_data_on_hold_data(self, report_older = 1):
        data = []
        try:
            today = CURRENT_DATE
            older_date = today - timedelta(days=report_older)

            _lowerbound = older_date.strftime("%Y-%m-%d")
            lowerbound_in_msec = int(cal_timegm(time_strptime(_lowerbound, '%Y-%m-%d')) * 1000)
            form_data_on_hold_data_model = quote(
                self.wfoperationdata["potential spam"], safe='')
            form_data_on_hold_node_filter = self.wfoperationdata["form data on hold node"]
            query_url = self.ip + "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                str(form_data_on_hold_data_model)+"&filter-step=" + \
                str(form_data_on_hold_node_filter)
            self.logger.debug(query_url)

            data_response = requests.get(query_url, auth=(
                self.user, self.passwd), timeout=self.timeout)
            sleep(self.sleeptime)
            if(data_response.status_code == 200):
                temp_data = data_response.json().get("items",[])
                for _itered_data in temp_data:
                    starttime = _itered_data.get("startTime", 0)
                    if starttime > lowerbound_in_msec:
                        data.append(_itered_data)
            elif(data_response.status_code == 401):
                data.append(
                    "Wrong username and Password - Http status " + str(data_response.status_code))
            else:
                data.append(
                    "Some Error occured while connecting. Http Status " + str(data_response.status_code))

            self.logger.debug(data)
            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return data

    def get_obscene_lang(self, report_older = 1):
        data = []
        try:
            today = CURRENT_DATE
            older_date = today - timedelta(days=report_older)

            _lowerbound = older_date.strftime("%Y-%m-%d")
            lowerbound_in_msec = int(cal_timegm(time_strptime(_lowerbound, '%Y-%m-%d')) * 1000)
            obscene_lang_data_model = quote(
                self.wfoperationdata["obscene language"], safe='')
            # obscene_lang_node_filter = self.wfoperationdata["potential spam node"]
            query_url = self.ip + "/libs/cq/workflow/content/inbox/list.json?filter-itemType=workitem&filter-model=" + \
                str(obscene_lang_data_model)
            # +"&filter-step="+str(obscene_lang_node_filter)
            self.logger.debug(query_url)

            data_response = requests.get(query_url, auth=(
                self.user, self.passwd), timeout=self.timeout)
            sleep(self.sleeptime)
            if(data_response.status_code == 200):
                temp_data = data_response.json().get("items",[])
                for _itered_data in temp_data:
                    starttime = _itered_data.get("startTime", 0)
                    if starttime > lowerbound_in_msec:
                        data.append(_itered_data)
            elif(data_response.status_code == 401):
                data.append(
                    "Wrong username and Password - Http status " + str(data_response.status_code))
            else:
                data.append(
                    "Some Error occured while connecting. Http Status " + str(data_response.status_code))

            self.logger.debug(data)
            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return data

    def get_form_readyforprocessing(self, report_older = 1):
        data = []
        try:
            status = "Ready for processing"
            self.logger.info("Processing Status: %s", str(status))
            data = self.get_form_data(status, report_older=report_older)

            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return data

    def get_form_processed(self, report_older = 1):
        data = []
        try:
            status = "Processed"
            self.logger.info("Processing Status: %s", str(status))
            data = self.get_form_data(status, report_older=report_older)

            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return data

    def get_form_submitted(self, report_older = 1):
        data = []
        try:
            status = "Submitted"
            self.logger.info("Processing Status: %s", str(status))
            data = self.get_form_data(status, report_older = report_older)

            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return data

    def get_form_data(self, status, report_older = 1):
        try:
            today = CURRENT_DATE

            ystrday = today - timedelta(days = report_older)
            _lowerbound = ystrday.strftime("%Y-%m-%d")
            lowerbound = _lowerbound
            self.logger.info("Lower Bound: %s", lowerbound)
            initial_path = self.wfoperationdata.get("form content path", "/content/usergenerated/content/pwc")
            daterange_prop = "cq%3alastReplicated"
            excluded_path = "%2fcontent%2fusergenerated%2fcontent%2fpwc%2fgx%2fen%2fservices%2fpeople-organisation%2fpublications%2fworkforce-of-the-future%2fquiz"
            filter_data = f"1_daterange.lowerBound={lowerbound}&1_daterange.property={daterange_prop}&2_property=*%2fstatus&2_property.value={str(status)}&3_property=formid&3_property.operation=exists&group.1_group.p.not=true&group.1_group.path={excluded_path}&group.1_group.path.self=true&p.limit=-1&path={initial_path}"

            query = self.ip + self.wfoperationdata["query builder link"] + "?" + filter_data

            self.logger.debug("Generated Query: %s",query)
            data_response = requests.get(query , auth=(self.user, self.passwd), timeout=self.timeout)
            sleep(self.sleeptime)
            self.logger.debug(data_response)
            if data_response.status_code == 200:
                if data_response.json()["success"]:
                    data = data_response.json().get("hits", [])
                    for _excerpt_data in data:
                        path = _excerpt_data["path"]
                        name = path.split("/")[-1]
                        suffix_list = name.split("_")
                        suffix = suffix_list[0] if bool(suffix_list) else name
                        new_path = f"{path}/{suffix}"
                        _excerpt_data["path"] = new_path
                else:
                    data = data_response.json().get("errorMessage", [])
            elif data_response.status_code == 401:
                data = ["Wrong username and Password - Http status " + str(data_response.status_code),]
            else:
                data = ["Some Error occured while connecting. Http Status " + str(data_response.status_code),]

            return data
        except:
            self.logger.error("Below Exception Occured!\n", exc_info=True)
            return []