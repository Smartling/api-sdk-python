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
    'uploadNewVisualContext',
    'getVisualContextsListByProject',
    #'getVisualContextInfo',
    'deleteVisualContext',
    #'downloadVisualContextFileContent,
    #'runAutomaticContextMatching',
    #'uploadAndMatchVisualContext',
    #'getAsyncContextMatchResults',
    #'createStringToContextBindings',
    #'getBindings',
    #'deleteBindings',
]

extra_initializations = '''
'''

test_evnironment = 'stg'

video_url = 'https://www.youtube.com/watch?v=0lJykuiS_9s'

test_decortators = {
    'uploadNewVisualContext':TestData(
        {
            'name' : video_url
        },
        [],
        [
            'self.context_uid = res.data.contextUid',
        ],
        custom_test_check = '''
assert_equal(res.data.contextType, 'VIDEO')
assert_equal(res.data.name, '%s')
''' % video_url
    ),

    'getVisualContextsListByProject':
        TestData({},custom_test_check = '''
print('Total context count:',len(res.data.items))
assert_equal(len(res.data.items) > 0, True)
'''
    ),
    'deleteVisualContext' : TestData(
        {
            'contextUid': Code('self.context_uid')
        }
    ),
}