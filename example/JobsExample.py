
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

from api.JobsApi import JobsApi
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
    ACCEPTED_TOKED = 'ACCEPTED'

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

        self.api = JobsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings)

        print("setUp", "OK", "\n")

        # setUp code add-on #
        self.jobname = 'test_job_'+str(int(time.time()))
        self.deleteTestJobs()

    def deleteTestJobs(self):
        response,code = self.api.getJobsByProject()
        c = 0
        sz = len(response.data.items)
        for job in response.data.items:
            c += 1
            if job['jobName'].startswith('test_job_'):
                uid = job['translationJobUid']
                cres, cstatus = self.api.cancelJob(uid, 'test reason')
                res, status = self.api.deleteJob(uid)
                print (c, 'of', sz, uid, cstatus, status)

    def dateTimeStr(self, offset):
        return datetime.datetime.fromtimestamp(time.time()+offset).strftime("%Y-%m-%dT%H:%M:%SZ")

    def checkAddJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs
            for details check: https://api-reference.smartling.com/#operation/addJob
            curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingJobJSON" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs

            ------------------------------------------------------------------------------------------------------------------------
        """
        jobName=self.jobname
        targetLocaleIds=[self.MY_LOCALE,]
        description='testDescription'
        dueDate=self.dateTimeStr(3600*24*30)
        referenceNumber='testReferenceNumber'
        callbackUrl='https://www.callback.com/smartling/job'
        callbackMethod='GET'
        customFields=[]
        res, status = self.api.addJob(jobName=jobName, targetLocaleIds=targetLocaleIds, description=description, dueDate=dueDate, referenceNumber=referenceNumber, callbackUrl=callbackUrl, callbackMethod=callbackMethod, customFields=customFields)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("addJob", "OK")
        self.test_job_uid = res.data.translationJobUid


    def checkAddLocaleToJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            for details check: https://api-reference.smartling.com/#operation/addLocaleToJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        targetLocaleId="zh-TW" #use your other locale here
        syncContent=True
        res, status = self.api.addLocaleToJob(translationJobUid=translationJobUid, targetLocaleId=targetLocaleId, syncContent=syncContent)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("addLocaleToJob", "OK")


    def checkAddStringsToJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/add
            for details check: https://api-reference.smartling.com/#operation/addStringsToJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        hashcodes=["5760794264f7f1f2bd80ee9bfd646869", ] # use your string hashcodes list here
        moveEnabled=False
        targetLocaleIds=[self.MY_LOCALE,]
        res, status = self.api.addStringsToJob(translationJobUid=translationJobUid, hashcodes=hashcodes, moveEnabled=moveEnabled, targetLocaleIds=targetLocaleIds)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("addStringsToJob", "OK")
        assert_equal(1, res.data.successCount, "addStringsToJob will fail if string was already in other job")


    def checkAddFileToJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add
            for details check: https://api-reference.smartling.com/#operation/addFileToJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        fileUri="test_import.xml_2.2.4_1629202583.584802" #use your actual file uri uploaded earielr to Smartling
        targetLocaleIds=[self.MY_LOCALE,]
        res, status = self.api.addFileToJob(translationJobUid=translationJobUid, fileUri=fileUri, targetLocaleIds=targetLocaleIds)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("addFileToJob", "OK")


    def checkGetJobFilesList(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files
            for details check: https://api-reference.smartling.com/#operation/getJobFilesList

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        res, status = self.api.getJobFilesList(translationJobUid=translationJobUid)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getJobFilesList", "OK")


    def checkGetJobFileProgress(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress
            for details check: https://api-reference.smartling.com/#operation/getJobFileProgress

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        fileUri="test_import.xml_2.2.4_1629202583.584802" #use your actual file uri uploaded earielr to Smartling
        res, status = self.api.getJobFileProgress(translationJobUid=translationJobUid, fileUri=fileUri)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getJobFileProgress", "OK")


    def checkAuthorizeJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize
            for details check: https://api-reference.smartling.com/#operation/authorizeJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        localeWorkflows= [ { "targetLocaleId": "zh-TW", "workflowUid": "748398939979" } ]
        res, status = self.api.authorizeJob(translationJobUid=translationJobUid, localeWorkflows=localeWorkflows)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("authorizeJob", "OK")


    def checkModifyScheduleItemsForTranslationJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            for details check: https://api-reference.smartling.com/#operation/modifyScheduleItemsForTranslationJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        schedules= [ { "targetLocaleId": "zh-TW", "workflowStepUid": "7f6126eff318", "dueDate": self.dateTimeStr(3600*24*30)} ]
        res, status = self.api.modifyScheduleItemsForTranslationJob(translationJobUid=translationJobUid, schedules=schedules)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("modifyScheduleItemsForTranslationJob", "OK")


    def checkCreateCustomField(self):
        """
            post
            /jobs-api/v3/accounts/{accountUid}/custom-fields
            for details check: https://api-reference.smartling.com/#operation/createCustomField

            ------------------------------------------------------------------------------------------------------------------------
        """
        self.api.httpClient.ignore_errors=True
        accountUid=self.MY_ACCOUNT_UID
        type='SHORT_TEXT'
        fieldName='python-sdk-test'
        enabled=True
        required=False
        searchable=True
        displayToTranslators=True
        options=[]
        defaultValue='default field value'
        description='Custom field example'
        res, status = self.api.createCustomField(accountUid=self.MY_ACCOUNT_UID, type=type, fieldName=fieldName, enabled=enabled, required=required, searchable=searchable, displayToTranslators=displayToTranslators, options=options, defaultValue=defaultValue, description=description)
        
        
        if 400 == status:
            assert_equal(True, 'Field name must be unique within account' in str(res))
        else:
            assert_equal(True, status in [200,202])
            assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        
        print("createCustomField", "OK")
        self.api.httpClient.ignore_errors=False


    def checkAssignCustomFieldsToProject(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/custom-fields
            for details check: https://api-reference.smartling.com/#operation/assignCustomFieldsToProject

            ------------------------------------------------------------------------------------------------------------------------
        """
        
        resp, code = self.api.getAccountCustomFields(self.MY_ACCOUNT_UID)
        self.fieldUid=None
        for fld in resp.data.items:
            if 'python-sdk-test' == fld['fieldName']:
                self.fieldUid = fld['fieldUid']
        
        
        CustomFieldAssignmentList=[{"fieldUid":self.fieldUid},]
        res, status = self.api.assignCustomFieldsToProject(CustomFieldAssignmentList=CustomFieldAssignmentList)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("assignCustomFieldsToProject", "OK")


    def checkUpdateCustomField(self):
        """
            put
            /jobs-api/v3/accounts/{accountUid}/custom-fields/{fieldUid}
            for details check: https://api-reference.smartling.com/#operation/updateCustomField

            ------------------------------------------------------------------------------------------------------------------------
        """
        accountUid=self.MY_ACCOUNT_UID
        fieldUid=self.fieldUid
        fieldName='python-sdk-test'
        enabled=True
        required=False
        searchable=True
        displayToTranslators=True
        options=[]
        defaultValue='New default field value'
        description='New custom field example'
        res, status = self.api.updateCustomField(accountUid=self.MY_ACCOUNT_UID, fieldUid=fieldUid, fieldName=fieldName, enabled=enabled, required=required, searchable=searchable, displayToTranslators=displayToTranslators, options=options, defaultValue=defaultValue, description=description)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("updateCustomField", "OK")


    def checkRemoveFileFromJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove
            for details check: https://api-reference.smartling.com/#operation/removeFileFromJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        fileUri="test_import.xml_2.2.4_1629202583.584802" #use your actual file uri uploaded earielr to Smartling
        res, status = self.api.removeFileFromJob(translationJobUid=translationJobUid, fileUri=fileUri)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("removeFileFromJob", "OK")


    def checkRemoveStringsFromJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove
            for details check: https://api-reference.smartling.com/#operation/removeStringsFromJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        hashcodes=["5760794264f7f1f2bd80ee9bfd646869", ] # use your string hashcodes list here
        localeIds=[self.MY_LOCALE,]
        res, status = self.api.removeStringsFromJob(translationJobUid=translationJobUid, hashcodes=hashcodes, localeIds=localeIds)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("removeStringsFromJob", "OK")


    def checkGetJobLastCompletionDatesPerLocale(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates
            for details check: https://api-reference.smartling.com/#operation/getJobLastCompletionDatesPerLocale

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        res, status = self.api.getJobLastCompletionDatesPerLocale(translationJobUid=translationJobUid)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getJobLastCompletionDatesPerLocale", "OK")


    def checkFindScheduleForTranslationJob(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            for details check: https://api-reference.smartling.com/#operation/findScheduleForTranslationJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        res, status = self.api.findScheduleForTranslationJob(translationJobUid=translationJobUid)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("findScheduleForTranslationJob", "OK")


    def checkRemoveLocaleFromJob(self):
        """
            delete
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            for details check: https://api-reference.smartling.com/#operation/removeLocaleFromJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        targetLocaleId="zh-TW" #use already added locale here
        res, status = self.api.removeLocaleFromJob(translationJobUid=translationJobUid, targetLocaleId=targetLocaleId)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("removeLocaleFromJob", "OK")


    def checkGetJobsByProject(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs
            for details check: https://api-reference.smartling.com/#operation/getJobsByProject
            curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs

            ------------------------------------------------------------------------------------------------------------------------
        """
        jobName=self.jobname
        res, status = self.api.getJobsByProject(jobName=jobName)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getJobsByProject", "OK")


    def checkUpdateJob(self):
        """
            put
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            for details check: https://api-reference.smartling.com/#operation/updateJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        jobName="new name" + self.jobname
        description='new Description'
        dueDate=self.dateTimeStr(3600*24*120)
        referenceNumber='new ReferenceNumber'
        callbackUrl='https://www.callback.com/smartling/new_job'
        callbackMethod='POST'
        customFields=[]
        res, status = self.api.updateJob(translationJobUid=translationJobUid, jobName=jobName, description=description, dueDate=dueDate, referenceNumber=referenceNumber, callbackUrl=callbackUrl, callbackMethod=callbackMethod, customFields=customFields)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("updateJob", "OK")


    def checkGetJobProgress(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress
            for details check: https://api-reference.smartling.com/#operation/getJobProgress

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        res, status = self.api.getJobProgress(translationJobUid=translationJobUid)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getJobProgress", "OK")


    def checkGetJobDetails(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            for details check: https://api-reference.smartling.com/#operation/getJobDetails

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        res, status = self.api.getJobDetails(translationJobUid=translationJobUid)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getJobDetails", "OK")


    def checkGetStringsForTranslationJob(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings
            for details check: https://api-reference.smartling.com/#operation/getStringsForTranslationJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        res, status = self.api.getStringsForTranslationJob(translationJobUid=translationJobUid)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getStringsForTranslationJob", "OK")


    def checkFindJobsByStrings(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings
            for details check: https://api-reference.smartling.com/#operation/findJobsByStrings

            ------------------------------------------------------------------------------------------------------------------------
        """
        hashcodes=[]
        localeIds=[self.MY_LOCALE,]
        res, status = self.api.findJobsByStrings(hashcodes=hashcodes, localeIds=localeIds)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("findJobsByStrings", "OK")


    def checkSearchForJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/search
            for details check: https://api-reference.smartling.com/#operation/searchForJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        fileUris=[]
        hashcodes=[]
        translationJobUids=[self.test_job_uid]
        res, status = self.api.searchForJob(fileUris=fileUris, hashcodes=hashcodes, translationJobUids=translationJobUids)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("searchForJob", "OK")


    def checkCancelJob(self):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel
            for details check: https://api-reference.smartling.com/#operation/cancelJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        reason='test reason'
        res, status = self.api.cancelJob(translationJobUid=translationJobUid, reason=reason)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("cancelJob", "OK")


    def checkDeleteJob(self):
        """
            delete
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            for details check: https://api-reference.smartling.com/#operation/deleteJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        translationJobUid=self.test_job_uid
        res, status = self.api.deleteJob(translationJobUid=translationJobUid)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("deleteJob", "OK")


    def checkGetProjectCustomFields(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/custom-fields
            for details check: https://api-reference.smartling.com/#operation/getProjectCustomFields

            ------------------------------------------------------------------------------------------------------------------------
        """
        res, status = self.api.getProjectCustomFields()
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getProjectCustomFields", "OK")


    def checkGetAccountCustomFields(self):
        """
            get
            /jobs-api/v3/accounts/{accountUid}/custom-fields
            for details check: https://api-reference.smartling.com/#operation/getAccountCustomFields

            ------------------------------------------------------------------------------------------------------------------------
        """
        accountUid=self.MY_ACCOUNT_UID
        res, status = self.api.getAccountCustomFields(accountUid=self.MY_ACCOUNT_UID)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getAccountCustomFields", "OK")


    def checkGetJobsByAccount(self):
        """
            get
            /jobs-api/v3/accounts/{accountUid}/jobs
            for details check: https://api-reference.smartling.com/#operation/getJobsByAccount
            curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/accounts/$smartlingAccountId/jobs

            ------------------------------------------------------------------------------------------------------------------------
        """
        accountUid=self.MY_ACCOUNT_UID
        res, status = self.api.getJobsByAccount(accountUid=self.MY_ACCOUNT_UID)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("getJobsByAccount", "OK")



def example():
    t = testJobsApi()
    t.setUp()
    t.checkAddJob()
    t.checkAddLocaleToJob()
    t.checkAddStringsToJob()
    t.checkAddFileToJob()
    t.checkGetJobFilesList()
    t.checkGetJobFileProgress()
    t.checkAuthorizeJob()
    t.checkModifyScheduleItemsForTranslationJob()
    t.checkCreateCustomField()
    t.checkAssignCustomFieldsToProject()
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

example()
