from json import dumps as json_dumps
from json import loads as json_loads

file_name_server = '/usr/local/servers_login_details.json'
file_name_database = '/usr/local/database_login_details.json'
file_name_app = '/usr/local/app_login_details.json'


def retrieve_server_login_details(hostname, username):
    '''
    Retrieve login details for a host and a specific application
    mutiple applications can be under same server
        input: two path params, host_name & application_name
        output: JSON result containing ip, user and password
    '''

    result_dictionary = {}
    apps_info_file = open(file_name_server).read()
    apps_info_dict = json_loads(apps_info_file)

    if hostname in apps_info_dict.keys():
        application_details = apps_info_dict[hostname]
        if username in application_details.keys():
            result_dictionary = application_details[username]

    return json_dumps(result_dictionary)


def retrieve_database_login_details(sid):
    '''
    Retrieve login details by a database SID
    only a single connection details can be under single SID
        input: one path param <sid>
        output: JSON result containing host, ip, port, user, password and sid
    '''
    result_dictionary = {}
    apps_info_file = open(file_name_database).read()
    apps_info_dict = json_loads(apps_info_file)

    if sid in apps_info_dict.keys():
        result_dictionary = apps_info_dict[sid]

    return json_dumps(result_dictionary)


def retrieve_application_login_details(app_id):
    '''
    Retrieve login details for a specific application
        input: one parameter , application_name
        output: JSON result containing ip, user and password , etc ...
    '''
    result_dictionary = {}
    apps_info_file = open(file_name_app).read()
    apps_info_dict = json_loads(apps_info_file)

    if app_id in apps_info_dict.keys():
        result_dictionary = apps_info_dict[app_id]

    return json_dumps(result_dictionary)


def handle(req):
    '''
    {
    "app_id": "",
    "sid": "",
    "machine": {
    "hostname": "",
    "username": ""
    }
    }
    '''
    json_req = json_loads(req)
    if 'app_id' in json_req.keys():
        app_id = json_req['app_id']
        if app_id != '':
            return retrieve_application_login_details(app_id)

    if 'sid' in json_req.keys():
        sid = json_req['sid']
        if sid != '':
            return retrieve_database_login_details(sid)

    if 'machine' in json_req.keys():
        machine = json_req['machine']
        if 'hostname' in machine.keys() and 'username' in machine.keys():
            hostname = machine['hostname']
            username = machine['username']
            return retrieve_server_login_details(hostname, username)

    return '{"error_message":"Missing or Wrong input"}'

