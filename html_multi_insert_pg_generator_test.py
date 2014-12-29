#!/usr/local/bin/python
#
# ReadLines.py :
# idioms for reading a file line at a time encapsulated as classes for re-use
#

import sys
import re
import glob
import string
import pickle
from copy import deepcopy

import wizard_conf

from wizard_conf_cls import Wizard_conf
wz = Wizard_conf()
jslib_dir = Wizard_conf.jslib_dir
default_no_cursor_flds = wz.default_no_cursor_flds


from html_1_tbl_pg_generator import mainPgGen
mainPg  = mainPgGen(wz)
print "---------------------------------------------\n"
mainPg.parser()
mainPg.js_columns_types()
print "---------------------------------------------\n"
chect_btn_dict=mainPg.chect_btn_dict
drop_down_dict=mainPg.drop_down_dict
fields_for_function_dict=mainPg.fields_for_function_dict
function1_dict=mainPg.function1_dict
function2_dict=mainPg.function2_dict
function3_dict=mainPg.function3_dict
function4_dict=mainPg.function4_dict
function5_dict=mainPg.function5_dict
pg_title_dict=mainPg.pg_title_dict           
tbl_dicts=mainPg.tbl_dicts
chinese_title=mainPg.chinese_title
type_dict=mainPg.type_dict
char_len_dict=mainPg.char_len_dict
d_type_info_dict=mainPg.d_type_info_dict
DBColumn_dict=mainPg.DBColumn_dict
pyfile_dict=mainPg.pyfile_dict
#not_in_order_by_clause_dict=mainPg.not_in_order_by_clause_dict                                                
#order_by_clause_dict=mainPg.order_by_clause_dict                                                
summation_dict=mainPg.summation_dict                                                

from TABLE_SPEC import _TABLE_SPEC

#########################################
# you have to customize the following data
search_length = 20
height_pixel  = 180
rp_tbl_width = 85    #for single table field

my_root_dir = wizard_conf.my_root_dir
my_prj_dir = wizard_conf.my_prj_dir
zxz_software = wizard_conf.zxz_software
my_office_page = wizard_conf.my_office_page
database0 = wizard_conf.database0
dateformat0 = wizard_conf.dateformat0

from wizard_lib.get_db_n_dateformat import get_db_n_dateformat

#########################################
# you have to customize the following data

prj_dir = "%s\\scripts\\%s"%(my_root_dir, my_prj_dir)
html_dir = "%s\\htdocs\\%s"%(my_root_dir, my_prj_dir)

#########################################


class InputLines:
    def __init__(self,file=sys.stdin):
	self.file, self.index, self.data = file, -1, ''

    def __getitem__(self,index):
	i=self.index
	if index == i: return self.data
	if index == 0 and i > 0:
	    self.file.seek(0)
	    i=-1
	while i < index:
	    l=self.file.readline()
	    if not l: raise IndexError, 'end of file'
	    i=i+1
	self.index, self.data = i, l
	return l


"""
tbl_dicts = {}
chinese_title = {}
type_dict = {}
DBColumn_dict = {}
char_len_dict={}
d_type_info_dict={}


pyfile_dict = {}
pg_title_dict = {}
"""
#zzzz 20040725
not_in_order_by_clause_dict = {}
order_by_clause_dict = {}
pg_info_dict = {
"my_office_page":my_office_page,
"PG_ZXZINC": zxz_software,
"PG_ALIASES": "xxxx",
"PG_ALIASES_DEF": "xxxx",
"PG_NAME": "xxxx", 
"PG_MAINBODY": "xxxx",
"LP_PG":"xxxx",
"RP_PG":"xxxx",
"RP_TITLE_LINE":"xxxx",
"RP_SINGLE_RECORD":"xxxx",
"RP_RECORDS":"xxxx",
"RP_TBL_WIDTH":1,
"TR_BGCOLOR":"xxxx",
"PG_SCH_LEN":"xxxx",
"FIELD_NAME":"xxxx",
"FIELD_NAME2":"xxxx",
"CHINESE_TITLE":"xxxx",
"H_PIXEL":0,
"COLSPAN":0,
"WHICH_ROW":0,
"xText":"STRING_LIST",
"xDate":"DATE_LIST",
"xDateTime":"DATE_LIST",
"oraDateTime":"DATE_LIST",
"xLong":"INTEGER_LIST",
"xInteger":"INTEGER_LIST",
"xFloat":"FLOAT_LIST",
"identity":"INTEGER_LIST",
"unknownType":"STRING_LIST",
"DATA_TYPE_LIST":"xxx",
"JS_COLUMNS":"xxx"}
pg_info_dict1 = pg_info_dict


lp_td_html = {"xLong":"", "xText": "", "xDate": "", "xDateTime":"","oraDateTime":""}
rp_td_html = {"rp_tmpl":"", "rp_records": "", "rp_title_line": ""}

all_td_html = {}
call_func = {}
# just consider *_query.py files
file_list = glob.glob(prj_dir+'\\*.py')

for file in file_list:
      aaa = string.split(file,"\\")
      if aaa[-1] != "__init__.py":
            cur_obj = string.split(file[:-3], "\\")
            cur_obj_idx = cur_obj.index('scripts')+1
            dynamic_module = '.'.join(cur_obj[cur_obj_idx:])
	    

def parser():

   _pg_title = "Table_title_error!!!"                        
   #find all files in this dir and put them into file_list
   for file in file_list:
      _isOrderByClauseThere = 0 # 0: no, 1: yes
      # trying to get "mSites_query" from "c:\xbop_his\scripts\his\mSites_query.py"
      cur_obj = string.split(file[:-3], "\\")
      cur_obj_idx = cur_obj.index('scripts')+1
      if cur_obj[-1]=='__init__':
            pass
      else:
            bbb = '.'.join(cur_obj[cur_obj_idx:])

      aaa = string.split(file,"\\")
      if aaa[-1] == "__init__.py":
         pass
      else:
             class_index = 0
             field_list = []
             chinese_list=[]
	     type_list = []
             char_len_list = []
             d_type_info_list = []

             not_in_order_by_clause_list= []
	
 	     DBColumn_list = []
             not_in_order_by_list = []
             order_by_list = []

	     pg_title_ready = 0 
	     for line in InputLines(open(file,'r')):
                 if line.startswith('##')==False:
		     if class_index == 0:
                        #reg1 = re.compile('^class.*:').match(line)	
		        if string.find(line,"class") == 0:
			        class_index = 1
				class_name = string.split(line," ")
				#finding the name of the class
                                class_name = string.split(class_name[1],"(")
		     else:
			#kick out comment lines
                        line = string.strip(line)
                        if line.startswith('#') and (not line.startswith('# l_'))  and (not line.startswith('# order_by_clause')) and (not line.startswith('# order_by_clause2')) and (not line.startswith('# not_in_order_by_clause')):
			     pgInfo_str = string.split(line)
                             if len(pgInfo_str) > 1:
                                 if pgInfo_str[1] == "table_title":
                                     _pg_title = pgInfo_str[2]                        
                             #if string.strip(pgInfo_str[1]) == "onweb":
                             #        onweb_dict[class_name[0]] = pgInfo_str[2:]
                                              	     	
                        else:
				if line.startswith('#'):
					line = string.strip(line[1:])
					if string.strip(string.split(line,"=")[0])=="not_in_order_by_clause":
                                              not_in_order_by_clause_list = string.split(string.strip((string.split(line, "=")[1])),"/")
					if string.strip(string.split(line,"=")[0])=="order_by_clause" or string.strip(string.split(line,"=")[0])=="order_by_clause2":
                                              _isOrderByClauseThere = 1  # 0: no, 1: yes
                                              
                                              
                                if string.find(line,"= DB") > 0 or string.find(line,"xList(tp") > 0:
                                        aaa1 = string.split(line, "=")
			                field_list.append(string.strip(string.strip(aaa1[0], " "), "\t"))
			                #type_list.append(string.strip(string.strip(string.split(aaa1[2], ")")[0], " "), ")\n"))

                                        #get xText, xLong, xDateTime etc
					#
					# Here are examples for aaa1: string.split(line, "=")
                                        # case 1. dbcRowid = DBIdentity("rowId")  #ID #0 #none none  
                                        # case 2. dbcOrderid = DBColumn("orderId", tp=xText)  #收据编号 #20 #none none
					#
					try:  # case 2
                                             type_list.append(string.strip(string.strip(string.split(aaa1[2], ")")[0], " "), ")\n"))
                                        except: # case 1 ... using identity as default
                                             type_list.append('identity')



                                        DBColumn_list.append(string.strip(string.strip(string.split(aaa1[1], "(")[0], " "), ")\n"))
                                        #getting the chinese field name 
          				if string.find(line, "#") >=0:
	     			            tmp = string.splitfields(line,"#")

					    #
					    #zzzz: getting char or varchar length recorded in mapping py file
					    #
					    char_len_list.append(tmp[-2])

                                            # zzzz: getting d_type_info: such as " oralce YYYY-MM-DD"
					    d_type_info_list.append(tmp[-1])
	

					    #char_len_list.append(tmp[-2])


				            if len(string.strip(string.strip(tmp[1], " "),"\n"))==0:
					          chinese_list.append(string.strip(string.strip(aaa1[0], " "), "\t"))
			                    else:
                                                  chinese_list.append(string.strip(tmp[1],"\n"))

						  #get page title
						  #if len(tmp) >= 3:
						  #	if len(string.strip(string.strip(tmp[2], " "),"\n"))!=0:
						  #              if pg_title_ready == 0: 
						  #	             _pg_title = string.strip(tmp[2], "\n")
						  #                     pg_title_ready = 1 
								     

                                        else:
				     	        chinese_list.append(string.strip(string.strip(aaa1[0], " "), "\t"))
                                                 
				
             #pg_title_dict[class_name[0]] = _pg_title             
	     #tbl_dicts[class_name[0]] = field_list
             #chinese_title[class_name[0]] = chinese_list
	     #type_dict[class_name[0]]= type_list
	     #char_len_dict[class_name[0]] = char_len_list
	     #d_type_info_dict[class_name[0]] = d_type_info_list

	     #DBColumn_dict[class_name[0]]= DBColumn_list
	     #pyfile_dict[class_name[0]] = string.split(string.split(file,"\\")[-1], ".")[0]
             not_in_order_by_clause_dict[class_name[0]]=not_in_order_by_clause_list                                                
             order_by_clause_dict[class_name[0]]=_isOrderByClauseThere                                                

   #print "table fields"	     
   #print tbl_dicts	     
   #print tbl_dicts	     
   #print "Chinese title"     
   #print chinese_title
   #print "type_list"
   #print type_dict
   #print pyfile_dict
   ###print not_in_order_by_clause_dict
	  
def mkdir():
     import os
     import dircache
     for k in tbl_dicts.keys():
         if pyfile_dict[k] not in dircache.listdir(html_dir):
               print "new directory: ", html_dir+"\\"+pyfile_dict[k]
               os.makedirs(html_dir+"\\"+pyfile_dict[k],0777)
         else:
               print "old directory  ", html_dir+"\\"+pyfile_dict[k]
     for k in tbl_dicts.keys():
         if pyfile_dict[k] not in dircache.listdir(html_dir):
               print "new directory: ", html_dir+"\\"+pyfile_dict[k]
               os.makedirs(html_dir+"\\"+pyfile_dict[k],0777)
         else:
               print "old directory  ", html_dir+"\\"+pyfile_dict[k]

