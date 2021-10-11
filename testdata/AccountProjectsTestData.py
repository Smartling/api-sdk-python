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
    "getProjectsByAccount",
    "getProjectDetails",
    "addLocaleToProject",
    "copyProject",
    "getProjectCopyRequestStatus",
]

extraInitializations = '''
'''

testEnvironment = 'stg'

testDecorators = {
    'getProjectsByAccount':TestData(
        {
        },
        customTestCheck='''
assert_equal(True, res.data.totalCount > 0)
project_name = ''
for p in res.data.items:
    if p['projectId'] == self.MY_PROJECT_ID:
        project_name = p['projectName']
assert_equal('test variants', project_name)
'''
    ),

    'getProjectDetails':TestData(
        {
        },
        customTestCheck='''
assert_equal(res.data.projectId, self.MY_PROJECT_ID)
assert_equal(res.data.projectName, 'test variants')
assert_equal(res.data.accountUid, self.MY_ACCOUNT_UID)
'''
    ),

    'addLocaleToProject':TestData(
        {
            'defaultWorkflowUid': '748398939979',
            'localeId':'es-MX',
        },
        customTestCheck='''
assert_equal(res.data.projectId, self.MY_PROJECT_ID)
assert_equal(res.data.projectName, 'test variants')
assert_equal(res.data.accountUid, self.MY_ACCOUNT_UID)
locales = [l['localeId'] for l in res.data.targetLocales]
assert_equal(True, 'es-MX' in locales)
''' ),

    'copyProject':TestData(
        {
            'projectName': 'python SDK test',
            'targetLocaleIds':['es-MX', 'zh-TW'],
        },
        [],
        ['self.copy_process_uid  = res.data.processUid'],
        customTestCheck='''
assert_equal(res.code, 'ACCEPTED')
'''),

    'getProjectCopyRequestStatus':TestData(
        {
            'processUid': Code('self.copy_process_uid'),
        },
        customTestCheck='''
assert_equal(res.data.processUid, self.copy_process_uid)
assert_equal(True, res.data.processState in ['IN_PROGRESS','COMPLETED'])
'''),

}