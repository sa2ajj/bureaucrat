#!/usr/bin/env python

import logging
import pika
import sys
import os.path
import json

from optparse import OptionParser

LOG = logging.getLogger(__name__)

def parse_cmdline():
    """Parse command line options."""

    parser = OptionParser()
    parser.add_option("-e", "--event", dest="event",
                      help="event name")
    parser.add_option("-d", "--data", dest="data",
                      default="{}",
                      help="event data")

    (options, args) = parser.parse_args()

    if options.event is None:
        LOG.error("Mandatory option 'event' is missing")
        sys.exit(1)

    return options

def main():
    """Entry point."""

    options = parse_cmdline()

    parameters = pika.ConnectionParameters(host="localhost")

    body = json.loads(options.data)
    body["event"] = options.event

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_publish(exchange='',
                          routing_key='bureaucrat_events',
                          body=json.dumps(body),
                          properties=pika.BasicProperties(
                              delivery_mode=2
                          ))
    connection.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