def gen_lp_pg():
	
	HTML_MULTI_pg_dict={}
        tmp = string.split(prj_dir,"\\")
        aaa = tmp.index("scripts")+1
        
	pg_info_dict = pg_info_dict1
	
        no_cursor_flds = default_no_cursor_flds
        for k in tbl_dicts.keys():
	        HTML_MULTI_pg_dict[k]={}
                lp_hidden_fields = ""
		delta_hh = 26
		hh  = 0
                tmp1 = tmp[:]    #this is differet from "tmp1 = tmp" which uses same chunk of memory.
                tmp2 = tmp[:]    #this is differet from "tmp2 = tmp" which uses same chunk of memory.
                tmp1.append(pyfile_dict[k])
                tmp2.append(pyfile_dict[k])
                tmp1.append("db" + k)
                #tmp1.append(k)
                pg_info_dict["PG_ALIASES_DEF"] = string.join(tmp1[aaa:],".")
                pg_info_dict["PG_ALIASES"] = "$"+k 
                aaa1 = string.join(tmp2[aaa:],"/")
                pg_info_dict["RP_PG"] = aaa1 + "/" + "rp_multi_edi_" + k + ".html"
                #pg_info_dict["SEARCH_PG"] = aaa1 + "/" + "stuff_edit_delete.html"
                pg_info_dict["SEARCH_PG"] = aaa1 + "/" + "lp_mr_"+ k + ".html"
		###############################################################################
		#
                _k_ = string.lower(k[1:])
                my_prj_dir = wizard_conf.my_prj_dir
		try:
		    other_tbl = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['OTHER_TBL']
                    pg_info_dict["DROP_DOWN_SEARCH_PG"] = my_prj_dir + "/m%s/"%string.capitalize(other_tbl) + "lp_mr_"+ "o%s"%string.capitalize(other_tbl) + ".html"
		except:
                    pg_info_dict["DROP_DOWN_SEARCH_PG"] = ""
                
		#
		################################################################################
		#
		pg_info_dict["HIDDEN_FIELDS_FOR_DATATRANSFER"] = "" 
                _k_ = string.lower(k[1:])
                my_prj_dir = wizard_conf.my_prj_dir
		hidden_name_all = ""
		hidden_name_str = """\
   <input type=hidden name="%(hidden_field_name)s.searchString" value="">
   <input type=hidden name="%(hidden_field_name)s.searchOffset" value=0>
   <input type=hidden name="%(hidden_field_name)s.searchLength" value=10>
                 """
		try:
		    for ky in _TABLE_SPEC[_k_]["TBL_INFO"]['DROP_DOWN_RELATION'].keys():
			  sub_drop_menu_tbl =_TABLE_SPEC[_k_]["TBL_INFO"]['DROP_DOWN_RELATION'][ky][0]
			  ak = string.capitalize(sub_drop_menu_tbl)
			  pg_info_dict["hidden_field_name"] = my_prj_dir+".m%s.dbo%s"%(ak,ak)
			  hidden_name_all += hidden_name_str%pg_info_dict 
		    pg_info_dict["HIDDEN_FIELDS_FOR_DATATRANSFER"] += hidden_name_all
		except:
		    pass 
	     
		try:
		    other_table = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']["OTHER_TBL"]
		    ak = string.capitalize(other_table)
		    pg_info_dict["hidden_field_name"] = my_prj_dir+".m%s.dbo%s"%(ak,ak)
		    hidden_name_all += hidden_name_str%pg_info_dict 
		    pg_info_dict["HIDDEN_FIELDS_FOR_DATATRANSFER"] += hidden_name_all
		except:
                    pass
                 
                hidden_drop_down_str = """\
    <input type=hidden name="%(PG_ALIASES)s.%(hidden_target)s[0]" value=''>
                """
		try:
		    for ky in _TABLE_SPEC[_k_]["TBL_INFO"]['DROP_DOWN_TARGET'].keys():
		        target_field = _TABLE_SPEC[_k_]["TBL_INFO"]['DROP_DOWN_TARGET'][ky]
		        ak = string.capitalize(target_field)
		        pg_info_dict["hidden_target"] = "dbc%s"%(ak)
		        hidden_name_all +=  hidden_drop_down_str%pg_info_dict 
		        pg_info_dict["HIDDEN_FIELDS_FOR_DATATRANSFER"] += hidden_name_all
		except:
                    pass

                #
		################################################################################
		pg_info_dict["SEARCH_RP_PG"] = aaa1 + "/" + "rp_search_"+k+".html"
                pg_info_dict["EDIT_RP_PG"] = aaa1 + "/" + "rp_edit_"+ k + ".html"
                #pg_info_dict["EDIT_RP_PG"] = aaa1 + "/" + "lp_insert_"+ k + ".html"
                pg_info_dict["DELETE_RP_PG"] = aaa1 + "/" + "rp_delete_"+ k + ".html"
                pg_info_dict["MULTI_EDI_RP_PG"] = aaa1 + "/" + "rp_multi_edi_" + k + ".html"

                pg_info_dict["PG_SCH_LEN"] = search_length
                pg_info_dict["PG_NAME"]=pg_title_dict[k]                 
                pg_info_dict["zxz_software"]=zxz_software                 
                pg_info_dict["my_prj_dir"]= string.replace(wizard_conf.my_prj_dir, "\\", "/")
                #preparing math calculation functions
                pg_info_dict["_FUNCTION1"] = ""
                pg_info_dict["_FUNCTION2"] = ""
                pg_info_dict["_FUNCTION3"] = ""
                pg_info_dict["_FUNCTION4"] = ""
                pg_info_dict["_FUNCTION5"] = ""
                pg_info_dict["MY_FUNCTION"] = ""
                #
                # here is for ckInsert() with sql identity
                #
                pg_info_dict['PY_INSERT_METHOD'] = 'insert'
	        
		pg_info_dict["DATABASE"] = database0
		pg_info_dict["DATEFORMAT"] = dateformat0




                # preparing fields called in functions
                #
                flds_4_func = {}
                if fields_for_function_dict[k][0] != 'none':
                                     # preparing _fields_for_function 
                                     flds = string.split(fields_for_function_dict[k][0],'/')
                                     for ik in range(len(flds)):
                                                   flds_4_func["f%d"%ik] = "%s"%flds[ik]

                # preparing fields for db_dateformat_flds: db: oracle, sqlserver, mysql....
                #                                          dateformat: YYYY-MM-DD HH24:MI:SS whatever you like 
                #this_tbl_db_dateformat_flds_dict = {}
                #if db_dateformat_flds_dict[k][0] != 'none':
                #                    # finding database and dateformat
                #                    flds = string.split(db_dateformat_flds_dict[k][0],'/')
                #                     this_tbl_db_dateformat_flds_dict["db"] = "%s"%flds[0]
                #                     this_tbl_db_dateformat_flds_dict["dateformat"] = "%s"%flds[1]
                #                     for ik in range(len(flds)):
                #                            this_tbl_db_dateformat_flds_dict["flds"%(ik)] = "%s"%flds[ik+2]
                #                            if ik+2 > len(flds): break
                                                     

                call_func["function1"]=[]
                if function1_dict[k][0] != 'none':
                                     # preparing _function1 javascript
                                     vars = ""
                                     not_NaN_str = ""
                                     flds = string.split(function1_dict[k][1],'/')
                                     for ik in range(len(flds)):
                                            pg_info_dict["junk"]= ".dbc"+string.capitalize(flds_4_func["%s"%flds[ik]])
                                            #fik = func_index + ik
                                            if ik != len(flds)-1: 
                                                   junk2 = "parseFloat(document.forms[0]['%(PG_ALIASES)s%(junk)s[0]'].value);\n"%pg_info_dict
                                                   call_func["function1"].append("%(PG_ALIASES)s%(junk)s[0]"%pg_info_dict)
                                                   if ik==0:
                                                         not_NaN_str = not_NaN_str + " !isNaN(%s)"%flds[ik] 
                                                   else:
                                                         not_NaN_str = not_NaN_str + " && !isNaN(%s)"%flds[ik]

                                            else:
                                                   junk2 = "document.forms[0]['%(PG_ALIASES)s%(junk)s[0]']; "%pg_info_dict
                                                   #func_index = fik + 1                 

                                            #junk3 = "var f"+ "%d = "%fik
                                            vars = vars + "var %s = "%flds[ik] + junk2
                                     func = string.split(function1_dict[k][0],'|')
                                     pg_info_dict["VAR"] = vars
                                     pg_info_dict["FUNCTION"] = func[0]
                                     pg_info_dict["RESULT_FIELD"] = func[1]

                                     no_cursor_flds.append("dbc"+string.capitalize(flds_4_func["%s"%func[1]]))

                                     pg_info_dict["FUNC1"] = "function1"
                                     pg_info_dict["NOT_NaN"] = not_NaN_str
                                     pg_info_dict["_FUNCTION1"] = all_td_html["_function"]%pg_info_dict
                                     
                call_func["function2"]=[]
                if function2_dict[k][0] != 'none':
                                     # preparing _function2 javascript
                                     vars = ""
                                     not_NaN_str = ""
                                     flds = string.split(function2_dict[k][1],'/')
                                     for ik in range(len(flds)):
                                            pg_info_dict["junk"]= ".dbc"+string.capitalize(flds_4_func["%s"%flds[ik]])
                                            if ik != len(flds)-1: 
                                                   junk2 = "parseFloat(document.forms[0]['%(PG_ALIASES)s%(junk)s[0]'].value);\n"%pg_info_dict
                                                   call_func["function2"].append("%(PG_ALIASES)s%(junk)s[0]"%pg_info_dict)
                                                   if ik==0:
                                                         not_NaN_str = not_NaN_str + " !isNaN(%s)"%flds[ik] 
                                                   else:
                                                         not_NaN_str = not_NaN_str + " && !isNaN(%s)"%flds[ik]
                                            else:
                                                   junk2 = "document.forms[0]['%(PG_ALIASES)s%(junk)s[0]']; "%pg_info_dict
                                            
                                            vars = vars + "var %s = "%flds[ik] + junk2
                                            
                                     func = string.split(function2_dict[k][0],'|')
                                     pg_info_dict["VAR"] = vars
                                     pg_info_dict["FUNCTION"] = func[0]
                                     pg_info_dict["RESULT_FIELD"] = func[1]

                                     no_cursor_flds.append("dbc"+string.capitalize(flds_4_func["%s"%func[1]]))
                                     pg_info_dict["FUNC1"] = "function2"
                                     pg_info_dict["NOT_NaN"] = not_NaN_str
                                     pg_info_dict["_FUNCTION2"] = all_td_html["_function"]%pg_info_dict
                                          
                call_func["function3"]=[]
                if function3_dict[k][0] != 'none':
                                     # preparing _function3 javascript
                                     vars = ""
                                     not_NaN_str = ""
                                     flds = string.split(function3_dict[k][1],'/')
                                     for ik in range(len(flds)):
                                            pg_info_dict["junk"]= ".dbc"+string.capitalize(flds_4_func["%s"%flds[ik]])
                                            if ik != len(flds)-1: 
                                                   junk2 = "parseFloat(document.forms[0]['%(PG_ALIASES)s%(junk)s[0]'].value);\n"%pg_info_dict
                                                   call_func["function3"].append("%(PG_ALIASES)s%(junk)s[0]"%pg_info_dict)
                                                   if ik==0:
                                                         not_NaN_str = not_NaN_str + " !isNaN(%s)"%flds[ik] 
                                                   else:
                                                         not_NaN_str = not_NaN_str + " && !isNaN(%s)"%flds[ik]
                                            else:
                                                   junk2 = "document.forms[0]['%(PG_ALIASES)s%(junk)s[0]']; "%pg_info_dict

                                            vars = vars + "var %s = "%flds[ik] + junk2
                                            
                                     func = string.split(function3_dict[k][0],'|')
                                     pg_info_dict["VAR"] = vars
                                     pg_info_dict["FUNCTION"] = func[0]
                                     pg_info_dict["RESULT_FIELD"] = func[1]

                                     no_cursor_flds.append("dbc"+string.capitalize(flds_4_func["%s"%func[1]]))
                                     pg_info_dict["FUNC1"] = "function3"
                                     pg_info_dict["NOT_NaN"] = not_NaN_str
                                     pg_info_dict["_FUNCTION3"] = all_td_html["_function"]%pg_info_dict
                                          
                call_func["function4"]=[]
                if function4_dict[k][0] != 'none':
                                     # preparing _function4 javascript
                                     vars = ""
                                     not_NaN_str = ""
                                     flds = string.split(function4_dict[k][1],'/')
                                     for ik in range(len(flds)):
                                            pg_info_dict["junk"]= ".dbc"+string.capitalize(flds_4_func["%s"%flds[ik]])
                                            if ik != len(flds)-1: 
                                                   junk2 = "parseFloat(document.forms[0]['%(PG_ALIASES)s%(junk)s[0]'].value);\n"%pg_info_dict
                                                   call_func["function4"].append("%(PG_ALIASES)s%(junk)s[0]"%pg_info_dict)
                                                   if ik==0:
                                                         not_NaN_str = not_NaN_str + " !isNaN(%s)"%flds[ik] 
                                                   else:
                                                         not_NaN_str = not_NaN_str + " && !isNaN(%s)"%flds[ik]
                                            else:
                                                   junk2 = "document.forms[0]['%(PG_ALIASES)s%(junk)s[0]']; "%pg_info_dict

                                            vars = vars + "var %s = "%flds[ik] + junk2
                                     func = string.split(function4_dict[k][0],'|')
                                     pg_info_dict["VAR"] = vars
                                     pg_info_dict["FUNCTION"] = func[0]
                                     pg_info_dict["RESULT_FIELD"] = func[1]

                                     no_cursor_flds.append("dbc"+string.capitalize(flds_4_func["%s"%func[1]]))
                                     pg_info_dict["FUNC1"] = "function4"
                                     pg_info_dict["NOT_NaN"] = not_NaN_str
                                     pg_info_dict["_FUNCTION4"] = all_td_html["_function"]%pg_info_dict
                                          
                                          
                call_func["function5"]=[]
                if function5_dict[k][0] != 'none':
                                     # preparing _function5 javascript
                                     vars = ""
                                     not_NaN_str = ""
                                     flds = string.split(function5_dict[k][1],'/')
                                     for ik in range(len(flds)):
                                            pg_info_dict["junk"]= ".dbc"+string.capitalize(flds_4_func["%s"%flds[ik]])
                                            if ik != len(flds)-1: 
                                                   junk2 = "parseFloat(document.forms[0]['%(PG_ALIASES)s%(junk)s[0]'].value);\n"%pg_info_dict
                                                   call_func["function5"].append("%(PG_ALIASES)s%(junk)s[0]"%pg_info_dict)
                                                   if ik==0:
                                                         not_NaN_str = not_NaN_str + " !isNaN(%s)"%flds[ik] 
                                                   else:
                                                         not_NaN_str = not_NaN_str + " && !isNaN(%s)"%flds[ik]
                                            else:
                                                   junk2 = "document.forms[0]['%(PG_ALIASES)s%(junk)s[0]']; "%pg_info_dict

                                            vars = vars + "var %s = "%flds[ik] + junk2
                                     func = string.split(function5_dict[k][0],'|')
                                     pg_info_dict["VAR"] = vars
                                     pg_info_dict["FUNCTION"] = func[0]
                                     pg_info_dict["RESULT_FIELD"] = func[1]

                                     no_cursor_flds.append("dbc"+string.capitalize(flds_4_func["%s"%func[1]]))
                                     pg_info_dict["FUNC1"] = "function5"

                                     pg_info_dict["NOT_NaN"] = not_NaN_str
                                     pg_info_dict["_FUNCTION5"] = all_td_html["_function"]%pg_info_dict

                """
		#get association table info ...
                assoc_tbl = string.strip(association_tbl_dict[k][0])
                if assoc_tbl != "none":
                     try:
                             single_or_multi = string.lower(string.strip(association_tbl_dict[k][1]))
                             _Assoc_tbl = string.capitalize(assoc_tbl) 
                             if single_or_multi == "m":  # multi records page
                                     pg_info_dict["ASSOCIATION_PG"]= my_prj_dir2 + "/" + "m" + _Assoc_tbl +"/" + "all_" +"o"+ string.capitalize(string.strip(association_tbl_dict[k][0])) + ".html"
                             else:   # single record page
                                     pg_info_dict["ASSOCIATION_PG"]= my_prj_dir2 + "/" + "m" + _Assoc_tbl +"/" +"o"+ string.capitalize(string.strip(association_tbl_dict[k][0])) + ".html"
                     except:
                             print "\n\noops! something wrong with table ", k, " with association table part\n\n"
                else:
                     pg_info_dict["ASSOCIATION_PG"]= ""
                """
                
		#
		# now handle the no_cursor_flds, such as data_type = "identity", "dbcCreate_on"
		#
		for j in range(len(tbl_dicts[k])):
			#if type_dict[k][j]== "identity" or tbl_dicts[k][j] =="dbcCreate_on" or tbl_dicts[k][j] =="dbcRowid":   
			if type_dict[k][j]== "identity" and tbl_dicts[k][j] not in no_cursor_flds:   
                                       no_cursor_flds.append(tbl_dicts[k][j])

                col = ""
                for j in range(len(tbl_dicts[k])):
                      #preparing javascript for columns
                      data_type = type_dict[k][j]
                      pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
                      pg_info_dict["FIELD_NAME2"] = tbl_dicts[k][j]+"2"
                      
                      pg_info_dict["CHARLEN"] = char_len_dict[k][j]
		      #zzzz
                      _k_ = string.lower(k[1:])
                      flds = string.lower(tbl_dicts[k][j])[3:]
                      getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC,data_type)
                      pg_info_dict = getDB()
		      #zzz
		      """
                      _db_dateformat= string.split(d_type_info_dict[k][j])
                      pg_info_dict["DATABASE"] = _db_dateformat[0]
                      pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
                      """

                      print "no curso fields ", k,j,  no_cursor_flds, tbl_dicts[k][j]
		      #if j < len(tbl_dicts[k])-1:
		      #           if tbl_dicts[k][j+1] == "order_by_clause" or tbl_dicts[k][j+1] == "order_by_clause2":
		      #                   pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][0]
                      #           else:
		      #                   pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][j+1]
		      #else:
		      #           pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][0]
				 
                      #if j < len(tbl_dicts[k])-1:
                      #      pg_info_dict["FIELD_NAME2_1"] = tbl_dicts[k][j+1]+"2"
                      #      if tbl_dicts[k][j+1] not in no_cursor_flds:
                      #              pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][j+1]
                      #      else:
		      #              if j == len(tbl_dicts[k])-2:
                      #                     jj = 0
                      #                     while 1:
                      #                          if tbl_dicts[k][jj] not in no_cursor_flds: 
                      #                                pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][jj]
                      #                                break
                      #                          else:
                      #                                jj = jj+1
                      #                                if jj > j:
		      #                                       print "something wrong with cursor movement, ask Ouyang"
		      #                                       break  
                      #              else:
                      #                     if tbl_dicts[k][j+2] not in no_cursor_flds: 
                      #                            pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][j+2]
                      #                      else:
                      #                            pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][j+3]
                      #else:
                      #      pg_info_dict["FIELD_NAME2_1"] = tbl_dicts[k][0]+"2"
                      #      #self.pg_info_dict["FIELD_NAME_1"] = self.tbl_dicts[k][0]
                      #      if tbl_dicts[k][0] not in no_cursor_flds: 
                      #                pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][0]
                      #      else:
                      #                pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][1]
                      if j < len(tbl_dicts[k])-1:
                                 pg_info_dict["FIELD_NAME2_1"] = tbl_dicts[k][j+1]+"2"
				 jj = j+1
				 while 1:
                                       if tbl_dicts[k][jj] in no_cursor_flds:
                                              if jj == len(tbl_dicts[k])-1: 
						      jj =0
					      else:
                                                      jj += 1
                                       else:
					      break
                                 pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][jj]
                      else:
                                 pg_info_dict["FIELD_NAME2_1"] = tbl_dicts[k][0]+"2"
				 jj = 0
				 while 1:
                                       if tbl_dicts[k][jj] in no_cursor_flds:
                                                      jj += 1
                                       else:
					      break
                                 pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][jj]                              
                      #xxxx                    
                      pg_info_dict["FIELD_NAME3"] = tbl_dicts[k][j][3:]  #cut off dbc-prefix such as dbcRecord_num
                      if data_type not in pg_info_dict.keys():
                              #unknown type, using default type xText
                              pg_info_dict["DATA_TYPE_LIST"] = pg_info_dict["unknownType"]
                      else:
                              pg_info_dict["DATA_TYPE_LIST"] = pg_info_dict[data_type]
                      col = col + all_td_html["js_columns"]%pg_info_dict
                
                pg_info_dict["JS_COLUMNS"] = col

                col = ""
                for j in range(len(tbl_dicts[k])):
                      #preparing javascript for columns
                      data_type = type_dict[k][j]
		      #
		      # this is hard code for sql identity (increment increase in sql server)
		      #
		      # in TABLE_SPEC.py
	              # ......
		      # 'TBL_INFO':{                     #1.2s
                      #   'ID_PREFIX':'sj', # this field is used for an index of using "insert" or "insert1" in html_multi_insert_pg_generator.py
		      _k_ = string.lower(k[1:])
		      if data_type == 'identity' and  _k_ in _TABLE_SPEC.keys():  
			        if "ID_PREFIX" in _TABLE_SPEC[_k_]["TBL_INFO"].keys():
                                             pg_info_dict['PY_INSERT_METHOD'] = 'insert1'


		      	
                      pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
                      pg_info_dict["DBCOLUMNS"] = DBColumn_dict[k][j]
                      pg_info_dict["COL_TYPES"] = type_dict[k][j]

                      pg_info_dict["CHARLEN"] = char_len_dict[k][j]
		      #zzzz
                      _k_ = string.lower(k[1:])
                      flds = string.lower(tbl_dicts[k][j])[3:]
                      getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC,data_type)
                      pg_info_dict = getDB()
		      #zzz
		      """
                      _db_dateformat= string.split(d_type_info_dict[k][j])
                      pg_info_dict["DATABASE"] = _db_dateformat[0]
                      pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
                      """
                      col = col + all_td_html["js_types"]%pg_info_dict
                
                pg_info_dict["JS_TYPES"] = col
		print "111111122222222", col


		col = ""
		for j in range(len(tbl_dicts[k])):
                      #preparing javascript for columns
                      data_type = type_dict[k][j]
		      pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]

		      
		      pg_info_dict["CHARLEN"] = char_len_dict[k][j]
		      #zzzz
                      _k_ = string.lower(k[1:])
                      flds = string.lower(tbl_dicts[k][j])[3:]
                      getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC, data_type)
                      pg_info_dict = getDB()
		      #zzz 
                      """
                      _db_dateformat= string.split(d_type_info_dict[k][j])
		      pg_info_dict["DATABASE"] = _db_dateformat[0]
		      pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
		      """
		      pg_info_dict["FIELD_NAME2"] = tbl_dicts[k][j][3:]  #cut off dbc-prefix such as dbcRecord_num
		      #pg_info_dict["FIELD_NAME2"] = tbl_dicts[k][j]  # no cut off dbc-prefix such as dbcRecord_num
                      if data_type not in pg_info_dict.keys():
                              #unknown type, using default type xText
			      pg_info_dict["DATA_TYPE_LIST"] = pg_info_dict["unknownType"]
                      else:
                              pg_info_dict["DATA_TYPE_LIST"] = pg_info_dict[data_type]
                      col = col + lp_td_html["js_columns"]%pg_info_dict
                
		pg_info_dict["JS_COLUMNS"] = col

                _needRank = len(tbl_dicts[k])-len(not_in_order_by_clause_dict[k])-order_by_clause_dict[k]
	        print "needRank ....", k	
		pg_info_dict["_myRank"] = range(_needRank+1)[1:]
		col = ""
		for j in range(len(tbl_dicts[k])):
                      #preparing javascript for columns
                      data_type = type_dict[k][j]
		      pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
		      pg_info_dict["DBCOLUMNS"] = DBColumn_dict[k][j]
		      if type_dict[k][j] == 'identity':
		              pg_info_dict["COL_TYPES"] = 'xInteger'
		      else:
		              pg_info_dict["COL_TYPES"] = type_dict[k][j]
			      
		      pg_info_dict["CHARLEN"] = char_len_dict[k][j]
		      #zzzz
                      _k_ = string.lower(k[1:])
                      flds = string.lower(tbl_dicts[k][j])[3:]
                      getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC,data_type)
                      pg_info_dict = getDB()
		      #zzz
		      """
                      _db_dateformat= string.split(d_type_info_dict[k][j])
		      pg_info_dict["DATABASE"] = _db_dateformat[0]
		      pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
		      """
                      col = col + lp_td_html["js_types"]%pg_info_dict
                
		pg_info_dict["JS_TYPES"] = col
                
                # recording how many table fields in a row for the search input pages.
                # we set up two table fields in a row currently.
                cols_in_a_row = 0  
		colsInRow = 3
                pg_info_dict["colSpan"] = colsInRow*3
	        strz = "<tr><td colspan=%(colSpan)s>&nbsp;</td></tr><tr>"%pg_info_dict
                #str = """<table style="FONT-SIZE: 10pt" cellSpacing=0 cellPadding=0 bgColor=#dee7ff border=0><TBODY><tr>"""
                for j in range(len(tbl_dicts[k])):
                           if cols_in_a_row == colsInRow:
                                   cols_in_a_row = 0
				   strz = strz + "</tr><tr><td colspan=%(colSpan)s>"%pg_info_dict
                                   strz = strz + """<TABLE cellSpacing=0 cellPadding=0  border=0 width=100%><TBODY><TR><TD  bgColor=#6386d6 height=1></TD> </TR></TBODY> </TABLE>  """
                                   strz = strz + """</td></tr><tr>"""
                           #preparing others like PG_MAINBODY
                           hh = hh + delta_hh
                           data_type = type_dict[k][j]
                           #data_type = type_dict[k][j]
                           pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
                           #
			   #
		           if tbl_dicts[k][j] !="dbcCreate_on" or tbl_dicts[k][j] !="dbcRowid":
                                    pg_info_dict["CHINESE_TITLE"] = chinese_title[k][j]
                           #pg_info_dict["CHINESE_TITLE"] = chinese_title[k][j]

			    
                           # this is for sql query lp page zzzz 20040722
                           lp_hidden_fields = lp_hidden_fields + "\n"+ lp_td_html["lp_hidden_fields"]%pg_info_dict
		      
		           if tbl_dicts[k][j] != "order_by_clause" and tbl_dicts[k][j] != "order_by_clause2":
                                    # zzzz 20040726
                                    pg_info_dict["xRank"]=""
                                    pg_info_dict["xASC"]=""

                                    if data_type not in lp_td_html.keys():
                                            #unknown type, using default type xText
                                            if cols_in_a_row ==1:
                                                   strz = strz + "<td>&nbsp;&nbsp;</td>" + lp_td_html["xText"]%pg_info_dict
                                            else:
                                                   strz = strz + "<td>&nbsp;&nbsp;</td>"+lp_td_html["xText"]%pg_info_dict
                                            cols_in_a_row = cols_in_a_row + 1
                                    else:
                                            if cols_in_a_row ==1:
                                                   strz = strz + "<td>&nbsp;&nbsp;</td>" + lp_td_html[data_type]%pg_info_dict
                                            else:
                                                   strz = strz +"<td>&nbsp;&nbsp;</td>"+ lp_td_html[data_type]%pg_info_dict
                                            cols_in_a_row = cols_in_a_row + 1

		pg_info_dict["H_PIXEL"] = height_pixel + hh
                if cols_in_a_row != colsInRow:
                       #pg_info_dict['TEMP'] = """ <TD vAlign=center align=right bgColor=#dee7ff color="#000000"><IMG style="CURSOR: hand" onclick="doQuerySelect('%(PG_ALIASES)s', '%(RP_PG)s', document.forms[0], d_type)" src="{{XBOP_WWW_ROOT}}/graphics/oa_images/button/find.gif" border=0 name=btnAct></TD> """ 
                       #str = str + pg_info_dict['TEMP']%pg_info_dict 
                       strz = strz + "</tr>"
                if cols_in_a_row == colsInRow:
                       strz = strz + "</tr><tr><td colspan=%(colSpan)s>"%pg_info_dict
                       pg_info_dict['TEMP'] = """ <TABLE cellSpacing=0 cellPadding=0 border=0 >
		       <TBODY><TR> <TD vAlign=center align=right width=50%% bgColor=#dee7ff 
	  color="#000000"><IMG style="CURSOR: hand" onclick="doQuerySelect('%(PG_ALIASES)s', '%(RP_PG)s', document.forms[0], d_type)" 
	  src="{{XBOP_WWW_ROOT}}/graphics/oa_images/button/find.gif" border=0 name=btnAct></TD></TR></TBODY></TABLE></td></tr>
	               """
		       # Don't need this. This is for query.
		       #
                       ##str = str + pg_info_dict['TEMP']%pg_info_dict
		       #
                         
                strz = strz + "<tr><td colspan=%(colSpan)s>"%pg_info_dict
		strz = strz + """<TABLE cellSpacing=0 cellPadding=0  border=0 > <TBODY> <TR> <TD  bgColor=#6386d6 height=1></TD></TR></TBODY></TABLE></td></tr>"""
                pg_info_dict["PG_MAINBODY"] = strz 
                pg_info_dict["LP_HIDDEN_FIELDS"] = lp_hidden_fields


                ##############################################################################################
		#preparing editing area (for one row only)
                strz = ""
                str1 = ""
                ii = 0
		is_div_4_date_time_inserted = 0
                #str = str + all_td_html["div_4_date_time"]
                call_Attributes_str = ""
                dropMenuStr = ""
                sub_dropMenuStr = ""
                pg_info_dict["CALL_ATTRIBUTES_DICT"]="" 
                pg_aliases_def2 = {}
                ref_tbl_field = {}
                local_chect_btn_dict= {}
                #############################################
		#
                # this is for get_info_from_other_table()
		#
		v_search_str = ""
	        v_search_index = 0
                sub_menu_dict = {}
                ##############################################
                for j in range(len(tbl_dicts[k])):
                            pg_info_dict["_MY_FUNCTION"] = []
                            #self.pg_info_dict["MY_FUNCTION"] = ""
			    #
			    #
		            if tbl_dicts[k][j] !="dbcCreate_on" or tbl_dicts[k][j] !="dbcRowid":
                                    pg_info_dict["CHINESE_TITLE"] = chinese_title[k][j]
                            #pg_info_dict["CHINESE_TITLE"] = chinese_title[k][j]
                            #
			    pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
                            pg_info_dict["FIELD_NAME0"] = tbl_dicts[k][j]+"0"
                            
                            pg_info_dict["CHARLEN"] = char_len_dict[k][j]
		            #zzzz
			    _k_ = string.lower(k[1:])
			    flds = string.lower(tbl_dicts[k][j])[3:]
                            data_type = type_dict[k][j]
                            getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC,data_type)
			    pg_info_dict = getDB()
		            #zzz
			    """
                            _db_dateformat= string.split(d_type_info_dict[k][j])
                            pg_info_dict["DATABASE"] = _db_dateformat[0]
                            pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
			    """
			    #
                            # Initialize pg_info_dict 
			    #
			    pg_info_dict["DATE_PICKER"] = ""
                            # summation javascript .... 
                            pg_info_dict["JS_SUM_CALL"] = ""
			    
			    #
                            # function ...?
			    #
			    cur_field_name = pg_info_dict["PG_ALIASES"] + "." + tbl_dicts[k][j]+"[0]"
                            for keys in call_func.keys():
                                      if string.strip(cur_field_name) in call_func[keys]:
                                                  pg_info_dict["_MY_FUNCTION"].append(" %s();"%keys)
    
                            pg_info_dict["MY_FUNCTION"] = ' '.join(pg_info_dict["_MY_FUNCTION"])
                            #
                            # prepare next cursor field?
			    #
                            #print "22 no curso fields ", k,j,  no_cursor_flds, tbl_dicts[k][j]
                            if j < len(tbl_dicts[k])-1:
                                 pg_info_dict["FIELD_NAME2_1"] = tbl_dicts[k][j+1]+"2"
				 jj = j+1
				 while 1:
                                       if tbl_dicts[k][jj] in no_cursor_flds:
                                              if jj == len(tbl_dicts[k])-1: 
						      jj =0
					      else:
                                                      jj += 1
                                       else:
					      break
                                 pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][jj]
                            else:
                                 pg_info_dict["FIELD_NAME2_1"] = tbl_dicts[k][0]+"2"
				 jj = 0
				 while 1:
                                       if tbl_dicts[k][jj] in no_cursor_flds:
                                                      jj += 1
                                       else:
					      break
                                 pg_info_dict["FIELD_NAME_1"] = tbl_dicts[k][jj]
                            
			    #
			    # what is the data_type?
			    #
			    data_type = type_dict[k][j]
			    

                                    
                            if data_type in ["xDateTime", "oraDateTime", "gfDateTime", "xDate"]:
		                    if is_div_4_date_time_inserted == 0:
                                               #pg_info_dict["DATE_PICKER"] = all_td_html["div_4_date_time"] + all_td_html["date_time"]%pg_info_dict
                                               pg_info_dict["DATE_PICKER"] = """ondblclick= "scwShow(this,this);" """ 
		                               is_div_4_date_time_inserted += 1
                                    else:
                                               #pg_info_dict["DATE_PICKER"] = all_td_html["date_time"]%pg_info_dict
                                               pg_info_dict["DATE_PICKER"] = """ondblclick= "scwShow(this,this);" """ 
                           
			    
                            pg_info_dict["GET_SUB_DROPDOWN"]=""
                            pg_info_dict["SESSION_STR"]=""
			    pg_info_dict["get_info_from_other_table"]=""
			    pg_info_dict["get_info_from_other_table_v2"]=""
                            pg_info_dict["display_2_in_1_search_link_for_img"] = ""
			    # I want hidden two fields here: 
			    #      one is "identity" field and the other is create_on field.
			    #
			    #if data_type != "identity":
			    if data_type == "identity" or tbl_dicts[k][j] =="dbcCreate_on" or tbl_dicts[k][j] =="dbcRowid":
                                    pg_info_dict["FLD2_BEHIND_FLD1_STR"] = "" 
				    pg_info_dict["DROP_DOWN"]=all_td_html["normal_cell_hidden"]%pg_info_dict
                            else:
                                    pg_info_dict["FLD2_BEHIND_FLD1_STR"] = "" 
                                    # some fields may need to be initialized.
				    # For example, "pname" field can be initialized with
                                    # "session.user.firstName". 
                                    pg_info_dict["pg_aliases_field_name0"] = all_td_html["pg_aliases_field_name0"]%pg_info_dict
				    pg_info_dict["DROP_DOWN"]=all_td_html["normal_cell"]%pg_info_dict
		                   
                                    # this part was commented out temporily
                                    _k_ = string.lower(k[1:])
		                    if _k_ in _TABLE_SPEC.keys():
			                     if "INITIALIZE" in _TABLE_SPEC[_k_]["TBL_INFO"].keys():
						     for key in _TABLE_SPEC[_k_]["TBL_INFO"]['INITIALIZE'].keys():
				                              dbc_field = "dbc"+string.capitalize(key)
							      if tbl_dicts[k][j] == dbc_field:
                                                                     pg_info_dict["pg_aliases_field_name0"] = _TABLE_SPEC[_k_]["TBL_INFO"]['INITIALIZE'][key]
				                                     pg_info_dict["DROP_DOWN"]=all_td_html["normal_cell"]%pg_info_dict
                                             # in _TABLE_SPEC.py
					     #'GET_INFO_FROM_OTHER_TBL':{'OTHER_TBL':'user_info','FIELDS_RELATIONS':{'course_id':'userID','teacher_name':'pname'},'FLD2_BEHIND_FLD1':{'class':'gender','weekday':'birthday'}},
					     #
			                     if "GET_INFO_FROM_OTHER_TBL" in _TABLE_SPEC[_k_]["TBL_INFO"].keys():
                                                 my_prj_dir = wizard_conf.my_prj_dir
						 other_tbl = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['OTHER_TBL']
						 current_field = string.lower(tbl_dicts[k][j][3:]) # tbl_dicts[k][j] ==> such as "dbcCreate_on"
						 if current_field in _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['FIELDS_RELATIONS'].keys():
			                               other_tbl = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['OTHER_TBL']
                                                       search_str_field = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['SEARCH_FIELD']
                                                       other_field0 = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['FIELDS_RELATIONS'][search_str_field]
                                                       #v2_search = ",%s.m%s.dbo%s.search"%(my_prj_dir,string.capitalize(other_tbl),string.capitalize(other_tbl))
						       other_field = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['FIELDS_RELATIONS'][current_field]
						       other_obj =  "%s.m%s.dbo%s"%(my_prj_dir,string.capitalize(other_tbl),string.capitalize(other_tbl))
						       if current_field != search_str_field:
						            pg_info_dict["pg_aliases_field_name0"] = other_obj+".dbc%s[0]"%(string.capitalize(other_field))
                                                       else:
                                                            #%(PG_ALIASES)s.%(FIELD_NAME)s[0]
							    PG_ALIASES = "$"+k
							    pg_info_dict["get_info_from_other_table"] = ";get_info_from_other_table('%s', '%s','%s.dbc%s[0]','%s')"%(PG_ALIASES,other_obj,PG_ALIASES, string.capitalize(current_field), other_field0)
							    pg_info_dict["get_info_from_other_table_v2"] = "get_info_from_other_table(\\'%s\\', \\'%s\\',\\'%s.dbc%s[0]\\',\\'%s\\')"%(PG_ALIASES,other_obj,PG_ALIASES, string.capitalize(current_field), other_field0)
                                                            pg_info_dict["display_2_in_1_search_link_for_img"]=all_td_html["display_2_in_1_search_link_for_img"]%pg_info_dict							    
				                       pg_info_dict["DROP_DOWN"]=all_td_html["normal_cell"]%pg_info_dict
						 
						 if current_field in _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['FLD2_BEHIND_FLD1'].keys():
						       other_field = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['FLD2_BEHIND_FLD1'][current_field]
                                                       pg_info_dict["FLD2_BEHIND_FLD1_STR"] = "{{%s.m%s.dbo%s.dbc%s[0]}}"%(my_prj_dir,string.capitalize(other_tbl),string.capitalize(other_tbl),string.capitalize(other_field)) 
				                       pg_info_dict["DROP_DOWN"]=all_td_html["normal_cell"]%pg_info_dict
                                                     
			    
                            if summation_dict[k][0] != 'none':
                                     # preparing summation javascript
                                     for ik in range(len(summation_dict[k])):
                                          mytmp = string.split(summation_dict[k][ik],"/")
                                          #mytmp[0] field1  say amount used
                                          #mytmp[1] field2  say unit price
                                          #mytmp[2] field3  for summation
                                          if mytmp[0]==string.lower(tbl_dicts[k][j][3:]) or mytmp[1]==string.lower(tbl_dicts[k][j][3:]):
                                                  oops= "dbc" + string.capitalize(mytmp[0])
                                                  pg_info_dict["SUM_FIELD1"] = oops 
                                                  oops= "dbc" + string.capitalize(mytmp[1])
                                                  pg_info_dict["SUM_FIELD2"] = oops 
                                                  oops= "dbc" + string.capitalize(mytmp[2])
                                                  pg_info_dict["SUM_FIELD3"] = oops
                                                  pg_info_dict["JS_SUM_CALL"] = all_td_html["sum_field"]%pg_info_dict
                                                  pg_info_dict["DROP_DOWN"]=all_td_html["normal_cell_summationCK"]%pg_info_dict
                                                  
   
  
                            # IF THIS K TABLE HAS _drop_down DEFINITION,
			    # we are in the loop of K TABLE FIELDS 
                            if drop_down_dict[k] != 'none':
				 print "=====>ddddmmmm 表:",k
			         #
				 # EXAMPLE:
				 #_drop_down periods/dboDrop_menu2/field_value/field_name='periods'  weekday/dboDrop_menu1/field_value/field_name='weekday' dept/sub_drop_menu/field_value/field_name='nothing9999' college/drop_menu/field_value/field_name='college' 
                                 #
                                 # preparing drop_down list, LOOP ON ALL drop_down DEFINITIONS
                                 for ik in range(len(drop_down_dict[k])):
					       mytmp = string.split(drop_down_dict[k][ik],"/")
					       #mytmp[0] fields in the current table : "periods", "weekday", "dept", "college"
                                               #mytmp[1] referenced tables
                                               #mytmp[2] field ins the referenced table
                                               #mytmp[3] searchStrings for the referenced table
					       isQuery = 0
					       if k.find('_query')>-1:
						  isQuery = 1
                                               if mytmp[0]==string.lower(tbl_dicts[k][j][3:]) or (k.find('_query')>-1 and mytmp[0]==string.lower(tbl_dicts[k][j])):
                                                         tmp3 = tmp[:]    # for drop_down reference table's field
                                                         if mytmp[1][:3] == "dbo":
                                                            try:
                                                               tmp3.append(pyfile_dict['o'+string.capitalize(mytmp[1][3:-1])])
                                                            except:
                                                               tmp3.append(pyfile_dict['o'+string.capitalize(mytmp[1][3:-2])])
                                                            tmp3.append(mytmp[1])
                                                         else:
                                                            tmp3.append(pyfile_dict['o'+string.capitalize(mytmp[1])])
                                                            tmp3.append("dbo" + string.capitalize(mytmp[1]))
                                                         pg_aliases_def2[ik]=string.join(tmp3[aaa:],".")

							 #if isQuery==1:
							 #  ref_tbl_field[ik] = mytmp[2]
							 #else:
							 ref_tbl_field[ik] = "dbc"+string.capitalize(mytmp[2])
                                                         #self.pg_info_dict["CALL_OBJECT"]=self.pg_info_dict["PG_ALIASES_DEF2"]
                                                         pg_info_dict["CALL_OBJECT"]=pg_aliases_def2[ik]
                                                         pg_info_dict["CALL_ATTRIBUTES_DICT"]={"search":{"searchString":mytmp[3]}} 
						         # bug 11111 here... remove the sub_menus out of attributes 
							 # 准备子菜单 part 1
							 try:
							      subValues = _TABLE_SPEC[_k_]["TBL_INFO"]["DROP_DOWN_RELATION"].values()
                                                              # 一个网页，多层相关联子菜单只能一个.
							      # 所以,第一个是总是主菜单
                                                              abc = 0
							      for kji in range(len(subValues)):
								  if mytmp[1] == subValues[kji][0]:
								      abc = 1
							      if abc == 0:		      
                                                                  call_Attributes_str += all_td_html["call_Attributes"]%pg_info_dict
							 except:
                                                                 call_Attributes_str += all_td_html["call_Attributes"]%pg_info_dict
								 pass

                                                         pg_info_dict["drop_down_list"] = "drop_down_list" + "%i"%ik 
                                                         pg_info_dict["_WHICH_"] = ik
							 
							 dropMenuStr += all_td_html['dropMenuStr']%pg_info_dict
							 # 准备子菜单 part 2
							 try:
                                                             #'DROP_DOWN_RELATION':{'drop_menu':['sub_drop_menu','field_name','kkkkk'],'sub_drop_menu':['dboUser_info','userID','xxxxx'],'dboUser_info':['dboComputer_info','computer_id','yyyyy']},  # kkkk/drop_menu==xxxxx/sub_drop_menu===yyyyy/dboSub_drop_menu  ====> table_field/table_instance
							     subObj = _TABLE_SPEC[_k_]["TBL_INFO"]["DROP_DOWN_RELATION"][string.strip(mytmp[1])]
							     sub_menu_dict = _TABLE_SPEC[_k_]["TBL_INFO"]["DROP_DOWN_RELATION"]
							     # subObj[0] ==> 子表名  (子菜单)
							     # subObj[1] ==> 字段名  (子表单)
							     # mytmp[1]  ==> 主表名  (主菜单) 
							     # mytmp[0]  ==> 字段名2 (主表)  该字段的值由子菜单提供
							     # subObj[2] ==> 字段名1 (主表)
                                                             my_prj_dir = wizard_conf.my_prj_dir
							     try:
								   #if subObj[0][:3] == "dbo":
								   # bug 222222 here subObj[0][3:-1]
								   endNum = string.atoi(subObj[0][-1])
								   capObj = string.capitalize(subObj[0][3:-1])
								   subObj_tbl = "%s.m%s.%s"%(my_prj_dir,capObj,subObj[0])
							     except:
							           subObj_tbl = "%s.m%s.dbo%s"%(my_prj_dir,string.capitalize(subObj[0]),string.capitalize(subObj[0]))
							     
                                                             xxxxx = """\
var  v%(v_search_index)s = getElementValue(document.forms[0]["%(SELECTED_VALUE)s"])
setElementValue(document.forms[0]["%(SUB_DROP_MENU_SEARCH)s.searchString"],"field_name='"+v%(v_search_index)s+"'")
if (v%(v_search_index)s.length > 0) v_search = v_search + ",%(SUB_DROP_MENU_SEARCH)s.search"
                                                             """
							     pg_info_dict["SELECTED_VALUE"]="$o%s.dbc%s[0]"%(string.capitalize(_k_),string.capitalize(subObj[2]))
							     pg_info_dict["SUB_DROP_MENU_SEARCH"]=subObj_tbl

                                                             v_search_index = v_search_index + 1
							     pg_info_dict["v_search_index"] = v_search_index
							     v_search_str = v_search_str + xxxxx%pg_info_dict
							     subObj_fld = subObj[1]
							     baseObj = "$o%s"%string.capitalize(_k_)
							     abcdefg = "getSubMenu('%s', '%s', local_drop_down%s[options.selectedIndex-1], '%s')"%(baseObj, subObj_tbl, ik, subObj_fld) 
                                                             pg_info_dict["GET_SUB_DROPDOWN"]=abcdefg
                                                         except:
                                                             # this is for non-subDropDownMenu
                                                             #call_Attributes_str += all_td_html["call_Attributes"]%pg_info_dict
                                                             pass
							 
						         pg_info_dict["SESSION_STR"]="""var kkk = "{{$o%s.dbc%s[0]}}" """%(string.capitalize(_k_), string.capitalize(mytmp[0]))
							 for kkk in sub_menu_dict.keys():
							   if mytmp[1] == sub_menu_dict[kkk][0]:
							      pg_info_dict["SESSION_STR"]="""var kkk = "{{session.cache.dbc%s[0]}}" """%(string.capitalize(mytmp[0]))
							 pg_info_dict["DROP_DOWN"]=all_td_html["drop_down"]%pg_info_dict
	                                                 
							 # ZZZZZ preparing drop_down for queries. 20091128
							 if isQuery==1:
						           pg_info_dict["SESSION_STR"]="""var kkk = dropDownList[which][0]"""
							   HTML_MULTI_pg_dict[k]["DROP_DOWN"]=all_td_html["query_drop_down"]%pg_info_dict
		                                         
                            
			    if chect_btn_dict[k] != 'none':
                                 for ik in range(len(chect_btn_dict[k])):
                                               mytmp = string.split(chect_btn_dict[k][ik],"/")
                                               #mytmp[0] field in the current table
                                               #mytmp[1] value1
                                               #mytmp[2] value2
                                               #mytmp[3] value3
                                               if mytmp[0]==string.lower(tbl_dicts[k][j][3:]):
                                                         pg_info_dict["VALUE1"]=mytmp[1]
                                                         pg_info_dict["VALUE2"]=mytmp[2]
                                                         if len(mytmp) > 3:
                                                              pg_info_dict["VALUE3"]=mytmp[3]
                                                              pg_info_dict["DROP_DOWN"]=all_td_html["check_btn3"]%pg_info_dict
                                                         else:
                                                              pg_info_dict["DROP_DOWN"]=all_td_html["check_btn2"]%pg_info_dict
              
	                    #
			    # for identity-related fields: type = hidden 
			    #
		            _k_ = string.lower(k[1:])
                            if data_type == "identity" or tbl_dicts[k][j] =="dbcCreate_on" or tbl_dicts[k][j] =="dbcRowid":
                                   strz = strz + all_td_html["display_2_in_1_hidden"]%pg_info_dict
                            else:
		               #######################################################
		               _k_ = string.lower(k[1:])
		               try:
                                      flds = string.lower(tbl_dicts[k][j])[3:]
				      if flds in  _TABLE_SPEC[_k_]["TBL_INFO"]["UPLOAD_FIELD"]:
				           pg_info_dict['WHICH_WINDOW'] = 'upload'
                                           strz = strz + all_td_html["display_2_in_1_link"]%pg_info_dict
                                      else:
                                        if long(char_len_dict[k][j])==0 and data_type == 'xText':
                                               pg_info_dict["WHICH_WINDOW"] = 'pop_up_input'
                                               strz = strz + all_td_html["display_2_in_1_link"]%pg_info_dict
				        else:
                                           if long(char_len_dict[k][j])<=100:
                                                temp99 = all_td_html["display_2_in_1"]%pg_info_dict
                                                #'GET_INFO_FROM_OTHER_TBL':{'OTHER_TBL':'user_info','FIELDS_RELATIONS':{'course_id'
					        try:
					           link_field = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['SEARCH_FIELD']
					           current_field = string.lower(tbl_dicts[k][j][3:])
					   
                                                   if current_field == link_field:
                                                         temp99 = all_td_html["display_2_in_1_search_link"]%pg_info_dict
					        except:
                                                     pass
				                strz = strz + temp99
				           else:
                                                pg_info_dict["WHICH_WINDOW"] = 'pop_up_input'
                                                strz = strz + all_td_html["display_2_in_1_link"]%pg_info_dict
		               except:
                               #####################################################
                                 if long(char_len_dict[k][j])==0 and data_type == 'xText':
                                        pg_info_dict["WHICH_WINDOW"] = 'pop_up_input'
                                        strz = strz + all_td_html["display_2_in_1_link"]%pg_info_dict
                                 else:  
                                   if long(char_len_dict[k][j])<=100:
                                        temp99 = all_td_html["display_2_in_1"]%pg_info_dict
                                        #'GET_INFO_FROM_OTHER_TBL':{'OTHER_TBL':'user_info','FIELDS_RELATIONS':{'course_id'
					try:
					   link_field = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['SEARCH_FIELD']
					   current_field = string.lower(tbl_dicts[k][j][3:])
					   
                                           if current_field == link_field:
                                                 temp99 = all_td_html["display_2_in_1_search_link"]%pg_info_dict
					except:
                                             pass
				        strz = strz + temp99
				   else:
                                       pg_info_dict["WHICH_WINDOW"] = 'pop_up_input'
                                       strz = strz + all_td_html["display_2_in_1_link"]%pg_info_dict
	                    			    

			    if data_type != 'identity': ii = ii + 1

                            if ii == 3 or j == len(tbl_dicts[k])-1:
                                   ii = 0
                                   str1 = str1 + "<tr> " + strz + " </tr>"
                                   strz = ""

                                    
                #pg_info_dict["PG_MAINBODY"] = str1
                pg_info_dict["DISPLAY_2_IN_1"] = str1
               
                pg_info_dict["CALL_ATTRIBUTES"]= call_Attributes_str
		print "------>Jeffery:",call_Attributes_str
                pg_info_dict["DROPDOWN_MENU_SEARCHSTRING"] = dropMenuStr

                pg_info_dict["CALLATTRIBUTES"]= all_td_html["callAttributes"]%pg_info_dict
		#print "pg_info_dict[CALLATTRIBUTES] ", pg_info_dict["CALLATTRIBUTES"], k 
                
                dd_list_str = ""
                for kkey in pg_aliases_def2.keys():
                         pg_info_dict["PG_ALIASES_DEF2"] = pg_aliases_def2[kkey]
                         pg_info_dict["REF_TBL_FIELD"] = ref_tbl_field[kkey]
                         pg_info_dict["_WHICH_"] = kkey
                         #self.pg_info_dict["drop_down_list"] = "drop_down_list" + "%i"%kkey 
                         dd_list_str = dd_list_str + all_td_html["drop_down_list"]%pg_info_dict
                pg_info_dict["DROP_DOWN_LIST"] = dd_list_str



                strz = ""
                pg_info_dict["WHICH_ROW"] = search_length
                for j in range(len(tbl_dicts[k])):
                           pg_info_dict["CHARLEN"] = char_len_dict[k][j]
		           #zzzz
			   _k_ = string.lower(k[1:])
			   flds = string.lower(tbl_dicts[k][j])[3:]
			   data_type = type_dict[k][j]
                           getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC,data_type)
			   pg_info_dict = getDB()
		           #zzz 
			   """
                           _db_dateformat= string.split(d_type_info_dict[k][j])
                           pg_info_dict["DATABASE"] = _db_dateformat[0]
                           pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
                           """
                           pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
                           strz = strz + all_td_html["hidden_row"]%pg_info_dict
                pg_info_dict["HIDDEN_ROW"] = strz


		pg_info_dict["identity_ck_js"] = ""
		pg_info_dict["identity_js_function"] = ""
	        pg_info_dict["print_receipt_button"] = ""
		pg_info_dict["identity_hidden_input_fields"] = ""
		pg_info_dict["identity_aliases"] = ""
		pg_info_dict["identity_genOrderId"] = "" 
		pg_info_dict["identity_create_on"] = "" 
		#
                #pg_info_dict["PG_ALIASES_DEF"] = string.join(tmp1[aaa:],".")
		#
		# trying to get 'a.b.c' out of 'a.b.c.d.e'
		#
		junk1 = string.split(pg_info_dict["PG_ALIASES_DEF"],'.')
		pg_info_dict["identity_aliases_head"] = string.join(junk1[:-2],'.')
		
		#
		# k ==> oRegister but we just need: register.
		#
		_k_ = string.lower(k[1:])
		if _k_ in _TABLE_SPEC.keys():
			if "IDENTITY_FIELD" in _TABLE_SPEC[_k_]["TBL_INFO"].keys():
		                pg_info_dict["ID_PREFIX"]= _TABLE_SPEC[_k_]["TBL_INFO"]["ID_PREFIX"]
				pg_info_dict["DBIdentity_dbc_field"]         = "dbc"+string.capitalize(_TABLE_SPEC[_k_]["TBL_INFO"]["IDENTITY_FIELD"])
		                pg_info_dict["identity_ck_js"]               = all_td_html["identity_ck_js"]%pg_info_dict
		                pg_info_dict["identity_js_function"]         = all_td_html["identity_js_function"]%pg_info_dict
		                pg_info_dict["identity_hidden_input_fields"] = all_td_html["identity_hidden_input_fields"]%pg_info_dict
		                pg_info_dict["identity_aliases"]             = all_td_html["identity_aliases"]%pg_info_dict
		                pg_info_dict["identity_genOrderId"]          = all_td_html["identity_genOrderId"]%pg_info_dict 
			if _TABLE_SPEC[_k_]["TBL_INFO"]['IDENTITY_FIELD'] == 'create_on': # so, 'create_on' field is required ?
		                #pg_info_dict["identity_genOrderId"]          = all_td_html["identity_create_on"]%pg_info_dict
				# 
				# do not need to call this function at on_load.
		                pg_info_dict["identity_genOrderId"]          = "" 
			if "RECEIPT_PRN_BTN" in _TABLE_SPEC[_k_]["TBL_INFO"].keys():
				if _TABLE_SPEC[_k_]["TBL_INFO"]["RECEIPT_PRN_BTN"] == 'yes':
				                  pg_info_dict["print_receipt_button"]         = all_td_html["print_receipt_button"]%pg_info_dict	
                        #<input type=hidden name="computer_lab.mUser_info.dboUser_info.searchString" value="">
   
                        pg_info_dict["SUB_DROPDOWN_MENU_SEARCHSTRING"] = ""
                        pg_info_dict["SUB_CALL_OBJECT"] = ""
			if "GET_INFO_FROM_OTHER_TBL" in _TABLE_SPEC[_k_]["TBL_INFO"].keys():
                              my_prj_dir = wizard_conf.my_prj_dir
			      other_tbl = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['OTHER_TBL']
                              pg_info_dict["SUB_CALL_OBJECT"] = "%s.m%s.dbo%s"%(my_prj_dir,string.capitalize(other_tbl),string.capitalize(other_tbl))
                              pg_info_dict["DROP_DOWN_SEARCH_PG"] = aaa1 + "/" + "lp_mr_"+ "o%s"%string.capitalize(other_tbl) + ".html"
			      sub_dropMenuStr = all_td_html['sub_dropMenuStr']%pg_info_dict
                              search_str_field = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['SEARCH_FIELD']
                              pg_info_dict["other_field0"] = _TABLE_SPEC[_k_]["TBL_INFO"]['GET_INFO_FROM_OTHER_TBL']['FIELDS_RELATIONS'][search_str_field]
                              pg_info_dict["v2_search"] = ",%s.m%s.dbo%s.search"%(my_prj_dir,string.capitalize(other_tbl),string.capitalize(other_tbl))
                              pg_info_dict["v2_obj"] = "%s.m%s.dbo%s"%(my_prj_dir,string.capitalize(other_tbl),string.capitalize(other_tbl))
                              pg_info_dict["v2"] = "$o%s.dbc%s[0]"%(string.capitalize(_k_),string.capitalize(search_str_field))
                              pg_info_dict["getSubMenuStr0"] = all_td_html["getSubMenuStr1"]
                        else:
                              pg_info_dict["getSubMenuStr0"] = all_td_html["getSubMenuStr2"]
                              pass
			
			try:
			    subObj = _TABLE_SPEC[_k_]["TBL_INFO"]["DROP_DOWN_RELATION"]
			    pg_info_dict['V_SEARCH'] = v_search_str
                        except:
			    pg_info_dict['V_SEARCH'] = "" 
				
		###########################################################################################
                pg_info_dict["SUB_DROPDOWN_MENU_SEARCHSTRING"] = sub_dropMenuStr


                pg_info_dict["page_title_image"] = all_td_html["page_title_image"]%pg_info_dict
                pg_info_dict["page_buttons"] = all_td_html["page_buttons"]%pg_info_dict
                pg_info_dict["page_update_button"] = ""
		pg_info_dict["page_title"] = "" 
                pg_info_dict["DISABLE_INPUT"] = ""
		pg_info_dict["WHICH_FRAME_AREA"] = 'frameArea'
		pg_info_dict["enableInput"] = ''
                pg_info_dict["getSubMenuStr"] = pg_info_dict["getSubMenuStr0"]%pg_info_dict
                pg_info_dict["EXCEL_PRT"]=""
                if "EXCEL_RPT1" in _TABLE_SPEC[_k_]["TBL_INFO"].keys():
		      if string.lower(_TABLE_SPEC[_k_]["TBL_INFO"]["EXCEL_RPT1"]) == "yes":
                          pg_info_dict["EXCEL_PRT"]="""\
<table align=center>
<tr >
<TD vAlign=center  bgColor=#dee7ff color="#000000">
【<a class="menu_linked_name" href="javascript:ckAll('%(PG_ALIASES)s', '%(RP_PG)s', document.forms[0], 'frameList','prn_excel_sheet0')">报表浏览</a>】
【<a class="menu_linked_name" href="javascript:ckAll('%(PG_ALIASES)s', '%(RP_PG)s', document.forms[0], 'frameList','prn_excel_sheet1')">生成报表</a>】</TD>
</tr>
</table>
                """
                          pg_info_dict["EXCEL_PRT"]=pg_info_dict["EXCEL_PRT"]%pg_info_dict
                pg_info_dict["TOOLBAR_depreciated"]="""\
var aToolBar=new dhtmlXToolbarObject(document.getElementById('toolbar_zone'),'100%%',16,"");
aToolBar.setOnClickHandler(onButtonClick);
aToolBar.loadXML("{{XBOP_WWW_ROOT}}/jslib_wh/toolbar01.xml")
aToolBar.showBar();
                """
                pg_info_dict["TOOLBAR"]="""\
var toolbar = new dhtmlXToolbarObject("toolbar_zone");
toolbar.setIconsPath("{{XBOP_WWW_ROOT}}/graphics/toolbar_images/");
toolbar.loadXML("{{XBOP_WWW_ROOT}}/jslib_wh/dhxtoolbar_button.xml?etc=" + new Date().getTime(), updateList);
toolbar.attachEvent("onClick", function(id){   
        onButtonClick(id)	
    });
/*****
function getId() {
    var id = sel.options[sel.selectedIndex].value;
    return id;
}
function setText(text) {
    toolbar.setItemText(getId(), document.getElementById("txt").value);
}
function getText() {
    alert(toolbar.getItemText(getId()));
}
****/
function updateList() {
    sel.options.length = 0;
    toolbar.forEachItem(function(itemId) {
        if (toolbar.getType(itemId) == "button") {
            sel.options.add(new Option(itemId, itemId));
        }
    });
}
		"""
                fff = html_dir + "\\" + pyfile_dict[k] + "\\" + "lp_insert_" + k + ".html"
                f = open(fff, 'w')
		pg_info_dict["jslib_dir"]=jslib_dir
                f.write(all_td_html["all_tmpl"]%pg_info_dict)
                f.close()
                
                # rp_edit_xxxxx.html page is used for single record editing
                pg_info_dict["TOOLBAR"]=""
		pg_info_dict["EXCEL_PRT"]=""
                
		pg_info_dict["page_title_image"] = all_td_html["page_title_image"]%pg_info_dict
                pg_info_dict["page_buttons"] = ""
		pg_info_dict["page_update_button"] = all_td_html["page_update_button"]%pg_info_dict
		pg_info_dict["page_title"] = all_td_html["page_title"]%pg_info_dict
                pg_info_dict["DISABLE_INPUT"] = "disableInput();"
		pg_info_dict["WHICH_FRAME_AREA"] = '_self'
		pg_info_dict["enableInput"] = 'enableInput();'
                pg_info_dict["getSubMenuStr"] = pg_info_dict["getSubMenuStr0"]%pg_info_dict
		
		fff = html_dir + "\\" + pyfile_dict[k] + "\\" + "rp_edit_" + k + ".html"
                f = open(fff, 'w')
                f.write(all_td_html["all_tmpl"]%pg_info_dict)
                f.close()

		#cc = pg_info_dick.copy()
		dc = deepcopy(pg_info_dict)
		HTML_MULTI_pg_dict[k]['pg_info_dict'] = dc
        
	# Save web page template from "all_td_html" dictionary
	HTML_MULTI_pg_dict["all_td_html"] = all_td_html
	file = open("HTML_MULTI_pg_dict.pck", "w") # write mode
        pickle.dump(HTML_MULTI_pg_dict, file)

        print "Written to disk. Deleting 'HTML_MULTI_pg_dict' now."
        del HTML_MULTI_pg_dict
        file.close()
        del file




