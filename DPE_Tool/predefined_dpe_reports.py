import json
import logging
import requests
from time import sleep, time
from urllib.parse import quote

class PreDefinedReports:
    def __init__(self,ip,uname, passwd):
        """ Initializing the Class, Usage :  PreDefinedReports(ip,username, password)"""

        self.logger = logging.getLogger(__name__)
        self.ip = ip.strip()
        self.user = uname.strip()
        self.passwd = passwd.strip()
        self.configdata = self.opencode("configfiles\\config.json")
        self.loglevel = self.configdata.get("loglevel","info")
        self.sleeptime = float(self.configdata.get("sleeptime","1.0"))
        self.timeout = float(self.configdata.get("timeout", "20"))
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

    def set_uname_pass(self,uname,passwd):
        try:
            self.user = uname
            self.passwd = passwd
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def join_list(self, sep, input_):
        try:
            self.logger.debug("Input List: "+str(input_))
            out = ""
            if isinstance(input_, list):
                for count, pr_ in enumerate(input_):
                    if count == len(input_) - 1:
                        out += str(pr_)
                    else:
                        out += str(pr_) + sep
                self.logger.debug("Final: "+out)
                return out
            else:
                return input_

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return input_

    def opencode(self, file):
        """ Open JSON Settings File """

        with open(file) as fin:
            data = json.loads(fin.read())
        return data

    def get_dict_data(self, _key, _data):
        try:
            val = None
            if _key in _data:
                val = _data[_key]
            return val
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def reform_data_in_list(self, _data, props):
        try:
            _data_list = _data["hits"]

            out_data = []
            for each in _data_list:
                chunks = []
                for _key in each:
                    if _key == "jcr:content":
                        for props in each[_key]:
                            chunks.append(each[_key][props])
                    else:
                        chunks.append(each[_key])
                out_data.append(chunks)
            return out_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def report_selector(self, **kwargs):
        try:
            report_name = self.get_dict_data("report_name", kwargs)
            territory = self.get_dict_data("territory", kwargs)
            props = self.get_dict_data("props", kwargs)
            year_data = self.get_dict_data("year", kwargs)
            month_data = self.get_dict_data("month", kwargs)
            day_data = self.get_dict_data("day", kwargs)
            s_dam_type = self.get_dict_data("type_of_dam", kwargs)

            report_data = None

            if report_name.lower() == "page report":
                # report_data = self.territory_page_report(territory, props)
                report_data = self.territory_report_generator(territory,"", report_name, props)
                self.logger.debug("Retrieved Data " +str(report_data))
            elif report_name.lower() == "published page report": #Published Page Report
                report_data = self.territory_report_generator(territory,s_dam_type, report_name, props)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "processed contactus form report":
                report_data = self.global_arch_contact_form_territory("Global arch Contactus", territory, year_data, month_data, day_data, props)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "in-progress contactus form report":
                report_data = self.global_arch_contact_form_territory("Global Contactus", territory, year_data, month_data, day_data, props)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "processed online form report":
                report_data = self.global_arch_contact_form_territory("Online Arch", territory, year_data, month_data, day_data, props)
                self.logger.debug("Retrieved Data " +str(report_data))
            
            elif report_name.lower() == "in-progress online form report":
                report_data = self.global_arch_contact_form_territory("Online", territory, year_data, month_data, day_data, props)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "dam assets report": #Published Page Report
                report_data = self.territory_report_generator(territory,s_dam_type, report_name, props)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "published dam assets report": #Published Page Report
                report_data = self.territory_report_generator(territory,s_dam_type, report_name, props)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "contact page report":
                report_data = self.contact_page_report(territory, props, published=False, content_fragment=False)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "contact page report - published":
                report_data = self.contact_page_report(territory, props, published=True, content_fragment=False)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "contact fragment report":
                report_data = self.contact_page_report(territory, props, published=False, content_fragment=True)
                self.logger.debug("Retrieved Data " +str(report_data))
            
            elif report_name.lower() == "contact fragment report - published":
                report_data = self.contact_page_report(territory, props, published=True, content_fragment=True)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "contact fragment reference":
                report_data = self.contact_fragment_page_reference_report(territory)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "tag report":
                report_data = self.tag_report(territory, props, published=False)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "tag report - published":
                report_data = self.tag_report(territory, props, published=True)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "component usage report": #Published Page Report
                report_data = self.retrieve_pages_with_resourcetype(territory, s_dam_type, props)
                self.logger.debug("Retrieved Data " +str(report_data))
                
            elif report_name.lower().startswith("user-def") :
                query = self.get_dict_data("query", kwargs)
                query_type = self.get_dict_data("query_type", kwargs)
                report_data = self.user_defined_report(query, props, query_type)
                self.logger.debug("Retrieved Data " +str(report_data))
            #fetch_redirection_details
            elif report_name.lower() == "redirection details":
                _environment = self.get_dict_data("environment", kwargs)
                report_data = self.fetch_redirection_details(territory, _environment, props)
                self.logger.debug("Retrieved Data " +str(report_data))

            elif report_name.lower() == "ghost page report":
                report_data = self.territory_report_generator(territory,s_dam_type, report_name, props)
                self.logger.debug("Retrieved Data " +str(report_data))

            return report_data
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)

    def territory_page_report(self, territory, cols):
        try:
            def prepare_and_rtrv_data(b_link, p_path, f_data, props):
                _limit_data = " limit:" + str(self.wfoperationdata.get("limit result",100)) if self.wfoperationdata.get("limit result",100) != -1 else ""
                _query_data = "path:"+ p_path +" "+f_data+_limit_data
                _query_data_enc = quote(_query_data, safe='')
                _col_data_enc = quote(props, safe='')
                time_in_ms = int(time()*1000)
                self.logger.debug("Fullpath-> "+str(p_path)+", Filter Data -> "+str(f_data)+", Columns-> "+str(props)
                        +", Query Data-> "+str(_query_data))
                self.logger.debug("Encoded Query-> "+str(_query_data_enc)+", Encoded ColumnData -> "+str(_col_data_enc))

                _final_query = self.ip + b_link + "?query=" + _query_data_enc + "&tidy=true&cols="+_col_data_enc+"&_dc="+str(time_in_ms)
                self.logger.debug("Final Query: "+str(_final_query))

                _resp_data = requests.get(_final_query, auth=(self.user, self.passwd), timeout = self.timeout)
                out_msg = None

                if _resp_data.status_code == 200:
                    out_msg = _resp_data.json()
                elif _resp_data.status_code == 401:
                    out_msg = "Wrong Username and Password - Http Code - "+str(_resp_data.status_code)
                    self.logger.error(out_msg)
                else:
                    out_msg = "Error Occurred - Http Code - "+str(_resp_data.status_code)
                    self.logger.error(out_msg)

                return out_msg
            
            def format_data(_data, _cleaned_cols):
                msg = []
                results = [_data.get("results",0),_data.get("total",0)]
                msg.append(results)
                    
                for each in _data["hits"]:
                    chunks = []
                    chunks.append(each.get("jcr:path", "Invalid Property"))
                    for prop in _cleaned_cols:
                        chunks.append(each.get(prop, "Invalid Property"))
                    msg.append(chunks)
                return msg

            content_root = self.wfoperationdata.get("content root", "/content/pwc")
            bulk_editor = self.wfoperationdata.get("bulk editor link", "/etc/importers/bulkeditor/query.json")
            query_builder_link = self.wfoperationdata.get("query builder link", "/bin/querybuilder.json")
            full_path = content_root + "/" + territory
            filter_data = "type:Page"

            cleaned_cols = ["jcr:content/"+(x.strip().replace("jcr:content/","")) for x in cols if x.strip() != ""]
            col_data = ",".join(cleaned_cols)
            self.logger.debug("Column Data passed: "+str(cols)+ ", Column data after converting: "+str(col_data))         

            msg = None
            outval = {}
            if len(territory) == 2:
                query_for_locale = "p.limit=-1&path="+quote(full_path, safe='')+"&path.flat=true&type=cq%3aPage"
                q_locale_query = self.ip + query_builder_link + "?" + query_for_locale
                self.logger.debug("Locale Query: %s" % q_locale_query)
                locale_res = requests.get(q_locale_query, auth = (self.user, self.passwd), timeout = self.timeout)
                if locale_res.status_code == 200:
                    for each_path in locale_res.json()["hits"]:
                        locale = each_path["path"].split("/")[-1]
                        if len(locale) == 2:
                            if not(bool(outval)):
                                outval = prepare_and_rtrv_data(bulk_editor, each_path["path"], filter_data, col_data)
                                if isinstance(outval, str):
                                    msg = outval
                                    self.logger.error(msg)
                                    break
                            elif bool(outval):
                                temp_data = prepare_and_rtrv_data(bulk_editor, each_path["path"], filter_data, col_data)
                                if not(isinstance(temp_data, str)) and isinstance(outval, dict):
                                    outval["results"] = outval["results"] + temp_data["results"]
                                    outval["hits"].extend(temp_data["hits"])
                                else:
                                    msg = temp_data
                                    self.logger.error(msg)
                                    break
                        else:
                            self.logger.error("Locale is more than 2 chars: %s" % locale)
                            continue

                    if outval is not None:
                        msg = format_data(outval, cleaned_cols)

                elif locale_res.status_code == 401:
                    msg = "Wrong Username and Password - Http Code - "+str(locale_res.status_code)

                else:
                    msg = "Error Occurred - Http Code - "+str(locale_res.status_code)
            else:
                outval = prepare_and_rtrv_data(bulk_editor, full_path,filter_data, col_data)
                if isinstance(outval, str):
                    msg = outval
                    self.logger.error(msg)
                else:
                    if outval is not None:
                        msg = format_data(outval, cleaned_cols)
                    else:
                        msg = "Block Exception - Code - 999"
                        self.logger.error(msg)

            return msg

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    def territory_report_generator(self, territory, dam_type, report_name, cols):
        try:
            # print(dam_type)
            def prepare_and_retrv_data(qb_link, p_path, props, r_name, d_type):
                filter_data = None
                if r_name.lower() == "page report":
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(p_path,safe='')) +\
                                    "&type=cq%3aPage&p.hits=selective"
                elif r_name.lower() == "published page report":
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(p_path,safe='')) +\
                                    "&1_property=jcr:content/activatedInPublish&1_property.value=true&2_property=jcr:content/cq:lastReplicationAction&2_property.value=Activate&type=cq%3aPage&p.hits=selective"
                elif r_name.lower() == "dam assets report":
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(p_path,safe='')) +\
                                    "&property="+str(quote("jcr:content/metadata/dc:format",safe=''))+"&property.operation=like&property.value="+str(quote("%"+str(d_type)+"%",safe=''))+"&type="+quote("dam:Asset",safe='')+"&p.hits=selective"
                elif r_name.lower() == "published dam assets report":
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(p_path,safe='')) +\
                                    "&1_property="+str(quote("jcr:content/cq:lastReplicationAction",safe=''))+"&1_property.value=Activate" +\
                                    "&2_property="+str(quote("jcr:content/metadata/dc:format",safe=''))+"&2_property.operation=like&2_property.value="+str(quote("%"+str(d_type)+"%",safe=''))+"&type="+quote("dam:Asset",safe='')+"&p.hits=selective"
                elif r_name.lower() == "ghost page report":
                    # filter_data = "p.limit=" + str(self.wfoperationdata.get('limit result', -1)) + "&path=" +str(quote(p_path,safe='')) +\
                    #                 "&property=" + str(quote('jcr:content/sling:resourceType')) + "&property.value=" + str(quote('pwc/components/page/ghost')) + "&type=cq:Page&p.hits=selective"
                    filter_data = "p.limit=" + str(self.wfoperationdata.get('limit result', -1)) + "&path=" +str(quote(p_path,safe='')) +\
                                    "&property=" + str(quote('jcr:content/cq:template')) + "&property.value=" + str(quote('/conf/pwc/settings/wcm/templates/ghost-template')) + "&type=cq:Page&p.hits=selective"
                _out_val = None
                if filter_data is not None: 
                    query_data = filter_data + "&p.properties="+ props
                    self.logger.debug("Fullpath-> "+str(p_path)+", Filter Data -> "+str(filter_data)+", Columns-> "+str(props)
                                +", Query Data-> "+str(query_data))
                    _final_query = self.ip + qb_link + "?" + query_data
                    self.logger.debug("Final Query: "+str(_final_query))
                    _resp_data = requests.get(_final_query, auth=(self.user, self.passwd), timeout = self.timeout)
                    # _resp_data.status_code = 401
                    if _resp_data.status_code == 200:
                        _out_val = _resp_data.json()
                    elif _resp_data.status_code == 401:
                        _out_val = "Wrong Username and Password - Http Code - "+str(_resp_data.status_code)
                        self.logger.error(msg)
                    else:
                        _out_val = "Error Occurred - Http Code - "+str(_resp_data.status_code)
                        self.logger.error(msg)

                return _out_val
            
            def format_out_data(t_data, _cleaned_cols):
                out_data = []
                results = [t_data.get("results",0),t_data.get("total",0)]
                out_data.append(results)
                for each in t_data["hits"]:
                    chunks = []
                    chunks.append(each.get("jcr:path", "Invalid Property"))
                    for prop in _cleaned_cols:
                        if prop != "jcr:path":
                            # chunks.append(each["jcr:content"].get(prop.replace("jcr:content/",""), "Invalid Property"))
                            splt_cols = [_x for _x in prop.split("/")]
                            _each_d = each.copy()
                            for _y in splt_cols:
                                if isinstance(_each_d.get(_y,""), dict):
                                    _each_d = _each_d[_y].copy()
                                else:
                                    chunks.append(_each_d.get(_y, "Invalid Property"))
                    out_data.append(chunks)
                return out_data

            content_root = self.wfoperationdata.get("content root","/content/pwc")
            content_dam_root = self.wfoperationdata.get("content dam root", "/content/dam/pwc")
            query_builder = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
            is_page_report = True if (report_name.lower() == "published page report" or report_name.lower() == "page report"or report_name.lower() == "ghost page report") else False
            full_path = content_root + "/" + territory if is_page_report else content_dam_root + "/" + territory
            enc_path = quote(full_path, safe='')
            type_of_node = "cq%3aPage" if is_page_report else "sling%3aFolder"

            # Preparation of Column
            cleaned_cols = ["jcr:content/"+(x.strip().replace("jcr:content/","")) for x in cols if x.strip() != ""]
            cleaned_cols.insert(0,"jcr:path")
            col_data = "+".join(cleaned_cols)

            msg = None
            outval = None

            if len(territory) == 2:
                query_for_locale = "p.limit=-1&path="+enc_path+"&path.flat=true&type="+str(type_of_node)
                q_locale_query = self.ip + query_builder + "?" + query_for_locale
                self.logger.debug("Locale Query: %s" % q_locale_query)
                
                # print(final_query)
                locale_res = requests.get(q_locale_query, auth = (self.user, self.passwd), timeout = self.timeout)

                if locale_res.status_code == 200:
                    for each_path in locale_res.json()["hits"]:
                        locale = each_path["path"].split("/")[-1]
                        if len(locale) == 2:
                            if outval is None:
                                outval = prepare_and_retrv_data(query_builder, each_path["path"], col_data, report_name, dam_type)
                                if isinstance(outval, str):
                                    msg = outval
                                    self.logger.error(msg)
                                    break
                            elif outval is not None:
                                temp_data = prepare_and_retrv_data(query_builder, each_path["path"], col_data, report_name, dam_type)
                                if isinstance(temp_data, str):
                                    msg = temp_data
                                    self.logger.error(msg)
                                    break
                                else:
                                    outval["results"] = outval["results"] + temp_data["results"]
                                    outval["total"] = outval["total"] + temp_data["total"]
                                    outval["hits"].extend(temp_data["hits"])

                        else:
                            self.logger.error("Locale is more than 2 chars: %s" % locale)
                            continue

                    if outval is not None:
                        msg = format_out_data(outval, cleaned_cols)
                    
                elif locale_res.status_code == 401:
                    msg = "Wrong Username and Password - Http Code - "+str(locale_res.status_code)

                else:
                    msg = "Error Occurred - Http Code - "+str(locale_res.status_code)
            else:
                outval = prepare_and_retrv_data(query_builder, full_path, col_data, report_name, dam_type)
                if isinstance(outval, str):
                    msg = outval
                    self.logger.error(msg)
                else:
                    if outval is not None:
                        msg = format_out_data(outval, cleaned_cols)
                    else:
                        msg = "Block Exception - Code - 999"
                        self.logger.error(msg)

            return msg

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    def form_date_filter(self, form_type, year, month, day):
        try:
            _year_month_filter = None
            self.logger.debug("Selected Form Type: "+ str(form_type))
            all_month = ['--MONTH--','january','february','march','april','may','june','july','august','september','october','november','december']
            all_month_abreviated = ["--Month--","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            month_in_number = all_month.index(month.lower()) if all_month.count(month.lower()) > 0 else 0
            self.logger.debug("Month in Number: "+ str(month_in_number))

            if bool(year):
                if form_type.lower() == "global arch contactus" or form_type.lower() == "global contactus":
                    _year_month_filter = str(year) if month_in_number == 0 else str(year) + "/" + str(month_in_number)
                    if month_in_number != 0 and str(day).lower() != "--day--":
                        _year_month_filter = _year_month_filter + "/" + str(day)

                elif form_type.lower() == "online arch" or form_type.lower() == "online":
                    selelcted_abr_month = all_month_abreviated[month_in_number]
                    if selelcted_abr_month != "--Month--":
                        _year_month_filter = selelcted_abr_month + ", " + str(year)
                        if month_in_number != 0 and str(day).lower() != "--day--":
                            _year_month_filter = str(day)+" " + _year_month_filter
                        _year_month_filter = "%" + _year_month_filter + "%"

                    elif selelcted_abr_month == "--Month--":
                        _year_month_filter = "%"+str(year)+"%"

            self.logger.debug("Year Month Filter: "+ str(_year_month_filter))
            return _year_month_filter

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def global_arch_contact_form_territory(self, form_type, territory, year, month, day, cols):
        try:
            year_month_filter = self.form_date_filter(form_type, year, month, day)
            msg = None
            
            if year_month_filter is not None:
                query_builder_link = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
                if form_type.lower() == "global arch contactus":
                    global_form_path = str(self.wfoperationdata.get("form archive content path","/content/usergenerated/archive/content/pwc"))+"/global/forms/contactUsForm"
                    full_path = global_form_path + "/" + year_month_filter
                    # filter_data = "territory:" + str(territory)
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(full_path,safe='')) +\
                                    "&1_property=formType&1_property.value=contactUs&2_property=territory&2_property.value="+ str(territory) +"&p.hits=selective"

                elif form_type.lower() == "global contactus":
                    global_form_path = str(self.wfoperationdata.get("form content path","/content/usergenerated/content/pwc"))+"/global/forms/contactUsForm"
                    full_path = global_form_path + "/" + year_month_filter
                    # filter_data = "territory:" + str(territory)
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(full_path,safe='')) +\
                                    "&1_property=formType&1_property.value=contactUs&2_property=territory&2_property.value="+ str(territory) +"&p.hits=selective"
                elif form_type.lower() == "online arch":
                    full_path = str(self.wfoperationdata.get("form archive content path","/content/usergenerated/archive/content/pwc")) + "/" +str(territory)
                    # full_path = global_form_path + "/" + year_month_filter
                    # filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(full_path,safe='')) +\
                    #                 "&1_property=formType&1_property.value=online&2_property=pwcSubmissionDatetime&2_property.value="+str(quote(year_month_filter,safe=''))+"&2_property.operation=like&p.hits=selective"
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(full_path,safe='')) +\
                                    "&group.1_property=formType&group.1_property.value=online&group.2_property=formType&group.2_property.value=simple&group.p.or=true&3_property=pwcSubmissionDatetime&3_property.value="+str(quote(year_month_filter,safe=''))+"&3_property.operation=like&p.hits=selective"
                    
                else:
                    full_path = str(self.wfoperationdata.get("form content path","/content/usergenerated/content/pwc"))+ "/" + str(territory)
                    # full_path = global_form_path + "/" + year_month_filter
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(full_path,safe='')) +\
                                    "&group.1_property=formType&group.1_property.value=online&group.2_property=formType&group.2_property.value=simple&group.p.or=true&3_property=pwcSubmissionDatetime&3_property.value="+str(quote(year_month_filter,safe=''))+"&3_property.operation=like&p.hits=selective"

                cleaned_cols = [(x.strip().replace("jcr:content/","")) for x in cols if x.strip() != ""]
                cleaned_cols.insert(0,"jcr:path")
                col_data = "+".join(cleaned_cols)
                query_data = filter_data + "&p.properties="+ col_data
                self.logger.debug("Fullpath-> "+str(full_path)+", Filter Data -> "+str(filter_data)+", Columns-> "+str(col_data)
                                    +", Query Data-> "+str(query_data))
                final_query = self.ip + query_builder_link + "?" + query_data
                self.logger.debug("Final Query: "+str(final_query))
                
                outval = None

                resp_data = requests.get(final_query, auth=(self.user, self.passwd), timeout = self.timeout)
                if resp_data.status_code == 200:
                    outval = resp_data.json()
                    msg = []
                    results = [outval.get("results",0),outval.get("total",0)]
                    msg.append(results)

                    for each_data in outval["hits"]:
                        chunks = []
                        for _prop in cleaned_cols:
                            chunks.append(each_data.get(_prop, "Invalid Property"))
                        msg.append(chunks)

                elif resp_data.status_code == 401:
                    msg = "Wrong Username and Password - Http Code - "+str(resp_data.status_code)
                    self.logger.error(msg)
                else:
                    msg = "Error Occurred - Http Code - "+str(resp_data.status_code)
                    self.logger.error(msg)
            else:
                msg = "Invalid Year, Month, Date Selected - Code - 999"

            # print(msg)
            return msg

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    def contact_page_report(self, territory, cols, published = False, content_fragment = False):
        try:
            content_root = self.wfoperationdata.get("content root","/content/pwc")
            content_dam_root = self.wfoperationdata.get("content dam root", "/content/dam/pwc")
            query_builder = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
            full_path = content_dam_root + "/" + territory if content_fragment else content_root + "/" + territory
            enc_path = quote(f"{content_root}/{territory}", safe='')
            
            prefix = "jcr:content/data/master/" if content_fragment else "jcr:content/"
            cleaned_cols = [prefix+(x.strip().replace("jcr:content/","")) for x in cols if x.strip() != ""]
            # cleaned_cols = ["jcr:content/contact-profile-par/contact/"+(x.strip().replace("jcr:content/","")) for x in cols if x.strip() != ""]
            cleaned_cols.insert(0,"jcr:path")
            col_data = "+".join(cleaned_cols)

            paths = []
            msg = None
            outval = None

            if len(territory) == 2:
                query_for_locale = "p.limit=-1&path="+enc_path+"&path.flat=true&type=cq%3aPage"
                q_locale_query = self.ip + query_builder + "?" + query_for_locale
                self.logger.debug("Locale Query: %s", q_locale_query)
                locale_res = requests.get(q_locale_query, auth = (self.user, self.passwd), timeout = self.timeout)
                if locale_res.status_code == 200:
                    for each_path in locale_res.json()["hits"]:
                        locale = each_path["path"].split("/")[-1]
                        if len(locale) == 2:
                            path = f'{full_path}/{locale}/content-fragments/contacts' if content_fragment else each_path.get("path")
                            paths.append(path)
                        else:
                            self.logger.error("Locale is more than 2 chars: %s" % locale)
                elif locale_res.status_code == 401:
                    msg = "Wrong Username and Password - Http Code - "+str(locale_res.status_code)

                else:
                    msg = "Error Occurred - Http Code - "+str(locale_res.status_code)

            else:
                paths.append(full_path)
            # print(final_query)
            if msg is None:
                for path in paths:
                    if published:
                        if content_fragment:
                            filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(path,safe='')) +\
                            "&1_property=jcr%3acontent%2fcq%3alastReplicationAction&1_property.value=Activate&type=dam%3aAsset\
                                &2_property=jcr%3acontent%2fdata%2fcq%3amodel&2_property.value=%2fconf%2fpwc%2fsettings%2fdam%2fcfm%2fmodels%2fcontactprofile&3_property=jcr%3acontent%2fcontentFragment&3_property.value=true&p.hits=selective"
                        else:
                            filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(path,safe='')) +\
                            "&group.1_property=jcr%3acontent%2fcq%3atemplate&group.1_property.value=%2fconf%2fpwc%2fsettings%2fwcm%2ftemplates%2fcontact-profile-template&type=cq%3aPage\
                                &group.2_property=jcr:content/activatedInPublish&group.2_property.value=true&group.3_property=jcr:content/cq:lastReplicationAction&group.3_property.value=Activate&p.hits=selective"
                    else:
                        if content_fragment:
                            filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(path,safe='')) +\
                            "&type=dam%3aAsset&1_property=jcr%3acontent%2fdata%2fcq%3amodel&1_property.value=%2fconf%2fpwc%2fsettings%2fdam%2fcfm%2fmodels%2fcontactprofile&2_property=jcr%3acontent%2fcontentFragment&2_property.value=true&p.hits=selective"
                        else:
                            filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(path,safe='')) +\
                            "&group.1_property=jcr%3acontent%2fcq%3atemplate&group.1_property.value=%2fconf%2fpwc%2fsettings%2fwcm%2ftemplates%2fcontact-profile-template&type=cq%3aPage&p.hits=selective"
                    
                    query_data = filter_data + "&p.properties="+ col_data
                    self.logger.debug("Fullpath-> "+str(path)+", Filter Data -> "+str(filter_data)+", Columns-> "+str(col_data)
                                +", Query Data-> "+str(query_data))
                    final_query = self.ip + query_builder + "?" + query_data
                    self.logger.debug("Final Query: "+str(final_query))
                    resp_data = requests.get(final_query, auth=(self.user, self.passwd), timeout = self.timeout)
                    if resp_data.status_code == 200:
                        if outval is None:
                            outval = resp_data.json()
                        else:
                            outval["results"] = outval["results"] + resp_data.json()["results"]
                            outval["total"] = outval["total"] + resp_data.json()["total"]
                            outval["hits"].extend(resp_data.json()["hits"])
                    elif resp_data.status_code == 401:
                        msg = "Wrong Username and Password - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)
                        break
                    else:
                        msg = "Error Occurred - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)
                        break
                
                if outval is not None:
                    msg = []
                    results = [outval.get("results",0),outval.get("total",0)]
                    msg.append(results)
                    for each in outval["hits"]:
                        chunks = []
                        chunks.append(each.get("jcr:path", "Invalid Property"))
                        for prop in cleaned_cols:
                            if prop != "jcr:path":
                                # contact = each["jcr:content"].get("contact-profile-par",{}).get("contact",{})
                                # chunks.append(contact.get(prop.replace("jcr:content/contact-profile-par/contact/",""), "Invalid Property"))
                                rep = [y.strip() for y in prop.split("/")]
                                deap = None
                                for _rep in rep:
                                    if deap is None:
                                        deap = each.get(_rep, "Invalid Property")
                                    else:
                                        if isinstance(deap, dict):
                                            deap = deap.get(_rep, "Invalid Property")
                                chunks.append(deap)
                        msg.append(chunks)

            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    def user_def_report_selector(self, repo_name):
        try:
            with open("configfiles\\user_defined_reports.json") as fin:
                data = json.loads(fin.read())
            
            return data

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    def user_defined_report(self, query, cols, query_type):
        try:
            cleaned_cols = [x.strip() for x in cols if x.strip() != ""]
            final_query = None
            out_msg = None
            self.logger.debug("Column selected: "+str(cleaned_cols)+", Query Type: "+str(query_type))

            if query_type.lower().strip() == "query builder":
                query_link = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
                cleaned_cols.insert(0,"jcr:path")
                col_data = "+".join(cleaned_cols)
                final_query = self.ip + query_link + "?" + query + "&p.limit="+str(self.wfoperationdata.get("limit result", -1))+"&p.hits=selective&p.properties="+ col_data
            elif query_type.lower().strip() == "bulk editor":
                query_link = self.wfoperationdata["bulk editor link"]
                col_data = ",".join(cleaned_cols)
                _limit_data = " limit:" + str(self.wfoperationdata.get("limit result",10)) if self.wfoperationdata.get("limit result",0) > 0  else ""
                query = query + _limit_data
                _query_data_enc = quote(query, safe='')
                _col_data_enc = quote(col_data, safe='')
                time_in_ms = int(time()*1000)
                final_query = self.ip + query_link + "?query=" + _query_data_enc + "&tidy=true&cols="+_col_data_enc+"&_dc="+str(time_in_ms)
            else:
                final_query = None
            self.logger.debug("Final Query generated: %s" % final_query)

            if final_query is not None:
                _resp_data = requests.get(final_query, auth=(self.user, self.passwd), timeout=self.timeout)
                if _resp_data.status_code == 200:
                    out_msg = _resp_data.json()
                elif _resp_data.status_code == 401:
                    out_msg = "Wrong Username and Password - Http Code - "+str(_resp_data.status_code)
                    self.logger.error(out_msg)
                else:
                    out_msg = "Error Occurred - Http Code - "+str(_resp_data.status_code)
                    self.logger.error(out_msg)

            # print(out_msg)
            msg = None
            if isinstance(out_msg, dict):
                msg = []
                if query_type.lower().strip() == "bulk editor":
                    if out_msg.get("results",0) > 0:
                        results = [out_msg.get("results",0),out_msg.get("total",0)]
                        msg.append(results)
                            
                        for each in out_msg["hits"]:
                            chunks = []
                            chunks.append(each.get("jcr:path", "Invalid Property"))
                            for prop in cleaned_cols:
                                chunks.append(each.get(prop, "Invalid Property"))
                            msg.append(chunks)
                    else:
                        msg = None
                elif query_type.lower().strip() == "query builder":
                    if out_msg.get("results",0) > 0:
                        results = [out_msg.get("results",0),out_msg.get("total",0)]
                        msg.append(results)
                            
                        for each in out_msg["hits"]:
                            chunks = []
                            chunks.append(each.get("jcr:path", "Invalid Property"))
                            for prop in cleaned_cols:
                                if prop != "jcr:path":
                                    rep = [y.strip() for y in prop.split("/")]
                                    deap = None
                                    for _rep in rep:
                                        if deap is None:
                                            deap = each.get(_rep, "Invalid Property")
                                        else:
                                            if isinstance(deap, dict):
                                                deap = deap.get(_rep, "Invalid Property")
                                    chunks.append(deap)
                            msg.append(chunks)
                    else:
                        msg = None
            else:
                msg = out_msg
            self.logger.debug(msg)
            return msg

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    def pwc_form_field_order_data(self, form_type, territory, year, month, day):
        try:
            year_month_filter = self.form_date_filter(form_type, year, month, day)
            msg = None

            if year_month_filter is not None:
                query_builder_link = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
                filter_data = None
                full_path = None
                
                if form_type.lower() == "online arch":
                    full_path = str(self.wfoperationdata.get("form archive content path","/content/usergenerated/archive/content/pwc")) + "/" +str(territory).replace(self.wfoperationdata["content root"]+"/", "")
                    # full_path = global_form_path + "/" + year_month_filter
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(full_path,safe='')) +\
                                    "&1_property=formType&1_property.value=online&2_property=pwcSubmissionDatetime&2_property.value="+str(quote(year_month_filter,safe=''))+"&2_property.operation=like"
                elif form_type.lower() == "online":
                    full_path = str(self.wfoperationdata.get("form content path","/content/usergenerated/content/pwc")) + "/" +str(territory).replace(self.wfoperationdata["content root"]+"/", "")
                    # full_path = global_form_path + "/" + year_month_filter
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(full_path,safe='')) +\
                                    "&1_property=formType&1_property.value=online&2_property=pwcSubmissionDatetime&2_property.value="+str(quote(year_month_filter,safe=''))+"&2_property.operation=like"

                if filter_data is not None:
                    query_data = filter_data
                    self.logger.debug("Fullpath-> "+str(full_path)+", Filter Data -> "+str(filter_data)+", Query Data-> "+str(query_data))
                    final_query = self.ip + query_builder_link + "?" + query_data
                    self.logger.debug("Final Query: "+str(final_query))
                    
                    resp_data = requests.get(final_query, auth=(self.user, self.passwd), timeout = self.timeout)

                    if resp_data.status_code == 200:
                        msg = resp_data.json()
                    elif resp_data.status_code == 401:
                        msg = "Wrong Username and Password - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)
                    
                    else:
                        msg = "Error Occurred - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)

            return msg

        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return None

    def get_pwc_form_field_order_data(self, payloads, cols):
        try:
            cleaned_cols = [(x.strip().replace("jcr:content/","")) for x in cols if (x.strip() != "" and x.strip() != "pwcFormFieldOrder")]
            
            _url = self.ip + payloads + ".json"
            _resp_data = requests.get(_url, auth = (self.user, self.passwd), timeout = self.timeout)
            msg = None
            outval = None
            if _resp_data.status_code == 200:
                msg = []
                msg.append(payloads)
                outval = _resp_data.json()
                for _each_prop in cleaned_cols:
                    msg.append(outval.get(_each_prop,"Invalid Property"))

                pwcFormFieldOrder = outval.get("pwcFormFieldOrder","")
                if bool(pwcFormFieldOrder):
                    if isinstance(pwcFormFieldOrder, str):
                        eVarCol = outval.get("pwcFormFieldOrder","")
                        msg.append(eVarCol)
                        form_cols_data = [x.strip() for x in eVarCol.split(",") if x.strip() != ""]
                        chunks = []
                        for _each_form_field in form_cols_data:
                            chunks.append(outval.get(_each_form_field,""))
                        msg.append("| ".join(chunks))

            elif _resp_data.status_code == 401:
                msg = "Wrong Username and Password - Http Code - "+str(_resp_data.status_code)
                self.logger.error(msg)
                
            else:
                msg = "Error Occurred - Http Code - "+str(_resp_data.status_code)
                self.logger.error(msg)

            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    def fetch_redirection_details(self, territory, env, cols):
        try:
            def diff_com_strategy_and(terr_or_path):
                try:
                    strategy_and_or_com = None
                    terr_code = terr_or_path[0:2]
                    if terr_code.isnumeric():
                        strategy_and_or_com = "SAND"
                    else:
                        strategy_and_or_com = "DOTCOM"

                    return strategy_and_or_com
                except:
                    self.logger.error("Below Exception occurred\n", exc_info=True)
                    return None

            def redirect_path_selector(environment, terr_or_path):
                try:
                    redirect_node = None
                    self.logger.info("Environment: %s, Territory or Path: %s" % (environment, terr_or_path))
                    com_or_strategy = diff_com_strategy_and(terr_or_path)
                    reirect_selector = f"redirectpath{com_or_strategy.lower()}{environment.lower()}"
                    redirect_node = self.configdata.get(reirect_selector)
                    # if environment.lower() == "production":
                    #     if com_or_strategy == "S&":
                    #         redirect_node = "/etc/map/http/strategyand-az-origin-extpubv2.pwc.com"
                    #     elif com_or_strategy == "COM":
                    #         redirect_node = "/etc/map/http/pwc-az-origin-extpubv2.pwc.com"
                    # elif environment.lower() == "stage":
                    #     if com_or_strategy == "S&":
                    #         redirect_node = "/etc/map/http/strategyand-az-origin-extpub-stgv2.pwc.com"
                    #     elif com_or_strategy == "COM":
                    #         redirect_node = "/etc/map/http/pwc-az-origin-extpub-stgv2.pwc.com"
                    # elif environment.lower() == "qa":
                    #     if com_or_strategy == "S&":
                    #         redirect_node = "/etc/map/http/strategyand-az-origin-extpub-qa2.pwc.com"
                    #     elif com_or_strategy == "COM":
                    #         redirect_node = "/etc/map/http/pwc-az-origin-extpub-qa2.pwc.com"

                    return redirect_node
                except:
                    self.logger.error("Below Exception occurred\n", exc_info=True)
                    return None

            def prepare_and_retrv_data(qb_link, p_path, props):
                # filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(p_path,safe='')) +\
                #                     "&1_property=sling:redirect&1_property.operation=exists&2_property=sling:status&2_property.value=301&p.hits=selective"
                
                filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(p_path,safe='')) +\
                                    "&group.1_property=sling%3aredirect&group.1_property.operation=exists&group.2_property=sling%3ainternalRedirect&group.2_property.operation=exists&group.p.or=true&p.hits=selective"
                
                _out_val = None
                query_data = filter_data + "&p.properties="+ props
                self.logger.debug("Fullpath-> "+str(p_path)+", Filter Data -> "+str(filter_data)+", Columns-> "+str(props)
                            +", Query Data-> "+str(query_data))
                _final_query = self.ip + qb_link + "?" + query_data
                self.logger.debug("Final Query: "+str(_final_query))
                _resp_data = requests.get(_final_query, auth=(self.user, self.passwd), timeout = self.timeout)
                # _resp_data.status_code = 401
                if _resp_data.status_code == 200:
                    _out_val = _resp_data.json()
                elif _resp_data.status_code == 401:
                    _out_val = "Wrong Username and Password - Http Code - "+str(_resp_data.status_code)
                    self.logger.error(msg)
                else:
                    _out_val = "Error Occurred - Http Code - "+str(_resp_data.status_code)
                    self.logger.error(msg)

                return _out_val
            
            def format_out_data(t_data, _cleaned_cols):
                out_data = []
                results = [t_data.get("results",0), t_data.get("total",0)]
                out_data.append(results)
                for each in t_data["hits"]:
                    chunks = []
                    chunks.append(each.get("jcr:path", "Invalid Property"))
                    for prop in _cleaned_cols:
                        if prop != "jcr:path":
                            # chunks.append(each["jcr:content"].get(prop.replace("jcr:content/",""), "Invalid Property"))
                            splt_cols = [_x for _x in prop.split("/")]
                            _each_d = each.copy()
                            for _y in splt_cols:
                                if isinstance(_each_d.get(_y,""), dict):
                                    _each_d = _each_d[_y].copy()
                                else:
                                    chunks.append(_each_d.get(_y, "Invalid Property"))
                    out_data.append(chunks)
                return out_data

            content_root = self.wfoperationdata["content root"]
            content_dam_root = self.wfoperationdata["content dam root"]
            query_builder = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
            territory = territory.replace(content_root+"/","").replace(content_dam_root+"/","")
            redirect_path = redirect_path_selector(env, territory)
            self.logger.debug("Selected Redirect Node: %s" % (redirect_path))
            msg = None
            outval = None
            
            if redirect_path is not None:
                #full_path_1 = redirect_path + "/" + content_root +"/"+ territory
                full_path_1 = redirect_path + content_root +"/"+ territory
                #full_path_2 = redirect_path + "/" + content_dam_root +"/"+ territory
                full_path_2 = redirect_path + content_dam_root +"/"+ territory
                
                all_paths = [full_path_1, full_path_2,]
                # Preparation of Column
                cleaned_cols = [x.strip().replace("jcr:content/","") for x in cols if x.strip() != ""]
                cleaned_cols.insert(0,"jcr:path")
                col_data = "+".join(cleaned_cols)

                for full_path in all_paths:
                    outval = prepare_and_retrv_data(query_builder, full_path, col_data)
                    if isinstance(outval, str):
                        msg = outval
                        self.logger.error(msg)
                        break
                    else:
                        if outval is not None:
                            if msg is None:
                                # msg = format_out_data(outval, cleaned_cols)
                                msg = outval.copy()
                            else:
                                old_res = msg.get("results",0)
                                old_total = msg.get("total",old_res)
                                new_res = outval.get("results",0)
                                new_total = outval.get("total",new_res)
                                msg["results"] = old_res + new_res
                                msg["total"] = old_total + new_total
                                msg["hits"].extend(outval["hits"])
                        else:
                            msg = "Block Exception - Code - 999"
                            self.logger.error(msg)
                            break
                if msg is not None and isinstance(msg, dict):
                    msg = format_out_data(msg, cleaned_cols)

            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    def retrieve_pages_with_resourcetype(self, territory, resource_type, cols):
        try:
            self.logger.debug("Type of Selected: %s", resource_type)
            content_root = self.wfoperationdata.get("content root", "/content/dam/pwc")
            query_builder = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
            full_path = content_root + "/" + territory.replace(content_root+"/","")
            enc_path = quote(full_path, safe='')

            cleaned_cols = [x.strip() for x in cols if x.strip() != ""]
            # cleaned_cols = ["jcr:content/contact-profile-par/contact/"+(x.strip().replace("jcr:content/","")) for x in cols if x.strip() != ""]
            cleaned_cols.insert(0,"jcr:path")
            col_data = "+".join(cleaned_cols)

            msg = None
            outval = None
            paths = []
            if len(territory) == 2:
                query_for_locale = "p.limit=-1&path="+enc_path+"&path.flat=true&type=cq%3aPage"
                q_locale_query = self.ip + query_builder + "?" + query_for_locale
                self.logger.debug("Locale Query: %s", q_locale_query)
                locale_res = requests.get(q_locale_query, auth = (self.user, self.passwd), timeout = self.timeout)

                if locale_res.status_code == 200:
                    for each_path in locale_res.json()["hits"]:
                        locale = each_path["path"].split("/")[-1]
                        if len(locale) == 2:
                            path = f'{each_path.get("path")}'
                            paths.append(path)
                        else:
                            self.logger.error("Locale is more than 2 chars: %s" % locale)
                elif locale_res.status_code == 401:
                    msg = "Wrong Username and Password - Http Code - "+str(locale_res.status_code)

                else:
                    msg = "Error Occurred - Http Code - "+str(locale_res.status_code)
            else:
                paths.append(full_path)

            if msg is None:
                for path in paths:
                    if resource_type.startswith("isection-xf"):
                        filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(path,safe='')) +\
                            "&1_property=sling:resourceType&1_property.value=pwc/components/modernized/content/ixfsection&2_property=fragmentVariationPath&2_property.operation=exists&nodename="+resource_type+\
                            "&3_property=disableInheritance&3_property.value=true&p.hits=selective"
                    else:
                        filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(path,safe='')) +\
                            "&1_property=sling%3aresourceType&1_property.value="+str(quote(resource_type, safe=''))+"&p.hits=selective"

                    final_query = self.ip + query_builder + "?" + filter_data + "&p.properties="+ col_data
                    # print(final_query)
                    self.logger.debug("Final Query: %s", str(final_query))
                    resp_data = requests.get(final_query, auth=(self.user, self.passwd), timeout = self.timeout)
                    if resp_data.status_code == 200:
                        if outval is None:
                            outval = resp_data.json()
                        else:
                            outval["results"] = outval["results"] + resp_data.json()["results"]
                            outval["total"] = outval["total"] + resp_data.json()["total"]
                            outval["hits"].extend(resp_data.json()["hits"])
                    elif resp_data.status_code == 401:
                        msg = "Wrong Username and Password - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)
                        break
                    else:
                        msg = "Error Occurred - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)
                        break
                
                if outval is not None:
                    msg = []
                    results = [outval.get("results",0),outval.get("total",0)]
                    msg.append(results)
                    for each in outval["hits"]:
                        chunks = []
                        chunks.append(each.get("jcr:path", "Invalid Property"))

                        for prop in cleaned_cols:
                            if prop != "jcr:path":
                                # contact = each["jcr:content"].get("contact-profile-par",{}).get("contact",{})
                                # chunks.append(contact.get(prop.replace("jcr:content/contact-profile-par/contact/",""), "Invalid Property"))
                                rep = [y.strip() for y in prop.split("/")]
                                deap = None
                                for _rep in rep:
                                    if deap is None:
                                        deap = each.get(_rep, "Invalid Property")
                                    else:
                                        if isinstance(deap, dict):
                                            deap = deap.get(_rep, "Invalid Property")
                                chunks.append(deap)    
                        msg.append(chunks)
            
            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"

    def pwc_form_field_order_data_v2(self, form_type, cols, territory, year, month, day):
        try:
            year_month_filter = self.form_date_filter(form_type, year, month, day)
            msg = None
            cleaned_cols = [(x.strip().replace("jcr:content/","")) for x in cols if (x.strip() != "" and x.strip() != "pwcFormFieldOrder")]

            if year_month_filter is not None:
                query_builder_link = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
                filter_data = None
                full_path = None
                
                if form_type.lower() == "online arch":
                    full_path = str(self.wfoperationdata.get("form archive content path","/content/usergenerated/archive/content/pwc")) + "/" +str(territory).replace(self.wfoperationdata.get("content root","/content/pwc")+"/", "")
                    # full_path = global_form_path + "/" + year_month_filter
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(full_path,safe='')) +\
                                    "&1_property=formType&1_property.value=online&2_property=pwcSubmissionDatetime&2_property.value="+str(quote(year_month_filter,safe=''))+"&2_property.operation=like&p.hits=full"
                elif form_type.lower() == "online":
                    full_path = str(self.wfoperationdata.get("form content path","/content/usergenerated/content/pwc")) + "/" +str(territory).replace(self.wfoperationdata["content root"]+"/", "")
                    # full_path = global_form_path + "/" + year_month_filter
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(full_path,safe='')) +\
                                    "&1_property=formType&1_property.value=online&2_property=pwcSubmissionDatetime&2_property.value="+str(quote(year_month_filter,safe=''))+"&2_property.operation=like&p.hits=full"

                if filter_data is not None:
                    query_data = filter_data
                    self.logger.debug("Fullpath-> "+str(full_path)+", Filter Data -> "+str(filter_data)+", Query Data-> "+str(query_data))
                    final_query = self.ip + query_builder_link + "?" + query_data
                    self.logger.debug("Final Query: "+str(final_query))
                    
                    # print(final_query)
                    resp_data = requests.get(final_query, auth=(self.user, self.passwd), timeout = self.timeout)
                    # resp_data.status_code == 401
                    if resp_data.status_code == 200:
                        output = resp_data.json()
                        msg = []
                        results = [output.get("results",0),output.get("total",0)]
                        msg.append(results)
                        for _each_data in output["hits"]:
                            chunks = []
                            chunks.append(_each_data.get("jcr:path", "Invalid Property"))
                            for prop in cleaned_cols:
                                chunks.append(_each_data.get(prop, "Invalid Property"))

                            form_filed_order_field = _each_data.get("pwcFormFieldOrder", "")
                            chunks.append(form_filed_order_field)
                            form_filed_order_data = ""
                            if isinstance(form_filed_order_field, str):
                                if bool(form_filed_order_field.strip()):
                                    f_field = [x.strip() for x in form_filed_order_field.split(",") if x.strip() !=""]
                                    small_chunk = []
                                    for f in f_field:
                                        small_chunk.append(_each_data.get(f, "Invalid Property"))
                                    form_filed_order_data = self.join_list(" | ", small_chunk) #" | ".join(small_chunk)

                            chunks.append(form_filed_order_data)
                            msg.append(chunks)

                    elif resp_data.status_code == 401:
                        msg = "Wrong Username and Password - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)
                    
                    else:
                        msg = "Error Occurred - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)

            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"
        
    def contact_fragment_page_reference_report(self, territory):
        try:
            content_dam_root = self.wfoperationdata.get("content dam root", "/content/dam/pwc")
            query_builder = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
            full_path = content_dam_root + "/" + territory.replace(content_dam_root+"/","")
            enc_path = quote(full_path, safe='')
            msg = None
            outval = None
            paths = []
            if len(territory) == 2:
                query_for_locale = "p.limit=-1&path="+enc_path+"&path.flat=true&type=sling%3aFolder"
                q_locale_query = self.ip + query_builder + "?" + query_for_locale
                self.logger.debug("Locale Query: %s", q_locale_query)
                locale_res = requests.get(q_locale_query, auth = (self.user, self.passwd), timeout = self.timeout)

                if locale_res.status_code == 200:
                    for each_path in locale_res.json()["hits"]:
                        locale = each_path["path"].split("/")[-1]
                        if len(locale) == 2:
                            path = f'{each_path.get("path")}/content-fragments/contacts'
                            paths.append(path)
                        else:
                            self.logger.error("Locale is more than 2 chars: %s", locale)
                elif locale_res.status_code == 401:
                    msg = "Wrong Username and Password - Http Code - "+str(locale_res.status_code)

                else:
                    msg = "Error Occurred - Http Code - "+str(locale_res.status_code)
            else:
                paths.append(full_path)

            if msg is None:
                for path in paths:
                    filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(quote(path,safe='')) +\
                            "&type=dam%3aAssetContent"+\
                            "&1_property=data%2fcq%3amodel&1_property.value=%2fconf%2fpwc%2fsettings%2fdam%2fcfm%2fmodels%2fcontactprofile&2_property=contentFragment&2_property.value=true&p.hits=full&p.nodedepth=0"

                    final_query = self.ip + query_builder + "?" + filter_data
                    # print(final_query)
                    self.logger.debug("Final Query: %s", str(final_query))
                    resp_data = requests.get(final_query, auth=(self.user, self.passwd), timeout = self.timeout)
                    if resp_data.status_code == 200:
                        if outval is None:
                            outval = resp_data.json()
                        else:
                            outval["results"] = outval["results"] + resp_data.json()["results"]
                            outval["total"] = outval["total"] + resp_data.json()["total"]
                            outval["hits"].extend(resp_data.json()["hits"])
                    elif resp_data.status_code == 401:
                        msg = "Wrong Username and Password - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)
                        break
                    else:
                        msg = "Error Occurred - Http Code - "+str(resp_data.status_code)
                        self.logger.error(msg)
                        break
                
                if outval is not None:
                    msg = []
                    results = [outval.get("results",0),outval.get("total",0)]
                    msg.append(results)
                    for each in outval["hits"]:
                        chunks = []
                        chunks.append(each.get("jcr:path", "Invalid Property"))
                        small = []
                        for _key, _value in each.items():
                            if _key.startswith("pagereference"):
                                # print(_key, _value)
                                # contact = each["jcr:content"].get("contact-profile-par",{}).get("contact",{})
                                small.append(f"{_key}: {_value}")
                        chunks.append(", ".join(small))
                        chunks.append(each.get("cq:lastReplicationAction", "Invalid Property"))      
                        chunks.append(each.get("cq:lastReplicatedBy", "Invalid Property"))      
                        chunks.append(each.get("cq:lastReplicated", "Invalid Property"))    
                        msg.append(chunks)

            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"
        
    def tag_report(self, territory, cols, published = False):
        try:
            content_tag_root = self.wfoperationdata.get("content tag root", "/content/cq:tags")
            query_builder = self.wfoperationdata.get("query builder link","/bin/querybuilder.json")
            full_path = content_tag_root + "/pwc-" + territory.replace(content_tag_root +"/pwc-", "")
            enc_path = quote(full_path, safe='')
            cleaned_cols = [x.strip() for x in cols if x.strip() != ""]
            cleaned_cols.insert(0,"jcr:path")
            col_data = "+".join(cleaned_cols)
            outval = None
            msg = None
            if published:
                filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) +\
                                "&type=cq%3aTag&1_property=sling%3aresourceType&1_property.value=cq%2Ftagging%2Fcomponents%2Ftag&2_property=cq%3alastReplicationAction&2_property.value=Activate&p.hits=selective"
            else:
                filter_data = "p.limit=" + str(self.wfoperationdata.get("limit result", 100)) + "&path="+ str(enc_path) +\
                                "&type=cq%3aTag&1_property=sling%3aresourceType&1_property.value=cq%2Ftagging%2Fcomponents%2Ftag&p.hits=selective"
                
            query_data = filter_data + "&p.properties="+ col_data
            self.logger.debug("Fullpath-> "+str(full_path)+", Filter Data -> "+str(filter_data)+", Columns-> "+str(col_data)
                        +", Query Data-> "+str(query_data))
            final_query = self.ip + query_builder + "?" + query_data
            self.logger.debug("Final Query: "+str(final_query))
            resp_data = requests.get(final_query, auth=(self.user, self.passwd), timeout = self.timeout)
            if resp_data.status_code == 200:
                outval = resp_data.json()
            elif resp_data.status_code == 401:
                msg = "Wrong Username and Password - Http Code - "+str(resp_data.status_code)
                self.logger.error(msg)
            else:
                msg = "Error Occurred - Http Code - "+str(resp_data.status_code)
                self.logger.error(msg)

            if outval is not None:
                msg = []
                results = [outval.get("results",0),outval.get("total",0)]
                msg.append(results)
                for each in outval["hits"]:
                    chunks = []
                    chunks.append(each.get("jcr:path", "Invalid Property"))
                    for prop in cleaned_cols:
                        if prop != "jcr:path":
                            chunks.append(each.get(prop, "Invalid Property"))
                    
                    msg.append(chunks)
            return msg
        except:
            self.logger.error("Below Exception occurred\n", exc_info=True)
            return "Exception - Code - 999"
