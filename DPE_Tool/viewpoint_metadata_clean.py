import pandas as pd
import os
import json
import logging
from datetime import datetime

METADATA_OPERATION = {
    "select": "--SELECT--",
    "more_column": "CSV/Excel with One or More column",
    "more_sheets": "Excel File with More Sheet"
}

class MetaDataClean:
    """docstring for MetaDataClean."""

    def __init__(self):
        """
        Initialize the MetaDataClean Class. default meta_data_clean = MetaDataClean()
        """
        self.outdir = None
        self.inputfilepath = None
        self.headerfile = "configfiles\\header_file.txt"
        self.logger = logging.getLogger()
        self.configdata = self.opencode("configfiles\\config.json")
        self.asset_prefix = '/content/dam/pwc-madison/ditaroot/'
        loglevel = self.configdata.get("loglevel", "error")
        log_level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        self.logger.setLevel(log_level[loglevel])
        self.logger.debug("Config data : " + str(self.configdata))

    def config(self, inputfilepath, outdir):
        """
        Configuring the File and Output Directory. 
        Default config_set_status = meta_data_clean.config(inputfilepath, outdir)
        """
        try:
            self.outdir = outdir
            self.inputfilepath = inputfilepath
            return True
        except:
            self.logger.error("Below exception occurred.\n", exc_info=True)
            return False

    def opencode(self, file):
        """
        Open the Operation Code from designated Files.
        Default operation_data = meta_data_clean.opencode(configfile)
        """
        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def merge_column(self, dataframe):
        """
        Merging CSV/Excel Columns.
        Default merge_column_data = meta_data_clean.merge_column(dataframe)
        """
        try:
            headers = dataframe.columns.values
            self.logger.debug("Headers: "+str(headers))
            for head in headers:
                itr = 1
                head_str = head + '.' + str(itr)
                self.logger.debug("HeadString: %s", head_str)
                while(head_str in headers):
                    for index, row in dataframe.iterrows():
                        if (pd.isna(row[head_str]) == False):
                            if not pd.isna(row[head]):
                                dataframe.loc[index, head] = str(
                                    row[head])+'|'+str(row[head_str])
                            else:
                                dataframe.loc[index, head] = str(row[head_str])
                    dataframe.drop(head_str, axis=1, inplace=True)

                    itr = itr + 1
                    head_str = head + '.' + str(itr)

            return dataframe
        except:
            self.logger.error("Below exception occurred.\n", exc_info=True)
            return pd.DataFrame()

    def create_header_list(self, header_file=None):
        """
        To Generate the HeaderList.
        Default header_list = meta_data_clean.create_header_list(header_file=filepath)
        """
        default_value = ["assetPath", "dc:title{{String}}", "pwc-contentId{{String}}", "pwc-contentType{{String}}",
                         "pwc-audience{{String}}", "pwc-access{{String}}", "pwc-copyright{{String: multi }}", "pwc-standardsetter{{String}}",
                         "cq:tags{{String: multi }}", "pwc-shortcode{{String}}", "pwc-guidanceTerms{{String: multi }}",
                         "pwc-suggestedGuidance{{String}}", "pwc:isPublishingPoint{{String}}", "dc:description{{String}}",
                         "docstate{{String}}", "jcr:description{{String}}", "attrValList{{String}}", "dam:size{{Long}}",
                         "dc:format{{String}}", "dita_class{{String}}", "dam:sha1{{String}}", "jcr:lastModifiedBy{{String}}",
                         "pwc-docContextSearch{{String}}", "pwc-editExpiryDateField{{String}}", "pwc-metaRobots{{String}}",
                         "pwc-hiddenFromSiteSearch{{String}}", "pwc-originalReleaseDate{{Date}}", "pwc-publicationDate{{Date}}",
                         "dc:modified{{Date}}", "jcr:lastModified{{Date}}", "dam:extracted{{Date}}"]
        try:
            if header_file is not None:
                with open(header_file, "r") as file:
                    header = [line.strip()
                              for line in file if line.strip() != ""]
            else:
                header = default_value.copy()

            self.logger.debug("Header List: "+str(header))
            return header
        except:
            self.logger.error(
                "Below exception occurred. Returning Default Value\n", exc_info=True)
            return default_value

    def check_file_type(self):
        """
        Determine the File Type of the selected File
        """
        try:
            _, file_ext = os.path.splitext(self.inputfilepath)
            self.logger.debug("Extension of the Input Filepath %s is %s", self.inputfilepath, file_ext)
            return str(file_ext).lower()
        except:
            self.logger.error(
                "Below exception occurred. Returning Default Value\n", exc_info=True)
            return None

    def get_data_frame(self):
        """
        Fetch the Dataframe for Different type of filetypes
        """
        try:
            data_frame_ = None
            file_ext_ = self.check_file_type()
            self.logger.debug("File Extenstion: %s", file_ext_)
            if file_ext_ in (".xlsx",".xls", ".xlsm", ):
                data_frame_ = pd.read_excel(self.inputfilepath)
            elif file_ext_ == ".csv":
                data_frame_ = pd.read_csv(self.inputfilepath)
            
            return data_frame_
        except:
            self.logger.error(
                "Below exception occurred. Returning Default Value\n", exc_info=True)
            return None

    def run(self, operation, log_list, vp_ui):
        """
        To Perform Initial Check before the Cleansing Operation on Dataframe
        """
        try:
            output_status = False
            if operation == METADATA_OPERATION["more_column"]:
                data_frame_ = self.get_data_frame()
                if data_frame_ is not None:
                    sheet_status = self.clean_data(data_frame_)
                    
                    sheet_status_code = sheet_status.get('code', 990)
                    sheet_status_message = sheet_status.get('message', 'Error in Process')
                    output_status = True if sheet_status_code == 200 else False
                    log_list.insert("end", f"Sheetname: sheet, Status: {sheet_status_code}, Message: {sheet_status_message}")
                    vp_ui.update()
                else:
                    log_list.insert("end", "Sheetname: sheet, Status: 999, Message: Invalid Filetype, Should be CSV or Excel")
                    vp_ui.update()

            elif operation == METADATA_OPERATION["more_sheets"]:
                file_ext_ = self.check_file_type()
                if file_ext_ in (".xlsx",".xls", ".xlsm", ):
                    all_data_frame = pd.read_excel(self.inputfilepath, sheet_name=None)
                    for sheet_name, sheet_data in all_data_frame.items():
                        sheet_status = self.clean_data(sheet_data)
                        sheet_status_code = sheet_status.get('code', 990)
                        sheet_status_message = sheet_status.get('message', 'Error in Process')
                        output_status = True if sheet_status_code == 200 else False
                        log_list.insert("end", f"Sheetname: {sheet_name}, Status: {sheet_status_code}, Message: {sheet_status_message}")
                        vp_ui.update()
                else:
                    log_list.insert("end", "Sheetname: sheet, Status: 999, Message: Invalid Filetype, Should be Excel")
                    vp_ui.update()
            else:
                log_list.insert("end", "Sheetname: sheet, Status: 999, Message: Invalid Operation Selection")
                vp_ui.update()
            
            return output_status
        except:
            self.logger.error(
                "Below exception occurred. Returning Default Value\n", exc_info=True)
            return False

    def clean_data(self, master_dataframe):
        """
        To Perform the Cleansing Operation on Dataframe
        """
        try:
            return_code = {}
            # master_dataframe = pd.read_csv(self.inputfilepath)
            master_dataframe = self.merge_column(master_dataframe)
            header_list = self.create_header_list(header_file=self.headerfile)
            data_frame_headers = master_dataframe.columns.values

            # Header Validation
            header_validated = True
            for elem in data_frame_headers:
                if elem not in header_list:
                    header_validated = False
                    return_code["code"] = 404
                    return_code["message"] = str(
                        elem) + " Header not in Predefined List"
                    break

            if header_validated:
                # Asset path validation and validation for // in asset path
                for index, row in master_dataframe.iterrows():
                    if (pd.isna(row[0])) or (not row[0].startswith(self.asset_prefix)) or (row[0].find('//') != -1):
                        master_dataframe.drop(index, inplace=True)

                # Remove duplicate assetPath
                master_dataframe.drop_duplicates(
                    subset=['assetPath'], keep='first', inplace=True)

                # Reset Index
                master_dataframe.reset_index(drop=True, inplace=True)

                _check_str = "{{Date}}"

                # Split Columns into CSV Files
                for i in range(len(data_frame_headers) - 1):
                    column_ = data_frame_headers[i+1]
                    new_dataframe = master_dataframe[master_dataframe[column_].notnull()][[
                        'assetPath', column_]]
                    # new_dataframe = new_dataframe.dropna()
                    new_dataframe = new_dataframe.mask(new_dataframe.eq("None")).dropna()
                    
                    if _check_str in column_:
                        new_dataframe.reset_index(inplace=True, drop=True)
                        new_dataframe[column_] = pd.to_datetime(new_dataframe[column_], errors='ignore', utc=True) #format="%Y-%m-%dT%H:%M:%S.000Z"
                        # new_dataframe[column_] = new_dataframe[column_].apply(lambda x :
                        #         x.strftime('%Y-%m-%d') + 'T' + x.strftime('%H:%M:%S') + '.000Z' if isinstance(x, datetime) else x ) 
                        new_dataframe[column_] = new_dataframe[column_].dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                    
                    save_file = os.path.join(self.outdir, column_.replace(':','-')+'.csv')
                    new_dataframe.to_csv(save_file, encoding = 'utf-8', index = False)
                return_code["code"] = 200
                return_code["message"] = "Successfully Generated"
            return return_code

        except:
            self.logger.error("Below exception occurred.\n", exc_info=True)
            return {"code": 999, "message": "Exception Occurred"}
