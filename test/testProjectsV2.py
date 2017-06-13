#!/usr/bin/python
# -*- coding: utf-8 -*-


''' Copyright 2012 Smartling, Inc.
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
'''

import os
import sys
import time
import zipfile
import io
from datetime import date

lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from smartlingApiSdk.SmartlingProjectsApiV2 import SmartlingProjectsApiV2
from smartlingApiSdk.ProxySettings import ProxySettings
from nose.tools import assert_equal
from smartlingApiSdk.version import version
from smartlingApiSdk.Credentials import Credentials
from smartlingApiSdk.Constants import FileTypes

class testProjectsV2(object):

    CODE_SUCCESS_TOKEN = 'SUCCESS'

    def setUp(self):
        credentials = Credentials() #Gets your Smartling credetnials from environment variables
        self.MY_USER_IDENTIFIER = credentials.MY_USER_IDENTIFIER
        self.MY_USER_SECRET = credentials.MY_USER_SECRET
        self.MY_PROJECT_ID = credentials.MY_PROJECT_ID
        self.MY_LOCALE = credentials.MY_LOCALE

        #needed for testProjects
        self.MY_ACCOUNT_UID = credentials.MY_ACCOUNT_UID

        useProxy = False
        if useProxy :
            proxySettings = ProxySettings("login", "password", "proxy_host", "proxy_port or None")
        else:
            proxySettings = None
        self.papi = SmartlingProjectsApiV2(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, proxySettings)

        print("setUp", "OK", "\n\n\n")

    def tearDown(self):        
        print("tearDown", "OK")

    def testProjects(self):
        if self.MY_ACCOUNT_UID == "CHANGE_ME":
            print("can't test projects api call, set self.MY_ACCOUNT_UID or export SL_ACCOUNT_UID=*********")
            return
        res, status = self.papi.projects(self.MY_ACCOUNT_UID)

        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)

        projects = [x['projectId'] for x in res.data.items]

        assert_equal(True, self.MY_PROJECT_ID in projects)
        print("testProjects", "OK")

    def testProjectDetails(self):
        res, status = self.papi.project_details(self.MY_PROJECT_ID)

        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        assert_equal(self.MY_PROJECT_ID, res.data.projectId)

        print("testProjectDetails", "OK")

