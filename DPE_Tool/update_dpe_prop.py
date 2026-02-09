import json
import logging
from time import sleep
import xlrd
import requests


class UpdateDPEProperties:
    def __init__(self, ip, uname, passwd):
        """ Initializing the Class, Usage :  UpdateDPEProperties(ip,username, password)"""

        self.logger = logging.getLogger(__name__)
        self.ip = ip.strip()
        self.user = uname.strip()
        self.passwd = passwd.strip()
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
        self.logger.debug("Configuration data : " + str(self.configdata))
        self.logger.debug("Operation data : " + str(self.wfoperationdata))

    def set_uname_pass(self, uname, passwd):
        try:
            self.user = uname
            self.passwd = passwd
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def opencode(self, file):
        """ Open JSON Settings File """

        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def ctype_to_val(self, ctype_data):
        try:
            out_data = None
            # print(ctype_value)
            if ctype_data == 3:
                out_data = "Date"
            elif ctype_data == 2:
                out_data = "String"
            elif ctype_data == 4:
                out_data = "Boolean"
            elif ctype_data == 1:
                out_data = "String"
            else:
                out_data = "String"
            return out_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "String"

    def ctype_return_data(self, data, ctype_value):
        try:
            out_data = None
            # print(ctype_value)
            if ctype_value == 3:
                out_data = self.convert_to_date(data)
            elif ctype_value == 2:
                out_data = int(data)
            elif ctype_value == 4:
                out_data = bool(data)
            elif ctype_value == 1:
                out_data = data
            else:
                out_data = ""

            self.logger.debug("Ctype : "+str(ctype_value) +
                              ", Data: "+str(out_data))
            return out_data

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return data

    def convert_to_date(self, data):
        try:
            datetime_date = xlrd.xldate_as_datetime(data, 0)
            mili_seconds = int(int(datetime_date.strftime("%f"))/1000)
            mili_seconds = str(mili_seconds) * \
                3 if mili_seconds == 0 else str(mili_seconds)
            string_date = datetime_date.strftime("%Y-%m-%dT%H:%M:%S")
            final_date = string_date + "." + str(mili_seconds) + "+05:30"
            return final_date
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return data

    def reform_data(self, file, validate_old_data):
        try:
            opened_wb = xlrd.open_workbook(file, on_demand=True)
            op_sheet = opened_wb.sheet_by_index(0)
            num_rows = op_sheet.nrows
            num_cols = op_sheet.ncols
            output_data = []
            for row_num in range(1, num_rows):
                init_row = None
                value_type = op_sheet.cell_value(row_num, num_cols-1)
                self.logger.debug(
                    "Excel Data Valuetype either multi/single: "+str(value_type))
                if value_type.lower().strip() == "multi":
                    value = op_sheet.cell(row_num, num_cols-2).value
                    self.logger.debug("Excel Data : "+str(value))
                    ctype_value = op_sheet.cell(row_num, num_cols-2).ctype
                    if ctype_value == 1:
                        splitted_value = [
                            x.strip() for x in value.split(",") if x.strip() != '']
                    elif ctype_value == 2:
                        splitted_value = [value, ]
                    else:
                        splitted_value = []

                    if num_cols == 5 and validate_old_data:
                        old_value = op_sheet.cell(row_num, 2).value
                        ctype_old_value = op_sheet.cell(row_num, 2).ctype
                        if ctype_old_value == 1:
                            splitted_old_value = [
                                x.strip() for x in old_value.split(",") if x.strip() != '']
                        elif ctype_old_value == 2:
                            splitted_old_value = [old_value, ]
                        else:
                            splitted_old_value = []

                        init_row = [op_sheet.cell_value(row_num, 0), op_sheet.cell_value(
                            row_num, 1), splitted_old_value, splitted_value, value_type.title()]
                    elif num_cols == 4:
                        init_row = [op_sheet.cell_value(row_num, 0), op_sheet.cell_value(
                            row_num, 1), splitted_value, value_type.title()]
                    else:
                        init_row = []
                else:
                    init_row = []
                    for col_id in range(0, num_cols - 1):
                        c_type = op_sheet.cell(row_num, col_id).ctype
                        val = op_sheet.cell(row_num, col_id).value
                        self.logger.debug("Excel Data : "+str(val))
                        init_row.append(self.ctype_return_data(val, c_type))

                    update_val_type = op_sheet.cell(
                        row_num, num_cols - 2).ctype
                    updated_val = self.ctype_to_val(update_val_type)
                    init_row.append(updated_val)

                    # init_row = init_row[:-1]
                self.logger.debug("Init Row: "+str(init_row))
                output_data.append(init_row)
            opened_wb.release_resources()
            return output_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def sorted_excel_to_list(self, file, validate_old_data, sort_column=0):
        """ Convert the excel data into userfriendly List Data. Usage:  excel_to_list(excel_file) """

        try:
            self.logger.debug("Excel File "+str(file))
            output_data = []
            # output_data = [sheet.row_values(i) for i in range(sheet.nrows)]
            output_data = self.reform_data(file, validate_old_data)
            # headers = output_data[0]
            # output_data = output_data[1:]
            output_data.sort(key=lambda x: x[sort_column])
            self.logger.debug(output_data)
            return output_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def update_or_create_node(self, uri, post_data, operation_type):
        try:
            """ Update Property with value. Usage:  update_or_create_node(uri, prop, data) """
            # append_value = True
            post_url = self.ip + uri
            msg = ""

            output_data = requests.post(post_url, data=post_data, auth=(
                self.user, self.passwd), timeout=self.timeout)
            post_stat_code = output_data.status_code

            if post_stat_code == 200:
                msg = uri + " - "+operation_type.title()+" Successfully - "+str(post_stat_code)
            elif post_stat_code == 401:
                msg = "Wrong username and Password - Http status " + \
                    str(post_stat_code)
            else:
                msg = uri + " - Failed to Update - "+str(post_stat_code)

            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return ""

    def get_keys(self, post_data):
        try:
            self.logger.debug("Passed Data: "+str(post_data))
            _out_val = []
            if isinstance(post_data, (list, tuple)):
                for _each_data in post_data:
                    for _each_key in _each_data:
                        self.logger.debug("Each Key: "+str(_each_key))
                        # Remove TypeHint and @Patch
                        _final_key = _each_key.replace(
                            "@TypeHint", "").replace("@Patch", "").strip()
                        self.logger.debug("Final Key: "+str(_final_key))
                        if _final_key not in (_out_val):
                            _out_val.append(_final_key)

            elif isinstance(post_data, dict):
                for _each_key in post_data:
                    self.logger.debug("Each Key: "+str(_each_key))
                    # Remove TypeHint and @Patch
                    _final_key = _each_key.replace(
                        "@TypeHint", "").replace("@Patch", "").strip()
                    self.logger.debug("Final Key: "+str(_final_key))
                    if _final_key not in (_out_val):
                        _out_val.append(_final_key)

            self.logger.debug("All Keys: "+str(_out_val))
            return _out_val

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return []

    def validate_old_data(self, resp_json, prop, old_data):
        try:
            output = False
            current_data = resp_json[prop]
            # _current_data = None
            # _old_data = None
            if isinstance(current_data, (list, tuple)):
                current_data.sort()
            if isinstance(old_data, (list, tuple)):
                old_data.sort()
            self.logger.debug("Current Data: " +
                              str(current_data)+", Old Data: "+str(old_data))

            output = current_data == old_data
            return output
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return False

    def update_property_value(self, uri, post_data, is_valid_old_data, old_data):
        """ Update Property with value. Usage:  update_property_value(uri, prop, data) """
        try:
            passed_data = str(uri) + " - " + str(post_data)
            self.logger.info(passed_data)
            msg = ""
            full_uri = self.ip + uri + ".json"
            valid_data = True

            resp_data = requests.get(full_uri, auth=(
                self.user, self.passwd), timeout=self.timeout)
            sleep(0.5)
            stat_code = resp_data.status_code
            prop_not_available = []
            if stat_code == 200:
                try:
                    resp_data_json = resp_data.json()
                except json.decoder.JSONDecodeError:
                    self.logger.exception("Invalid JSON returned. Unable to decode the JSON Object")
                    return f"{uri} - Invalid JSON - 980"
                except requests.JSONDecodeError:
                    self.logger.exception("Invalid JSON returned. Unable to decode the JSON Object")
                    return f"{uri} - Invalid JSON - 980"

                self.logger.debug(resp_data_json)
                if not isinstance(post_data, (list, tuple)):
                    for each in post_data:
                        _prop_name = each.split("@")[0]
                        self.logger.debug("Property Name: %s", _prop_name)
                        if _prop_name not in resp_data_json:
                            prop_not_available.append(_prop_name)
                else:
                    for each_dict in post_data:
                        for each_list in each_dict:
                            _prop_name = each_list.split("@")[0]
                            self.logger.debug("Property Name: %s", _prop_name)
                            if _prop_name not in resp_data_json:
                                if _prop_name not in prop_not_available:
                                    prop_not_available.append(_prop_name)

                if len(prop_not_available) > 0:
                    msg = uri + " - " + \
                        ", ".join(prop_not_available) + " - Not Avail"
                else:
                    if is_valid_old_data:
                        _all_keys = self.get_keys(post_data)
                        for _key in _all_keys:
                            if _key.find("@TypeHint") < 0 and _key.find("@Patch") < 0:
                                if bool(old_data):
                                    valid_data = self.validate_old_data(
                                        resp_data_json, _key, self.get_prop_value(_key, old_data))
                                else:
                                    valid_data = False
                            if not(valid_data):
                                msg = "Provided Old Data is not matching - 999"
                                break
                    if valid_data:
                        # msg = self.update_or_create_node(uri, post_data,"Updated")
                        if isinstance(post_data, (list, tuple)):
                            for each_post_data in post_data:
                                msg = self.update_or_create_node(
                                    uri, each_post_data, "Updated")
                        else:
                            msg = self.update_or_create_node(
                                uri, post_data, "Updated")

            elif stat_code == 401:
                msg = "Wrong username and Password - Http status " + \
                    str(stat_code)
            else:
                msg = uri + " - Failed(Node not available) - " + \
                    str(stat_code)

            self.logger.info(msg)
            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def create_property_value(self, uri, post_data, is_valid_old_data, old_data):
        """ Create Property with value. Usage:  create_property_value(uri, prop, data) """
        try:
            passed_data = str(uri) + " - " + str(post_data)
            self.logger.info(passed_data)
            msg = ""
            full_uri = self.ip + uri + ".json"

            resp_data = requests.get(full_uri, auth=(
                self.user, self.passwd), timeout=self.timeout)
            sleep(0.5)
            stat_code = resp_data.status_code
            prop_available = []
            if stat_code == 200:
                # resp_data_json = resp_data.json()
                try:
                    resp_data_json = resp_data.json()
                except json.decoder.JSONDecodeError:
                    self.logger.exception("Invalid JSON returned. Unable to decode the JSON Object")
                    return f"{uri} - Invalid JSON - 980"
                except requests.JSONDecodeError:
                    self.logger.exception("Invalid JSON returned. Unable to decode the JSON Object")
                    return f"{uri} - Invalid JSON - 980"

                if not isinstance(post_data, (list, tuple)):
                    for each in post_data:
                        _prop_name = each.split("@")[0]
                        if _prop_name in resp_data_json:
                            prop_available.append(_prop_name)
                else:
                    for each_dict in post_data:
                        for each_list in each_dict:
                            _prop_name = each_list.split("@")[0]
                            if _prop_name not in resp_data_json:
                                prop_available.append(_prop_name)

                if len(prop_available) > 0:
                    msg = uri+" - "+", ".join(prop_available) + " - Available"
                else:
                    msg = self.update_or_create_node(uri, post_data, "Created")

            elif stat_code == 401:
                msg = "Wrong username and Password - Http status " + \
                    str(stat_code)
            else:
                msg = uri + " - Failed(Node not available) - " + \
                    str(stat_code)

            self.logger.debug(msg)
            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def update_or_create_property_value(self, uri, post_data, is_valid_old_data, old_data):
        """ Create Property with value. Usage:  create_property_value(uri, prop, data) """
        try:
            passed_data = str(uri) + " - " + str(post_data)
            self.logger.info(passed_data)
            msg = ""
            full_uri = self.ip + uri + ".json"
            valid_data = True

            resp_data = requests.get(full_uri, auth=(
                self.user, self.passwd), timeout=self.timeout)
            sleep(0.5)
            stat_code = resp_data.status_code
            if stat_code == 200:
                try:
                    resp_data_json = resp_data.json()
                except json.decoder.JSONDecodeError:
                    self.logger.exception("Invalid JSON returned. Unable to decode the JSON Object")
                    return f"{uri} - Invalid JSON - 980"
                except requests.JSONDecodeError:
                    self.logger.exception("Invalid JSON returned. Unable to decode the JSON Object")
                    return f"{uri} - Invalid JSON - 980"

                if is_valid_old_data:
                    _all_key = self.get_keys(post_data)
                    for _key in _all_key:
                        if _key in resp_data_json:
                            valid_data = self.validate_old_data(
                                resp_data_json, _key, self.get_prop_value(_key, old_data))
                            if not(valid_data):
                                msg = "Provided Old Data is not matching - 999"
                                break
                if valid_data:
                    if isinstance(post_data, (list, tuple)):
                        for each_post_data in post_data:
                            msg = self.update_or_create_node(
                                uri, each_post_data, "Updated or Created")
                    else:
                        msg = self.update_or_create_node(
                            uri, post_data, "Updated or Created")

            elif stat_code == 401:
                msg = "Wrong username and Password - Http status " + \
                    str(stat_code)
            else:
                msg = uri + " - Failed(Node not available) - " + \
                    str(stat_code)

            self.logger.debug(msg)
            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def get_prop_value(self, _key, _data):
        try:
            msg = ""

            if _key in _data:
                msg = _data[_key]

            self.logger.info("Retrieved Value is: " + str(msg))
            return msg

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return ""
