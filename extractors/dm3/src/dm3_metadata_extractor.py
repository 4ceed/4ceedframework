'''
Created on 14 Mar 2013

@author: Constantinos Sophocleous
'''

'''
modified by Todd Nicholson, June 2015. The purpose is now to get metadata from TEM and SEM electron microscope
files.
'''

#!/usr/bin/env python
import pika
import sys
import logging
import json
import traceback
import requests
import tempfile
import subprocess
import os
import itertools
import re
import codecs
import time
import collections
import dm3reader_v072
import dm3_metadata_config
from dm3_metadata_config import*


def main(rabbitmqIP):
    global logger

    # name of receiver
    receiver='t2c2.metadata'

    # configure the logging system
    logging.basicConfig(format="%(asctime)-15s %(name)-10s %(levelname)-7s : %(message)s", level=logging.WARN)
    logger = logging.getLogger(receiver)
    logger.setLevel(logging.DEBUG)

    if len(sys.argv) < 8:
        logger.info("Input RabbitMQ server address, followed by RabbitMQ server port,  RabbitMQ username, RabbitMQ password, Medici REST API key, RabbitMQ exchange name and whether SSL is to be used to communicate with the RabbitMQ messaging service (true of false).")
        logger.info("If SSL is used, add the path to the key certificate file and the path to the key file.")
        #sys.exit()
        #commented out - we are now using a separate config file rather than command line arguments

    global playserverKey
    #playserverKey = sys.argv[5]
    playserverKey = dm3_metadata_config.playserverKey

    global exchangeName
    #exchangeName = sys.argv[6]
    exchangeName = dm3_metadata_config.exchange_name

