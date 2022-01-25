#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012-2021 Smartling, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this work except in compliance with the License.
 * You may obtain a copy of the License in the LICENSE file, or at:
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
"""

import sys
import logging
import threading

isPython3 = sys.version_info[:2] >= (3, 0)


class Logger(object):
    collected = []

    def __init__(self, name, loglevel, logfile="smartling-api-sdk-python.log"):
        logFormat = ('[%(asctime)s] %(levelname)-2s %(name)-4s %(message)s')

        logging.basicConfig(filename=logfile, filemode='a', format=logFormat, level=logging.DEBUG)
        self.sys_write = sys.stdout.write
        self.loglevel = loglevel
        name = self.addThreadName(name)
        self.logger = logging.getLogger(name)

    def addThreadName(self, name):
        threadName = threading.current_thread().name
        if 'MainThread' != threadName:
            name += "-" + threadName
        return name

    def write(self, message):
        self.sys_write(message)

        hasNewline = '\n' in message
        if message.startswith("\n"):
            message = message[1:]

        if isPython3:
            self.collected.append(message)
            if not hasNewline:
                return
            message = ''.join(self.collected)
            self.collected = []

        self.logger.log(self.loglevel, message)

    def flush(self):
        if self.collected:
            message = ''.join(self.collected)
            self.logger.info(message)
