
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

import os
import sys
import time, datetime

sys.path += [os.path.abspath('../'), os.path.abspath('../../')]  # allow to import ../smartlingApiSdk.api

import smartlingApiSdk
from smartlingApiSdk.api.StringsApi import StringsApi
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

# example of custom user-agent setup
from smartlingApiSdk.Settings import Settings
Settings.userAgent = "My Custom User Agent"

# example of custom logger settings
from smartlingApiSdk.Settings import Settings
import logging
Settings.logPath = '/tmp/python.sdk.log'
Settings.logLevel = logging.DEBUG

def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testStringsApi(object):

    CODE_SUCCESS_TOKEN = 'SUCCESS'
    ACCEPTED_TOKEN = 'ACCEPTED'

    def tearDown(self):
        print("tearDown", "OK")

    def setUp(self):
        credentials = Credentials('stg') #Gets your Smartling credetnials from environment variables
        self.MY_USER_IDENTIFIER = credentials.MY_USER_IDENTIFIER
        self.MY_USER_SECRET = credentials.MY_USER_SECRET
        self.MY_PROJECT_ID = credentials.MY_PROJECT_ID

        #needed for testProjects
        self.MY_ACCOUNT_UID = credentials.MY_ACCOUNT_UID
        self.MY_LOCALE = credentials.MY_LOCALE

        if self.MY_ACCOUNT_UID == "CHANGE_ME":
            print("can't test projects api call, set self.MY_ACCOUNT_UID or export SL_ACCOUNT_UID=*********")
            return

        useProxy = False
        if useProxy :
            proxySettings = ProxySettings("login", "password", "proxy_host", "proxy_port or None")
        else:
            proxySettings = None

        self.strings_api = StringsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

        print("setUp", "OK", "\n")

    def checkAddStringsToProject(self):
        """
            method  :  POST
            api url :  /strings-api/v2/projects/{projectId}
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringJSON" https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId
            Responses:
                200 : OK
                202 : ACCEPTED
            details :  https://api-reference.smartling.com/#operation/addStringsToProject
        """
        strings=[
                {
                    "stringText": "Strings API test from python api sdk",
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
                {
                    "stringText": "Another Strings API test from python api sdk",
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
                {
                    "stringText": 'Service',
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
                {
                    "stringText": 'Usability Testing',
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
            ]
        placeholderFormat='none'
        placeholderFormatCustom=''
        namespace=''
        res, status = self.strings_api.addStringsToProject(strings=strings, placeholderFormat=placeholderFormat, placeholderFormatCustom=placeholderFormatCustom, namespace=namespace)


        assert_equal(res.data.wordCount, 18)
        assert_equal(res.data.stringCount, 4)
        stringTexts = [res.data.items[0]['stringText'], res.data.items[1]['stringText']]
        assert_equal(True, 'Strings API test from python api sdk' in stringTexts)
        assert_equal(True, 'Another Strings API test from python api sdk' in stringTexts)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('addStringsToProject', 'OK')
        self.processUid = res.data.processUid
        self.hashcode_0 = res.data.items[0]['hashcode']
        self.hashcode_1 = res.data.items[1]['hashcode']


    def checkGetAddStringsToProjectRequestStatus(self):
        """
            method  :  GET
            api url :  /strings-api/v2/projects/{projectId}/processes/{processUid}
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/processes/$processUid
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getAddStringsToProjectRequestStatus
        """
        processUid=self.processUid
        res, status = self.strings_api.getAddStringsToProjectRequestStatus(processUid=processUid)


        assert_equal(res.data.processUid, self.processUid)
        assert_equal(res.data.processStatistics['requested'], 4)
        assert_equal(res.data.processStatistics['errored'], 0)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getAddStringsToProjectRequestStatus', 'OK')


    def checkGetAllSourceStringsByProject(self):
        """
            method  :  POST
            api url :  /strings-api/v2/projects/{projectId}/source-strings
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G -d "fileUri=$smartlingFileUri" https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/source-strings
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getAllSourceStringsByProject
        """
        hashcodes=[self.hashcode_0,self.hashcode_1]
        res, status = self.strings_api.getAllSourceStringsByProject(hashcodes=hashcodes)


        assert_equal(res.data.totalCount, 2)
        stringTexts = [res.data.items[0]['stringText'], res.data.items[1]['stringText']]
        assert_equal(True, 'Strings API test from python api sdk' in stringTexts)
        assert_equal(True, 'Another Strings API test from python api sdk' in stringTexts)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getAllSourceStringsByProject', 'OK')


    def checkGetAllTranslationsByProject(self):
        """
            method  :  POST
            api url :  /strings-api/v2/projects/{projectId}/translations
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/translations
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getAllTranslationsByProject
        """
        targetLocaleId='zh-TW'
        hashcodes=[self.hashcode_0,self.hashcode_1]
        res, status = self.strings_api.getAllTranslationsByProject(targetLocaleId=targetLocaleId, hashcodes=hashcodes)


        assert_equal(res.data.totalCount, 0)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getAllTranslationsByProject', 'OK')



    def test_all(self):
        t = self
        t.checkAddStringsToProject()
        t.checkGetAddStringsToProjectRequestStatus()
        t.checkGetAllSourceStringsByProject()
        t.checkGetAllTranslationsByProject()
