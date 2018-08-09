import sys
from json import dumps as json_dumps
from json import loads as json_loads
import paramiko
from lib.validations import input_validations


# constant keys list for input validation
INPUT_KEYS = ['remote_ip', 'remote_port', 'remote_user',
              'remote_password', 'remote_file']


# main Atom method
def remote_copy(json_input):
    '''
    SFTP copy of a file from remote server and retutn its content as text
    input: a dictionary containing below information
        {
            "remote_ip":"",
            "remote_port":"",
            "remote_user":"",
            "remote_password":"",
            "remote_file":""
        }
    result:
        Success -> free text response
        Failure --> JSON response with relevant message
    '''
    # Two values tuple:
    # 1. boolean flag
    # 2. missing keys list
    check = input_validations.all_keys_exists(json_input, INPUT_KEYS)

    if not check[0]:
        result = {'status': 'Failure'}
        result['missing-keys-list'] = check[1]
        return json_dumps(result)  # return JSON format

    # error details, contains: ( error_type, error_message, error_traceback )
    error_details = None
    transport_trg = None
    sftp_trg = None
    file_to_read = None

    trg_ip = json_input['remote_ip']
    trg_port = int(json_input['remote_port'])  # cast to int
    trg_user = json_input['remote_user']
    trg_pass = json_input['remote_password']
    trg_file = json_input['remote_file']

    try:
        transport_trg = paramiko.Transport((trg_ip, trg_port))
        transport_trg.connect(username=trg_user, password=trg_pass)
        sftp_trg = paramiko.SFTPClient.from_transport(transport_trg)

        # open the target file on the target location for writing
        # file_to_read <class 'paramiko.sftp_file.SFTPFile'>
        file_to_read = sftp_trg.open(trg_file, 'r')
        # file_text <class 'bytes'>
        file_text = file_to_read.read()  # extract all characters in the file
        file_text = str(file_text)  # convet to string
        file_text = file_text.replace('\\n', '<br>')

    except (IOError,
            paramiko.ssh_exception.AuthenticationException,
            paramiko.ssh_exception.BadAuthenticationType,
            paramiko.ssh_exception.SSHException
            ):
        error_details = sys.exc_info()

    finally:
        # handle closing all remote connections
        if(sftp_trg is not None):
            sftp_trg.close()  # close SFTP client
        if(transport_trg is not None):
            transport_trg.close()  # close transport
        if(file_to_read is not None and not file_to_read.closed):
            file_to_read.close()  # close file

    if error_details is None:
        return file_text
    else:
        result = {'Status': 'Failure'}
        result['Error occurred'] = "{} {}".format(
            str(error_details[0]),
            str(error_details[1])
            )

    return json_dumps(result)  # return JSON format


# OpenFaaS handler method
def handle(req):
    json_req = json_loads(req)
    return remote_copy(json_req)