def gen_rp_pg():
        tmp = string.split(prj_dir,"\\")
        aaa = tmp.index("scripts")+1
        primary_keys = ["DBPrimaryKey","DBCompositeKey","DBUnique", "DBIdentity"]
        pg_info_dict = pg_info_dict1	
        for k in tbl_dicts.keys():
                SW_primary_keys = []
                SO_primary_keys = []
                str = ""
                tmp1 = tmp[:]    #this is differet from "tmp1 = tmp" which uses same chunk of memory.
                tmp2 = tmp[:]    #this is differet from "tmp2 = tmp" which uses same chunk of memory.
                tmp1.append(pyfile_dict[k])
                tmp2.append(pyfile_dict[k])
                tmp1.append("db" + k)
                #tmp1.append(k)
                pg_info_dict["PG_ALIASES_DEF"] = string.join(tmp1[aaa:],".")
                pg_info_dict["PG_ALIASES"] = "$"+k 
                aaa1 = string.join(tmp2[aaa:],"/")
                pg_info_dict["LP_PG"] = aaa1 + "/" + "lp_insert_" + k + ".html"
                pg_info_dict["ONE_RECORD_PG"] = aaa1 + "/" + "rp_sr_" + k + ".html"
                pg_info_dict["SEARCH_RP_PG"] = aaa1 + "/" + "rp_search_"+k+".html"
                pg_info_dict["EDIT_RP_PG"] = aaa1 + "/" + "rp_edit_"+ k + ".html"
                #pg_info_dict["EDIT_RP_PG"] = aaa1 + "/" + "lp_insert_"+ k + ".html"
                pg_info_dict["DELETE_RP_PG"] = aaa1 + "/" + "rp_delete_"+ k + ".html"
                pg_info_dict["PG_SCH_LEN"] = search_length
                #pg_info_dict["TD_PERCENT"] = "%d%%"%(100.0/(len(tbl_dicts[k])+2))
                #pg_info_dict["TD_PERCENT"] = "200"
	        pg_info_dict["DATABASE0"] = database0
		pg_info_dict["DATEFORMAT0"] = dateformat0
	        pg_info_dict["DATABASE"] = database0
		pg_info_dict["DATEFORMAT"] = dateformat0
		
		pg_info_dict["CELL_LENGTH_DEL"] = 30
		pg_info_dict["CELL_LENGTH_EDIT"] = 30
                
		str2 = ""
		str3 = ""
		jk = 0
                str = rp_td_html["rp_title_line_head"]%pg_info_dict
                for j in range(len(tbl_dicts[k])):
		      pg_info_dict["CHARLEN"] = char_len_dict[k][j]
		      
                      if string.atoi(char_len_dict[k][j]) == 0:  # datetime
			            pg_info_dict["CELL_LENGTH"] = 100
                      elif string.atoi(char_len_dict[k][j])*5 < 70:
				    pg_info_dict["CELL_LENGTH"] = 70
                      elif string.atoi(char_len_dict[k][j])*5 > 400:
				    pg_info_dict["CELL_LENGTH"] = 400
                      else:
				    pg_info_dict["CELL_LENGTH"] = string.atoi(char_len_dict[k][j])*5
		      #zzzz
                      _k_ = string.lower(k[1:])
                      flds = string.lower(tbl_dicts[k][j])[3:]
		      #data_type = type_dict[k][j]
                      data_type = type_dict[k][j]
		      getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC, data_type)
                      pg_info_dict = getDB()
		      #zzz
		      """
                      _db_dateformat= string.split(d_type_info_dict[k][j])
		      pg_info_dict["DATABASE"] = _db_dateformat[0]
		      pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
                      """
                      sw_list_at_j = []
                      pg_info_dict["CHINESE_TITLE"] = ""

		      if tbl_dicts[k][j] !="dbcCreate_on" and tbl_dicts[k][j] !="dbcRowid":
                                    pg_info_dict["CHINESE_TITLE"] = chinese_title[k][j]
				    ##### ouyang for dbcRowid purpose 
                                    pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
                                    str = str + rp_td_html["rp_title_line"]%pg_info_dict

                      pg_info_dict["TEXTAREA_S"]=""
                      pg_info_dict["TEXTAREA_E"]=""
                      char_len_ratio = long(char_len_dict[k][j])/100.0
                      if char_len_ratio >= 2.0:
                              pg_info_dict["TEXTAREA_S"]="<textarea NAME='comments' ROWS='10' COLS='35' wrap='virtual'>"
                              pg_info_dict["TEXTAREA_E"]="</textarea>"
                                			      
                      if jk == 2:
                            jk = 1
                            pg_info_dict["TWO_CELLS"] = str2
                            str3 = str3 + rp_sr_td_html["one_row"]%pg_info_dict
			    str2 = rp_sr_td_html["one_cell_one_row"]%pg_info_dict
                      else:
		            str2 = str2 + rp_sr_td_html["one_cell_one_row"]%pg_info_dict
                            jk += 1

                      # preparing primarykey_list for SW search
		      if DBColumn_dict[k][j] in primary_keys:
			      sw_list_at_j.append(tbl_dicts[k][j][3:])
			      ###sw_list_at_j.append(tbl_dicts[k][j])
                              sw_list_at_j.append(pg_info_dict[type_dict[k][j]])
                      if len(sw_list_at_j)>0:
                              SW_primary_keys.append(sw_list_at_j)
                pg_info_dict["TWO_CELLS"] = str2
                str3 = str3 + rp_sr_td_html["one_row"]%pg_info_dict
		
                pg_info_dict["PRIMARY_KEYS_LIST"]=SW_primary_keys
		#
		# this is added for ..zzzz 20040904
		#
		searchStr = ""
		if len(SW_primary_keys) > 0:
                       pg_info_dict["FIRST_PRIMARY_KEY"] = "dbc%s"%SW_primary_keys[0][0]
                else:
                       pg_info_dict["FIRST_PRIMARY_KEY"] = "Error001"

                pg_info_dict["ALL_CELLS"] = str3
		
                pg_info_dict["RP_TBL_WIDTH"] = len(tbl_dicts[k])*rp_tbl_width
                pg_info_dict["COLSPAN0"] = len(tbl_dicts[k])
                pg_info_dict["COLSPAN"] = len(tbl_dicts[k])+2
                pg_info_dict["COLSPAN_1"] = len(tbl_dicts[k])+2+1
                pg_info_dict["PG_NAME"]=pg_title_dict[k] 
                pg_info_dict["PG_TITLE"]=pg_title_dict[k] 
				
                pg_info_dict["RP_TITLE_LINE"] = str
                str = ""
		so_add_str = ""
                pg_info_dict["TR_BGCOLOR"]=""
                ALL_SO_primary_keys={}

                for i in range(search_length):
                      str1 = ""
                      pg_info_dict["WHICH_ROW"] = i
                      #
                      # the following two lines are for edit and delete icons on that row
		      #
		      #pg_info_dict["CELL_LENGTH_DEL"] = 30
                      TOTAL_CELL_LENGTH = 30
		      #pg_info_dict["CELL_LENGTH_EDIT"] = 30
                      TOTAL_CELL_LENGTH += 30
                      

                      ALL_SO_primary_keys[i]=[]
                      kj = 0
                      for j in range(len(tbl_dicts[k])):
			      
		            pg_info_dict["CHARLEN"] = char_len_dict[k][j]
			    if string.atoi(char_len_dict[k][j]) == 0:  # datetime
			            pg_info_dict["CELL_LENGTH"] = 100
			    elif string.atoi(char_len_dict[k][j])*5 < 70:
				    pg_info_dict["CELL_LENGTH"] = 70
                            elif string.atoi(char_len_dict[k][j])*5 > 400:
				    pg_info_dict["CELL_LENGTH"] = 400
                            else:
				    pg_info_dict["CELL_LENGTH"] = string.atoi(char_len_dict[k][j])*5
			    #
			    # Add cell length to total length for a whole table
			    #
                            TOTAL_CELL_LENGTH += pg_info_dict["CELL_LENGTH"]
		            #zzzz
			    _k_ = string.lower(k[1:])
			    flds = string.lower(tbl_dicts[k][j])[3:]
                            data_type = type_dict[k][j]
		            #data_type = type_dict[k][j]
		            getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC, data_type)
			    pg_info_dict = getDB()
		            #zzz 
			    """
			    _db_dateformat= string.split(d_type_info_dict[k][j])
		            pg_info_dict["DATABASE"] = _db_dateformat[0]
		            pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
                            """
                            data_type = type_dict[k][j]
                            #data_type = type_dict[k][j]
                            pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
                            pg_info_dict["rp_tbl_width"] = rp_tbl_width
                            if j==0:
                                   str1 = str1 + rp_td_html["rp_single_record_first"]%pg_info_dict
                            else:
		                   if tbl_dicts[k][j] !="dbcCreate_on":
			                     str1 = str1 + rp_td_html["rp_single_record"]%pg_info_dict


			    so_list_at_j = []
                            # preparing primarykey_list for SW search
		            if DBColumn_dict[k][j] in primary_keys:
                                    if kj==0:
                                           so_list_at_j.append("")
                                           kj = 1
                                    else:
				           so_list_at_j.append("AND")
                                    so_list_at_j.append(tbl_dicts[k][j][3:])
                                    ###so_list_at_j.append(tbl_dicts[k][j])
                                    so_list_at_j.append("EQ")
                                    so_list_at_j.append("{{$"+k+"."+tbl_dicts[k][j]+"[%d]}}"%i)
                            if len(so_list_at_j)>0:
                                    ALL_SO_primary_keys[i].append(so_list_at_j)
				    
                                            
                      pg_info_dict["RP_SINGLE_RECORD"]=str1
                      str = str + rp_td_html["rp_records"]%pg_info_dict
                      if pg_info_dict["TR_BGCOLOR"] == "":
                               pg_info_dict["TR_BGCOLOR"] = "bgcolor='lightblue'"
                      else:
                               pg_info_dict["TR_BGCOLOR"] = ""
                      # 
		      # put TOTAL_CELL_LENGTH into here. Just do once since all are same.
		      #
		      if i==0:
		            pg_info_dict["TOTAL_CELL_LENGTH"] = TOTAL_CELL_LENGTH 
                
		pg_info_dict["RP_RECORDS"] = str
               


	       
		so_add_str = ""
                for i in range(search_length):
                       pg_info_dict["_JS_SO_ADD"] = ALL_SO_primary_keys[i]
                       pg_info_dict["WHICH_ROW"] = i
                       so_add_str = so_add_str + rp_td_html["js_so_add"]%pg_info_dict
                
		pg_info_dict["JS_SO_ADD"] = so_add_str
                 
		####### rp_multi_edi_****.html is generated in html_edit_pg_generator.y ####################
		#
                #fff = html_dir + "\\" + pyfile_dict[k] + "\\" + "rp_multi_edi_" + k + ".html"
                #f = open(fff, 'w')
		#pg_info_dict["jslib_dir"]=jslib_dir
                #f.write(rp_td_html["rp_tmpl"]%pg_info_dict)
                #f.close()
		#
		#############################################################################################

                #fff = html_dir + "\\" + pyfile_dict[k] + "\\" + "rp_sr_" + k + ".html"
                #f = open(fff, 'w')
		#pg_info_dict["jslib_dir"]=jslib_dir
                #f.write(rp_sr_td_html["rp_sr_tmpl"]%pg_info_dict)
                #f.close()


                ############################################################################################
                str = rp_td_html["rp_title_line_head_4_rp_mr"]%pg_info_dict
                for j in range(len(tbl_dicts[k])):
		      pg_info_dict["CHARLEN"] = char_len_dict[k][j]
		      
                      if string.atoi(char_len_dict[k][j]) == 0:  # datetime
			            pg_info_dict["CELL_LENGTH"] = 100
                      elif string.atoi(char_len_dict[k][j])*5 < 70:
				    pg_info_dict["CELL_LENGTH"] = 70
                      elif string.atoi(char_len_dict[k][j])*5 > 400:
				    pg_info_dict["CELL_LENGTH"] = 400
                      else:
				    pg_info_dict["CELL_LENGTH"] = string.atoi(char_len_dict[k][j])*5
		      #zzzz
                      _k_ = string.lower(k[1:])
                      flds = string.lower(tbl_dicts[k][j])[3:]
                      data_type = type_dict[k][j]
		      #data_type = type_dict[k][j]
		      getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC, data_type)
                      pg_info_dict = getDB()
		      #zzz
		      """
                      _db_dateformat= string.split(d_type_info_dict[k][j])
		      pg_info_dict["DATABASE"] = _db_dateformat[0]
		      pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
                      """
                      sw_list_at_j = []
                      pg_info_dict["CHINESE_TITLE"] = ""

		      ###print "abcdef ....", tbl_dicts[k][j]
		      if tbl_dicts[k][j] !="dbcCreate_on" and tbl_dicts[k][j] !="dbcRowid":
                                    pg_info_dict["CHINESE_TITLE"] = chinese_title[k][j]
				    ##### ouyang for dbcRowid purpose
                                    pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
                                    str = str + rp_td_html["rp_title_line"]%pg_info_dict

                      pg_info_dict["TEXTAREA_S"]=""
                      pg_info_dict["TEXTAREA_E"]=""
                      char_len_ratio = long(char_len_dict[k][j])/100.0
                      if char_len_ratio >= 2.0:
                              pg_info_dict["TEXTAREA_S"]="<textarea NAME='comments' ROWS='10' COLS='35' wrap='virtual'>"
                              pg_info_dict["TEXTAREA_E"]="</textarea>"
                                			      
                      if jk == 2:
                            jk = 1
                            pg_info_dict["TWO_CELLS"] = str2
                            str3 = str3 + rp_sr_td_html["one_row"]%pg_info_dict
			    str2 = rp_sr_td_html["one_cell_one_row"]%pg_info_dict
                      else:
		            str2 = str2 + rp_sr_td_html["one_cell_one_row"]%pg_info_dict
                            jk += 1

                      # preparing primarykey_list for SW search
		      if DBColumn_dict[k][j] in primary_keys:
			      sw_list_at_j.append(tbl_dicts[k][j][3:])
			      ###sw_list_at_j.append(tbl_dicts[k][j])
                              sw_list_at_j.append(pg_info_dict[type_dict[k][j]])
                      if len(sw_list_at_j)>0:
                              SW_primary_keys.append(sw_list_at_j)
                pg_info_dict["TWO_CELLS"] = str2
                str3 = str3 + rp_sr_td_html["one_row"]%pg_info_dict
		
                pg_info_dict["PRIMARY_KEYS_LIST"]=SW_primary_keys
		#
		# this is added for ..zzzz 20040904
		#
		searchStr = ""
		if len(SW_primary_keys) > 0:
                       pg_info_dict["FIRST_PRIMARY_KEY"] = "dbc%s"%SW_primary_keys[0][0]
                else:
                       pg_info_dict["FIRST_PRIMARY_KEY"] = "Error001"

                pg_info_dict["ALL_CELLS"] = str3
		
                pg_info_dict["RP_TBL_WIDTH"] = len(tbl_dicts[k])*rp_tbl_width
                pg_info_dict["COLSPAN0"] = len(tbl_dicts[k])
                pg_info_dict["COLSPAN"] = len(tbl_dicts[k])+2
                pg_info_dict["COLSPAN_1"] = len(tbl_dicts[k])+2+1
                pg_info_dict["PG_NAME"]=pg_title_dict[k] 
                pg_info_dict["PG_TITLE"]=pg_title_dict[k] 
				
                pg_info_dict["RP_TITLE_LINE"] = str
                str = ""
		so_add_str = ""
                pg_info_dict["TR_BGCOLOR"]=""
                ALL_SO_primary_keys={}

                for i in range(search_length):
                      str1 = ""
                      pg_info_dict["WHICH_ROW"] = i
                      #
                      # the following two lines are for edit and delete icons on that row
		      #
		      #pg_info_dict["CELL_LENGTH_DEL"] = 30
                      TOTAL_CELL_LENGTH = 30
		      #pg_info_dict["CELL_LENGTH_EDIT"] = 30
                      TOTAL_CELL_LENGTH += 30
                      

                      ALL_SO_primary_keys[i]=[]
                      kj = 0
                      for j in range(len(tbl_dicts[k])):
			      
		            pg_info_dict["CHARLEN"] = char_len_dict[k][j]
			    if string.atoi(char_len_dict[k][j]) == 0:  # datetime
			            pg_info_dict["CELL_LENGTH"] = 100
			    elif string.atoi(char_len_dict[k][j])*5 < 70:
				    pg_info_dict["CELL_LENGTH"] = 70
                            elif string.atoi(char_len_dict[k][j])*5 > 400:
				    pg_info_dict["CELL_LENGTH"] = 400
                            else:
				    pg_info_dict["CELL_LENGTH"] = string.atoi(char_len_dict[k][j])*5
			    #
			    # Add cell length to total length for a whole table
			    #
                            TOTAL_CELL_LENGTH += pg_info_dict["CELL_LENGTH"]
		            #zzzz
			    _k_ = string.lower(k[1:])
			    flds = string.lower(tbl_dicts[k][j])[3:]
                            data_type = type_dict[k][j]
		            #data_type = type_dict[k][j]
		            getDB = get_db_n_dateformat(_k_, flds, pg_info_dict, _TABLE_SPEC, data_type)
			    pg_info_dict = getDB()
		            #zzz
			    """
			    _db_dateformat= string.split(d_type_info_dict[k][j])
		            pg_info_dict["DATABASE"] = _db_dateformat[0]
		            pg_info_dict["DATEFORMAT"] = _db_dateformat[1]
                            """
                            data_type = type_dict[k][j]
                            #data_type = type_dict[k][j]
                            pg_info_dict["FIELD_NAME"] = tbl_dicts[k][j]
                            pg_info_dict["rp_tbl_width"] = rp_tbl_width
                            if j==0:
                                   str1 = str1 + rp_td_html["rp_single_record_first_4_rp_mr"]%pg_info_dict
                            else:
		                   if tbl_dicts[k][j] !="dbcCreate_on":
			                 str1 = str1 + rp_td_html["rp_single_record"]%pg_info_dict


			    so_list_at_j = []
                            # preparing primarykey_list for SW search
		            if DBColumn_dict[k][j] in primary_keys:
                                    if kj==0:
                                           so_list_at_j.append("")
                                           kj = 1
                                    else:
				           so_list_at_j.append("AND")
                                    so_list_at_j.append(tbl_dicts[k][j][3:])
                                    ###so_list_at_j.append(tbl_dicts[k][j])
                                    so_list_at_j.append("EQ")
                                    so_list_at_j.append("{{$"+k+"."+tbl_dicts[k][j]+"[%d]}}"%i)
                            if len(so_list_at_j)>0:
                                    ALL_SO_primary_keys[i].append(so_list_at_j)
				    
                                            
                      pg_info_dict["RP_SINGLE_RECORD"]=str1
                      str = str + rp_td_html["rp_records"]%pg_info_dict
                      if pg_info_dict["TR_BGCOLOR"] == "":
                               pg_info_dict["TR_BGCOLOR"] = "bgcolor='lightblue'"
                      else:
                               pg_info_dict["TR_BGCOLOR"] = ""
                      # 
		      # put TOTAL_CELL_LENGTH into here. Just do once since all are same.
		      #
		      if i==0:
		            pg_info_dict["TOTAL_CELL_LENGTH"] = TOTAL_CELL_LENGTH 
                
		pg_info_dict["RP_RECORDS"] = str
               


	       
		so_add_str = ""
                for i in range(search_length):
                       pg_info_dict["_JS_SO_ADD"] = ALL_SO_primary_keys[i]
                       pg_info_dict["WHICH_ROW"] = i
                       so_add_str = so_add_str + rp_td_html["js_so_add"]%pg_info_dict
                
		pg_info_dict["JS_SO_ADD"] = so_add_str

                # do this later.....
		#
                #fff = html_dir + "\\" + pyfile_dict[k] + "\\" + "rp_mr_" + k + ".html"
                #f = open(fff, 'w')
		#pg_info_dict["jslib_dir"]=jslib_dir
                #f.write(rp_td_html["rp_tmpl"]%pg_info_dict)
                #f.close()




