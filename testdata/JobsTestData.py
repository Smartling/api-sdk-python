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
   'assignCustomFieldsToProject', #result is used in addJob
   'addJob',
   'addLocaleToJob',
   'addStringsToJob',
   'addFileToJob',
   'getJobFilesList',
   'getJobFileProgress',
   'authorizeJob',
   'modifyScheduleItemsForTranslationJob',
   'createCustomField',
   'updateCustomField',
   'removeFileFromJob',
   'removeStringsFromJob',
   'getJobLastCompletionDatesPerLocale',
   'findScheduleForTranslationJob',
   'removeLocaleFromJob',
   'getJobsByProject',
   'updateJob',
   'getJobProgress',
   'getJobDetails',
   'getStringsForTranslationJob',
   'findJobsByStrings',
   'searchForJob',
   'cancelJob',
   'deleteJob',
   'getProjectCustomFields',
   'getAccountCustomFields',
   'getJobsByAccount',
]

extraInitializations = '''
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
'''

jobUidCode = Code('self.test_job_uid')

testDecorators = {
'addJob':TestData(
    {
        'jobName' : Code('self.jobname'),
        'targetLocaleIds' : Code('[self.MY_LOCALE,]'),
        'description' : 'testDescription',
        'dueDate' : Code('self.dateTimeStr(3600*24*30)'),
        'referenceNumber' : 'testReferenceNumber',
        'callbackUrl' : 'https://www.callback.com/smartling/job',
        'callbackMethod': 'GET',
        'customFields' : Code('[{"fieldUid": self.fieldUid, "fieldValue": "Test Field Value"}]'),
    },
    [],
    ["self.test_job_uid = res.data.translationJobUid",]
),

'updateJob':  TestData(
    {
        'translationJobUid':Code('self.test_job_uid'),
        'jobName' : Code('"new name" + self.jobname'),
        'description' : 'new Description',
        'dueDate' : Code('self.dateTimeStr(3600*24*120)'),
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
resp, code = self.jobs_api.getAccountCustomFields(self.MY_ACCOUNT_UID)
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


'createCustomField' : TestData(
    {'accountUid':Code('self.MY_ACCOUNT_UID'),
      "type": "SHORT_TEXT",
      "fieldName": "python-sdk-test",
      "enabled": True,
      "required": False,
      "searchable": True,
      "displayToTranslators": True,
      "options": [],
      "defaultValue": "default field value",
      "description": "Custom field example"

    },
    ['self.jobs_api.httpClient.ignore_errors=True'],
    ['self.jobs_api.httpClient.ignore_errors=False'],
    customTestCheck='''
if 400 == status:
    assert_equal(True, 'Field name must be unique within account' in str(res))
else:
    assert_equal(True, status in [200,202])
    assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
''',
    isApiV2Response= False,
),

'getJobProgress' :                     TestData({'translationJobUid':jobUidCode}),
'getJobDetails' :                      TestData({'translationJobUid':jobUidCode}),
'deleteJob' :                          TestData({'translationJobUid':jobUidCode}),
'getStringsForTranslationJob' :        TestData({'translationJobUid':jobUidCode}),
'getJobLastCompletionDatesPerLocale' : TestData({'translationJobUid':jobUidCode}),
'findScheduleForTranslationJob' :      TestData({'translationJobUid':jobUidCode}),
'getJobFilesList' :                    TestData({'translationJobUid':jobUidCode}),

'authorizeJob' : TestData({
    'localeWorkflows': Code(' [ { "targetLocaleId": "zh-TW", "workflowUid": "748398939979" } ]'),
    'translationJobUid': jobUidCode,
}
),

'modifyScheduleItemsForTranslationJob' : TestData({
    'schedules': Code(' [ { "targetLocaleId": "zh-TW", "workflowStepUid": "7f6126eff318", "dueDate": self.dateTimeStr(3600*24*30)} ]'),
    'translationJobUid': jobUidCode,
}
),

'addStringsToJob' : TestData({
    'hashcodes' : Code('["e1159037badca0a2a618f62c50eff1bb", ] # use your string hashcodes list here'),
    'moveEnabled': Code('False'),
    'targetLocaleIds' : Code('[self.MY_LOCALE,]'),
    'translationJobUid': jobUidCode,
}, [], [
    'assert_equal(0, res.data.failCount, "addStringsToJob will fail if string was already in other job")',
]
),

'removeStringsFromJob' : TestData({
    'hashcodes' : Code('["e1159037badca0a2a618f62c50eff1bb", ] # use your string hashcodes list here'),
    'localeIds' : Code('[self.MY_LOCALE,]'),
    'translationJobUid': jobUidCode,
}
),

'searchForJob' : TestData({
    'fileUris':Code('[]'),
    'hashcodes':Code('[]'),
    'translationJobUids':Code('[self.test_job_uid]'),
}),


'cancelJob' : TestData(
    {'translationJobUid':jobUidCode, 'reason':'test reason'}
),

'getJobsByProject' : TestData({'jobName':Code('self.jobname')}),

'addLocaleToJob' : TestData({'translationJobUid':jobUidCode,
                                        'targetLocaleId' : Code('"zh-TW" #use your other locale here'),
                                        'syncContent' : Code('True')
                                        }),

'removeLocaleFromJob' : TestData({'translationJobUid':jobUidCode,
                                        'targetLocaleId' : Code('"zh-TW" #use already added locale here'),
                                        }),

'addFileToJob' : TestData({'translationJobUid':jobUidCode,
                                      'targetLocaleIds' : Code('[self.MY_LOCALE,]'),
                                      'fileUri' : Code('"test_import.xml_2.2.4_1629202583.584802" #use your actual file uri uploaded earielr to Smartling')
                                      }),

'getJobFileProgress' : TestData({'translationJobUid':jobUidCode,
                                      'fileUri' : Code('"test_import.xml_2.2.4_1629202583.584802" #use your actual file uri uploaded earielr to Smartling')
                                      }),
'removeFileFromJob' : TestData({'translationJobUid':jobUidCode,
                                      'fileUri' : Code('"test_import.xml_2.2.4_1629202583.584802" #use your actual file uri uploaded earielr to Smartling')
                                      }),
}