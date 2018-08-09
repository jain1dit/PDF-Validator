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

import json

# OpenFaaS handler method
def handle(req):

    #TODO: Below code can be moved to another atom once parallel/persistence issue around JESI is resolved
    merge_json = json.loads(req)
    db_values = merge_json['db_json'][0]
    pdf_values = merge_json['txt_json'][0]

    final_result = ''
    diffkeys = [k for k in db_values if db_values[k] != pdf_values[k]]

    #If there is any mismatch in any attribute, diffkeys will be non-empty
    if diffkeys:
        final_result = 'PDF Validation Fail \n'
    else:
        final_result = 'PDF Validation Success \n'

    for k in diffkeys:
        #print(k, ':', db_values[k], '->', pdf_values[k])
        final_result = final_result + k + ' : ' + db_values[k] + ' -> ' + pdf_values[k] + '\n'

    return final_result