def _rp_td_html():
     rp_title_line = """\
    <TD vAlign=center borderColor=#214194 align=middle width=%(CELL_LENGTH)s 
    background={{XBOP_WWW_ROOT}}/graphics/oa_images/list_middle.jpg bgColor=#f7f7f7><FONT 
    style="FONT-SIZE: 10pt" color=#00000>%(CHINESE_TITLE)s</FONT></TD>
     """
     rp_td_html["rp_title_line"] = rp_title_line
     
     #rp_td_html["rp_title_line_head"] = """\
     #<TD vAlign=center borderColor=#3b82f1 width="%(CELL_LENGTH_EDIT)s" 
     #background={{XBOP_WWW_ROOT}}/graphics/oa_images/list_middle.jpg bgColor=#f7f7f7>
     #<FONT style="FONT-SIZE: 10pt" color=#000000>修改</FONT></TD>
     # <TD vAlign=center borderColor=#3b82f1 width="%(CELL_LENGTH_DEL)s" 
     #background={{XBOP_WWW_ROOT}}/graphics/oa_images/list_middle.jpg bgColor=#f7f7f7><FONT 
     # style="FONT-SIZE: 10pt" color=#000000>删除</FONT></TD>
     #"""
     #rp_td_html["rp_title_line_head_4_rp_mr"] = ""
     
     rp_td_html["rp_title_line_head"] = """\
     <TD class="fld_name" vAlign=center borderColor=#3b82f1 width=30 
     background={{XBOP_WWW_ROOT}}/graphics/oa_images/list_middle.jpg bgColor=#f7f7f7>
     No.</TD>
     <TD  class="fld_name" vAlign=center borderColor=#3b82f1 width="%(CELL_LENGTH_EDIT)s" 
     background={{XBOP_WWW_ROOT}}/graphics/oa_images/list_middle.jpg bgColor=#f7f7f7>
     修改</TD>
      <TD  class="fld_name" vAlign=center borderColor=#3b82f1 width="%(CELL_LENGTH_DEL)s" 
     background={{XBOP_WWW_ROOT}}/graphics/oa_images/list_middle.jpg bgColor=#f7f7f7>
      删除</TD>
     """
     rp_td_html["rp_title_line_head_4_rp_mr"] = ""
     
        
     rp_single_record = """\
    <TD  class="fld_name" vAlign=bottom borderColor=#3b82f1 align=middle width=%(CELL_LENGTH)s 
    bgColor=#f7f7f7><nobr>&nbsp;{{%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]}}</nobr></TD>
     """
     rp_td_html["rp_single_record"] = rp_single_record
     
     #rp_single_record_first = """\
     #   <td width=%(rp_tbl_width)s><a href="javascript:SW.doSearch('%(PG_ALIASES)s/wc_%(WHICH_ROW)s/0/1', '%(ONE_RECORD_PG)s', '_blank')"><font size="2" face="Arial,Helvetica,Sans-serif">{{%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]}}</font></a></td>
     #"""
     
     rp_single_record_first = """
    <TD class="fld_name" vAlign=bottom borderColor=#3b82f1 align=middle width=30 bgColor=#f7f7f7><nobr>&nbsp;
    <a class="menu_linked_name" href="javascript:SW.doSearch('%(PG_ALIASES)s/wc_%(WHICH_ROW)s/0/1', '%(SEARCH_RP_PG)s', '_blank','ms_sql_svr','YYYY-MM-DD HH24:MI:SS')">{{%(PG_ALIASES)s.%(FIRST_PRIMARY_KEY)s[%(WHICH_ROW)s]}}</a>
    </nobr></TD>
    <script language = "javascript">
	    edit_delete_rows('%(PG_ALIASES)s', '{{%(PG_ALIASES)s.%(FIRST_PRIMARY_KEY)s[%(WHICH_ROW)s]}}', %(WHICH_ROW)s, '%(EDIT_RP_PG)s', 'ms_sql_svr','YYYY-MM-DD HH24:MI:SS','go_mod.gif')
    </script>
    <script language = "javascript">
	    edit_delete_rows('%(PG_ALIASES)s', '{{%(PG_ALIASES)s.%(FIRST_PRIMARY_KEY)s[%(WHICH_ROW)s]}}', %(WHICH_ROW)s, '%(DELETE_RP_PG)s', 'ms_sql_svr','YYYY-MM-DD HH24:MI:SS','go_del.gif')
    </script>
     """
     rp_td_html["rp_single_record_first"] = rp_single_record_first
     rp_td_html["rp_single_record_first_4_rp_mr"] = """
     <TD class="fld_name" vAlign=bottom borderColor=#3b82f1 align=middle width=%(CELL_LENGTH)s bgColor=#f7f7f7>
    <a class="menu_linked_name" href="javascript:SW.doSearch('%(PG_ALIASES)s/wc_%(WHICH_ROW)s/0/1', '%(SEARCH_RP_PG)s', '_blank','ms_sql_svr','YYYY-MM-DD HH24:MI:SS')">{{%(PG_ALIASES)s.%(FIRST_PRIMARY_KEY)s[%(WHICH_ROW)s]}}</a>
    </TD>
    """

     rp_td_html["js_so_add"]="""\
      so.add(%(_JS_SO_ADD)s,"wc_%(WHICH_ROW)s")
     """
     rp_records = """\
     <tr height = 25>
          %(RP_SINGLE_RECORD)s
     </tr>
   <TR height=1>
  <TD colspan = %(COLSPAN)s vAlign=center borderColor=#3b82f1 align=middle background={{XBOP_WWW_ROOT}}/graphics/oa_images/line.gif bgColor=#f7f7f7></TD>
  </TR>
     """
     rp_td_html["rp_records"] = rp_records
     
     rp_td_html["rp_middle_line"] = """\
  <TD vAlign=center borderColor=#3b82f1 align=middle width=%(TD_PERCENT)s background={{XBOP_WWW_ROOT}}/graphics/oa_images/line.gif bgColor=#f7f7f7></TD>
     """
     
     rp_tmpl = """
      <html>
      <head>
      <meta name="generator" content="X*bop Table Wizard">
      <meta http-equiv="content-type" content="text/html; charset={{session.DEF.L.CHARSET}}">
      <title> %(PG_ZXZINC)s</title>
      <!-- Aliases
              "%(PG_ALIASES)s": "%(PG_ALIASES_DEF)s"
      -->

      <style type="text/css">
      <!--
      -->
      </style>
      <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/scw.js"></script>
      <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/form.js"></script>
      <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/formcheckers.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/form_special.js"></script>
<!--
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/datePick.js"></script>
-->
<script language="JavaScript" src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/overlib_mini.js"></script>
<script language="JavaScript" src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/printSpecial.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dynaSelect.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/searchWizard.js"></script>
      <script language=javascript>
      /*
      function pages()
      {
      var p = new Object()
      p._rc       = {{%(PG_ALIASES)s.rowCount}};
      p._sf       = {{%(PG_ALIASES)s.searchFrom}};
      p._st       = {{%(PG_ALIASES)s.searchTo}};
      p.searchLength = {{%(PG_ALIASES)s.searchLength}};
      p.previousN    = "%(PG_ALIASES)s.previousN"
      p.nextN    = "%(PG_ALIASES)s.nextN"
      p.gen_rpt    = "%(PG_ALIASES)s.gen_rpt"
      p.searchPage = "%(LP_PG)s"
      p.colspan  = %(COLSPAN)s

      var tmp1 = {{%(PG_ALIASES)s.%(FIELD_NAME)s}}	
      p.curr_record_length = tmp1.length	
          //If no searchString, searchLength is -1 first time.
          var searchLen = p.searchLength
          var leftLen   = searchLen - p.curr_record_length
       var rc = String(p._rc);
       var sf = String(p._sf);
       var st = String(p._st);
       if (p._rc == -1)
       {  
          document.write("<tr> <td align=left bgcolor= #6666ff>;");
          document.write("<FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>")
          document.write("无记录");
          document.write("</font>")
          document.write("</td></tr>")
          return;
      }
      
      if(p._rc>0){
       var rc = String(p._rc);
       var sf = String(p._sf);
       var st = String(p._st);
       var tmp = "第"+ sf +"条到第"+st+"条记录-共"+ rc +"条";

       if (p._rc > p.searchLength){
               if(p._sf == 1) {
            document.write("<tr> <td align=left bgcolor=#6666ff>");
            document.write("<a href=\\"javascript:handleRequest('[" + p.nextN + "]', '{{pageId}}')\\"><FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>下页</font></a>&nbsp;&nbsp;&nbsp;");
            document.write("<!-- <a href=\\"javascript:handleRequest('[" + p.gen_rpt + "]', '{{pageId}}')\\"><FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>报表</font></a> --> &nbsp;&nbsp;&nbsp;");
            document.write("<FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>"+tmp+"</font>");
            document.write("</td></tr>")
       }
               else if (p._st == p._rc)
               {
            document.write("<tr> <td align=left bgcolor=#6666ff>");
            document.write("<a href=\\"javascript:handleRequest('[" + p.previousN + "]','{{pageId}}')\\"><FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>上页</font></a>&nbsp;&nbsp;&nbsp;");
            document.write("<!-- <a href=\\"javascript:handleRequest('[" + p.gen_rpt + "]', '{{pageId}}')\\"><FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>报表</font></a> --> &nbsp;&nbsp;&nbsp;");
            document.write("<FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>"+tmp+"</font>");
            document.write("</td></tr>")
       }
               else
               {	 
            document.write("<tr> <td align=left bgcolor=#6666ff>");
            document.write("<a href=\\"javascript:handleRequest('[" + p.previousN + "]','{{pageId}}')\\"><FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>上页</font></a>");
            document.write("<a href=\\"javascript:handleRequest('[" + p.nextN + "]', '{{pageId}}')\\"><FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>下页</font></a>&nbsp;&nbsp;&nbsp;");
            document.write("<!-- <a href=\\"javascript:handleRequest('[" + p.gen_rpt + "]', '{{pageId}}')\\"><FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>报表</font></a> -->&nbsp;&nbsp;&nbsp;");
            document.write("<FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>"+tmp+"</font>");
            document.write("</td></tr>")
       }
                   }
           else{
            document.write("<tr> <td align=left bgcolor=#6666ff>");
                   document.write("<!-- <a href=\\"javascript:handleRequest('[" + p.gen_rpt + "]', '{{pageId}}')\\"><FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>报表</font></a> --> &nbsp;&nbsp;&nbsp;");
                   document.write("<FONT style=\\"FONT-SIZE: 10pt\\" color=#ffffff>"+tmp+"</font>");
                   document.write("</td></tr>")
           }
               }
      }
      */
var SW = new bopSearchWizard()
var so = new bopSearchObject(%(PRIMARY_KEYS_LIST)s)
%(JS_SO_ADD)s
SW.add("%(PG_ALIASES)s", so)

function edit_delete_rows(alias, field_value, i, rp, db, date_format,img) {
            if (field_value.length>0){
			document.write("<TD class="fld_name" width=%(CELL_LENGTH_DEL)s><A href=\\"javascript:SW.doSearch('"+alias+"/wc_" + i + "/0/1', '"+rp+"', '_blank','"+db+"','"+date_format+"')\\"><IMG src=\\"{{XBOP_WWW_ROOT}}/graphics/oa_images/"+img+"\\"  border=0></A></TD>")
	    }
	    else {
			document.write("<TD width=%(CELL_LENGTH_DEL)s >&nbsp;</TD>")
	    }
       }
</script>
  </head>
      <body style="FONT-SIZE: 10pt" bgColor=#dee7ff leftMargin=0 background="" topMargin=0 marginheight="0" marginwidth="0" >
      <TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0 WIDTH="100%%">
      <TR><TD WIDTH="100%%" >
      <form name=""
            action="{{CGI_HANDLER}}"
            method="POST">
      <input type=hidden name="SID"
             value="{{SID}}">
      <input type=hidden name="pageId" value="{{pageId}}">
      <input type=hidden name="gRequestIds" value="[]">
      <input type=hidden name="requestIds" value="[]">
      <input type=hidden name="responseId" value="{{pageId}}">
      <input type=hidden name="%(PG_ALIASES)s.searchOffset"
             value="{{%(PG_ALIASES)s.searchOffset}}">
      <input type=hidden name="%(PG_ALIASES)s.searchLength"
             value="{{%(PG_ALIASES)s.searchLength}}">
      <input type=hidden name="%(PG_ALIASES)s.searchString" value = "{{%(PG_ALIASES)s.searchString}}">
      <input type=hidden name="_browserDateTime_"
       value="">

      %(HIDDEN_FIELDS_FOR_DATATRANSFER)s
      
<TABLE style="FONT-SIZE: 10pt" cellSpacing=0 cellPadding=0 width=%(TOTAL_CELL_LENGTH)s bgColor=#f7f7f7 border=0>
<TBODY>
    <script language = "javascript">
         //pages()
    </script>
</TBODY></TABLE>
<TABLE style="FONT-SIZE: 10pt" cellSpacing=0 cellPadding=0 width=%(TOTAL_CELL_LENGTH)s bgColor=#f7f7f7 border=0>
<TBODY>
  <TR height=28>
            %(RP_TITLE_LINE)s
  </TR>
             %(RP_RECORDS)s
  <TR height=28>
            %(RP_TITLE_LINE)s
    </TR>
</TBODY></TABLE>
<TABLE style="FONT-SIZE: 10pt" cellSpacing=0 cellPadding=0 width=%(TOTAL_CELL_LENGTH)s bgColor=#f7f7f7 border=0>
<TBODY>
    <script language = "javascript">
         //pages()
    </script>
</TBODY></TABLE>

</form>

</TD></TR></TABLE>

</body>
</html>
     """
     rp_td_html["rp_tmpl"] = rp_tmpl


