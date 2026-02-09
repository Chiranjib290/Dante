import os
import re
from cryptography.fernet import Fernet as CRISP
import logging
import xlrd
from datetime import datetime
import webbrowser
from random import randint

logger = logging.getLogger(__name__)
# Encryption Key
ENCRYPTION_KEY = b'OajUImTpdXWDXrBS_WYffcVzZtxJxds1lrc0cF2YscE='


class GenericFunctions:
    """This is All validation in place """

    @staticmethod
    def removetrailingspecialchar(val):
        try:
            val = str(val)
            if val.strip() != "":
                while not (val[-1].isalnum()):
                    val = val[0: len(val) - 1]
                    if val == "":
                        break

            return val
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    @staticmethod
    def removepayloadtrailingspecialchar(val):
        try:
            val = str(val)
            if val.strip() != "":
                pat = "[A-Za-z0-9\$]$"
                find = re.search(pat, val)
                while find is None:
                    val = val[0: len(val) - 1]
                    find = re.search(pat, val)
                    if val == "":
                        break

            return val
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    @staticmethod
    def removeleadingspecialchar(val):
        try:
            val = str(val)
            if val.strip() != "":
                while not (val[0].isalnum()):
                    val = val[1: len(val)]
                    if val == "":
                        break

            return val
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    @staticmethod
    def validateIP(ip, env):
        try:
            output = False
            cleanedip = ip[0: ip.rfind(":")] if ip.count(":") > 1 else ip
            # print(cleanedip)
            logger.debug("IP: "+str(cleanedip))
            # logger.debug("Env: ", env)
            # reenv = r"^(http|https)\:\/\/(\w+\-\w+|\w+)\.\w+\.\w+"
            reenv = r"^(http|https)\:\/\/\w+(\-\w+){0,5}\.pwc.com$"
            reip = r"^http\:\/\/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            recloud = r"^(http|https)\:\/\/\w+(\-\w+){0,5}\.adobeaemcloud\.com$"
            if env.lower().startswith("ip"):
                out = re.match(reip, cleanedip)
                logger.debug("IP Match Data: "+str(out))
                if out:
                    output = True
            else:
                out = re.match(reenv, cleanedip)
                logger.debug("IP Match Data: "+str(out))
                if out:
                    output = True
                else:
                    out = re.match(recloud, cleanedip)
                    logger.debug("IP Cloud Match Data: "+str(out))
                    if out:
                        output = True
            logger.info("IP Matched: "+str(output))
            return output
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return None

    @staticmethod
    def isUrlProcessed(pros_status):
        try:
            logger.debug("Received Status: "+str(pros_status))
            dataprocessed = False
            # url_split = pros_status.split(":")
            # logger.debug("Received Status after splitting: "+str(url_split))
            pros_status = pros_status.lower()

            if pros_status.find("processed") > -1 or pros_status.find("failed") > -1:  # Processed
                dataprocessed = True

            logger.debug("Is Data Processed: "+str(dataprocessed))
            return dataprocessed
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    @staticmethod
    def encrypt_passwd(passwd):
        try:
            crispy = CRISP(ENCRYPTION_KEY)
            if not(isinstance(passwd, bytes)):
                encoded_passwd = passwd.encode()
            else:
                encoded_passwd = passwd
            encrypted_passwd = crispy.encrypt(encoded_passwd)

            return encrypted_passwd.decode()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    @staticmethod
    def decrypt_passwd(encrypted_passwd):
        try:
            crispy = CRISP(ENCRYPTION_KEY)
            if not(isinstance(encrypted_passwd, bytes)):
                encoded_passwd = encrypted_passwd.encode()
            else:
                encoded_passwd = encrypted_passwd
            # encoded_passwd = encrypted_passwd.encode()
            decrypted_passwd = crispy.decrypt(encoded_passwd)

            return decrypted_passwd.decode()
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return ""

    @staticmethod
    def is_belong_to_list(token, data_list):
        try:
            out = ""
            for each in data_list:
                if each.startswith(token):
                    out = each
                    break
            return out

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return ""

    @staticmethod
    def is_valid_file_types(file, types):
        try:
            out = False

            filename, fileext = os.path.splitext(file)
            if fileext in types:
                out = True

            return out

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return ""

    @staticmethod
    def wrap_text_with_dot(value, max_len):
        try:
            out = value
            value_len = len(value)
            if value_len > max_len:
                startpos = (value_len-max_len) + 3
                value = "..." + str(value[startpos:])
                out = value
            return out

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return value

    @staticmethod
    def is_signed_numeric(val):
        try:
            val = str(val)
            logger.debug("Value to be checked: "+val)
            output = False
            if val.strip() != "":
                if val[0] == "-" or val[0] == "+":
                    re_val = val[1:]
                    logger.debug("Value has sign, without sign val: "+re_val)
                    if re_val.isnumeric():
                        output = True
                else:
                    output = val.isnumeric()
                    logger.debug("Value has no sign, Output: "+str(output))

            return output
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    @staticmethod
    def read_country_name(file):
        try:
            logger.debug("File to be Opened: "+str(file))
            # output_data = []
            output_data = {}
            wb = xlrd.open_workbook(file)
            sheet = wb.sheet_by_index(0)
            numrows = sheet.nrows
            logger.debug("Total Territories: "+str(numrows))
            for i in range(1, numrows):
                # output_data.append(str(sheet.cell_value(i, 0)).upper())
                output_data[str(sheet.cell_value(i, 0)).lower()
                            ] = str(sheet.cell_value(i, 1))
            return output_data
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            # return []
            return {}

    @staticmethod
    def on_mouse_wheel(component, event):
        component.yview_scroll(-1*(event.delta//120), "units")

    @staticmethod
    def generate_five_years_past():
        try:
            year_list = []
            current_year = datetime.now().year

            for i in range(5):
                year_list.append(current_year - i)

            return year_list
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return []

    @staticmethod
    def match_pattern(pat, val):
        try:
            out = False
            logger.info("Pattern: "+str(pat) + ", Value: "+str(val))
            matched = re.match(pat, val)
            logger.debug("Matched: "+str(matched))
            if matched:
                out = True

            logger.info("Value Mathced: "+str(out))
            return out
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    @staticmethod
    def find_with_regex(pat, val):
        try:
            outval = re.findall(pat, val)
            logger.debug("Matched value: %s" % outval)
            return outval
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return []

    @staticmethod
    def validate_query(query_list, query_type, forbidden_path):
        try:
            is_valid = (False, ["Query Not validated"])

            def validator(query, pattern):
                _is_valid = False
                _error_list = []
                _content_root_error = "Content Root selected."
                logger.debug("Pattern Line: %s" % (pattern))
                logger.debug("Forbidden Path: %s" % forbidden_path)
                for _query in query:
                    logger.debug("Checking Query line: "+str(_query))
                    _is_valid = False
                    if re.match(pattern, _query):
                        _query = GenericFunctions.removetrailingspecialchar(
                            _query)
                        # _query.startswith("path"):
                        if re.match("^.*path(=|:)(\/\w+)+$", _query):
                            # GenericFunctions.removetrailingspecialchar(_query.replace("path:","").replace("=","").strip())
                            content_path_list = re.split("(:|=)", _query)
                            content_path = content_path_list[-1]
                            logger.debug("Content path selected: %s" %
                                         content_path)
                            if content_path not in forbidden_path:
                                _is_valid = True
                                if content_path == "/content/pwc":
                                    _error_list.append(_content_root_error)
                            else:
                                logger.error(
                                    "Path filter is forbidden. Please change path")
                                _is_valid = False
                                _error_list.append("Path filter is forbidden.")
                        else:
                            _is_valid = True
                    else:
                        _is_valid = False
                        _error_list.append("Invalid Query format.")
                    logger.debug("Valid? : %s" % (_is_valid))
                    if not(_is_valid):
                        break
                if not(_is_valid):
                    if _error_list.count(_content_root_error) > 0:
                        _error_list.remove(_content_root_error)
                return (_is_valid, _error_list, )

            if query_type.lower() == "query builder":
                pat = "\w+(\.{0,1}\w+)*\=(-){0,1}(\{\w+\}|\/{0,1}\w+|\w+$|\w+\:\w+)+"
                is_valid = validator(query_list, pat)
            elif query_type.lower() == "bulk editor":
                pat = "\'*\"*\w+\:*\w+\'*\"*\:(\/\w+|\'*\"*\w+\:*\w+\'*\"*|\{\w+\})"
                is_valid = validator(query_list, pat)
            logger.debug("Query is Valid: " + str(is_valid))
            return is_valid
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    @staticmethod
    def get_int_value(_value, default_val):
        try:
            return int(_value)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return default_val

    @staticmethod
    def download_google_sheet(_url):
        try:
            download_url = _url
            webbrowser.register(
                "chrome",
                None,
                webbrowser.BackgroundBrowser(
                    "C://Program Files//Google//Chrome//Application//chrome.exe"
                ),
            )
            chrome = webbrowser.get("chrome")
            chrome.open(download_url)
        except:
            logger.error("Below Exception occurred\n", exc_info=True)

    @staticmethod
    def check_date(_value, _format):
        try:
            out_val = datetime.strptime(_value, _format)
            return True
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    @staticmethod
    def validate_input_url(_url):
        try:
            _output = False
            logger.debug("Input URL: %s" % _url)
            pat = r'^(https://|http://){0,1}(www|[a-zA-Z0-9_\-]+)*(\.\w+)+(\/[a-zA-Z0-9_\-\+\?\%~]*)*(.){0,1}'
            if re.match(pat, _url):
                _output = True
            logger.debug("%s is a Valid URL? %s" % (_url, _output))
            return _output

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    @staticmethod
    def check_pwc_microsites(_url):
        try:
            _output = False
            logger.debug("Input URL: %s" % _url)
            pat = r'^\/content\/pwc\/\w{2}\/\w{2}\/website\/[a-zA-Z0-9_\-]+'
            if re.match(pat, _url):
                _output = True
            logger.debug("%s is a Microsite? %s" % (_url, _output))
            return _output
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    @staticmethod
    def get_pwc_microsite_contentpath(_url):
        try:
            # _output = False
            logger.debug("Input URL: %s" % _url)
            pat = r'^\/content\/pwc\/\w{2}\/\w{2}\/website\/([a-zA-Z0-9_\-]+)'
            _matched = re.search(pat, _url)
            _matched_group = _matched.group()
            logger.debug("%s Microsite? %s" % (_url, _matched_group))
            return _matched_group
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return None

    @staticmethod
    def reformat_form_payload(_payload):
        try:
            # /content/usergenerated/content/pwc/id/en/careers/graduates/internship/2021/4/28/OnlineForm4505/1619637803228_934
            # /content/usergenerated/content/pwc/global/forms/contactUsForm/2021/4/28/ContactUsForm8940/1619637690634_248/1619637690634.json
            updated_payload = _payload.replace(".html", "").strip()
            logger.debug("Input URL: %s and Updated URL: %s" %
                         (_payload, updated_payload))
            _last_node = updated_payload.strip().split("/")[-1]
            last_node_pat = r'\d+\_\d+'
            _matched = re.match(last_node_pat, _last_node)
            logger.debug("Matched? " + str(_matched))
            if _matched:
                final_node = _last_node.split("_")[0]
                updated_payload = updated_payload + "/" + str(final_node)
            logger.debug("Updated Payload: %s" % (updated_payload))
            return updated_payload
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return None

    @staticmethod
    def random_number_gen(_end):
        try:
            random_number = randint(1, _end)
            logger.debug("Random number: "+str(random_number))
            return random_number
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return "1111111111"

    @staticmethod
    def get_key_of_val(data, value):
        try:
            _key = None
            logger.debug("Data: "+str(data) + ", Value: "+str(value))
            for key in data:
                if str(data[key]).strip().lower() == str(value).strip().lower():
                    _key = key
                    break

            return _key
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return None

    @staticmethod
    def validate_source_with_target(source, target, valid_paths):
        try:
            return_code = "Invalid"
            for _each_path in valid_paths:
                if source.startswith(_each_path) and target.startswith(_each_path) and _each_path.find("usergenerated") == -1:
                    if source == target:
                        return_code = "Same Source and Target"
                        logger.debug(
                            "Source and Target is same. Return Code: "+str(return_code))
                    else:
                        return_code = "Valid"
                        logger.debug(
                            "Source and Target is valid. Return Code: "+str(return_code))
                        break
                elif _each_path.find("usergenerated") > -1:
                    if source.startswith("/content/usergenerated") and target.startswith("/content/usergenerated"):
                        return_code = "Valid"
                        logger.debug(
                            "Source and Target is form and valid. Return Code: "+str(return_code))
                        break
                else:
                    logger.debug(
                        "Source and Target is invalid. Return Code: "+str(return_code))

            return return_code
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return 999

    @staticmethod
    def join_list(sep, input_):
        try:
            logger.debug("Input List: "+str(input_))
            out = ""
            if isinstance(input_, list):
                for count, pr_ in enumerate(input_):
                    if count == len(input_) - 1:
                        out += str(pr_)
                    else:
                        out += str(pr_) + sep

                return out
            else:
                return input_

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return input_

    @staticmethod
    def filter_utf8_chars(input_):
        try:
            if isinstance(input_, str):
                logger.debug("Input Value: "+str(input_))
                out = ""
                charlist = [input_[j] for j in range(
                    len(input_)) if ord(input_[j]) in range(65536)]
                for char in charlist:
                    out = out+char
            else:
                out = input_

            return out

        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return input_

    @staticmethod
    def read_yaml_file(file):
        import yaml
        try:
            with open(file, "r+") as filestream:
                data = yaml.load(filestream, Loader=yaml.FullLoader)
            return data
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return {}
    
    @staticmethod
    def is_valid_dpepath(url, env, path):
        try:
            """
            Check if paths is a valid DPE Path
            """
            logger.info("URL is: %s and Env is: %s", url,env)
            is_valid_url = url.startswith(path)
            if env.lower().startswith("ip"):
                if bool(url.strip()):
                    return is_valid_url
                else:
                    return True
            else:
                return is_valid_url
        except:
            logger.error("Below Exception occurred\n", exc_info=True)
            return False

    # @staticmethod
    # def is_valid_etcmappath(url, env):
    #     import yaml
    #     try:
    #         """
    #         Check if redirectpath startswith /etc/map/http
    #         """
    #         logger.info("URL is: %s and Env is: %s", url,env)
    #         is_valid_url = url.startswith("/etc/map/http")
    #         if env.lower().startswith("ip"):
    #             if bool(url.strip()):
    #                 return is_valid_url
    #             else:
    #                 return True
    #         else:
    #             return is_valid_url
    #     except:
    #         logger.error("Below Exception occurred\n", exc_info=True)
    #         return False
    #     except:
    #         logger.error("Below Exception occurred\n", exc_info=True)
    #         return False
