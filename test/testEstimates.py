
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
from smartlingApiSdk.api.EstimatesApi import EstimatesApi
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)
from smartlingApiSdk.api.JobsApi import JobsApi
def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testEstimatesApi(object):

    CODE_SUCCESS_TOKEN = 'SUCCESS'
    ACCEPTED_TOKEN = 'ACCEPTED'

    def tearDown(self):

        self.jobs_api.cancelJob(self.test_job_uid, 'test reason')
        self.jobs_api.deleteJob(translationJobUid=self.test_job_uid)
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

        self.estimates_api = EstimatesApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings)

        print("setUp", "OK", "\n")

        self.addTestJob(proxySettings)
        self.addStringsToJob()

    def dateTimeStr(self, offset):
        return datetime.datetime.fromtimestamp(time.time()+offset).strftime("%Y-%m-%dT%H:%M:%SZ")
         
    def addTestJob(self, proxySettings):
        self.jobs_api = JobsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='prod')
        self.jobname = 'test_job_'+str(int(time.time()))
        jobName=self.jobname
        targetLocaleIds=["zh-TW",]
        description='testDescription'
        dueDate=self.dateTimeStr(3600*24*30)
        referenceNumber='testReferenceNumber'
        callbackUrl='https://www.callback.com/smartling/job'
        callbackMethod='GET'
        customFields=[]
        res, status = self.jobs_api.addJob(jobName=jobName, targetLocaleIds=targetLocaleIds, description=description, dueDate=dueDate, referenceNumber=referenceNumber, callbackUrl=callbackUrl, callbackMethod=callbackMethod, customFields=customFields)
        self.test_job_uid = res.data.translationJobUid

    def addStringsToJob(self):
        translationJobUid=self.test_job_uid
        hashcodes=["e1159037badca0a2a618f62c50eff1bb", ] # use your string hashcodes list here
        moveEnabled=False
        targetLocaleIds=["zh-TW",]
        res, status = self.jobs_api.addStringsToJob(translationJobUid=translationJobUid, hashcodes=hashcodes, moveEnabled=moveEnabled, targetLocaleIds=targetLocaleIds)

    def checkGenerateJobFuzzyEstimateReports(self):
        """
            method  :  POST
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/generateJobFuzzyEstimateReports
        """
        translationJobUid=self.test_job_uid
        contentType='JOB_CONTENT_ALL_CONTENT'
        tags=['some', 'tags']
        res, status = self.estimates_api.generateJobFuzzyEstimateReports(translationJobUid=translationJobUid, contentType=contentType, tags=tags)


        self.report_uid = res.data.reportUid
        assert_equal(res.data.reportType, 'FUZZY')
        assert_equal(res.data.reportStatus, 'PENDING')

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('generateJobFuzzyEstimateReports', 'OK')


    def checkGetJobFuzzyEstimateReports(self):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobFuzzyEstimateReports
        """
        translationJobUid=self.test_job_uid
        res, status = self.estimates_api.getJobFuzzyEstimateReports(translationJobUid=translationJobUid)


        assert_equal(res.data.totalCount, 1)
        assert_equal(res.data.items[0]['translationJobUid'], self.test_job_uid)


        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobFuzzyEstimateReports', 'OK')


    def checkGenerateJobCostEstimateReports(self):
        """
            method  :  POST
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/generateJobCostEstimateReports
        """
        translationJobUid=self.test_job_uid
        contentType='JOB_CONTENT_ALL_CONTENT'
        tags=['some', 'tags']
        localeWorkflows= [ { "targetLocaleId": "zh-TW", "workflowUid": "748398939979" } ]
        fuzzyProfileUid='624e06b333af'
        res, status = self.estimates_api.generateJobCostEstimateReports(translationJobUid=translationJobUid, contentType=contentType, tags=tags, localeWorkflows=localeWorkflows, fuzzyProfileUid=fuzzyProfileUid)


        assert_equal(True, res.data.reportType in ('FUZZY','COST'))
        assert_equal(True, res.data.reportStatus in ('PENDING'))

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('generateJobCostEstimateReports', 'OK')


    def checkGetJobCostEstimateReports(self):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobCostEstimateReports
        """
        translationJobUid=self.test_job_uid
        reportStatus='PENDING'
        res, status = self.estimates_api.getJobCostEstimateReports(translationJobUid=translationJobUid, reportStatus=reportStatus)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobCostEstimateReports', 'OK')


    def checkGetJobEstimateReportStatus(self):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}/status
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobEstimateReportStatus
        """
        reportUid=self.report_uid
        res, status = self.estimates_api.getJobEstimateReportStatus(reportUid=reportUid)


        assert_equal(True, res.data.reportStatus in ('PENDING', 'PROCESSING', 'COMPLETED'))

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobEstimateReportStatus', 'OK')


    def checkGetJobEstimateReport(self):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobEstimateReport
        """
        reportUid=self.report_uid
        res, status = self.estimates_api.getJobEstimateReport(reportUid=reportUid)


        assert_equal(True, res.data.reportStatus in ('PENDING', 'PROCESSING', 'COMPLETED'))

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobEstimateReport', 'OK')


    def checkModifyJobEstimateReportTags(self):
        """
            method  :  PUT
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}/tags
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/modifyJobEstimateReportTags
        """
        reportUid=self.report_uid
        tags=['tags', 'remodeling']
        res, status = self.estimates_api.modifyJobEstimateReportTags(reportUid=reportUid, tags=tags)


        assert_equal(res.data.tags[0], 'tags')
        assert_equal(res.data.tags[1], 'remodeling')

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('modifyJobEstimateReportTags', 'OK')


    def checkExportJobEstimationReport(self):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectUid}/reports/{reportUid}/download
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/exportJobEstimationReport
        """
        projectUid=self.MY_PROJECT_ID
        reportUid=self.report_uid
        format='csv'
        res, status = self.estimates_api.exportJobEstimationReport(projectUid=projectUid, reportUid=reportUid, format=format)


        assert_equal(True, res.decode('utf-8').startswith('Project Name,Job Name,'))

        print('exportJobEstimationReport', 'OK')


    def checkDeleteJobEstimateReport(self):
        """
            method  :  DELETE
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/deleteJobEstimateReport
        """
        reportUid=self.report_uid
        res, status = self.estimates_api.deleteJobEstimateReport(reportUid=reportUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('deleteJobEstimateReport', 'OK')



    def test_all(self):
        t = self
        t.checkGenerateJobFuzzyEstimateReports()
        t.checkGetJobFuzzyEstimateReports()
        t.checkGenerateJobCostEstimateReports()
        t.checkGetJobCostEstimateReports()
        t.checkGetJobEstimateReportStatus()
        t.checkGetJobEstimateReport()
        t.checkModifyJobEstimateReportTags()
        t.checkExportJobEstimationReport()
        t.checkDeleteJobEstimateReport()
