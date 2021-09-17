
#!/usr/bin/python
# -*- coding: utf-8 -*-


''' Copyright 2012-2021 Smartling, Inc.
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
import time, datetime

lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from api.AccountProjectsApi import AccountProjectsApi
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testAccountProjectsApi(object):

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

        self.api = AccountProjectsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

        print("setUp", "OK", "\n")


    def checkGetProjectsByAccount(self):
        """
            get
            /accounts-api/v2/accounts/{accountUid}/projects
            for details check: https://api-reference.smartling.com/#operation/getProjectsByAccount
            curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/accounts-api/v2/accounts/$smartlingAccountId/projects


        """
        accountUid=self.MY_ACCOUNT_UID
        res, status = self.api.getProjectsByAccount(accountUid=self.MY_ACCOUNT_UID)
        
        
        assert_equal(True, res.data.totalCount > 0)
        project_name = ''
        for p in res.data.items:
            if p['projectId'] == self.MY_PROJECT_ID:
                project_name = p['projectName']
        assert_equal('test variants', project_name)
        
        print("getProjectsByAccount", "OK")


    def checkGetProjectDetails(self):
        """
            get
            /projects-api/v2/projects/{projectId}
            for details check: https://api-reference.smartling.com/#operation/getProjectDetails
            curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/projects-api/v2/projects/$smartlingProjectId


        """
        res, status = self.api.getProjectDetails()
        
        
        assert_equal(res.data.projectId, self.MY_PROJECT_ID)
        assert_equal(res.data.projectName, 'test variants')
        assert_equal(res.data.accountUid, self.MY_ACCOUNT_UID)
        
        print("getProjectDetails", "OK")


    def checkAddLocaleToProject(self):
        """
            post
            /projects-api/v2/projects/{projectId}/targetLocales
            for details check: https://api-reference.smartling.com/#operation/addLocaleToProject

            ------------------------------------------------------------------------------------------------------------------------
        """
        defaultWorkflowUid='748398939979'
        localeId='es-MX'
        res, status = self.api.addLocaleToProject(defaultWorkflowUid=defaultWorkflowUid, localeId=localeId)
        
        
        assert_equal(res.data.projectId, self.MY_PROJECT_ID)
        assert_equal(res.data.projectName, 'test variants')
        assert_equal(res.data.accountUid, self.MY_ACCOUNT_UID)
        locales = [l['localeId'] for l in res.data.targetLocales]
        assert_equal(True, 'es-MX' in locales)
        
        print("addLocaleToProject", "OK")


    def checkCopyProject(self):
        """
            post
            /projects-api/v2/projects/{projectId}/copy
            for details check: https://api-reference.smartling.com/#operation/copyProject

            ------------------------------------------------------------------------------------------------------------------------
        """
        projectName='python SDK test'
        targetLocaleIds=['es-MX', 'zh-TW']
        res, status = self.api.copyProject(projectName=projectName, targetLocaleIds=targetLocaleIds)
        
        
        assert_equal(res.code, 'ACCEPTED')
        
        print("copyProject", "OK")
        self.copy_process_uid  = res.data.processUid


    def checkGetProjectCopyRequestStatus(self):
        """
            get
            /projects-api/v2/projects/{projectId}/copy/{processUid}
            for details check: https://api-reference.smartling.com/#operation/getProjectCopyRequestStatus

            ------------------------------------------------------------------------------------------------------------------------
        """
        processUid=self.copy_process_uid
        res, status = self.api.getProjectCopyRequestStatus(processUid=processUid)
        
        
        assert_equal(res.data.processUid, self.copy_process_uid)
        assert_equal(True, res.data.processState in ['IN_PROGRESS','COMPLETED'])
        
        print("getProjectCopyRequestStatus", "OK")



    def test_all(self):
        t = self
        t.checkGetProjectsByAccount()
        t.checkGetProjectDetails()
        t.checkAddLocaleToProject()
        t.checkCopyProject()
        t.checkGetProjectCopyRequestStatus()