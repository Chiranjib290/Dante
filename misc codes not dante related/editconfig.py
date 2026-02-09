import json
from datetime import datetime
import logging
import pickle

ALLOWED_CRX_DE_PATH = [
            "/apps/pwc/i18n", "/content/dam",
            "/content/pwc/", "/content/cq:tags",
            "/etc/map/http", "/home", "/var/workflow/instances"
            ]

class EditConfig:
    def __init__(self):
        #self.file = file
        crnt_date = datetime.now()
        frmt_crnt_date = crnt_date.strftime("%m%d%Y")
        self.logfile = "logs\\" + "mainlogfile_"+frmt_crnt_date+".log"
        # logging.basicConfig(filename=self.logfile, filemode='a', level=logging.INFO,
        #                     format='%(asctime)s -> %(name)s -> {%(module)s : %(funcName)s} -> %(lineno)d -> %(levelname)s -> %(message)s')

        logging.basicConfig(handlers=[logging.FileHandler(filename=self.logfile, mode='a+', encoding='utf-8')],
                            format='%(asctime)s -> %(name)s -> {%(module)s : %(funcName)s} -> %(lineno)d -> %(levelname)s -> %(message)s', level=logging.INFO)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def readConfig(self, file):
        data = None
        try:
            with open(file) as fin:
                data = json.loads(fin.read())
            return data
        except FileNotFoundError:
            if file.find("\\config.json") > -1:
                with open(file, "w") as fout:
                    data = {
                            "environments": [
                                "PRODUCTION",
                                "STAGE",
                                "QA",
                                "IP"
                            ],
                            "stage": "https://dpe-stg.pwc.com",
                            "production": "https://dpe.pwc.com",
                            "qa": "https://dpe-qa.pwc.com",
                            "varpathproduction": "/var/workflow/instances/server1",
                            "varpathstage": "/var/workflow/instances/server1",
                            "varpathqa": "/var/workflow/instances/server1",
                            "varpathip": "/var/workflow/instances/server0",
                            "redirectpathdotcomproduction": "/etc/map/http/pwc-az-origin-extpubv3.pwc.com",
                            "redirectpathsandproduction": "/etc/map/http/strategyand-az-origin-extpubv3.pwc.com",
                            "redirectpathdotcomstage": "/etc/map/http/pwc-az-origin-extpub-stgv3.pwc.com",
                            "redirectpathsandstage": "/etc/map/http/strategyand-az-origin-extpub-stgv3.pwc.com",
                            "redirectpathdotcomqa": "/etc/map/http/pwc-az-origin-extpub-qa2.pwc.com",
                            "redirectpathsandqa": "/etc/map/http/strategyand-az-origin-extpub-qa2.pwc.com",
                            "formpath": "/content/usergenerated",
                            "loglevel": "error",
                            "sleeptime": 1.0,
                            "timeout": 30.0,
                            "ip": "",
                            "redirectpathdotcomip": "/etc/map/http/pwc-az-origin-extpub-stgv2.pwc.com",
                            "redirectpathsandip": "/etc/map/http/strategyand-az-origin-extpub-stgv2.pwc.com",
                        }
                    json.dump(data, fout)
                self.logger.error("Below Exception occurred\n", exc_info=True)
                return data
            elif file.find("\\basicconfig.json") > -1:
                with open(file, "w") as fout:
                    data = {"selected theme": "clam"}
                    json.dump(data, fout)
                self.logger.error("Below Exception occurred\n", exc_info=True)
                return data
            elif file.find("\\operationcode.json") > -1:
                with open(file, "w") as fout:
                    data = {"content root": "/content/pwc", "potential spam": "/var/workflow/models/pwc-form-submission-spam-check-v2", "delivery failure": "/var/workflow/models/pwc-form-email", "archive data failed": "/var/workflow/models/pwc-form-email", "mx lookup": "/var/workflow/models/pwc-form-submission-mx-lookup-check-v2", "obscene language": "/var/workflow/models/pwc-form-submission-obscene-check-v2", "email delivery failure title":
                            "Email Delivery Failure due to missing mandatory fields in form or unable to fetch form data as form submission instance is down", "archive failure title": "Archive Data Failed", "allow once": -333061537, "incorrect email domain": -333061545, "add to whitelist": 404898082, "mark as spam": 554442135, "not spam": 554442143, "send email again": -1220565221, "delivery permanently failed": 376268930, "banned words identified": 404898082, "obscene language not used": -333061539, "retry archive data": -38139123, "limit result": 200}
                    json.dump(data, fout)
                self.logger.error("Below Exception occurred\n", exc_info=True)
                return data
            else:
                with open(file, "w") as fout:
                    data = {}
                    json.dump(data, fout)
                self.logger.error("Below Exception occurred\n", exc_info=True)
                return data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def updateConfig(self, data, file):
        try:
            with open(file, "w") as fout:
                json.dump(data, fout, indent=4)
            return True
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def read_pickle_data(self, file):
        data = None
        self.logger.debug("File to be opened: %s", file)
        try:
            with open(file, "rb") as fin:
                data = pickle.load(fin)
            return data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return ALLOWED_CRX_DE_PATH

    def update_pickle_data(self, data, file):
        try:
            self.logger.debug("File to be written: %s", file)
            with open(file, "wb") as fout:
                pickle.dump(data, fout)
            return True
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False
