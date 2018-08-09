from json import loads as json_loads
from json import dumps as json_dumps
from lib.database import oracle  # requires cx_Oracle import to be available


# Global constant
SELECT_OPEN_SESSION_QUERY = "SELECT \
    sid, inst_id, serial#, username, status, schemaname, \
    machine, osuser, port, process, module, \
    sql_id, sql_exec_start, state \
FROM gv$session \
WHERE schemaname!='SYS'"


# main Atom method
def retrieve_open_sessions(json_input):
    '''
    runs an SQL query retrieving open sessions using the views: gv$session
    Input structre:
        {
         "connection": {
            "host": "", "ip": "", "port": "",
            "sid": "", "user": "", "password": ""
            }
        }
    '''
    db_conn = oracle.db_connect(json_input)
    db_cursor = db_conn.cursor()
    db_cursor.execute(SELECT_OPEN_SESSION_QUERY)
    formatted_result = oracle.result_to_json(db_cursor)
    db_conn.close()  # close connection to DB

    # create dictionaly to be converted to JSON response
    response = {"result_set_count": formatted_result[0]}
    response["session_details"] = formatted_result[1]

    return json_dumps(response)


def handle(req):
    # result = {"found": False}
    json_req = json_loads(req)
    print(retrieve_open_sessions(json_req))
