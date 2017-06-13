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

lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from smartlingApiSdk.SmartlingProjectsApiV2 import SmartlingProjectsApiV2
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

def assert_equal(a,b):
    if a != b :
        err = "Assertion Failed: '%s' != '%s'" % (a,b)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testProjetcsV2(object):

    CODE_SUCCESS_TOKEN = 'SUCCESS'
            

    def setUp(self):
        credentials = Credentials() #Gets your Smartling credetnials from environment variables
        self.MY_USER_IDENTIFIER = credentials.MY_USER_IDENTIFIER
        self.MY_USER_SECRET = credentials.MY_USER_SECRET
        
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


    def testProjects(self, projectIdToCheck):
        if self.MY_ACCOUNT_UID == "CHANGE_ME":
            print("can't test projects api call, set self.MY_ACCOUNT_UID or export SL_ACCOUNT_UID=*********")
            return
        res, status = self.papi.projects(self.MY_ACCOUNT_UID)
        
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        
        projects = [x['projectId'] for x in res.data.items]

        assert_equal(True, projectIdToCheck in projects)
        print("testProjects", "OK")

    def testProjectDetails(self, projectId):
        res, status = self.papi.project_details(projectId)
        
        assert_equal(200, status)
        assert_equal(self.CODE_SUCCESS_TOKEN, res.code)
        assert_equal(projectId, res.data.projectId)
        
        print("testProjectDetails", "OK")
        
        
t = testProjetcsV2()
t.setUp()
projectId = Credentials().MY_PROJECT_ID
t.testProjects(projectId)
t.testProjectDetails( projectId )
t.tearDown()