rp_sr_td_html = {}

def _rp_sr_td_html():

      one_cell_one_row = """\
     <td nowrap class="fld_name">%(CHINESE_TITLE)s</td>
     <td class="fld_name" width = 200 bgcolor="lightblue">%(TEXTAREA_S)s{{%(PG_ALIASES)s.%(FIELD_NAME)s[0]}}%(TEXTAREA_E)s</td> <td width = 40>&nbsp;</td>
      """
      rp_sr_td_html["one_cell_one_row"]=one_cell_one_row
      
      one_row = """\
<tr>%(TWO_CELLS)s</tr>
      """
      rp_sr_td_html["one_row"]=one_row
	
      rp_sr_tmpl="""
<html>
<head>
<meta name="generator" content="X*bop Table Wizard">
<meta http-equiv="content-type" content="text/html; charset={{session.DEF.L.CHARSET}}">
<title>%(PG_ZXZINC)s</title>
<!-- Aliases
        "%(PG_ALIASES)s": "%(PG_ALIASES_DEF)s"
-->

<style type="text/css">
<!--

-->
</style>
 <link href="{{XBOP_WWW_ROOT}}/css/xbop_studio_css.css" rel="stylesheet" type="text/css">
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/scw.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/form.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/formcheckers.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/form_special.js"></script>
<script language=javascript>

//form validation (called by handleRequest). 
//If it returns true, then the form will be submitted. 
function formOk(requestIds, reponseId, form){
	return true
}
</script>
</head>
<body style="FONT-SIZE: 10pt" bgColor=#dee7ff leftMargin=0 background="" topMargin=0 marginheight="0" marginwidth="0">
<TABLE BORDER=0 CELLSPACING=0 CELLPADDING=0  >
<TR><TD  >
<form name="topForm"
      action="{{CGI_HANDLER}}"
      method="POST">
<input type=hidden name="SID"
       value="{{SID}}">
<input type=hidden name="pageId"
       value="{{pageId}}">
<input type=hidden name="gRequestIds"
       value="[]">
<input type=hidden name="requestIds"
       value="[]">
<input type=hidden name="responseId"
       value="{{pageId}}">
<input type=hidden name="%(PG_ALIASES)s.searchOffset"
       value="{{%(PG_ALIASES)s.searchOffset}}">
<input type=hidden name="%(PG_ALIASES)s.searchLength"
       value="{{%(PG_ALIASES)s.searchLength}}">
<input type=hidden name="L.CODE"
       value="{{session.DEF.L.CODE}}">
<input type=hidden name="C.CODE"
       value="{{session.DEF.C.CODE}}">
<input type=hidden name="C.SYM"
       value="{{session.DEF.C.SYM}}">
<input type=hidden name="C.XR"
       value="{{session.DEF.C.XR}}">
<input type=hidden name="M.SET0.MF"
       value="{{session.DEF.M.SET0.MF}}">
<input type=hidden name="M.SET0.CF"
       value="{{session.DEF.M.SET0.CF}}">
<input type=hidden name="M.SET0.DF"
       value="{{session.DEF.M.SET0.DF}}">
<input type=hidden name="_browserDateTime_"
       value="">

<table border="0" cellspacing="0" cellpadding="0">
<tr>
     <td align="center" colspan="6"><b><font size="4" face="仿宋_GB2312">%(PG_TITLE)s</font></b></td>
</tr>
<tr>
     <td colspan="6"><hr align="center"></td>
</tr>
%(ALL_CELLS)s
<tr>
     <td colspan="6"><hr align="center"></td>
</tr>
<tr>
<td align="center" colspan="6">
<a href="javascript:window.close()"><b><font size="4" face="仿宋_GB2312">返回</font></b></a>
</td>
</tr>
</table>
</form>
</TD></TR></TABLE>
</body>
</html>
	"""

      rp_sr_td_html["rp_sr_tmpl"]=rp_sr_tmpl




     