#    if(sys.argv[1].endswith(os.sep)):
#        sys.argv[1] = (sys.argv[1])[:-1]

    # connect to rabbitmq using input username and password
    #credentials = pika.PlainCredentials(sys.argv[3], sys.argv[4])
    credentials = pika.PlainCredentials(dm3_metadata_config.credentials_name,
                                        dm3_metadata_config.credentials_pass)
    #host = sys.argv[1]
    #port = int(sys.argv[2])
    # host = dm3_metadata_config.host
    host = rabbitmqIP
    port = dm3_metadata_config.port

    #useSsl = (sys.argv[7] == "true")
    useSsl = (dm3_metadata_config.use_ssl == "true")
    if useSsl:
        sslCertPath = sys.argv[8]
        sslKeyPath = sys.argv[9]

        ssl_options = {"certfile": sslCertPath, "server_side": True, "keyfile": sslKeyPath}

        parameters = pika.ConnectionParameters(credentials=credentials, ssl=useSsl, ssl_options=ssl_options, port=port, host=host)
    else:
        parameters = pika.ConnectionParameters(credentials=credentials, port=port, host=host)
    connection = pika.BlockingConnection(parameters)

    # connect to channel
    channel = connection.channel()

    # declare the exchange
    channel.exchange_declare(exchange=exchangeName, exchange_type='topic', durable=True)

    # declare the queue
    channel.queue_declare(queue=receiver, durable=True)

    # Set prefetch-count to 1 to avoid crashing due to interleaved frames and also send jobs to idle workers first
    channel.basic_qos(prefetch_count=1)

    # connect queue and exchange
    channel.queue_bind(queue=receiver, exchange=exchangeName, routing_key='*.file.image.#')

    # create listener
    channel.basic_consume(on_message, queue=receiver, no_ack=False, consumer_tag="t2c2_metadata_extractor")

    # start listening
    logger.info("Waiting for messages. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    # close connection
    connection.close()

def create_dm3_metadata(fileid,host,fpath,tags,*args):
    jsonArray = json.dumps(tags)

    logger.debug(jsonArray)

    headers={'Content-Type': 'application/json'}
    url=host + '/api/files/' + fileid + '/metadata' + '?key=' + playserverKey
    r = requests.post(url, headers=headers, data=jsonArray, verify=False)
    r.raise_for_status()

    logger.debug("[%s] created metadata.", fileid)



def on_message(channel, method, header, body):
    global logger
    statusreport = {}
    try:
        # parse body back from json
        jbody=json.loads(body)

        if not 'wasRaw' in jbody['flags']:
            host=jbody['host']
            fileid=jbody['id']
            intermediatefileid=jbody['intermediateId']

            # for status reports
            statusreport['file_id'] = fileid
            statusreport['extractor_id'] = 'T2C2_Metadata'

            # print what we are doing
            logger.debug("[%s] started processing", fileid)

            # fetch data
            statusreport['status'] = 'Downloading image file.'
            statusreport['start'] = time.strftime('%Y-%m-%dT%H:%M:%S')
            channel.basic_publish(exchange='',
                         routing_key=header.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         header.correlation_id),
                         body=json.dumps(statusreport))
            url=host + '/api/files/' + intermediatefileid + '?key=' + playserverKey
            r=requests.get(url, stream=True, verify=False)
            r.raise_for_status()

            fd,fpath = tempfile.mkstemp()
            f = open(fpath, "wb")
            for chunk in r.iter_content(chunk_size=10*1024):
                f.write(chunk)
            f.close()
            os.close(fd)
            tags = []
            pgm_file = None
            """
            the code below extracts the metadata tags and the pgm_file, a greyscale image of the .dm3 file
            """


            fileName = jbody['filename']



            if ".dm3" in fileName:
                try:
                    tags = dm3reader_v072.extract_dm3_metadata(fpath,dump=False)
                    #below - this is the short list of tags - not a full list
                    #tags = dm3reader_v072.get_metadata_shortlist(**tags)
                    #TO DO - make short or long list either separate extractors, or add an field that
                    #indicates which we want
                except:
                    pass


            # create metadata
            statusreport['status'] = 'Extracting metadata.'
            statusreport['start'] = time.strftime('%Y-%m-%dT%H:%M:%S')
            channel.basic_publish(exchange='',
                         routing_key=header.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         header.correlation_id),
                         body=json.dumps(statusreport))
            try:
                if (type(tags) == dict) or (type(tags) == collections.OrderedDict):
                    create_dm3_metadata(fileid,host,fpath,tags,None)
                else:
                    pass
            except:
                logger.info("Failed to upload dm3 metadata")

            logger.debug("[%s] finished processing", fileid)
        else:
            logger.info("Image metadata to be extracted from raw image. Aborting processing.");

        # Ack
        channel.basic_ack(method.delivery_tag)

    except subprocess.CalledProcessError as e:
        logger.exception("[%s] error processing [exit code=%d]\n%s", fileid, e.returncode, e.output)
        statusreport['status'] = 'Error processing.'
        statusreport['start'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        channel.basic_publish(exchange='',
                routing_key=header.reply_to,
                properties=pika.BasicProperties(correlation_id = \
                                                header.correlation_id),
                body=json.dumps(statusreport))
        channel.basic_ack(method.delivery_tag)
    except Exception as e:
        logger.exception("[%s] error processing:\n%s", fileid, e.message)
        statusreport['status'] = 'Error processing.'
        statusreport['start'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        channel.basic_publish(exchange='',
                routing_key=header.reply_to,
                properties=pika.BasicProperties(correlation_id = \
                                                header.correlation_id),
                body=json.dumps(statusreport))
        if('r' in vars()):
            if(r.status_code == 500 or r.status_code == 503):
                channel.basic_nack(method.delivery_tag, multiple=False, requeue=True)
            else:
                channel.basic_ack(method.delivery_tag)
        else:
            channel.basic_ack(method.delivery_tag)
    finally:
        statusreport['status'] = 'DONE.'
        statusreport['start'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        channel.basic_publish(exchange='',
                         routing_key=header.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                         header.correlation_id),
                         body=json.dumps(statusreport))
        try:
            os.remove(fpath)
        except OSError:
            pass
        except UnboundLocalError:
            pass



if __name__ == "__main__":
    rabbitmqIP = sys.argv[1]
    main(rabbitmqIP)

