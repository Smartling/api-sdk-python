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
from ExampleData import TestData

tests_order = [
    'createJobBatchV2',
]

extra_initializations = '''
'''


TestDecorators = {
'addJob':TestData(
    {
        'jobName' : Code('self.jobname'),
        'targetLocaleIds' : Code('[self.MY_LOCALE,]'),
        'description' : 'testDescription',
        'dueDate' : Code('self.dateTimeStr(2)'),
        'referenceNumber' : 'testReferenceNumber',
        'callbackUrl' : 'https://www.callback.com/smartling/job',
        'callbackMethod': 'GET',
        'customFields' : [],
    },
    [],
    ["self.test_job_uid = res.data.translationJobUid",]
),

'updateJob':  TestData(
    {
        'translationJobUid':Code('self.test_job_uid'),
        'jobName' : Code('"new name" + self.jobname'),
        'description' : 'new Description',
        'dueDate' : Code('self.dateTimeStr(300)'),
        'referenceNumber' : 'new ReferenceNumber',
        'callbackUrl' : 'https://www.callback.com/smartling/new_job',
        'callbackMethod': 'POST',
        'customFields' : [],
    }
),

'findJobsByStrings' : TestData(
    {'hashcodes':Code('[]'), 'localeIds' : Code('[self.MY_LOCALE,]'),}
),

'getAccountCustomFields' : TestData(
    {'accountUid':Code('self.MY_ACCOUNT_UID')}
),

'assignCustomFieldsToProject' : TestData(
    {'accountUid':Code('self.MY_ACCOUNT_UID'),
     'CustomFieldAssignmentList': Code('[{"fieldUid":self.fieldUid},]')
    },
'''
resp, code = self.api.getAccountCustomFields(self.MY_ACCOUNT_UID)
self.fieldUid=None
for fld in resp.data.items:
    if 'python-sdk-test' == fld['fieldName']:
        self.fieldUid = fld['fieldUid']

'''.split('\n')
),

'updateCustomField' : TestData(
    {'accountUid':Code('self.MY_ACCOUNT_UID'),
     "fieldUid": Code("self.fieldUid"),
     "fieldName": "python-sdk-test",
     "enabled": True,
     "required": False,
     "searchable": True,
     "displayToTranslators": True,
     "options": [],
     "defaultValue": "New default field value",
     "description": "New custom field example"
     },
),

}