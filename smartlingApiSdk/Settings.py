#!/usr/bin/python
# -*- coding: utf-8 -*-




import logging
import sys
from .version import version

class Settings:
    logLevel = logging.INFO
    logPath  = "smartling-api-sdk-python.log"
    requestTimeoutSeconds = 30
    userAgent = "Python SDK client v%s py:%s" % (version, sys.version.split()[0])

# Configure logging
logging.basicConfig(
    level=Settings.logLevel,
    format='[%(asctime)s] %(levelname)-2s %(name)-4s %(message)s',
    filename=Settings.logPath,
    filemode='a'
)
