from json import JSONDecodeError
from json import loads as json_loads
import json2html
import sys


# Global constants
TABLE_CSS_OLD = '<table border="1">'
TABLE_CSS_NEW = '<table border="1" cellpadding="5">'


# Main atom function
def conver_json2html(json_string):
    json2html_converter = json2html.Json2Html()

    try:
        converted = json2html_converter.convert(json_string)
        return converted.replace(TABLE_CSS_OLD, TABLE_CSS_NEW)

    except JSONDecodeError:
        exc_type, value, exc_traceback = sys.exc_info()
        return 'JSON convertion failed: ' + str(exc_type) + str(value)


# OpenFaaS handler method
def handle(req):
    json_req = json_loads(req)
    return conver_json2html(json_req)
