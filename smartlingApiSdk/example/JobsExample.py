
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
from smartlingApiSdk.api.JobsApi import JobsApi
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testJobsApi(object):

    CODE_SUCCESS_TOKEN = 'SUCCESS'
    ACCEPTED_TOKEN = 'ACCEPTED'

    def tearDown(self):
        print("tearDown", "OK")

    def setUp(self):
        credentials = Credentials() #Gets your Smartling credetnials from environment variables
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

        self.jobs_api = JobsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings)

        print("setUp", "OK", "\n")

        # setUp code add-on #
        self.jobname = 'test_job_'+str(int(time.time()))
        self.deleteTestJobs()

    def deleteTestJobs(self):
        response,code = self.jobs_api.getJobsByProject()
        c = 0
        sz = len(response.data.items)
        for job in response.data.items:
            c += 1
            if job['jobName'].startswith('test_job_'):
                uid = job['translationJobUid']
                cres, cstatus = self.jobs_api.cancelJob(uid, 'test reason')
                res, status = self.jobs_api.deleteJob(uid)
                print (c, 'of', sz, uid, cstatus, status)

    def dateTimeStr(self, offset):
        return datetime.datetime.fromtimestamp(time.time()+offset).strftime("%Y-%m-%dT%H:%M:%SZ")

    def checkAssignCustomFieldsToProject(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/custom-fields
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/assignCustomFieldsToProject
        """

        resp, code = self.jobs_api.getAccountCustomFields(self.MY_ACCOUNT_UID)
        self.fieldUid=None
        for fld in resp.data.items:
            if 'python-sdk-test' == fld['fieldName']:
                self.fieldUid = fld['fieldUid']


        CustomFieldAssignmentList=[{"fieldUid":self.fieldUid},]
        res, status = self.jobs_api.assignCustomFieldsToProject(CustomFieldAssignmentList=CustomFieldAssignmentList)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('assignCustomFieldsToProject', 'OK')


    def checkAddJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingJobJSON" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs
            Responses:
                200 : OK
                400 : Validation error during job creation.
            details :  https://api-reference.smartling.com/#operation/addJob
        """
        jobName=self.jobname
        targetLocaleIds=[self.MY_LOCALE,]
        description='testDescription'
        dueDate=self.dateTimeStr(3600*24*30)
        referenceNumber='testReferenceNumber'
        callbackUrl='https://www.callback.com/smartling/job'
        callbackMethod='GET'
        customFields=[{"fieldUid": self.fieldUid, "fieldValue": "Test Field Value"}]
        res, status = self.jobs_api.addJob(jobName=jobName, targetLocaleIds=targetLocaleIds, description=description, dueDate=dueDate, referenceNumber=referenceNumber, callbackUrl=callbackUrl, callbackMethod=callbackMethod, customFields=customFields)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('addJob', 'OK')
        self.test_job_uid = res.data.translationJobUid


    def checkAddLocaleToJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            Responses:
                200 : OK
                202 : ACCEPTED
            details :  https://api-reference.smartling.com/#operation/addLocaleToJob
        """
        translationJobUid=self.test_job_uid
        targetLocaleId="zh-TW" #use your other locale here
        syncContent=True
        res, status = self.jobs_api.addLocaleToJob(translationJobUid=translationJobUid, targetLocaleId=targetLocaleId, syncContent=syncContent)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('addLocaleToJob', 'OK')


    def checkAddStringsToJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/add
            Responses:
                200 : OK
                202 : ACCEPTED
                400 : Validation error response
            details :  https://api-reference.smartling.com/#operation/addStringsToJob
        """
        translationJobUid=self.test_job_uid
        hashcodes=["e1159037badca0a2a618f62c50eff1bb", ] # use your string hashcodes list here
        moveEnabled=False
        targetLocaleIds=[self.MY_LOCALE,]
        res, status = self.jobs_api.addStringsToJob(translationJobUid=translationJobUid, hashcodes=hashcodes, moveEnabled=moveEnabled, targetLocaleIds=targetLocaleIds)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('addStringsToJob', 'OK')
        assert_equal(0, res.data.failCount, "addStringsToJob will fail if string was already in other job")


    def checkAddFileToJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add
            Responses:
                200 : OK
                202 : ACCEPTED
                400 : Validation error adding file to a job
                423 : The requested file is currently being processed by another operation. The file will be unlocked after the operation completes.
            details :  https://api-reference.smartling.com/#operation/addFileToJob
        """
        translationJobUid=self.test_job_uid
        fileUri="test_import.xml_2.2.4_1629202583.584802" #use your actual file uri uploaded earielr to Smartling
        targetLocaleIds=[self.MY_LOCALE,]
        res, status = self.jobs_api.addFileToJob(translationJobUid=translationJobUid, fileUri=fileUri, targetLocaleIds=targetLocaleIds)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('addFileToJob', 'OK')


    def checkGetJobFilesList(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobFilesList
        """
        translationJobUid=self.test_job_uid
        res, status = self.jobs_api.getJobFilesList(translationJobUid=translationJobUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobFilesList', 'OK')


    def checkGetJobFileProgress(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobFileProgress
        """
        translationJobUid=self.test_job_uid
        fileUri="test_import.xml_2.2.4_1629202583.584802" #use your actual file uri uploaded earielr to Smartling
        res, status = self.jobs_api.getJobFileProgress(translationJobUid=translationJobUid, fileUri=fileUri)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobFileProgress', 'OK')


    def checkAuthorizeJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize
            Responses:
                200 : OK
                400 : Validation error when authorizing a job
            details :  https://api-reference.smartling.com/#operation/authorizeJob
        """
        translationJobUid=self.test_job_uid
        localeWorkflows= [ { "targetLocaleId": "zh-TW", "workflowUid": "748398939979" } ]
        res, status = self.jobs_api.authorizeJob(translationJobUid=translationJobUid, localeWorkflows=localeWorkflows)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('authorizeJob', 'OK')


    def checkModifyScheduleItemsForTranslationJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/modifyScheduleItemsForTranslationJob
        """
        translationJobUid=self.test_job_uid
        schedules= [ { "targetLocaleId": "zh-TW", "workflowStepUid": "7f6126eff318", "dueDate": self.dateTimeStr(3600*24*30)} ]
        res, status = self.jobs_api.modifyScheduleItemsForTranslationJob(translationJobUid=translationJobUid, schedules=schedules)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('modifyScheduleItemsForTranslationJob', 'OK')


    def checkCreateCustomField(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/createCustomField
        """
        self.jobs_api.httpClient.ignore_errors=True
        accountUid=self.MY_ACCOUNT_UID
        required=False
        type='SHORT_TEXT'
        fieldName='python-sdk-test'
        enabled=True
        searchable=True
        displayToTranslators=True
        options=[]
        defaultValue='default field value'
        description='Custom field example'
        res, status = self.jobs_api.createCustomField(accountUid=self.MY_ACCOUNT_UID, required=required, type=type, fieldName=fieldName, enabled=enabled, searchable=searchable, displayToTranslators=displayToTranslators, options=options, defaultValue=defaultValue, description=description)


        if 400 == status:
            assert_equal(True, 'Field name must be unique within account' in str(res))
        else:
            assert_equal(True, status in [200,202])
            assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])

        print('createCustomField', 'OK')
        self.jobs_api.httpClient.ignore_errors=False


    def checkUpdateCustomField(self):
        """
            method  :  PUT
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields/{fieldUid}
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/updateCustomField
        """
        accountUid=self.MY_ACCOUNT_UID
        fieldUid=self.fieldUid
        required=False
        fieldName='python-sdk-test'
        enabled=True
        searchable=True
        displayToTranslators=True
        options=[]
        defaultValue='New default field value'
        description='New custom field example'
        res, status = self.jobs_api.updateCustomField(accountUid=self.MY_ACCOUNT_UID, fieldUid=fieldUid, required=required, fieldName=fieldName, enabled=enabled, searchable=searchable, displayToTranslators=displayToTranslators, options=options, defaultValue=defaultValue, description=description)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('updateCustomField', 'OK')


    def checkRemoveFileFromJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove
            Responses:
                200 : OK
                202 : ACCEPTED
                404 : Not found validation error
            details :  https://api-reference.smartling.com/#operation/removeFileFromJob
        """
        translationJobUid=self.test_job_uid
        fileUri="test_import.xml_2.2.4_1629202583.584802" #use your actual file uri uploaded earielr to Smartling
        res, status = self.jobs_api.removeFileFromJob(translationJobUid=translationJobUid, fileUri=fileUri)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('removeFileFromJob', 'OK')


    def checkRemoveStringsFromJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove
            Responses:
                200 : OK
                202 : ACCEPTED
            details :  https://api-reference.smartling.com/#operation/removeStringsFromJob
        """
        translationJobUid=self.test_job_uid
        hashcodes=["e1159037badca0a2a618f62c50eff1bb", ] # use your string hashcodes list here
        localeIds=[self.MY_LOCALE,]
        res, status = self.jobs_api.removeStringsFromJob(translationJobUid=translationJobUid, hashcodes=hashcodes, localeIds=localeIds)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('removeStringsFromJob', 'OK')


    def checkGetJobLastCompletionDatesPerLocale(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/getJobLastCompletionDatesPerLocale
        """
        translationJobUid=self.test_job_uid
        res, status = self.jobs_api.getJobLastCompletionDatesPerLocale(translationJobUid=translationJobUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobLastCompletionDatesPerLocale', 'OK')


    def checkFindScheduleForTranslationJob(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/findScheduleForTranslationJob
        """
        translationJobUid=self.test_job_uid
        res, status = self.jobs_api.findScheduleForTranslationJob(translationJobUid=translationJobUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('findScheduleForTranslationJob', 'OK')


    def checkRemoveLocaleFromJob(self):
        """
            method  :  DELETE
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            Responses:
                200 : OK
                202 : ACCEPTED
            details :  https://api-reference.smartling.com/#operation/removeLocaleFromJob
        """
        translationJobUid=self.test_job_uid
        targetLocaleId="zh-TW" #use already added locale here
        res, status = self.jobs_api.removeLocaleFromJob(translationJobUid=translationJobUid, targetLocaleId=targetLocaleId)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('removeLocaleFromJob', 'OK')


    def checkGetJobsByProject(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobsByProject
        """
        jobName=self.jobname
        res, status = self.jobs_api.getJobsByProject(jobName=jobName)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobsByProject', 'OK')


    def checkUpdateJob(self):
        """
            method  :  PUT
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            Responses:
                200 : OK
                400 : Validation error on updating a job
                404 : Job not found error
            details :  https://api-reference.smartling.com/#operation/updateJob
        """
        translationJobUid=self.test_job_uid
        jobName="new name" + self.jobname
        description='new Description'
        dueDate=self.dateTimeStr(3600*24*120)
        referenceNumber='new ReferenceNumber'
        callbackUrl='https://www.callback.com/smartling/new_job'
        callbackMethod='POST'
        customFields=[]
        res, status = self.jobs_api.updateJob(translationJobUid=translationJobUid, jobName=jobName, description=description, dueDate=dueDate, referenceNumber=referenceNumber, callbackUrl=callbackUrl, callbackMethod=callbackMethod, customFields=customFields)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('updateJob', 'OK')


    def checkGetJobProgress(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/getJobProgress
        """
        translationJobUid=self.test_job_uid
        res, status = self.jobs_api.getJobProgress(translationJobUid=translationJobUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobProgress', 'OK')


    def checkGetJobDetails(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            Responses:
                200 : OK
                404 : Job not found error
            details :  https://api-reference.smartling.com/#operation/getJobDetails
        """
        translationJobUid=self.test_job_uid
        res, status = self.jobs_api.getJobDetails(translationJobUid=translationJobUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobDetails', 'OK')


    def checkGetStringsForTranslationJob(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings
            Responses:
                200 : OK
                404 : Job not found error
            details :  https://api-reference.smartling.com/#operation/getStringsForTranslationJob
        """
        translationJobUid=self.test_job_uid
        res, status = self.jobs_api.getStringsForTranslationJob(translationJobUid=translationJobUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getStringsForTranslationJob', 'OK')


    def checkFindJobsByStrings(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings
            Responses:
                200 : OK
                400 : Validation error response
            details :  https://api-reference.smartling.com/#operation/findJobsByStrings
        """
        hashcodes=[]
        localeIds=[self.MY_LOCALE,]
        res, status = self.jobs_api.findJobsByStrings(hashcodes=hashcodes, localeIds=localeIds)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('findJobsByStrings', 'OK')


    def checkSearchForJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/search
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/searchForJob
        """
        fileUris=[]
        hashcodes=[]
        translationJobUids=[self.test_job_uid]
        res, status = self.jobs_api.searchForJob(fileUris=fileUris, hashcodes=hashcodes, translationJobUids=translationJobUids)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('searchForJob', 'OK')


    def checkCancelJob(self):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel
            Responses:
                200 : OK
                202 : ACCEPTED
                400 : Validation error when cancelling a job
                401 : Authentication error
            details :  https://api-reference.smartling.com/#operation/cancelJob
        """
        translationJobUid=self.test_job_uid
        reason='test reason'
        res, status = self.jobs_api.cancelJob(translationJobUid=translationJobUid, reason=reason)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('cancelJob', 'OK')


    def checkDeleteJob(self):
        """
            method  :  DELETE
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            Responses:
                200 : OK
                400 : Validation error when deleting a job
                401 : Authentication error
            details :  https://api-reference.smartling.com/#operation/deleteJob
        """
        translationJobUid=self.test_job_uid
        res, status = self.jobs_api.deleteJob(translationJobUid=translationJobUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('deleteJob', 'OK')


    def checkGetProjectCustomFields(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/custom-fields
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/getProjectCustomFields
        """
        res, status = self.jobs_api.getProjectCustomFields()

        print('getProjectCustomFields', 'OK')


    def checkGetAccountCustomFields(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/getAccountCustomFields
        """
        accountUid=self.MY_ACCOUNT_UID
        res, status = self.jobs_api.getAccountCustomFields(accountUid=self.MY_ACCOUNT_UID)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getAccountCustomFields', 'OK')


    def checkGetJobsByAccount(self):
        """
            method  :  GET
            api url :  /jobs-api/v3/accounts/{accountUid}/jobs
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/accounts/$smartlingAccountId/jobs
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobsByAccount
        """
        accountUid=self.MY_ACCOUNT_UID
        res, status = self.jobs_api.getJobsByAccount(accountUid=self.MY_ACCOUNT_UID)

        print('getJobsByAccount', 'OK')



def example():
    t = testJobsApi()
    t.setUp()
    t.checkAssignCustomFieldsToProject()
    t.checkAddJob()
    t.checkAddLocaleToJob()
    t.checkAddStringsToJob()
    t.checkAddFileToJob()
    t.checkGetJobFilesList()
    t.checkGetJobFileProgress()
    t.checkAuthorizeJob()
    t.checkModifyScheduleItemsForTranslationJob()
    t.checkCreateCustomField()
    t.checkUpdateCustomField()
    t.checkRemoveFileFromJob()
    t.checkRemoveStringsFromJob()
    t.checkGetJobLastCompletionDatesPerLocale()
    t.checkFindScheduleForTranslationJob()
    t.checkRemoveLocaleFromJob()
    t.checkGetJobsByProject()
    t.checkUpdateJob()
    t.checkGetJobProgress()
    t.checkGetJobDetails()
    t.checkGetStringsForTranslationJob()
    t.checkFindJobsByStrings()
    t.checkSearchForJob()
    t.checkCancelJob()
    t.checkDeleteJob()
    t.checkGetProjectCustomFields()
    t.checkGetAccountCustomFields()
    t.checkGetJobsByAccount()
    # not covered by tests #
    '''
    closeJob
    getJobAsyncProcessStatus
    '''
    t.tearDown()

if __name__ == '__main__':
    example()
