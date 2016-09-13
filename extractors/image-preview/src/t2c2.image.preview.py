#!/usr/bin/env python

import logging
import os
import sys
import subprocess
import tempfile
import re
from t2c2_image_preview_config import *
import pyclowder.extractors as extractors
import dm3reader_v072

"""

to install pyclowder :

pip install git+https://opensource.ncsa.illinois.edu/stash/scm/cats/pyclowder.git

"""



def main(rabbitmqURL):
    global extractorName, messageType, rabbitmqExchange, logger

    #set logging
    logging.basicConfig(format='%(levelname)-7s : %(name)s -  %(message)s', level=logging.INFO)
    logging.getLogger('pymedici.extractors').setLevel(logging.DEBUG)
    logger = logging.getLogger(extractorName)
    logger.setLevel(logging.DEBUG)

    #connect to rabbitmq
    extractors.connect_message_bus(extractorName=extractorName,
                                   messageType=messageType,
                                   processFileFunction=process_file,
                                   rabbitmqExchange=rabbitmqExchange,
                                   rabbitmqURL=rabbitmqURL)

# ----------------------------------------------------------------------
# Process the file and upload the results
def process_file(parameters):
    global imageBinary, imageType, imageThumbnail, imagePreview
    global previewBinary, previewType, previewCommand

    print(parameters['inputfile'])

    if imageBinary:
        execute_command(parameters, imageBinary, imageThumbnail, imageType, True)
        execute_command(parameters, imageBinary, imagePreview, imageType, False)
    if previewBinary:
        execute_command(parameters, previewBinary, previewCommand, previewType, False)

def execute_command(parameters, binary, commandline, ext, thumbnail=False):
    global logger

    (fd, tmpfile)=tempfile.mkstemp(suffix='.' + ext)
    try:
        # close tempfile
        os.close(fd)
        file_name = None
        try:
            file_name = parameters['filename']
        except:
            file_name = parameters['inputfile']
        if ".dm3" in file_name:
            input_file = dm3reader_v072.make_pgm_tempfile(parameters['inputfile'])
            commandline = commandline.replace('@BINARY@', binary)
            commandline = commandline.replace('@INPUT@', input_file)
            commandline = commandline.replace('@OUTPUT@', tmpfile)
        #inputFile = parameters['inputfile']
        # replace some special tokens
        else:
            commandline = commandline.replace('@BINARY@', binary)
            commandline = commandline.replace('@INPUT@', parameters['inputfile'])
            commandline = commandline.replace('@OUTPUT@', tmpfile)

        # split command line
        p = re.compile(r'''((?:[^ "']|"[^"]*"|'[^']*')+)''')
        commandline = p.split(commandline)[1::2]


        # execute command
        x = subprocess.check_output(commandline, stderr=subprocess.STDOUT)
        if x:
            logger.debug(binary + " : " + x)

        if(os.path.getsize(tmpfile) != 0):
            # upload result
            if thumbnail:
                extractors.upload_thumbnail(thumbnail=tmpfile, parameters=parameters)
                extractors.upload_preview(previewfile=tmpfile,parameters=parameters)
            else:
                extractors.upload_preview(previewfile=tmpfile, parameters=parameters)
    except subprocess.CalledProcessError as e:
        logger.error(binary + " : " + str(e.output))
        raise
    finally:
      try:
        os.remove(tmpfile)
      except:
        pass

if __name__ == "__main__":
    rabbitmqURL="amqp://guest:guest@" + sys.argv[1] + ":5672/%2f"
    main(rabbitmqURL)
