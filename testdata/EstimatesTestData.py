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
 * limit
"""

from builder.Parameters import Code
from builder.ExampleData import TestData

testsOrder = [
    "generateJobFuzzyEstimateReports",
    "getJobFuzzyEstimateReports",
    "generateJobCostEstimateReports",
    "getJobCostEstimateReports",
    "getJobEstimateReportStatus",
    "getJobEstimateReport",
    "modifyJobEstimateReportTags",
    "exportJobEstimationReport",
    "deleteJobEstimateReport",
]

tearDown = '''
        self.jobs_api.cancelJob(self.test_job_uid, 'test reason')
        self.jobs_api.deleteJob(translationJobUid=self.test_job_uid)
'''

imports = "from smartlingApiSdk.api.JobsApi import JobsApi"

extraInitializations = '''
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
'''

testEnvironment = 'prod'


testDecorators = {

    'getJobFuzzyEstimateReports':TestData(
        {
            'translationJobUid' : Code('self.test_job_uid')
        },
        customTestCheck='''
assert_equal(res.data.totalCount, 1)
assert_equal(res.data.items[0]['translationJobUid'], self.test_job_uid)

'''
    ),

    'generateJobFuzzyEstimateReports':TestData(
        {
            'translationJobUid' : Code('self.test_job_uid'),
            'contentType' : 'JOB_CONTENT_ALL_CONTENT',
            'tags': ['some','tags'],
        },
        customTestCheck='''
self.report_uid = res.data.reportUid
assert_equal(res.data.reportType, 'FUZZY')
assert_equal(res.data.reportStatus, 'PENDING')
'''
    ),

    'getJobCostEstimateReports':TestData(
        {
            'translationJobUid' : Code('self.test_job_uid'),
            'reportStatus' : 'PENDING',
        },
    ),

    'generateJobCostEstimateReports':TestData(
        {
            'translationJobUid' : Code('self.test_job_uid'),
            'contentType' : 'JOB_CONTENT_ALL_CONTENT',
            'tags': ['some','tags'],
            'localeWorkflows': Code(' [ { "targetLocaleId": "zh-TW", "workflowUid": "748398939979" } ]'),
            'fuzzyProfileUid' : '624e06b333af',
        },
        customTestCheck='''
assert_equal(True, res.data.reportType in ('FUZZY','COST'))
assert_equal(True, res.data.reportStatus in ('PENDING'))
'''
    ),

    'getJobEstimateReportStatus':TestData(
        {
            'reportUid' : Code('self.report_uid'),
        },
        customTestCheck='''
assert_equal(True, res.data.reportStatus in ('PENDING', 'PROCESSING', 'COMPLETED'))
'''
    ),

    'getJobEstimateReport':TestData(
        {
            'reportUid' : Code('self.report_uid'),
        },
        customTestCheck='''
assert_equal(True, res.data.reportStatus in ('PENDING', 'PROCESSING', 'COMPLETED'))
'''
    ),

    'modifyJobEstimateReportTags':TestData(
        {
            'reportUid' : Code('self.report_uid'),
            'tags': ['tags','remodeling'],
        },
        customTestCheck='''
assert_equal(res.data.tags[0], 'tags')
assert_equal(res.data.tags[1], 'remodeling')
'''
    ),


    'exportJobEstimationReport':TestData(
        {
            'projectUid': Code('self.MY_PROJECT_ID'),
            'reportUid' : Code('self.report_uid'),
            'format' : 'csv'
        },
        [],
        customTestCheck='''
assert_equal(True, res.decode('utf-8').startswith('Project Name,Job Name,'))
''',
        isApiV2Response= False,
    ),



    'deleteJobEstimateReport':TestData(
        {
            'reportUid' : Code('self.report_uid'),
        },
    ),
}
