#For reading values from a database for specific fields
#This atom reads a configuration file for field and table related details
#and directly connects to remote database and prepares the JSON output
#
#TODO: Original design included building Database JSON in parallel to PDF-to-text JSON.
#Tihs atom is intended to be completely generic and can be used in several business flows 
#where data needs to be retreived from a remote database (Specific fields from a particular table)
#However, due to JESI issues around persistence in parallel flows we need to leave that as future enhancement


#Input ==> A JSON file containing all necessary attributes as derived from PDF file
#Configuration ==> An input configuration file that contains the following information:
#   - Remote database details
#   - Table and field details
#Output ==> This atom checks the JSON prepared from database with input JSON and compares all attributes.
#           If the value matches the atom declares that the PDF is valid, else it gives a fail message printing
#           the attributes that did not match with value from databse followed by value from PDF

import cx_Oracle
import json
import re

# OpenFaaS handler method
def handle(req):

    if (re.search('ATOM_ERROR:', req)):
        return req

    try:
        with open('function/config.json') as con:
            jsn = json.load(con)
    except:
        return ("ATOM_ERROR: get-db-to-json: Invalid Configuration file\n")
    
    fetch_field = ''
    txt_output = json.loads(req)
    
    for j in jsn['field_details']:
        fetch_field = fetch_field + j['db_col_name'] + ', '
        
    fetch_field = fetch_field[:-2]
        
    ip = jsn['database_details'][0]['ip']
    port = jsn['database_details'][0]['port']
    SID = jsn['database_details'][0]['sid']
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)

    #Preparing database connection
    try:
        db = cx_Oracle.connect(jsn['database_details'][0]['db_name'], jsn['database_details'][0]['password'], dsn_tns)
    except:
        return ("ATOM_ERROR: get-db-to-json: Unable to connect to Billing database\n") 
    cur = db.cursor()

    #Prepare the query

    #TODO: For the pelatom we have taken a scenario of single table, with a single primary key.
    #This can be enhanced to be more generic in the future

    query = 'select ' + fetch_field + ' from ' + jsn['database_details'][0]['table_name'] + ' where ' + jsn['database_details'][0]['table_key'] + ' = :tab_key'
    cur.prepare(query)
    cur.execute(None, tab_key = txt_output[jsn['field_details'][0]['entity']])
    db_result = cur.fetchall()
    db.close()
    i=0
    db_values = {}

    if not db_result:
       return ("ATOM_ERROR: get-db-to-json:No record returned from Billing database\n")

    #Converting extracted data to string for JSON comparison 
    #if  db_result:
    for j in jsn['field_details']:
        db_values[j['entity']] = str(db_result[0][i])
        i+=1


    #TODO: Below code can be moved to another atom once parallel/persistence issue around JESI is resolved
    final_result = ''
    diffkeys = [k for k in db_values if db_values[k] != txt_output[k]]

    #If there is any mismatch in any attribute, diffkeys will be non-empty
    if diffkeys:
        final_result = 'PDF Validation Fail for \n'
    else:
        final_result = 'PDF Validation Success \n'

    for k in diffkeys:
        #print(k, ':', db_values[k], '->', txt_output[k])
        final_result = final_result + k + ' : ' + db_values[k] + ' (DB Value) -> ' + txt_output[k] + ' (PDF Value)\n'

    return final_result 