def _all_td_html():

	    all_td_html["identity_ck_js"] = """\
if (document.forms[0]["%(PG_ALIASES)s.%(DBIdentity_dbc_field)s[0]"]){
	 genCreateOn();
        //
      	// check if there is a DBIdentity Key
	// 
	//if (d_type.columns[fieldName].column == "DBIdentity"){
	/*
	 * This is dbcCreate_on field
	 */
               fieldName = '%(PG_ALIASES)s.%(DBIdentity_dbc_field)s'
               fieldName0 = '%(PG_ALIASES)s.%(DBIdentity_dbc_field)s'+'[0]'
	       value = getElementValue(document['topForm'][fieldName0]);

	 //if(value.length == 0){
	//	     document['topForm'][fieldName0].focus();
	//	     alert("该字段不能为空!");
	//             return;
	//     }
	//     else {
		  searchStr = columns.getSearchString(fieldName, op, value, valueB);
                  submitForm[theDBO+".searchString"].value= searchStr
		  handleRequest('['+theDBO+'.insert1]', responseId, submitForm, frameName)
                  return;
	    // }
        //}
	}
	    """
	    
	    all_td_html["print_receipt_button"] = """\
              <TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
              <A class="fld_name" href="javascript:id_tableInsert()">打印收据</A></TD>
	    """

            all_td_html["identity_js_function"] = """\
    function timeStr () {
    var now = new Date();
    var dd = now.getDate();
    var mm = now.getMonth() + 1;
    var yy = now.getFullYear();
    var timeValue = "" + yy;
	timeValue += ((mm < 10) ? "0" : "") + mm
        timeValue += ((dd < 10) ? "0" : "") + dd
	return timeValue;
}
     
    function timeStr2 () {
    var now = new Date();
    var dd = now.getDate();
    var mm = now.getMonth() + 1;
    var yy = now.getFullYear();
    var hh = now.getHours();
    var mi = now.getMinutes();
    var ss = now.getSeconds();
    var timeValue = "" + yy;
	timeValue += ((mm < 10) ? "-0" : "-") + mm
        timeValue += ((dd < 10) ? "-0" : "-") + dd
	timeValue += " "
	timeValue += ((hh < 10) ? "0" : "") + hh
	timeValue += ((mi < 10) ? ":0" : ":") + mi
	timeValue += ((ss < 10) ? ":0" : ":") + ss
	return timeValue;
    }

function timeStr3 () {
    var now = new Date();
    var dd = now.getDate();
    var mm = now.getMonth() + 1;
    var yy = now.getFullYear();
    var hh = now.getHours();
    var mi = now.getMinutes();
    var ss = now.getSeconds();
    var timeValue = "" + yy;
	timeValue += ((mm < 10) ? "-0" : "-") + mm
        timeValue += ((dd < 10) ? "-0" : "-") + dd
	return timeValue;
}

function setSearchStr(theDBO){
  if (document.forms[0][theDBO+".dbcCreate_on[0]"]){
         document.forms[0][theDBO+".mySqlOrderBy"].value= "create_on DESC"
	 document.forms[0][theDBO+".searchString"].value= " create_on > " + "'"+timeStr3()+"'"
  }
}


     function genCreateOn(){
		 var _timeStr = timeStr2();
	         document.forms[0]["%(PG_ALIASES)s.%(DBIdentity_dbc_field)s[0]"].value =  _timeStr
      }
            """
	    
	    all_td_html["identity_hidden_input_fields"]="""\
	    """
           
	    all_td_html["identity_genOrderId"]="""\
            genOrderId()
            """
	    
	    all_td_html["identity_create_on"]="""\
            genCreateOn()
            """
	    all_td_html["identity_aliases"]="""\
	    """
	    
            #div_4_date_time = """\
            # <div id="overDiv" style="position:absolute; visibility:hidden; z-index:1000;"></div>
            #"""
            div_4_date_time = ""
            all_td_html["div_4_date_time"] =  div_4_date_time
            
            #date_time = """\
            #<a href="javascript:ggPosX=200;ggPosY=50;show_calendar('topForm.%(FIELD_NAME0)s');" onMouseOver="window.status='Date Picker';  return true;" onMouseOut="window.status=''; nd(); return true;"><img src="{{XBOP_WWW_ROOT}}/graphics/misc/show-calendar.gif" width=20 height=20 border=0></a>
            #"""
            date_time = ""
     
            all_td_html["date_time"] = date_time
            table_title = """\
             <td align="center" nowrap class="fld_name">%(CHINESE_TITLE)s</td>
            """
            all_td_html["table_title"]=table_title

            js_columns = """\
                    columns.add("%(PG_ALIASES)s.%(FIELD_NAME)s", "%(FIELD_NAME3)s", "%(DATA_TYPE_LIST)s",  "%(CHARLEN)s", "%(DATABASE)s","%(DATEFORMAT)s")
                    """
            all_td_html["js_columns"] = js_columns
     
            #zzzz: add CHARLEN for web page validation
            js_types  = """\
                        d_type.add("%(PG_ALIASES)s.%(FIELD_NAME)s", "%(DBCOLUMNS)s", "%(COL_TYPES)s", "%(CHARLEN)s", "%(DATABASE)s","%(DATEFORMAT)s")
                        """
            all_td_html["js_types"] = js_types


            display_chinese_title = """\
        <td nowrap class="fld_name">%(CHINESE_TITLE)s</td>
            """
            all_td_html["display_chinese_title"] = display_chinese_title
     
            rows_onweb = """\
          <td class="fld_name">{{%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]}}</td>
            """
            all_td_html["rows_onweb"] = rows_onweb
     
            hidden_rows = """\
            <input type=hidden name="%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]" value="{{%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]}}" size="18">
            """
            all_td_html["hidden_rows"] = hidden_rows
     

            all_td_html["query_drop_down"]="""\
var which = %(_WHICH_)s
//var kkk = "{{%(PG_ALIASES)s.%(FIELD_NAME)s[0]}}"
%(SESSION_STR)s
var local_drop_down%(_WHICH_)s = new Array()
for (var ii = 0; ii < dropDownList[which].length; ii++){
  if (dropDownList[which][ii].length == 0){
     break;
   }
   else{
     local_drop_down%(_WHICH_)s[ii]=_stripString(dropDownList[which][ii])
   }
}
 //%%(PG_ALIASES)s.%%(FIELD_NAME)s.C needs to be done in query.py
 var %(FIELD_NAME)s_list = {"name": "%%(PG_ALIASES)s.%%(FIELD_NAME)s.C",
                 "values": local_drop_down%(_WHICH_)s,
                 "captions": local_drop_down%(_WHICH_)s,
                 "defaultSelected": _stripString(kkk),
                 "withNone": true,
                 "size": "1",
                 "multiple": false,
                 "onChange": "%(GET_SUB_DROPDOWN)s",
                 "onFocus": "",
                 "onKeyPress":"",
                 "onBlur": ""}
document.write(generateDYNA_SELECT( %(FIELD_NAME)s_list))
            """


            all_td_html["drop_down"]="""\
     <td class="fld_name"><script language=javascript>
     var which = %(_WHICH_)s
     //var kkk = "{{%(PG_ALIASES)s.%(FIELD_NAME)s[0]}}"
     %(SESSION_STR)s
     var local_drop_down%(_WHICH_)s = new Array()
         for (var ii = 0; ii < dropDownList[which].length; ii++){
               if (dropDownList[which][ii].length == 0){
                   break;
               }
               else{
                   local_drop_down%(_WHICH_)s[ii]=_stripString(dropDownList[which][ii])
               }
         }
     var %(FIELD_NAME)s_list = {"name": "%(PG_ALIASES)s.%(FIELD_NAME)s[0]",
                 "values": local_drop_down%(_WHICH_)s,
                 "captions": local_drop_down%(_WHICH_)s,
                 "defaultSelected": _stripString(kkk),
                 "withNone": true,
                 "size": "1",
                 "multiple": false,
                 "onChange": "%(GET_SUB_DROPDOWN)s",
                 "onFocus": "",
                 "onKeyPress":"enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')",
                 "onBlur": ""}
     document.write(generateDYNA_SELECT( %(FIELD_NAME)s_list))
     </script>
     </td> <td width=40></td>
            """
     
            all_td_html["drop_down_w_default_value"]="""\
     <td class="fld_name"><script language=javascript>
     var which = %(_WHICH_)s
     var local_drop_down%(_WHICH_)s = new Array()
         for (var ii = 0; ii < dropDownList[which].length; ii++){
               if (dropDownList[which][ii].length == 0){
                   break;
               }
               else{
                   local_drop_down%(_WHICH_)s[ii]=_stripString(dropDownList[which][ii])
               }
         }
     var %(FIELD_NAME)s_list = {"name": "%(PG_ALIASES)s.%(FIELD_NAME)s[0]",
                 "values": local_drop_down%(_WHICH_)s,
                 "captions": local_drop_down%(_WHICH_)s,
                 "defaultSelected": "{{%(PG_ALIASES)s.%(FIELD_NAME)s[0]}}",
                 "withNone": true,
                 "size": "1",
                 "multiple": false,
                 "onChange": "",
                 "onFocus": "",
                 "onKeyPress":"enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')",
                 "onBlur": ""}
     document.write(generateDYNA_SELECT( %(FIELD_NAME)s_list))
     </script>
     </td> <td width=40></td>
            """
	    
            all_td_html["_function"] = """\
function %(FUNC1)s() {
%(VAR)s
if (%(NOT_NaN)s){
  var aaa = %(FUNCTION)s
  %(RESULT_FIELD)s.value = myRound(aaa)
    }
}
            """
            
     
            all_td_html["sum_field"] = """\
summationCK('%(PG_ALIASES)s.%(SUM_FIELD1)s[0]','%(PG_ALIASES)s.%(SUM_FIELD2)s[0]','%(PG_ALIASES)s.%(SUM_FIELD3)s[0]');
            """
     
            #all_td_html["normal_cell_summationCK"] = """\
            #<td><input type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" onChange = "return %(JS_SUM_CALL)s" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="{{%(PG_ALIASES)s.%(FIELD_NAME)s[0]}}" size="18"> %(DATE_PICKER)s </td><td width=40></td> 
            #"""
            all_td_html["normal_cell_summationCK"] = """\
            <td><input type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" %(DATE_PICKER)s onChange = "return %(JS_SUM_CALL)s" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="{{%(PG_ALIASES)s.%(FIELD_NAME)s[0]}}" size="18"> </td><td width=40></td> 
            """
            
	    #all_td_html["normal_cell_99"] = """\
            #<td><input id=%(FIELD_NAME0)s type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" onChange = "%(MY_FUNCTION)s  return data_ck('topForm', '%(PG_ALIASES)s.%(FIELD_NAME)s[0]')" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="{{%(PG_ALIASES)s.%(FIELD_NAME)s[0]}}" size="18"> %(DATE_PICKER)s </td><td width=40></td> 
            #"""
	    
	    all_td_html["normal_cell_99"] = """\
            <td><input id=%(FIELD_NAME0)s type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" %(DATE_PICKER)s onChange = "%(MY_FUNCTION)s  return data_ck('topForm', '%(PG_ALIASES)s.%(FIELD_NAME)s[0]')" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="{{%(PG_ALIASES)s.%(FIELD_NAME)s[0]}}" size="18">  </td><td width=40></td> 
            """
            
	    all_td_html["pg_aliases_field_name0"] = "%(PG_ALIASES)s.%(FIELD_NAME)s[0]"
	    
	    #all_td_html["normal_cell"] = """\
            #<td><input id=%(FIELD_NAME0)s type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" onChange = "%(MY_FUNCTION)s  data_ck('topForm', '%(PG_ALIASES)s.%(FIELD_NAME)s[0]')%(get_info_from_other_table)s" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="{{%(pg_aliases_field_name0)s}}" size="18"> %(DATE_PICKER)s </td><td width=40>%(FLD2_BEHIND_FLD1_STR)s</td> 
            #"""
	    all_td_html["normal_cell"] = """\
            <td class="fld_name"><input id=%(FIELD_NAME0)s type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" %(DATE_PICKER)s onChange = "%(MY_FUNCTION)s  data_ck('topForm', '%(PG_ALIASES)s.%(FIELD_NAME)s[0]')%(get_info_from_other_table)s" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="{{%(pg_aliases_field_name0)s}}" size="18">%(display_2_in_1_search_link_for_img)s</td><td width=40>%(FLD2_BEHIND_FLD1_STR)s</td> 
            """
            
	    all_td_html["normal_cell_hidden"] = """\
          <input type=hidden name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]"  value="{{%(PG_ALIASES)s.%(FIELD_NAME)s[0]}}">  
            """
	    
            all_td_html["check_btn2"] = """\
          <td class="fld_name"><input type=radio  checked name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')"  value="%(VALUE1)s">%(VALUE1)s
     <input type=radio name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="%(VALUE2)s">%(VALUE2)s
         </td>  <td width=40></td>
            """
            all_td_html["check_btn3"] = """\
          <td  class="fld_name"><input type=radio checked name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="%(VALUE1)s">%(VALUE1)s
     <input type=radio name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="%(VALUE2)s">%(VALUE2)s
     <input type=radio name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="%(VALUE3)s">%(VALUE3)s
          </td>  <td width=40></td>
            """
     
            display_2_in_1_link = """\
      <td><a class="menu_linked_name" href="javascript:inputWindow('%(PG_ALIASES)s.%(FIELD_NAME)s[0]','%(CHINESE_TITLE)s','%(WHICH_WINDOW)s')" >%(CHINESE_TITLE)s</a></td>
            %(DROP_DOWN)s 
            """
            all_td_html["display_2_in_1_link"] = display_2_in_1_link

            display_2_in_1_search_link_NOTUSED = """\
	<td><A class="menu_linked_name" href="javascript:dataStore('%(PG_ALIASES)s.%(FIELD_NAME)s[0]','%(get_info_from_other_table_v2)s'); handleRequestTarget('[]','%(DROP_DOWN_SEARCH_PG)s', document.forms[0], target='_search')">%(CHINESE_TITLE)s</A></TD>
	%(DROP_DOWN)s
	    """
            display_2_in_1_search_link = """\
	<td nowrap class="fld_name">%(CHINESE_TITLE)s</TD>
	%(DROP_DOWN)s
	    """
            all_td_html["display_2_in_1_search_link"] = display_2_in_1_search_link
            display_2_in_1_search_link_for_img = """\
<a href="javascript:dataStore('%(PG_ALIASES)s.%(FIELD_NAME)s[0]','%(get_info_from_other_table_v2)s'); handleRequestTarget('[]','%(DROP_DOWN_SEARCH_PG)s', document.forms[0], target='_search')"><img src="{{XBOP_WWW_ROOT}}/graphics/misc/find.gif" height=25 align=top border=0>
	    """
            all_td_html["display_2_in_1_search_link_for_img"] = display_2_in_1_search_link_for_img
	    
            display_2_in_1 = """\
          <td nowrap class="fld_name">%(CHINESE_TITLE)s</td>
          %(DROP_DOWN)s
          """
            all_td_html["display_2_in_1"] = display_2_in_1
    
            all_td_html["display_2_in_1_hidden"] = """%(DROP_DOWN)s"""
     
            all_single_row_new = """\
            <td class="fld_name"><input type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]" onChange = " return tbl_cell_data_ck('topForm', '%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]', %(WHICH_ROW)s)" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[%(WHICH_ROW)s]')" value="{{%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]}}" size="8"></td>
             """
            all_td_html["all_single_row_new"]=all_single_row_new
            
            all_onweb_row = """\
              <td class="fld_name">{{%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]}}</td>
             """
            all_td_html["all_onweb_row"]=all_onweb_row
            
            all_single_row_search = """\
              <td class="fld_name">{{%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]}}</td>
             """
            all_td_html["all_single_row_search"]=all_single_row_search
     
            all_single_record = """\
            <tr>
            <td class="fld_name"><input type=checkbox name="%(PG_ALIASES)s.checked" value=%(WHICH_ROW)s></td>
            %(ALL_SINGLE_RECORD)s
            </tr>
            """
            all_td_html["all_single_record"]=all_single_record
     
            all_td_html["hidden_row"] = """\
            <td class="fld_name"><input type=hidden name="%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]" value="{{%(PG_ALIASES)s.%(FIELD_NAME)s[%(WHICH_ROW)s]}}" size="8"></td>
            """
     
     
            all_td_html["item_on_img_pg"] = """\
            <td>
             <A class="menu_linked_name" href="javascript:handleRequestTarget2('[]', '%(my_html_dir)s/%(nodePg)s', document.forms[0], '_self', true)">
             <center>
             <img src="%(icon_path)s/%(tbl_image)s" width=64 height=64 border="0"><br>
             %(GROUP_NAME)s 
             </center>
             </a></td>
              """
     
            all_td_html["callAttributes"]="""\
     <!-- callAttributes
             %(CALL_ATTRIBUTES)s
     -->
             """
            all_td_html["call_Attributes"]="""\
              "%(CALL_OBJECT)s":
              %(CALL_ATTRIBUTES_DICT)s,
            """
            
	    all_td_html["dropMenuStr"]="""
 <input type=hidden name="%(CALL_OBJECT)s.searchString" value="">
            """
	    
	    all_td_html["sub_dropMenuStr"]="""
 <input type=hidden name="%(SUB_CALL_OBJECT)s.searchString" value="">
            """
            
	    all_td_html["drop_down_list"]="""\
     dropDownList[%(_WHICH_)s]={{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s}}
            """
            all_td_html["drop_down_list_old"]="""\     
          dropDownList[%(_WHICH_)s]=['{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[0]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[1]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[2]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[3]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[4]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[5]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[6]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[7]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[8]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[9]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[10]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[11]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[12]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[13]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[14]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[15]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[16]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[17]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[18]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[19]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[20]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[21]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[22]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[23]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[24]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[25]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[26]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[27]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[28]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[29]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[30]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[31]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[32]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[33]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[34]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[35]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[36]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[37]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[38]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[39]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[40]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[41]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[42]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[43]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[44]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[45]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[46]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[47]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[48]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[49]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[50]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[51]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[52]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[53]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[54]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[55]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[56]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[57]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[58]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[59]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[60]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[61]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[62]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[63]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[64]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[65]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[66]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[67]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[68]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[69]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[70]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[71]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[72]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[73]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[74]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[75]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[76]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[77]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[78]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[79]}}',
         '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[80]}}', '{{%(PG_ALIASES_DEF2)s.%(REF_TBL_FIELD)s[81]}}'];
          """
            all_td_html["page_buttons"]="""\
<TR height=10><TD>
<div id="toolbar_zone" style="width:250;border :1px solid silver;"/>
 </TD></TR>            
	    """
            all_td_html["page_buttons_不用了"]="""\
     <TR><TD>
<TABLE  borderColor=#000000 height=21  cellSpacing=0 cellPadding=0 bgColor=#dee7ff border=0>
<TBODY>
<TR vAlign=bottom align=middle>
<TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
<A class="menu_linked_name"  href="javascript:ckInsert('%(PG_ALIASES)s', '%(RP_PG)s', document.forms[0], 'frameList')">保&nbsp;存</A></TD>
<TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
<A class="menu_linked_name" href="javascript:cleanInput('topForm', '[0]')">清&nbsp;除</A></TD>
<TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
<A class="menu_linked_name"  href="javascript:doSearchOBC88('%(PG_ALIASES)s', 0, %(PG_SCH_LEN)s, '%(RP_PG)s',  document.forms[0], document.forms[0],'frameList')">查&nbsp;找</A></TD>
<TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
<A class="menu_linked_name"  href="javascript:doSearchOBC99('%(PG_ALIASES)s', 0, %(PG_SCH_LEN)s, '%(RP_PG)s', false, document.forms[0], document.forms[0],'frameList')">全&nbsp;部</A></TD>
<TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
<A class="menu_linked_name"  href="javascript:handleRequestTarget('[]','%(SEARCH_PG)s', document.forms[0], target='_search')">详&nbsp;查</A></TD>
%(print_receipt_button)s

<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td>{{%(PG_ALIASES)s.duplicated}}</td>
</TR>
</TBODY></table>
     </TD></TR>
            """

        
            all_td_html["page_title_image"]="""\
     <TABLE border=0>
            """

        
            all_td_html["page_title"]="""\
     <TR><TD>
<TABLE style="FONT-SIZE: 10pt" align=center borderColor=#000000 height=21  cellSpacing=0 cellPadding=0 bgColor=#dee7ff border=0>
<TBODY>
<TR vAlign=bottom >
<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
</tr><tr>
<td ><b><font size="4" face="仿宋_GB2312">%(PG_NAME)s</font></b></td>
</TR>
</TBODY></table>
     </TD></TR>
            """
            
	    all_td_html["page_update_button"]="""\
<TABLE style="FONT-SIZE: 10pt" borderColor=#000000 height=21  cellSpacing=0 cellPadding=0 bgColor=#dee7ff border=0  align="center" >
<TBODY>
<tr><td>&nbsp;</td></tr>
<tr>
	<td>
<!--
<input type=button onclick="javascript:enableInput();if(final_ck()){ setSearchStr('%(PG_ALIASES)s'); ck4update(); handleRequest('[%(PG_ALIASES)s.update,%(PG_ALIASES)s.mySearch ]', '%(MULTI_EDI_RP_PG)s', document.forms[0], 'frameList');window.close()}"  value="更 新">
-->
<input type=button onclick="javascript:ck4update()"  value="更 新">
	<input type=button onclick="javascript:window.close()"  value="返 回">
</td> </tr> </TBODY></table>
            """
                              
	    all_td_html["getSubMenuStr1"] = """\
var v2 = getElementValue(document.forms[0]["%(v2)s"])
document.forms[0]["%(v2_obj)s.searchString"].value = "%(other_field0)s = '"+v2+"'"
document.forms[0][subObj+".searchString"].value = field_name + "='"+selectedValue+"'"
if (v2.length < 1)
{
  %(enableInput)s
  handleRequest("'["+baseObj+".dataTransfer,"+ subObj +".search"+"]'",'{{pageId}}', document.forms[0], target='%(WHICH_FRAME_AREA)s')
}
else	    
{
%(enableInput)s
handleRequest("'["+baseObj+".dataTransfer,"+ subObj +".search"+"%(v2_search)s]'",'{{pageId}}', document.forms[0], target='%(WHICH_FRAME_AREA)s')
}            """
            all_td_html["getSubMenuStr2"] = """\
  document.forms[0][subObj+".searchString"].value = field_name + "='"+selectedValue+"'"
  handleRequest("'["+baseObj+".dataTransfer,"+ subObj +".search"+"]'",'{{pageId}}', document.forms[0], target='%(WHICH_FRAME_AREA)s')
            """
			    
            all_tmpl = """
     <html>
     <head>
     <meta name="generator" content="X*bop Table Wizard">
     <meta http-equiv="pragma" content="no-cache">
     <meta http-equiv="content-type" content="text/html;charset={{session.DEF.L.CHARSET}}">
     <title>%(zxz_software)s</title>
     <!-- Aliases
             %(identity_aliases)s "%(PG_ALIASES)s": "%(PG_ALIASES_DEF)s"
     -->
     
     %(CALLATTRIBUTES)s
     
     
     <style type="text/css">
     <!--
     
     -->
     </style>
     <link href="{{XBOP_WWW_ROOT}}/css/xbop_studio_css.css" rel="stylesheet" type="text/css">
     <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/scw.js"></script>
     <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/form.js"></script>
     <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/form_special.js"></script>
     <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/search.js"></script>
     <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/mysearch2.js"></script>
     <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/formcheckers.js"></script>
     <!--
     <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/datePick.js"></script>
     -->
     <script language="JavaScript" src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/overlib_mini.js"></script>
     <script language="JavaScript" src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/printSpecial.js"></script>
     <script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dynaSelect.js"></script>
<link rel="STYLESHEET" type="text/css" href="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dhtmlxSuite/dhtmlxToolbar/codebase/skins/dhtmlxtoolbar_dhx_black.css">
<link rel="STYLESHEET" type="text/css" href="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dhtmlxSuite/dhtmlxToolbar/codebase/skins/dhtmlxtoolbar_dhx_blue.css">
<link rel="STYLESHEET" type="text/css" href="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dhtmlxSuite/dhtmlxToolbar/codebase/skins/dhtmlxtoolbar_dhx_skyblue.css">
<link rel="STYLESHEET" type="text/css" href="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dhtmlxSuite/dhtmlxToolbar/codebase/skins/dhtmlxtoolbar_dhx_web.css">
<!--
<script language="JavaScript" src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dhtmlxSuite/dhtmlxToolbar/codebase/dhtmlxprotobar.js"></script>
-->
<script language="JavaScript" src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dhtmlxSuite/dhtmlxToolbar/codebase/dhtmlxtoolbar.js"></script>
<script language="JavaScript" src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dhtmlxSuite/dhtmlxToolbar/codebase/dhtmlxcommon.js"></script>




     <script language=javascript>
     // ********************************************************************
     // Searchable fields.
     // RDBColumns is an object defined in the search.js lib. It is used for
     // collecting searchable form fields and creating search string that
     // can be used by X*bop search method.
     // *******************************************************************
     var columns = new RDBColumns()
     %(JS_COLUMNS)s
     var d_type = new RDBColumns()
     %(JS_TYPES)s
     var dropDownList = new Array()
     %(DROP_DOWN_LIST)s
var myRank     = {{%(PG_ALIASES)s.RANK}}
var myScending = {{%(PG_ALIASES)s.SCENDING}}
     
     function strlen(str)
     {
     var len;
     var i;
         len = 0;
         for (i=0;i<str.length;i++)
         {
           if (str.charCodeAt(i)>255) len+=2; else len++;
         }
         return len;
     }
    
function data_ck_new(sForm, sField){
	var temp="";
	var temp1="";
	var temp2="";
	var temp3;
	var fieldName;
	var fieldName1;
	var fieldNameB;
	var fieldNameC;
var db, dateformat;
	//
	//validate input data
	//
	for (var i=0; i<columns.indexes.length; i++) {
             fieldName = columns.indexes[i]
             fieldNameC = fieldName + "[0]"
	     if (_stripString(fieldNameC)==_stripString(sField)){break;}
          }
             temp=getElementValue(document[sForm][sField])
	     temp1=_stripString(temp)
	     setElementValue(document[sForm][sField],temp1)
	     temp3=strlen(temp1)
	     //
	     //data type checking
	     //
	     if(temp3 > 0)
	     {
	     if(d_type.columns[fieldName].type=="xText"|| d_type.columns[fieldName].type=="xString")
             {
		if (temp3 > d_type.columns[fieldName].charLen && d_type.columns[fieldName].charLen != 0)
		{ alert("你输入的内容长度已超过规定长度" + d_type.columns[fieldName].charLen + "." )
                  document[sForm][sField].focus()
		  return false
		}
	      }  
	     if(d_type.columns[fieldName].type=="xLong"||
	        d_type.columns[fieldName].type=="xInteger"){
                if(!isSignedInteger(temp1)){
			alert("数据输入错误...")
			document[sForm][sField].focus()
			return false;
                }
	     }
	     
	     if(d_type.columns[fieldName].type=="xFloat"){
		     if(!isFloat(temp1)){
			document[sForm][sField].focus()
			alert("数据输入错误...")
			return false;
		     } 
	     }
		
             if(d_type.columns[fieldName].type=="xDateTime"||
                d_type.columns[fieldName].type=="oraDateTime"||
                d_type.columns[fieldName].type=="gfDateTime"||
		d_type.columns[fieldName].type=="xDate"){
                db         = 	d_type.columns[fieldName].db
                dateformat = 	d_type.columns[fieldName].dateformat
                var valid = ckDateFormat99(sForm, sField, false, true, sField, db, dateformat)
		return valid;
            }
    }
    return true
}

    
     function data_ck(sForm, sField){
             var temp="";
             var temp1="";
             var temp2="";
             var temp3;
             var fieldName;
             var fieldNameC;
             var db, dateformat;
             
             //
             //validate input data
             //
             for (var i=0; i<columns.indexes.length; i++) {
                  fieldName = columns.indexes[i]
                  fieldNameC = fieldName + "[0]"
                  if (_stripString(fieldNameC)==_stripString(sField)){break;}
               }
                  ////temp=document[sForm][sField].value
                  temp=getElementValue(document[sForm][sField])
                  temp1=_stripString(temp)
                  setElementValue(document[sForm][sField],temp1)
                  temp3=strlen(temp1)
	     //alert(" temp: "+temp + " temp1:  " + temp1+ " temp3: " + temp3)
     
                  //
                  //data type checking
                  //
     
                  if(temp3 > 0)
                  {
                  if(d_type.columns[fieldName].type=="xText"||
                     d_type.columns[fieldName].type=="xString"){
                     if (temp3 > d_type.columns[fieldName].charLen && d_type.columns[fieldName].charLen != 0)
                     { alert("你输入的内容长度已超过规定长度" + d_type.columns[fieldName].charLen + "." )
                       document[sForm][sField].focus()
                       return false
                     }
                     else{
                            return true
                         }
                   } 
                  if(d_type.columns[fieldName].type=="xLong"||
                     d_type.columns[fieldName].type=="xInteger"){
                     if(!isSignedInteger(temp1)){
                             alert("数据输入错误...")
                             document[sForm][sField].focus()
                             return false;
                     }
                   //return isInteger(temp)
                   //isPositiveInteger(_stripString(document[sForm][sField].value))
                  }
                  
                  if(d_type.columns[fieldName].type=="xFloat"){
                          if(!isFloat(temp1)){
                             document[sForm][sField].focus()
                             alert("数据输入错误...")
                             return false;
                          } 
                  }
     
                  if(d_type.columns[fieldName].type=="xDateTime"||
                     d_type.columns[fieldName].type=="oraDateTime"||
                     d_type.columns[fieldName].type=="gfDateTime"||
                     d_type.columns[fieldName].type=="xDate"){
                     db         =         d_type.columns[fieldName].db
                     dateformat =         d_type.columns[fieldName].dateformat
                     
                     var valid = ckDateFormat99(sForm, sField, false, true, sField, db, dateformat)
                     return valid;
                 }
         }
         return true
     }
     
     
function final_ck(){
	var temp="";
	var temp1="";
	var temp2="";
	var temp3;
	var sFieldName;
        var sForm = 'topForm';
	var sField;
	var fieldName0;
	var fieldName;
	
var db, dateformat;
	//
	//validate input data
	//
for (var i=0; i<columns.indexes.length; i++) {
        fieldName = columns.indexes[i]
	fieldName0 = fieldName + "[0]"
             sField = fieldName0
	     temp=getElementValue(document[sForm][sField])
	     temp1=_stripString(temp)
	     setElementValue(document[sForm][sField], temp1)
	     //temp1=temp
	     temp3=strlen(temp1)
	     //
	     //data type checking
	     //
	     //if(temp1.length > 0)
	     if(temp3 > 0)
	     {
	     if(d_type.columns[fieldName].type=="xText"|| d_type.columns[fieldName].type=="xString")
             {
		if (temp3 > d_type.columns[fieldName].charLen && d_type.columns[fieldName].charLen != 0)
		{ alert("你输入的内容长度已超过规定长度" + d_type.columns[fieldName].charLen + "." )
                  document[sForm][sField].focus()
		  return false
		}
	      }  
	     if(d_type.columns[fieldName].type=="xLong"||
	        d_type.columns[fieldName].type=="xInteger"){
                if(!isSignedInteger(temp1)){
			alert("数据输入错误...")
			document[sForm][sField].focus()
			return false;
                }
	     }
	     
	     if(d_type.columns[fieldName].type=="xFloat"){
		     if(!isFloat(temp1)){
			document[sForm][sField].focus()
			alert("数据输入错误...")
			return false;
		     } 
	     }
		
             if(d_type.columns[fieldName].type=="xDateTime"||
                d_type.columns[fieldName].type=="oraDateTime"||
                d_type.columns[fieldName].type=="gfDateTime"||
		d_type.columns[fieldName].type=="xDate"){
                db         = 	d_type.columns[fieldName].db
                dateformat = 	d_type.columns[fieldName].dateformat
                var valid = ckDateFormat99(sForm, sField, false, true, sField, db, dateformat)
		if (valid == false){
			document[sForm][sField].focus()
		        return valid;
	        }
            }
         }
      }             
    return true
}

function ck4update()
{
enableInput();
if(final_ck()){ 
if (!notnull_fields()) return;
if (!gt_fields()) return;
setSearchStr('%(PG_ALIASES)s'); 
handleRequest('[%(PG_ALIASES)s.update,%(PG_ALIASES)s.mySearch ]', '%(MULTI_EDI_RP_PG)s', document.forms[0], 'frameList');
window.close();
 }
}


function gt_fields02(){
var GT_FIELDS1 = {{%(PG_ALIASES)s.GT_FIELDS1}}
var GT_FIELDS2 = {{%(PG_ALIASES)s.GT_FIELDS2}}
var ERR_MSG    = {{%(PG_ALIASES)s.ERR_MSG}}
var fl, ol，fname1, fname2, v1, v2, fieldName;
var ck1 = 0
var ck2 = 0
for (var i=0; i<GT_FIELDS1.length; i++)
{
 if (GT_FIELDS1.length == GT_FIELDS2.length)
 {
    fl=GT_FIELDS1[i].charAt(0).toUpperCase();
    ol=GT_FIELDS1[i].substring(1, GT_FIELDS1[i].length);
    fname1 = '%(PG_ALIASES)s.dbc'+fl+ol
    v1=_stripString(document.forms[0][fname1+'[0]'].value);
    fl=GT_FIELDS2[i].charAt(0).toUpperCase();
    ol=GT_FIELDS2[i].substring(1, GT_FIELDS2[i].length);
    fname2 = '%(PG_ALIASES)s.dbc'+fl+ol
    v2=_stripString(document.forms[0][fname2+'[0]'].value);
for (var j=0; j<columns.indexes.length; j++)
{
       fieldName = columns.indexes[j]
       if (fieldName==fname1){
          ck1 = 1
       }
       if (fieldName==fname2){
          ck2 = 1
       }
}
 
if (ck1*ck2!=1){
 // if we can not find two fields in the definition
 alert('Please check TABLE_SPEC.py for the configuration.')
 return false;
}

ck1 = 0;
ck2 = 0;

if(d_type.columns[fname1].type=="xDateTime"||
  d_type.columns[fname1].type=="oraDateTime"||
  d_type.columns[fname1].type=="gfDateTime"||
  d_type.columns[fname1].type=="xDate")
  {
   ck1 = 1
  }
if(d_type.columns[fname2].type=="xDateTime"||
  d_type.columns[fname2].type=="oraDateTime"||
  d_type.columns[fname2].type=="gfDateTime"||
  d_type.columns[fname2].type=="xDate")
  {
   ck2 = 1
  }
if (ck1*ck2!=1){
 alert('有的字段不是时间格式。Please check TABLE_SPEC.py for the configuration.')
 return false;
 } 
//v1 = new Date(2005,12,15);
//v2 = new Date(2005,12,25);
v1 = v1.split(' ')[0]
v2 = v2.split(' ')[0]
v1 = new Date(v1.split('-')[0],v1.split('-')[1],v1.split('-')[2]);
v2 = new Date(v2.split('-')[0],v2.split('-')[1],v2.split('-')[2]);
if (v2.getTime()>v1.getTime()) {
  document.forms[0][fname1+'[0]'].focus();
  if (ERR_MSG[i].length<1)
        alert('该输入框的时间不对！');
  else 
        alert(ERR_MSG[i]);
  return false;
 }
}
else
{
    alert("关于'大于'的校验，你的两个LIST中的表字段个数不一致！请检查TABLE_SPEC.py.")
    return false;
 }
}
 return true
}


function gt_fields(){
var GT_FIELDS1 = {{%(PG_ALIASES)s.GT_FIELDS1}}
var GT_FIELDS2 = {{%(PG_ALIASES)s.GT_FIELDS2}}
var ERR_MSG    = {{%(PG_ALIASES)s.ERR_MSG}}
var fl, ol，fname1, fname2, v1, v2, fieldName;
var ck1 = 0
var ck2 = 0
for (var i=0; i<GT_FIELDS1.length; i++)
{
 if (GT_FIELDS1.length == GT_FIELDS2.length)
 {
    fl=GT_FIELDS1[i].charAt(0).toUpperCase();
    ol=GT_FIELDS1[i].substring(1, GT_FIELDS1[i].length);
    fname1 = '%(PG_ALIASES)s.dbc'+fl+ol
    v1=_stripString(document.forms[0][fname1+'[0]'].value);
    fl=GT_FIELDS2[i].charAt(0).toUpperCase();
    ol=GT_FIELDS2[i].substring(1, GT_FIELDS2[i].length);
    fname2 = '%(PG_ALIASES)s.dbc'+fl+ol
    v2=_stripString(document.forms[0][fname2+'[0]'].value);
for (var j=0; j<columns.indexes.length; j++)
{
       fieldName = columns.indexes[j]
       if (fieldName==fname1){
          ck1 = 1
       }
       if (fieldName==fname2){
          ck2 = 1
       }
}
 
if (ck1*ck2!=1){
 // if we can not find two fields in the definition
 alert('Please check TABLE_SPEC.py for the configuration.')
 return false;
}

ck1 = 0;
ck2 = 0;

if(d_type.columns[fname1].type=="xDateTime"||
  d_type.columns[fname1].type=="oraDateTime"||
  d_type.columns[fname1].type=="gfDateTime"||
  d_type.columns[fname1].type=="xDate")
  {
   ck1 = 1
  }
if(d_type.columns[fname2].type=="xDateTime"||
  d_type.columns[fname2].type=="oraDateTime"||
  d_type.columns[fname2].type=="gfDateTime"||
  d_type.columns[fname2].type=="xDate")
  {
   ck2 = 1
  }

var cckk1 = 0;
var cckk2 = 0;
if(d_type.columns[fname1].type=="xInteger"||
  d_type.columns[fname1].type=="xFloat")
  {
   cckk1 = 1
  }
if(d_type.columns[fname2].type=="xInteger"||
  d_type.columns[fname2].type=="xFloat")
  {
   cckk2 = 1
   }
   
if (cckk1*cckk2==1){
var field1 = _stripString(getElementValue(document.forms[0][fname1+'[0]']))
var field2 = _stripString(getElementValue(document.forms[0][fname2+'[0]']))
if (field1.length > 0 && field2.length > 0){
   if(parseFloat(field2) > parseFloat(field1)){      
   document.forms[0][fname1+'[0]'].focus();
   if (ERR_MSG[i].length<1)
        alert('该输入框的数据小了!');
   else 
      alert(ERR_MSG[i]);
   return false   
   }
   return true
}
else{
  document.forms[0][fname1+'[0]'].focus();
  if (ERR_MSG[i].length<1)
        alert('数据输入不对!');
  else 
  alert(ERR_MSG[i]);

   return false   
  }
}

if (ck1*ck2==1){
//v1 = new Date(2005,12,15);
//v2 = new Date(2005,12,25);
v1 = v1.split(' ')[0]
v2 = v2.split(' ')[0]
v1 = new Date(v1.split('-')[0],v1.split('-')[1],v1.split('-')[2]);
v2 = new Date(v2.split('-')[0],v2.split('-')[1],v2.split('-')[2]);
if (v2.getTime()>v1.getTime()) {
  document.forms[0][fname1+'[0]'].focus();
  if (ERR_MSG[i].length<1)
        alert('该输入框的时间不对！');
  else 
        alert(ERR_MSG[i]);
  return false;
  }
 return true
}
  alert("TABLE_SPEC中配置的比较字段不是同一类型！请检查TABLE_SPEC.py.")
  return false
}
else
{
    alert("关于'大于'的校验，你的两个LIST中的表字段个数不一致！请检查TABLE_SPEC.py.")
    return false;
}
}
 return true
}

function notnull_fields(){
var NOTNULL_FIELDS = {{%(PG_ALIASES)s.NOTNULL_FIELDS}}
var ERR_MSG_NULL    = {{%(PG_ALIASES)s.ERR_MSG_NULL}}
var fl, ol，fname1, v1;
for (var i=0; i<NOTNULL_FIELDS.length; i++)
{
    fl=NOTNULL_FIELDS[i].charAt(0).toUpperCase();
    ol=NOTNULL_FIELDS[i].substring(1, NOTNULL_FIELDS[i].length);
    fname1 = '%(PG_ALIASES)s.dbc'+fl+ol
    v1=_stripString(document.forms[0][fname1+'[0]'].value);
    if (v1.length < 1)
    {
       document.forms[0][fname1+'[0]'].focus();
       if (ERR_MSG_NULL[i].length<1)
            alert('该输入框不能为空！');
       else 
            alert(ERR_MSG_NULL[i]);
       return false;
    }
}
return true
}


function ckInsert(theDBO,  responseId, submitForm, frameName) {
var op='EQ';
//var op='GT';
var valueB = "";
var value, fieldName, fieldName0;
var s=""; 
var searchStr="";

if (final_ck()){
for (var i=0; i<columns.indexes.length; i++) {
        fieldName = columns.indexes[i]
	fieldName0 = fieldName + "[0]"
	
        if(d_type.columns[fieldName].column=="DBPrimaryKey"||
	    d_type.columns[fieldName].column=="DBCompositeKey"||
            d_type.columns[fieldName].column=="DBUnique"){
	if (document['topForm'][fieldName0]) {
	     value = getElementValue(document['topForm'][fieldName0]);
	     if(value.length == 0){
		     document['topForm'][fieldName0].focus();
		     alert("该字段不能为空!");
	             return;
	     }
	     else {
		  s = columns.getSearchString(fieldName, op, value, valueB);
                  if (s != "") {
                           if (searchStr == "") searchStr = s;
                           else searchStr += " AND " + s;
                        }
	     }
          }
        }
        else{
	     //d_type.columns[fieldName].column=="DBIdentity"
	     //since searchStr = ""
	     // submitForm[theDBO+".searchString"].value= searchStr
	     //so, submitForm[theDBO+".searchString"].value= ""
	}
    }

if (!notnull_fields()) return;
if (!gt_fields()) return;

    submitForm[theDBO+".searchString_ck_duplicate"].value= searchStr
    submitForm[theDBO+".searchString"].value= searchStr
for (var i=0; i<columns.indexes.length; i++) {
        fieldName = columns.indexes[i]
	fieldName0 = fieldName + "[0]"
       // if identity field is there, the value from "create_on" field is alway in "searchStr"
       // that means "searchStr" is not empty at all
  if (document.forms[0][theDBO+".dbcCreate_on[0]"]){
         // this always put current inserted record on top
         submitForm[theDBO+".mySqlOrderBy"].value= "create_on DESC"
	 genCreateOn();
         fieldName = theDBO+'.dbcCreate_on'
         fieldName0 = theDBO+'.dbcCreate_on'+'[0]'
	 value = getElementValue(document['topForm'][fieldName0]);
         //searchStr = columns.getSearchString(fieldName, op, value, valueB);
         //submitForm[theDBO+".searchString"].value= searchStr
	 submitForm[theDBO+".searchString"].value= " create_on > " + "'"+timeStr3()+"'"
         handleRequest('['+theDBO+'.insert1]', responseId, submitForm, frameName)
         return;
	  }
	}
     handleRequest('['+theDBO+'.insert1]', responseId, submitForm, frameName) 
 }
}


function ckPrint(theDBO,  responseId, submitForm, frameName,action) {
var op='EQ';
//var op='GT';
var valueB = "";
var value, fieldName, fieldName0;
var s=""; 
var searchStr="";
var fieldName1 = theDBO+'.dbcCreate_on'+'[0]'
	
if (final_ck()){
for (var i=0; i<columns.indexes.length; i++) {
        fieldName = columns.indexes[i]
	fieldName0 = fieldName + "[0]"
	
	if (document['topForm'][fieldName0]) {
	     value = getElementValue(document['topForm'][fieldName0]);
	if (fieldName1 != fieldName0){	  
		  s = columns.getSearchString(fieldName, op, value, valueB);
                  if (s != "") {
                           if (searchStr == "") searchStr = s;
                           else searchStr += " AND " + s;
		  }
	      }
        }
}
submitForm[theDBO+".searchString"].value= searchStr
if(searchStr.length<=0)
{  return false}
else {return true}

     //handleRequest('['+theDBO+'.'+action+']', responseId, submitForm, frameName) 
 }
}

function ckAll(theDBO,  responseId, submitForm, frameName,action){
if (ckPrint(theDBO,  responseId, submitForm, frameName,action))
{
   window.open('{{XBOP_WWW_ROOT}}/system/application/preloadit.htm','attesa','width=500,height=100');
   //handleRequest('['+theDBO+'.'+action+']', responseId, submitForm, frameName); 
   //doSearchOBC99(theDBO, 0, %(PG_SCH_LEN)s, responseId, true, document.forms[0], document.forms[1],frameName,action)
   doSearchOBC99(theDBO, 0, 600, responseId, true, document.forms[0], document.forms[1],frameName,action)
}
else {
     alert('您必须先输入您的查询条件。');
}
}



function ckInsert22(theDBO,  responseId, submitForm, frameName) {

var op='EQ';
var valueB = "";
var value, fieldName, fieldName0;
var s=""; 
var searchStr="";

if (final_ck()){
for (var i=0; i<columns.indexes.length; i++) {
        fieldName = columns.indexes[i]
	fieldName0 = fieldName + "[0]"
       // if identity field is there, the value from "create_on" field is alway in "searchStr"
       // that means "searchStr" is not empty at all
	%(identity_ck_js)s
	
        if(d_type.columns[fieldName].column=="DBPrimaryKey"||
	    d_type.columns[fieldName].column=="DBCompositeKey"||
            d_type.columns[fieldName].column=="DBUnique"){
	if (document['topForm'][fieldName0]) {
	     value = getElementValue(document['topForm'][fieldName0]);
	     if(value.length == 0){
		     document['topForm'][fieldName0].focus();
		     alert("该字段不能为空!");
	             return;
	     }
	     else {
                  //op = "EQ"
                  //valueB = "" 
		  s = columns.getSearchString(fieldName, op, value, valueB);
                  if (s != "") {
                           if (searchStr == "") searchStr = s;
                           else searchStr += " AND " + s;
                        }
	     }
          }
        }
    }
    	
     submitForm[theDBO+".searchString_ck_duplicate"].value= searchStr
    submitForm[theDBO+".searchString"].value= searchStr
    //handleRequest('['+theDBO+'.myinsert]',  'whxh001/his/mSites_query/rp_multi_edi_dboSites_query.html', document.forms[0], 'frameList')
    // 
    // duplicated records are not checked here yet. myinsert will do this checking.
    // 
     //handleRequest('['+theDBO+'.insert1, '+theDBO+'.mySearch]', responseId, submitForm, frameName) 
     //
     //mySearch method in theDBO is included in insert1 method
     //
     handleRequest('['+theDBO+'.%(PY_INSERT_METHOD)s1]', responseId, submitForm, frameName) 
 }
}


    
     
     function reset_iframe(){
      if(self.name=="basefrm"){
      parent.document.getElementById("botfrm").style.height="0%%";
      parent.document.getElementById("basefrm").style.height="100%%";
      }
     }
//    
// the following two functions are called by popUpwindows for the "big" field
// 
        
     function getWhichField(){
         return document.forms[0]["currentField"].value
     }
       
     
     function getFieldChineseTitle(){
         return document.forms[0]["chineseTitle"].value
     }
      
     
     
     function saveWhichField(fieldName,chineseTitle){
     document.forms[0]["currentField"].value = fieldName
     document.forms[0]["chineseTitle"].value = chineseTitle
     }
     
     
     
     function inputWindow(fieldName,chineseTitle,whichWindow){
           var features = "toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=no, width=520,height=400,left=50,top=23"
           saveWhichField(fieldName,chineseTitle)
	if (whichWindow == "pop_up_input")
           window.open("{{XBOP_WWW_ROOT}}/%(my_prj_dir)s/popUpInput.html", '',  features)
	else if (whichWindow == "upload")
           window.open("{{XBOP_WWW_ROOT}}/upload.htm", '',  features)
        else
            alert("inputWindow() javascript: whichWindow must be either 'popUpInput' or 'upload'") 
     }
     
function summationCK(f1, f2, f3){
var field1 = _stripString(getElementValue(document.forms[0][f1]))
var field2 = _stripString(getElementValue(document.forms[0][f2]))
if (!data_ck('topForm', f1) || !data_ck('topForm', f2)){return false}
  if (field1.length > 0 && field2.length > 0){
     document.forms[0][f3].value = parseFloat(field1) * parseFloat(field2)      
      }
      return true;
     }
    
function cleanInput(sForm, postFix){
var _postFix = postFix 
var fieldName
var fieldName0
   for (var i=0; i<columns.indexes.length; i++) {
        fieldName = columns.indexes[i]
        fieldName0 = fieldName + _postFix
        if (document[sForm][fieldName0]) {
            setElementValue(document[sForm][fieldName0], "")
         }
      }
}

function getSubMenu(baseObj,subObj,selectedValue, field_name){
enableInput();
%(getSubMenuStr)s
////document.forms[0][subObj+".searchString"].value = field_name + "='"+selectedValue+"'"
////handleRequest("'["+baseObj+".dataTransfer,"+ subObj +".search"+"]'",'{{pageId}}', document.forms[0], target='frameArea')
}

function IsNumeric(sText)
{
   var ValidChars = "0123456789.";
   var IsNumber=true;
   var Char;
   for (i = 0; i < sText.length && IsNumber == true; i++) 
      { 
      Char = sText.charAt(i); 
      if (ValidChars.indexOf(Char) == -1) 
         {
         IsNumber = false;
         }
      }
   return IsNumber;
}

%(identity_js_function)s
%(_FUNCTION1)s
%(_FUNCTION2)s
%(_FUNCTION3)s
%(_FUNCTION4)s
%(_FUNCTION5)s
function  get_info_from_other_table (baseObj,subObj,baseInputName, tbl_field){
//
// preparing searchString for first sub_drop_menu
//	
var v_search = ""
%(V_SEARCH)s
////var  v1 = getElementValue(document.forms[0]["$oCourses_info.dbcCollege[0]"])
////setElementValue(document.forms[0]["computer_lab.mSub_drop_menu.dboSub_drop_menu.searchString"],"field_name='"+v1+"'")
////if (v1.length > 0) v_search = v_search + ",computer_lab.mSub_drop_menu.dboSub_drop_menu.search"
//
// preparing searchString for second sub_drop_menu
//
////////var  v2 = getElementValue(document.forms[0]["$oCourses_info.dbcCollege[0]"])
////////setElementValue(document.forms[0]["computer_lab.mSub_drop_menu.dboSub_drop_menu.searchString"],"field_name='"+v2+"'")
////////if (v2.length > 0) v_search = v_search + ",computer_lab.mSub_drop_menu.dboSub_drop_menu.search"
	
var selectedValue = _stripString(document.forms[0][baseInputName].value)
document.forms[0][subObj+".searchString"].value = tbl_field + "='"+selectedValue+"'"
if (v_search.length < 1)
	handleRequest("'["+baseObj+".dataTransfer,"+ subObj +".search"+"]'",'{{pageId}}', document.forms[0], target='frameArea')
else
   handleRequest("'["+baseObj+".dataTransfer,"+ subObj +".search"+v_search+"]'",'{{pageId}}', document.forms[0], target='frameArea')
}

function disableInput(){
var fieldName;
               for (var jj = 0;  jj < columns.indexes.length; jj++)
               {
                     fieldName = columns.indexes[jj]
                     if(d_type.columns[fieldName].column=="DBPrimaryKey"|| d_type.columns[fieldName].column=="DBCompositeKey"|| d_type.columns[fieldName].column=="DBUnique"|| d_type.columns[fieldName].column=="DBIdentity") {
                     //primary_key is always disabled. 
                          document["topForm"][fieldName+"[0]"].disabled = true
                     }
               }
}

function enableInput(){
var fieldName;
               for (var jj = 0;  jj < columns.indexes.length; jj++)
               {
                     fieldName = columns.indexes[jj]
                     if(d_type.columns[fieldName].column=="DBPrimaryKey"|| d_type.columns[fieldName].column=="DBCompositeKey"|| d_type.columns[fieldName].column=="DBUnique"|| d_type.columns[fieldName].column=="DBIdentity") {
                     //primary_key is always disabled. 
                          document["topForm"][fieldName+"[0]"].disabled = false
                     }
               }
} 

function dataStore(v1,v2){
document.forms[0]["dataStore"].value = v1
document.forms[0]["jsStore"].value = v2
}
     </script>
     </head>
<body  bgColor=#dee7ff leftMargin=0 topMargin=0 onLoad="javascript:reset_iframe(); %(DISABLE_INPUT)s %(identity_genOrderId)s">
     
<form name="topForm" action="{{CGI_HANDLER}}" method="POST">
<input type=hidden name="SID" value="{{SID}}">
<input type=hidden name="pageId" value="{{pageId}}">
<input type=hidden name="gRequestIds" value="[]">
<input type=hidden name="requestIds" value="[]">
<input type=hidden name="responseId" value="{{pageId}}">
<input type=hidden name="%(PG_ALIASES)s.searchOffset" value="0">
<!--
<input type=hidden name="%(PG_ALIASES)s.searchLength" value="%(PG_SCH_LEN)s">
-->
<input type=hidden name="%(PG_ALIASES)s.searchLength" value="600">
<input type=hidden name="%(PG_ALIASES)s.searchString" value="">
<input type=hidden name="%(PG_ALIASES)s.searchString_ck_duplicate" value="{{%(PG_ALIASES)s.searchString_ck_duplicate}}">
<input type=hidden name="%(PG_ALIASES)s.checked" value="[0]">
<input type=hidden name = "%(PG_ALIASES)s.rowCount" value="{{%(PG_ALIASES)s.rowCount}}">
<input type=hidden name = "%(PG_ALIASES)s.searchFrom" value="{{%(PG_ALIASES)s.searchFrom}}">
<input type=hidden name = "%(PG_ALIASES)s.searchTo" value="{{%(PG_ALIASES)s.searchTo}}">
<input type=hidden name = "%(PG_ALIASES)s.searchTo" value="{{%(PG_ALIASES)s.searchTo}}">
<input type=hidden name = "%(PG_ALIASES)s.mySqlOrderBy" value="">
%(DROPDOWN_MENU_SEARCHSTRING)s
%(SUB_DROPDOWN_MENU_SEARCHSTRING)s
<input type=hidden name = "currentField" value="">
<input type=hidden name = "chineseTitle" value="">
<input type=hidden name="_browserDateTime_" value="">
<input type=hidden name = "dataStore" value="">
<input type=hidden name = "jsStore" value="">
 %(identity_hidden_input_fields)s
 %(page_title_image)s
 %(page_title)s
 %(page_buttons)s
<!--
     <TR height="10"><TD> &nbsp;</td></tr>
-->
     <TR><TD >
     <table border="0" cellspacing="0" cellpadding="0">
     %(DISPLAY_2_IN_1)s
     <tr>
 %(page_update_button)s
     <td><input type=hidden name="whichRow" value=""></td>
          <td> &nbsp;</td>
          <td> &nbsp;</td>
          <td> &nbsp;</td>
     </tr>
     </table>
<!--
%(EXCEL_PRT)s
-->
     </TD></TR></TABLE>
<script>
function onButtonClick(itemId,itemValue) {
	if (itemId =="0_save")
                ckInsert('%(PG_ALIASES)s', '%(RP_PG)s', document.forms[0], 'frameList')
        else if (itemId =="0_clean")
	  cleanInput('topForm', '[0]')
        else if (itemId =="0_search"){
	  //doSearchOBC88('%(PG_ALIASES)s', 0, %(PG_SCH_LEN)s, '%(RP_PG)s',  document.forms[0], document.forms[0],'frameList')
	  doSearchOBC88('%(PG_ALIASES)s', 0, 600, '%(RP_PG)s',  document.forms[0], document.forms[0],'frameList')
        }
        else if (itemId =="0_takeall") {
	  //doSearchOBC99('%(PG_ALIASES)s', 0, %(PG_SCH_LEN)s, '%(RP_PG)s', false, document.forms[0], document.forms[0],'frameList')
	  doSearchOBC99('%(PG_ALIASES)s', 0, 600, '%(RP_PG)s', false, document.forms[0], document.forms[0],'frameList')
        }
	else if (itemId =="0_advanced")
          handleRequestTarget('[]','%(SEARCH_PG)s', document.forms[0], target='_search')
	else
	    alert("错误。")
	};
%(TOOLBAR)s
</script>
     </form>
     
<form name="submitForm" action="{{CGI_HANDLER}}" method=POST>
<input type=hidden name="SID" value="{{SID}}">
<input type=hidden name="pageId" value="{{pageId}}">
<input type=hidden name="gRequestIds" value="[]">
<input type=hidden name="requestIds" value="[]">
<input type=hidden name="responseId" value="{{pageId}}">
<input type=hidden name="%(PG_ALIASES)s.searchString" value="{{%(PG_ALIASES)s.searchString}}">
<input type=hidden name="%(PG_ALIASES)s.searchOffset" value="0">
<!--
<input type=hidden name="%(PG_ALIASES)s.searchLength" value="%(PG_SCH_LEN)s">
-->
<input type=hidden name="%(PG_ALIASES)s.searchLength" value="600">
<input type=hidden name="L.CODE" value="{{session.DEF.L.CODE}}">
<input type=hidden name="C.CODE" value="{{session.DEF.C.CODE}}">
<input type=hidden name="C.SYM" value="{{session.DEF.C.SYM}}">
<input type=hidden name="C.XR" value="{{session.DEF.C.XR}}">
<input type=hidden name="M.SET0.MF" value="{{session.DEF.M.SET0.MF}}">
<input type=hidden name="M.SET0.CF" value="{{session.DEF.M.SET0.CF}}">
<input type=hidden name="M.SET0.DF" value="{{session.DEF.M.SET0.DF}}">
<input type=hidden name="_browserDateTime_" value="">
</form>
</body>
     </html>
            """
            
            all_td_html["all_tmpl"] = all_tmpl




