import sys
from json import dumps as json_dumps
from json import loads as json_loads
import paramiko


# helper method
def validate_input(json_input):
    '''
    Validate that all 3 input keys exists in the input:
        remote_ip, remote_user,
        remote_password
    returned value:
        Pass --> None
        Failure --> dictionary with details about missing keys
            example: {"Status":"Failure", "Message":"Invalid input",
                        "Missing-keys-list":["remote_user"]}
    '''
    key_list = ['remote_ip', 'remote_user',
                'remote_password']
    error_list = []
    error_result = None
    is_valid = True

    for input_key in key_list:
        is_valid = True
        try:
            val = json_input[input_key]
            if type(val) is not str:
                is_valid = False
            elif len(val) == 0:
                is_valid = False
        except KeyError:
            is_valid = False

        if(not is_valid):
            error_list.append(input_key)

    if len(error_list) > 0:
        error_result = {'Status': 'Failure'}
        error_result['Message'] = 'Missing input keys'
        error_result['Missing-keys-list'] = error_list

    return error_result


# main Atom method
def check_system(json_input):
    '''
    check the status of the CPU/Memory on remote machine
            Success -> JSON response with status Success
                {"system_status":cpu_output}
            Failure --> JSON response with Failure message
    '''
    error_details = None
    result = None
    # validations = validate_input(json_input)
    # if validations is not None:
    # exist with error "Missing input keys"
    # return dumps(validations)  # return JSON format
    remote_ip = json_input['remote_ip']
    remote_user = json_input['remote_user']
    remote_pass = json_input['remote_password']
    # cpu_command = "ps aux | sort -nrk 3,3 | head -n 10"
    cpu_command = "ps -eo pcpu,pid,user,args | tail -n +2 | sort -rnk 2 | head"
    mem_command = "ps -eo pmem,pid,user,args | tail -n +2 | sort -rnk 3 | head"
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(remote_ip, username=remote_user, password=remote_pass)
        cpu_output = []
        mem_output = []
        stdin, stdout, stderr = client.exec_command(cpu_command)
        stdout1 = stdout.readlines()
        stdin, stdout, stderr = client.exec_command(mem_command)
        stdout2 = stdout.readlines()
        # out = chan.recv_exit_status()
        for line in stdout1:
            cpu_output.append(line)
        for line in stdout2:
            mem_output.append(line)
    except (IOError,
            paramiko.ssh_exception.AuthenticationException,
            paramiko.ssh_exception.BadAuthenticationType,
            paramiko.ssh_exception.SSHException
            ):
            error_details = sys.exc_info()
    finally:
            client.close()  # close SSH client
    if error_details is None:
        # result = {"CPU consuming": cpu_output, "MEM consuming": mem_output}
        result = {"resource": "Top 10 processes",
                  "CPU": cpu_output, "MEM": mem_output}
    else:
        result = {'Status': 'Failure'}
        result['Error occurred'] = "{} {}".format(
         str(error_details[0]),
         str(error_details[1])
         )
    # return JSON format
    return json_dumps(result)


# OpenFaaS handler method
def handle(req):
    json_req = json_loads(req)
    # print(check_system(json_req))
    return check_system(json_req)
