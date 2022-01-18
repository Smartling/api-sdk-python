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
    'createJobBatchV2',
    'getJobBatchesListV2',
    'getJobBatchStatusV2',
    'uploadFileToJobBatchV2',
    'processBatchActionV2',
]

extraInitializations = '''
'''

testEnvironment = 'stg'

testDecorators = {
'createJobBatchV2':TestData(
    {
        'authorize' : False,
        'translationJobUid' : Code('"c4e4b14773bd"  #use real batch job here'),
        'fileUris': Code('[self.file_uri, "file_to_cancel_later"]'),
        'localeWorkflows': Code(' [ { "targetLocaleId": "zh-TW", "workflowUid": "748398939979" } ]'),
},
    ['self.file_uri = "java.properties.jb2.%d" % time.time()',],
    ['self.batch_uid = res.data.batchUid']
),

'getJobBatchStatusV2': TestData({'batchUid':Code('self.batch_uid')}),

'processBatchActionV2': TestData({
    'batchUid': Code('self.batch_uid'),
    'action' : 'CANCEL_FILE',
    'fileUri': 'file_to_cancel_later',
    'reason' : 'test reason'
}),

'uploadFileToJobBatchV2': TestData({
    'batchUid': Code('self.batch_uid'),
    'file' : Code('textData'),
    'fileUri': Code('self.file_uri'),
    'fileType':'javaProperties',
    'authorize':False,
    'localeIdsToAuthorize':Code('["zh-TW",]'),
    'callbackUrl' : 'https://www.callback.com/smartling/python/sdk/jb2.test',
},
    ["textData = open(smartlingApiSdk.__path__[0]+'/resources/java.properties', 'rb').read().decode('utf-8', 'ignore')"]
),



}