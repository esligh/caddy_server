#coding:utf-8
'''
Created on 

@author: ThinkPad
'''

PAGE_SIZE = 10 ;
#collection type 
COLLECTION_TYPE_TEXT = '10' ; 
COLLECTION_TYPE_TEXTPIC = '20' ; 
COLLECTION_TYPE_IMAGE = '30';


#server response status  
OPER_SUCCESS = "1000";
OPER_EXCEPTION = "2000";
OPER_INVALID = "-1" ; 


#register STATUS 
REG_SUCCESS = "1101";
REG_INVALIDEMAIL = "1110";
REG_SENDEMAIL = "1103";
REG_SAMENAME = "1104";
REG_SAMEEMAIL = "1105";


#login status 
LOGIN_SUCCESS  = "610"
LOGIN_NFUSER  = "621"
LOGIN_PWDWRONG = "622"

#collection status 
COLLETION_NFRECORD = "1200"
DEL_COLLECTION_DENIESS = "1210";
DEL_COLLECTION_SUCCESS = "1201"


#upload status  
UPLOAD_SUCCESS = "1400"
UPLOAD_FAILD = "1410"
FILE_TOOLARGE = "1414"
FILE_NOPEMITTION = "1415"


if __name__ == '__main__':
    pass