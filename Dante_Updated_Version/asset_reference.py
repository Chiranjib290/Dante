from bs4 import BeautifulSoup
import pandas as pd
import requests
import threading
import logging
import json
import xlrd
from time import sleep as time_sleep, time as current_time_in_secs

class AssetRefernceException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        

class AssetReference:
    """
    Asset Reference docstring.
    """
    domain = None
    username = None
    password = None
    thread_count = 1
    query_builder_link = None
    current_row = 0
    writeafter = 0
    isplaced = False
    # save_semaphone = []

    def __init__(self):
        """
        Initialize Asset Reference finding from the UI.
        """
        log_level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        self.configdata = self.opencode("configfiles\\config.json")
        self.loglevel = self.configdata["loglevel"]
        self.sleeptime = self.configdata["sleeptime"]
        self.timeout = self.configdata["timeout"]
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level[self.loglevel])
        self.wfoperationdata = self.opencode("configfiles\\operationcode.json")

    def opencode(self, file):
        """
        Open the Operation Code from designated Files
        """
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def config(self, domain, username, password, thread_count = 1):
        """
        Configuring the Asset Reference Script
        """
        self.domain = domain
        self.username = username
        self.password = password
        self.thread_count = thread_count
        self.query_builder_link = self.wfoperationdata.get("query builder link", "/bin/querybuilder.json")

    def read_excel(self, file):
        try:
            self.logger.debug("Excel File to be read: %s", file)
            work_book = xlrd.open_workbook(file)
            work_sheet = work_book.sheet_by_index(0)
            num_rows = work_sheet.nrows
            url_list = []
            for row in range(1, num_rows):
                _payload = str(work_sheet.cell_value(row, 0)).strip()
                if _payload not in url_list:
                    url_list.append(_payload)
            self.logger.debug("Retrieved Payloads -->")
            self.logger.debug(url_list)
            return url_list
        except:
            self.logger.error("Below Exception occurred.\n", exc_info=True)
            return None

    def run_query(self, querystring):
        try:
            connection_url = f'{self.domain}{self.query_builder_link}?{querystring}'
            resp_data = requests.get(connection_url, auth=(self.username, self.password), timeout=self.configdata.get("timeour", 20))
            time_sleep(self.configdata.get("sleeptime", 1.0))
            excerpt_data = {}

            if resp_data.status_code == 200:
                payloads = []
                for hits in resp_data.json().get("hits", []):
                    payloads.append(hits.get("path",""))
                
                excerpt_data = {"status_code": resp_data.status_code, "data": payloads}

            elif resp_data.status_code == 401:
                excerpt_data = {"status_code": resp_data.status_code, "data": "Wrong username and password!"}
            else:
                excerpt_data = {"status_code": resp_data.status_code, "data": "Some Error occurred!"}
            return excerpt_data
        except:
            self.logger.error("Below Exception occurred.\n", exc_info=True)
            return {"status_code": 999, "data": "Exception occurred, Check logs"}

    def get_dam_assets(self, territory):
        """
        Generate Dam asset report for territory
        """
        try:
            if self.domain is None:
                raise AssetRefernceException("Domain can't be None. Please configure the Asset Refernce and pass the value.")
            if self.username is None:
                raise AssetRefernceException("Username can't be None. Please configure the Asset Refernce and pass the value.")
            if self.password is None:
                raise AssetRefernceException("Password can't be None. Please configure the Asset Refernce and pass the value.")

            query = f'p.limit=-1&path=%2fcontent%2fdam%2fpwc%2f{territory}&type=dam%3aAsset'
            c_s = self.run_query(query)
            return c_s
        except Exception as e:
            print(e)
            self.logger.error("Below Exception occurred.\n", exc_info=True)
            return None

    def find_asset_reference(self, payload, lock=False):
        """
        Finding the Asset reference of the given page with in DPE
        """
        matrix = []
        matrix.append(str(payload))

        asset_page_properties = f"{self.domain}/mnt/overlay/dam/gui/content/assets/metadataeditor.external.html?_charset_=utf-8&item={payload}"

        try:
            data = requests.get(self.domain+payload+'/jcr:content.json',
                                auth=(self.username, self.password)).json()
        except:
            data = None

        if data is not None:
            matrix.append(data.get('cq:lastReplicationAction', ""))
            matrix.append(data.get('cq:lastReplicatedBy', ""))
            matrix.append(data.get('cq:lastReplicated', ""))
        else:
            matrix.append("nodata")
            matrix.append("nodata")
            matrix.append("nodata")

        try:
            page_html = BeautifulSoup(requests.get(asset_page_properties, auth=(self.username, self.password)).text, "html.parser")
            asset_referer = ""
            for references in page_html.findAll('div', {'class': 'references-referencing'})[0].findAll('a'):
                asset_referer += references.get("title","Invalid data") + " | "
            matrix.append(asset_referer)
        except:
            matrix.append("Unreferenced")

        return matrix

    def find_page_reference(self, payload):
        """
        Finding the Page reference of the given page with in DPE
        """