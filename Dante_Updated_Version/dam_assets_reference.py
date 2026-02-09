import logging
import json
import requests

class DamAssetReference():
    """docstring for DamAssetReference. """ 
    def __init__(self, ip, user, passwd):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.configdata = self.opencode("configfiles\\config.json")
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