def _lp_td_html():

       xRank = """ 
<td class="fld_name"><script language=javascript>
var %(FIELD_NAME)s_rank = {"name": "%(PG_ALIASES)s.%(FIELD_NAME)s.RANK",
            "values": %(_myRank)s,
            "captions": %(_myRank)s,
            "defaultSelected": "",
            "withNone": true,
            "size": "1",
            "multiple": false,
            "onChange": "",
            "onFocus": "",
            "onBlur": ""}
document.write(generateDYNA_SELECT( %(FIELD_NAME)s_rank))
</script>
</td>
       """
       
       xASC="""
<td class="fld_name"><script language=javascript>
var  %(FIELD_NAME)s_asc = {"name": "%(PG_ALIASES)s.%(FIELD_NAME)s.ASC",
            "values": myScending,
            "captions": ['升序','降序'],
            "defaultSelected": "",
            "withNone": true,
            "size": "1",
            "multiple": false,
            "onChange": "",
            "onFocus": "",
            "onBlur": ""}
document.write(generateDYNA_SELECT(%(FIELD_NAME)s_asc))
</script>
</td>
       """
       lp_td_html["xRank"] = xRank
       lp_td_html["xASC"] = xASC
	
       xLong_field = """
            <td nowrap class="fld_name"> %(CHINESE_TITLE)s &nbsp;&nbsp</td> 
            <td class="fld_name"><input type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]" 
            onChange = "return data_ck_new('topForm', '%(PG_ALIASES)s.%(FIELD_NAME)s[0]')" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value=""     size="20"></td> 
            """
       lp_td_html["xLong"] = xLong_field
       lp_td_html["xInteger"] = xLong_field
       lp_td_html["xFloat"] = xLong_field
      

      
       xText_field = """
<td nowrap class="fld_name"> %(CHINESE_TITLE)s</td>
<td class="fld_name"><input type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]"
 onChange = "return data_ck_new('topForm', '%(PG_ALIASES)s.%(FIELD_NAME)s[0]')" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value=""   size="20"></td>
     """
  
       lp_td_html["xText"] = xText_field
       lp_td_html["xString"] = xText_field

       xDate_field = """
            <td nowrap class="fld_name"> %(CHINESE_TITLE)s &nbsp;&nbsp</td>
            <td class="fld_name"><input type=text name="%(PG_ALIASES)s.%(FIELD_NAME)s[0]"
 ondblclick= "scwShow(this,this);"  onChange = "return data_ck_new('topForm', '%(PG_ALIASES)s.%(FIELD_NAME)s[0]')" onkeypress = "enterKey(event, 'topForm', '%(PG_ALIASES)s.%(FIELD_NAME_1)s[0]')" value="" size="20"></td>
    """
       
       lp_td_html["xDate"] = xDate_field
       lp_td_html["xDateTime"] = xDate_field
       lp_td_html["oraDateTime"] = xDate_field

       lp_td_html["lp_hidden_fields"] = """<input type=hidden name="%(PG_ALIASES)s.%(FIELD_NAME)s" value="">"""

       js_columns = """\
columns.add("%(PG_ALIASES)s.%(FIELD_NAME)s", "%(FIELD_NAME2)s", "%(DATA_TYPE_LIST)s",  "%(CHARLEN)s", "%(DATABASE)s","%(DATEFORMAT)s")
               """
       
       lp_td_html["js_columns"] = js_columns

       js_types  = """\
d_type.add("%(PG_ALIASES)s.%(FIELD_NAME)s", "%(DBCOLUMNS)s", "%(COL_TYPES)s", "%(CHARLEN)s", "%(DATABASE)s","%(DATEFORMAT)s")
                   """
		   
       lp_td_html["js_types"] = js_types

       lp_tmpl = """
<html>
<head>
<meta name="generator" content="X*bop Table Wizard">
<meta http-equiv="pragma" content="no-cache">
<meta http-equiv="content-type" content="text/html; charset={{session.DEF.L.CHARSET}}">
<title> %(PG_ZXZINC)s </title>
<!-- Aliases
"%(PG_ALIASES)s": "%(PG_ALIASES_DEF)s"
-->
<style type="text/css">
<!--
-->
</style>
<link href="{{XBOP_WWW_ROOT}}/css/xbop_studio_css.css" rel="stylesheet" type="text/css">
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/scw.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/form.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/search.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/formcheckers.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/form_special.js"></script>
<!--
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/datePick.js"></script>
-->
<script language="JavaScript" src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/overlib_mini.js"></script>
<script language="JavaScript" src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/printSpecial.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/dynaSelect.js"></script>
<script language=javascript src="{{XBOP_WWW_ROOT}}/%(jslib_dir)s/mysearch2.js"></script>
<script language=javascript>
               // ********************************************************************
               // Searchable fields.
               // RDBColumns is an object defined in the search.js lib. It is used for
               // collecting searchable form fields and creating search string that
               // can be used by X*bop search method.
               // *******************************************************************
               var columns = new RDBColumns()
	       %(JS_COLUMNS)s

               // By default, DateTime data are quoted using ' sign.
               // If you are using Microsoft Access, uncomment the following line.
               // DATETIME_QUOTATION_SYMBOL = "#"

               var d_type = new RDBColumns()
               %(JS_TYPES)s

var myRank     = {{%(PG_ALIASES)s.RANK}}
var myScending = {{%(PG_ALIASES)s.SCENDING}}

// this function is defined in jslib/form_special.js
function strlen(str)
{
var len;
var i;
    len = 0;
    for (i=0;i<str.length;i++)
    {
      if (str.charCodeAt(i)>255) len+=2; else len++;
    }
    return len;
}


function data_ck_new(sForm, sField){
	var temp="";
	var temp1="";
	var temp2="";
	var temp3;
	var fieldName;
	var fieldName1;
	var fieldNameB;
	var fieldNameC;
var db, dateformat;
	//
	//validate input data
	//
	for (var i=0; i<columns.indexes.length; i++) {
             fieldName = columns.indexes[i]
             fieldNameC = fieldName + "[0]"
	     if (_stripString(fieldNameC)==_stripString(sField)){break;}
          }
             temp=getElementValue(document[sForm][sField])
	     temp1=_stripString(temp)
	     setElementValue(document[sForm][sField],temp1)
	     temp3=strlen(temp1)
	     //
	     //data type checking
	     //
	     if(temp3 > 0)
	     {
	     if(d_type.columns[fieldName].type=="xText"|| d_type.columns[fieldName].type=="xString")
             {
		if (temp3 > d_type.columns[fieldName].charLen && d_type.columns[fieldName].charLen != 0)
		{ alert("你输入的内容长度已超过规定长度" + d_type.columns[fieldName].charLen + "." )
                  document[sForm][sField].focus()
		  return false
		}
	      }  
	     if(d_type.columns[fieldName].type=="xLong"||
	        d_type.columns[fieldName].type=="xInteger"){
                if(!isSignedInteger(temp1)){
			alert("数据输入错误...")
			document[sForm][sField].focus()
			return false;
                }
	     }
	     
	     if(d_type.columns[fieldName].type=="xFloat"){
		     if(!isFloat(temp1)){
			document[sForm][sField].focus()
			alert("数据输入错误...")
			return false;
		     } 
	     }
		
             if(d_type.columns[fieldName].type=="xDateTime"||
                d_type.columns[fieldName].type=="oraDateTime"||
                d_type.columns[fieldName].type=="gfDateTime"||
		d_type.columns[fieldName].type=="xDate"){
                db         = 	d_type.columns[fieldName].db
                dateformat = 	d_type.columns[fieldName].dateformat
                var valid = ckDateFormat99(sForm, sField, false, true, sField, db, dateformat)
		return valid;
            }
    }
    return true
}


function reset_iframe(){
// if(self.name=="basefrm"){
parent.parent.document.getElementById("basefrm").style.height="100%%"
parent.parent.document.getElementById("botfrm").style.height="0%%"
//	 }
}


function final_ck(){
	var temp="";
	var temp1="";
	var temp2="";
	var temp3;
	var sFieldName;
        var sForm = 'topForm';
	var sField;
	var fieldName0;
	var fieldName;
	
var db, dateformat;
	//
	//validate input data
	//
for (var i=0; i<columns.indexes.length; i++) {
        fieldName = columns.indexes[i]
	fieldName0 = fieldName + "[0]"
             sField = fieldName0
	     temp=getElementValue(document[sForm][sField])
	     //temp1=_stripString(temp)
	     temp1=temp
	     temp3=strlen(temp1)
	     //
	     //data type checking
	     //
	     //if(temp1.length > 0)
	     if(temp3 > 0)
	     {
	     if(d_type.columns[fieldName].type=="xText"|| d_type.columns[fieldName].type=="xString")
             {
		if (temp3 > d_type.columns[fieldName].charLen && d_type.columns[fieldName].charLen != 0)
		{ alert("你输入的内容长度已超过规定长度" + d_type.columns[fieldName].charLen + "." )
                  document[sForm][sField].focus()
		  return false
		}
	      }  
	     if(d_type.columns[fieldName].type=="xLong"||
	        d_type.columns[fieldName].type=="xInteger"){
                if(!isSignedInteger(temp1)){
			alert("数据输入错误...")
			document[sForm][sField].focus()
			return false;
                }
	     }
	     
	     if(d_type.columns[fieldName].type=="xFloat"){
		     if(!isFloat(temp1)){
			document[sForm][sField].focus()
			alert("数据输入错误...")
			return false;
		     } 
	     }
		
             if(d_type.columns[fieldName].type=="xDateTime"||
                d_type.columns[fieldName].type=="oraDateTime"||
                d_type.columns[fieldName].type=="gfDateTime"||
		d_type.columns[fieldName].type=="xDate"){
                db         = 	d_type.columns[fieldName].db
                dateformat = 	d_type.columns[fieldName].dateformat
                var valid = ckDateFormat99(sForm, sField, false, true, sField, db, dateformat)
		if (valid == false){
			document[sForm][sField].focus()
		        return valid;
	        }
            }
         }
      }             
    return true
}


function ckInsert(theDBO,  responseId, submitForm, frameName) {

var op='EQ';
var valueB = "";
var value, fieldName, fieldName0;
var s=""; searchStr="";

if (final_ck()){
for (var i=0; i<columns.indexes.length; i++) {
        fieldName = columns.indexes[i]
	fieldName0 = fieldName + "[0]"

        %(identity_ck_js)s

	
        if(d_type.columns[fieldName].column=="DBPrimaryKey"||
	    d_type.columns[fieldName].column=="DBCompositeKey"||
            d_type.columns[fieldName].column=="DBUnique"){
	if (document['topForm'][fieldName0]) {
	     value = getElementValue(document['topForm'][fieldName0]);
	     if(value.length == 0){
		     document['topForm'][fieldName0].focus();
		     alert("该字段不能为空!");
	             return;
	     }
	     else {
                  //valueB = "" 
		  s = columns.getSearchString(fieldName, op, value, valueB);
                  if (s != "") {
                           if (searchStr == "") searchStr = s;
                           else searchStr += " AND " + s;
                        }
	     }
          }
        }
    }
     //submitForm[theDBO+".searchString_ck_duplicate"].value= searchStr
    // 
    // duplicated records are not checked here yet. myinsert will do this checking.
    // 
     //handleRequest('['+theDBO+'.insert1, '+theDBO+'.mySearch]', responseId, submitForm, frameName)
     //
     //mySearch method in theDBO is included in insert1 method
     //
     handleRequest('['+theDBO+'.%(PY_INSERT_METHOD)s]', responseId, submitForm, frameName) 
 }
}

function inputWindow(fieldName,chineseTitle){
           var features = "toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=no, width=520,height=400,left=50,top=23"
           saveWhichField(fieldName,chineseTitle)
           window.open("{{XBOP_WWW_ROOT}}/%(my_prj_dir)s/popUpInput.html", '',  features)
     }
     
function summationCK(f1, f2, f3){
     var field1 = _stripString(getElementValue(document.forms[0][f1]))
     var field2 = _stripString(getElementValue(document.forms[0][f2]))
     if (!data_ck('topForm', f1) || !data_ck('topForm', f2)){return false}
     if (field1.length > 0 && field2.length > 0){
        document.forms[0][f3].value = parseFloat(field1) * parseFloat(field2)      
      }
      return true;
     }
   
function cleanInput(sForm, postFix){
var _postFix = postFix 
var fieldName
var fieldName0
   for (var i=0; i<columns.indexes.length; i++) {
        fieldName = columns.indexes[i]
        fieldName0 = fieldName + _postFix
        if (document[sForm][fieldName0]) {
            setElementValue(document[sForm][fieldName0], "")
         }
      }
}
</script>
 </head>
 <body style="FONT-SIZE: 10pt" bgColor=#dee7ff leftMargin=0 background="" topMargin=0 marginheight="0" marginwidth="0" onLoad="javascript:reset_iframe()">
 <form name="topForm" action="{{CGI_HANDLER}}" method="POST">
 <input type=hidden name="SID" value="{{SID}}">
 <input type=hidden name="pageId" value="{{pageId}}">
 <input type=hidden name="gRequestIds" value="[]">
 <input type=hidden name="requestIds" value="[]">
 <input type=hidden name="responseId" value="{{pageId}}">
<input type=hidden name="%(PG_ALIASES)s.searchLength" value="%(PG_SCH_LEN)s">
<input type=hidden name="%(PG_ALIASES)s.offSet" value="0">

<input type=hidden name="%(PG_ALIASES)s.searchString" value="">

<input type=hidden name="%(PG_ALIASES)s.checked" value="[0]">
<input type=hidden name = "%(PG_ALIASES)s.rowCount" value="{{%(PG_ALIASES)s.rowCount}}">
<input type=hidden name = "%(PG_ALIASES)s.searchFrom" value="{{%(PG_ALIASES)s.searchFrom}}">
<input type=hidden name = "%(PG_ALIASES)s.searchTo" value="{{%(PG_ALIASES)s.searchTo}}">
<input type=hidden name = "currentField" value="">
<input type=hidden name = "chineseTitle" value="">
<input type=hidden name="_browserDateTime_" value="">
<table style="FONT-SIZE: 10pt" cellSpacing=0 cellPadding=0 bgColor=#dee7ff border=0>
<TBODY>

<tr>
<td colspan = 12>
<TABLE borderColor=#000000 height=21  cellSpacing=0 cellPadding=0 bgColor=#dee7ff border=0>
<TBODY>
<TR vAlign=bottom align=middle>
<TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
<A class="menu_linked_name"  href="javascript:ckInsert('%(PG_ALIASES)s', '%(RP_PG)s', document.forms[0], 'frameList')">新&nbsp增</A> </TD>
<TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
<A class="menu_linked_name" href="javascript:cleanInput('topForm','[0]')">清&nbsp;除</A></TD>
<TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
<A class="menu_linked_name" href="javascript:doSearchOBC88('%(PG_ALIASES)s', 0, %(PG_SCH_LEN)s, '%(RP_PG)s',  document.forms[0], document.forms[1],'frameList')">查&nbsp;找</A></TD>
<TD width=54 background={{XBOP_WWW_ROOT}}/graphics/oa_images/face/page_button.gif bgColor=#dee7ff>
<A class="menu_linked_name"  href="javascript:handleRequestTarget2('[]','%(SEARCH_PG)s', document.forms[0], target='basefrm')">详&nbsp;查</A></TD>

<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td class="fld_name">{{%(PG_ALIASES)s.duplicated}}</td>
</TR>
</TBODY></table>
</tr></td>
%(PG_MAINBODY)s
</TBODY></TABLE>
          </form>
          <form name="submitForm" action="{{CGI_HANDLER}}" method=POST>
          <input type=hidden name="SID" value="{{SID}}">
          <input type=hidden name="pageId" value="{{pageId}}">
      <input type=hidden name="gRequestIds" value="[]">
      <input type=hidden name="requestIds" value="[]">
      <input type=hidden name="responseId" value="{{pageId}}">
<input type=hidden name="%(PG_ALIASES)s.sqlOrderBy">
<input type=hidden name="%(PG_ALIASES)s.mySqlOrderBy">
          <input type=hidden name="%(PG_ALIASES)s.searchString" value="{{%(PG_ALIASES)s.searchString}}">
          <input type=hidden name="%(PG_ALIASES)s.searchOffset" value="0">
          <input type=hidden name="%(PG_ALIASES)s.searchLength" value="%(PG_SCH_LEN)s">
          <input type=hidden name="L.CODE" value="{{session.DEF.L.CODE}}">
          <input type=hidden name="C.CODE" value="{{session.DEF.C.CODE}}">
          <input type=hidden name="C.SYM" value="{{session.DEF.C.SYM}}">
          <input type=hidden name="C.XR" value="{{session.DEF.C.XR}}">
          <input type=hidden name="M.SET0.MF" value="{{session.DEF.M.SET0.MF}}">
          <input type=hidden name="M.SET0.CF" value="{{session.DEF.M.SET0.CF}}">
          <input type=hidden name="M.SET0.DF" value="{{session.DEF.M.SET0.DF}}">
          <input type=hidden name="_browserDateTime_" value="">
          </form>
	  
          </body>
          </html>
       
           """
       
       lp_td_html["lp_tmpl"] = lp_tmpl



def runAll():
    _lp_td_html()
    _rp_td_html()
    _rp_sr_td_html()
    _all_td_html()
    parser()
    mkdir()
    gen_lp_pg()
    gen_rp_pg()	

if (__name__=='__main__'):
    _lp_td_html()
    _rp_td_html()
    _rp_sr_td_html()
    parser()
    mkdir()
    gen_lp_pg()
    gen_rp_pg()
    #print lp_tmpl
    
