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
 * limit
 '''

from Parameters import Code

class TestData:
    def __init__(self, fields, pre = [], post = [], runnable = True):
        self.fields = fields
        self.pre_calls = pre
        self.post_calls = post
        self.runnable = runnable

JobsTests = {}


addJobFields  =  {
    'jobName' : Code('self.jobname'),
    'targetLocaleIds' : Code('[self.MY_LOCALE,]'),
    'description' : 'testDescription',
    'dueDate' : Code('self.dateTimeStr(2)'),
    'referenceNumber' : 'testReferenceNumber',
    'callbackUrl' : 'https://www.callback.com/smartling/job',
    'callbackMethod': 'GET',
    'customFields' : [],
}
add_job_post = ['', 'self.testDeleteJob()', ]
addJob = TestData(addJobFields, [], add_job_post)

JobsTests['addJob'] = addJob

deleteJobInstr = '''
d, status = self.papi.getJobsByProject(jobName=self.jobname)
jobs_list = d.data.items
translationJobUid=jobs_list[0]["translationJobUid"]
self.papi.cancelJob(translationJobUid, 'test reason')
'''
JobsTests['deleteJob'] = TestData(
    {'translationJobUid':Code('translationJobUid=jobs_list[0]["translationJobUid"]')},
    deleteJobInstr.split('\n'),
    runnable = False
)
