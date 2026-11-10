
#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012-2025 Smartling, Inc.
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
from smartlingApiSdk.api.AccountProjectsApi import AccountProjectsApi
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

        self.account_projects_api = AccountProjectsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

        print("setUp", "OK", "\n")


    def waitForCopiedProject(self):
        for i in range(30):
            res, status = self.account_projects_api.getProjectCopyRequestStatus(self.copy_process_uid)
            if res.data.processState != 'IN_PROGRESS':
                break
            time.sleep(2)
        assert_equal('COMPLETED', res.data.processState)
        return res.data.newProjectUid

    def copiedProject(self, field):
        # looked up by id under the base name, so a lost rename doesn't break archive checks
        offset = 0
        while True:
            res, status = self.account_projects_api.getProjectsByAccount(self.MY_ACCOUNT_UID, projectNameFilter='python SDK test',
                                                                         includeArchived=True, limit=100, offset=offset)
            for p in res.data.items:
                if p['projectId'] == self.copied_project_uid:
                    return p[field]
            if len(res.data.items) < 100:
                return None
            offset += 100

    def waitFor(self, getValue, expected, attempts=30):
        # project changes reach reads asynchronously on the server (getProjectDetails may stay stale longer)
        for i in range(attempts):
            value = getValue()
            if value == expected:
                break
            time.sleep(1)
        return value

    def checkGetProjectsByAccount(self):
        """
            method  :  GET
            api url :  /accounts-api/v2/accounts/{accountUid}/projects
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/accounts-api/v2/accounts/$smartlingAccountId/projects
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getProjectsByAccount
        """
        accountUid=self.MY_ACCOUNT_UID
        res, status = self.account_projects_api.getProjectsByAccount(accountUid=self.MY_ACCOUNT_UID)


        assert_equal(True, res.data.totalCount > 0)
        project_name = ''
        for p in res.data.items:
            if p['projectId'] == self.MY_PROJECT_ID:
                project_name = p['projectName']
        assert_equal('test variants', project_name)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getProjectsByAccount', 'OK')


    def checkGetProjectDetails(self):
        """
            method  :  GET
            api url :  /projects-api/v2/projects/{projectId}
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/projects-api/v2/projects/$smartlingProjectId
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getProjectDetails
        """
        res, status = self.account_projects_api.getProjectDetails()


        assert_equal(res.data.projectId, self.MY_PROJECT_ID)
        assert_equal(res.data.projectName, 'test variants')
        assert_equal(res.data.accountUid, self.MY_ACCOUNT_UID)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getProjectDetails', 'OK')


    def checkGetAccountProjectTypes(self):
        """
            method  :  GET
            api url :  /accounts-api/v2/accounts/{accountUid}/project-types
            as curl :  curl -H "Authorization: Bearer $smartlingToken" "https://api.smartling.com/accounts-api/v2/accounts/$smartlingAccountId/project-types?projectTypeGroupCode=GENERAL"
            Responses:
                200 : OK
                400 : The `projectTypeGroupCode` value is not supported.
                403 : The user is not allowed to list project types of the account.
            details :  https://api-reference.smartling.com/#operation/getAccountProjectTypes
        """
        accountUid=self.MY_ACCOUNT_UID
        res, status = self.account_projects_api.getAccountProjectTypes(accountUid=self.MY_ACCOUNT_UID)


        assert_equal(True, res.data.totalCount > 0)
        assert_equal(True, 'APPLICATION_RESOURCES' in [t['projectTypeCode'] for t in res.data.items])

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getAccountProjectTypes', 'OK')


    def checkAddLocaleToProject(self):
        """
            method  :  POST
            api url :  /projects-api/v2/projects/{projectId}/targetLocales
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/addLocaleToProject
        """
        defaultWorkflowUid='748398939979'
        localeId='es-MX'
        res, status = self.account_projects_api.addLocaleToProject(defaultWorkflowUid=defaultWorkflowUid, localeId=localeId)


        assert_equal(res.data.projectId, self.MY_PROJECT_ID)
        assert_equal(res.data.projectName, 'test variants')
        assert_equal(res.data.accountUid, self.MY_ACCOUNT_UID)
        locales = [l['localeId'] for l in res.data.targetLocales]
        assert_equal(True, 'es-MX' in locales)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('addLocaleToProject', 'OK')


    def checkCopyProject(self):
        """
            method  :  POST
            api url :  /projects-api/v2/projects/{projectId}/copy
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/copyProject
        """
        projectName='python SDK test'
        targetLocaleIds=['es-MX', 'zh-TW']
        res, status = self.account_projects_api.copyProject(projectName=projectName, targetLocaleIds=targetLocaleIds)


        assert_equal(res.code, 'ACCEPTED')

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('copyProject', 'OK')
        self.copy_process_uid  = res.data.processUid


    def checkGetProjectCopyRequestStatus(self):
        """
            method  :  GET
            api url :  /projects-api/v2/projects/{projectId}/copy/{processUid}
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getProjectCopyRequestStatus
        """
        processUid=self.copy_process_uid
        res, status = self.account_projects_api.getProjectCopyRequestStatus(processUid=processUid)


        assert_equal(res.data.processUid, self.copy_process_uid)
        assert_equal(True, res.data.processState in ['IN_PROGRESS','COMPLETED'])

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getProjectCopyRequestStatus', 'OK')


    def checkRenameProject(self):
        """
            method  :  PUT
            api url :  /projects-api/v2/projects/{projectId}/rename
            as curl :  curl -X PUT -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d '{"projectName": "Android XML Content v2"}' https://api.smartling.com/projects-api/v2/projects/$smartlingProjectId/rename
            Responses:
                200 : OK
                400 : Provided request parameters are invalid.
            details :  https://api-reference.smartling.com/#operation/renameProject
        """
        self.copied_project_uid = self.waitForCopiedProject()
        self.copy_project_name = "python SDK test renamed %d" % time.time()
        self.main_projects_api = self.account_projects_api
        self.account_projects_api = AccountProjectsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.copied_project_uid, env="stg")
        projectName=self.copy_project_name
        res, status = self.account_projects_api.renameProject(projectName=projectName)


        assert_equal(self.copy_project_name, self.waitFor(lambda: self.copiedProject('projectName'), self.copy_project_name))

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('renameProject', 'OK')


    def checkArchiveProject(self):
        """
            method  :  POST
            api url :  /projects-api/v2/projects/{projectId}/archive
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/projects-api/v2/projects/$smartlingProjectId/archive
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/archiveProject
        """
        res, status = self.account_projects_api.archiveProject()


        assert_equal(True, self.waitFor(lambda: self.copiedProject('archived'), True))

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('archiveProject', 'OK')


    def checkUnarchiveProject(self):
        """
            method  :  POST
            api url :  /projects-api/v2/projects/{projectId}/unarchive
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/projects-api/v2/projects/$smartlingProjectId/unarchive
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/unarchiveProject
        """
        res, status = self.account_projects_api.unarchiveProject()


        assert_equal(False, self.waitFor(lambda: self.copiedProject('archived'), False))

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('unarchiveProject', 'OK')
        # leave the throwaway copy archived
        res, status = self.account_projects_api.archiveProject()
        assert_equal(200, status)
        self.account_projects_api = self.main_projects_api



    def test_all(self):
        t = self
        t.checkGetProjectsByAccount()
        t.checkGetProjectDetails()
        t.checkGetAccountProjectTypes()
        t.checkAddLocaleToProject()
        t.checkCopyProject()
        t.checkGetProjectCopyRequestStatus()
        t.checkRenameProject()
        t.checkArchiveProject()
        t.checkUnarchiveProject()
