############################
#      TEAM NUCLEUS -(23)  #
#  vandit.jain@amdocs.com  #
############################
#For PDF to Text atom we are using the Python package PDFMiner. 
#This atom reads the PDF directly from remote server. 
#Input ==> PDF Filename
#Configuration ==> An input configuration file that contains the following information:
#   - Remote Serve IP
#   - Remote Server username
#   - Remote server password
#   - Remote server directory path
#Output ==> A text stream representing the data of input file

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.pdfdevice import TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.utils import set_debug_logging
import time
import io
import paramiko
import json
import os
import re

# OpenFaaS handler method
def handle(req):

    if (re.search('ATOM_ERROR:', req)):
        return req

    rsrcmgr = PDFResourceManager(caching=True)
   
    # A temporary file that holds the text data. This will be removed
    outfile = '/root/pdf2txt_' + str(time.time()) + '.txt'
    outfp = io.open(outfile, 'wt', errors='ignore')
    
    laparams = LAParams()

    with open('function/config.json') as con:
        pdf_file_details= json.load(con)
    
    device = TextConverter(rsrcmgr, outfp, laparams=laparams)

    #Following code uses paramiko ssh client to read the remote pdf file

    ssh = paramiko.SSHClient() #Define value 'ssh' as calling the paramiko.sshclient
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    #Must come before connect line to add hosts to known_hosts

    try:
        ssh.connect(hostname = pdf_file_details['remote_address'], username = pdf_file_details['user_name'], password = pdf_file_details['password']) 
    except:
        ssh.close()
        device.close()
        outfp.close()
        return ("ATOM_ERROR: pdf-to-text Unable to open connection to remote file server\n")
 
    sftp_client = ssh.open_sftp()
    try:    
        fp = sftp_client.file(pdf_file_details['pdf_path'] + req,'rb')
    except:
        ssh.close()
        device.close()
        outfp.close()
        return ("ATOM_ERROR: pdf-to-text Unable to open file\n")
        
    process_pdf(rsrcmgr, device, fp, caching=True, check_extractable=True)

    #Cleanup 
    fp.close()
    device.close()
    outfp.close()
    ssh.close()

    #Prepare output string from temp file
    with open(outfile) as f:
        data = f.read()

    #Remove temp file
    os.remove(outfile)
    return data
