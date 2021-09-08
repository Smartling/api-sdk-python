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

test_evnironment = 'stg'

TestDecorators = {
'createJobBatchV2':TestData(
    {
        'authorize' : False,
        'translationJobUid' : 'zzzzz',
        'fileUris': Code('["test_import.xml_2.2.4_1629202583.584802",] #use your actual file uris uploaded earielr to Smartling'),
        'localeWorkflows': Code(' [ { "targetLocaleId": "zh-TW", "workflowUid": "748398939979" } ]'),
},
    [],
    []
),
}