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

from builder.Parameters import Code
from builder.ExampleData import TestData

tests_order = [
    'uploadNewVisualContext',
    'getVisualContextsListByProject',
    'getVisualContextInfo',
    'downloadVisualContextFileContent',
    'runAutomaticContextMatching',
    'uploadAndMatchVisualContext',
    'getAsyncContextMatchResults',
    'createStringToContextBindings',
    'getBindings',
    'deleteBindings',
    'deleteVisualContext',
]

extra_initializations = '''
'''

test_evnironment = 'stg'

video_url = 'https://www.youtube.com/watch?v=0lJykuiS_9s'

strings_added = [
    {"hashcode":"ede6083ebd2594ca4e557612aaa05b2e","stringText":"Usability Testing","parsedStringText":"Usability Testing"},
    {"hashcode":"4f25feab674accf572433f22dc516e2e","stringText":"Service","parsedStringText":"Service"},
    {"hashcode":"b60df7845b7a3755fa00a833a31fa91e","stringText":"Design for Context","parsedStringText":"Design for Context"}
]

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

res_img, status = self.api.uploadNewVisualContext(content='../resources/ctx_api_test.png')
self.context_uid_img = res_img.data.contextUid
''' % video_url
    ),

    'getVisualContextsListByProject':
        TestData({},custom_test_check = '''
print('Total context count:',len(res.data.items))
assert_equal(len(res.data.items) > 0, True)
'''
    ),


    'getVisualContextInfo' : TestData(
        {
            'contextUid': Code('self.context_uid'),
        },
        custom_test_check = '''
assert_equal(res.data.contextType, 'VIDEO')
assert_equal(res.data.name, '%s')
''' % video_url
    ),


    'downloadVisualContextFileContent' : TestData(
        {
            'contextUid': Code('self.context_uid_img'),
        },
        custom_test_check = '''
assert_equal(86324, len(res)) #empty for video context
''',
        is_apiv2_response = False,
    ),


    'runAutomaticContextMatching' : TestData(
        {
            'contextUid': Code('self.context_uid_img'),
            'contentFileUri' : '',
            'stringHashcodes' : '',
            'overrideContextOlderThanDays' : 1,
        },
        custom_test_check = '''
self.match_id = res.data.matchId
'''
    ),

    'getAsyncContextMatchResults' : TestData(
        {
            'matchId': Code('self.match_id_upl_n_match'),
        },
        custom_test_check = '''
'''
    ),


    'deleteVisualContext' : TestData(
        {
            'contextUid': Code('self.context_uid'),
        },
        custom_test_check = '''
res2, status = self.api.deleteVisualContext(contextUid=self.context_uid_img)
'''
    ),

    'uploadAndMatchVisualContext' : TestData(
        {
            'content' : '../resources/ctx_api_test.png',
        },
        custom_test_check = '''
self.match_id_upl_n_match = res.data.matchId
'''
    ),

    'createStringToContextBindings': TestData(
        {
            'bindings': Code("[{'contextUid': self.context_uid, 'stringHashcode': 'ede6083ebd2594ca4e557612aaa05b2e'},\n             {'contextUid': self.context_uid_img, 'stringHashcode': '4f25feab674accf572433f22dc516e2e'}]"),
        },
        custom_test_check = '''
assert_equal(res.data.errors['totalCount'], 0)
assert_equal(res.data.created['totalCount'], 2)
items = res.data.created['items']
self.binding_uno = items[0]['bindingUid']
self.binding_dos = items[1]['bindingUid']
'''
    ),

    'getBindings': TestData(
        {
            'stringHashcodes': ['ede6083ebd2594ca4e557612aaa05b2e','4f25feab674accf572433f22dc516e2e'],
            'contentFileUri' : '',
            'contextUid' : '',
            'bindingUids' : [],
        },
        custom_test_check = '''
print('Total bindings count:',len(res.data.items))
assert_equal(len(res.data.items), 2)
'''
    ),

    'deleteBindings': TestData(
        {
            'stringHashcodes': [],
            'contentFileUri' : '',
            'contextUid' : '',
            'bindingUids' : Code('[self.binding_uno, self.binding_dos]'),
        },
        custom_test_check = '''
assert_equal(res.data.totalCount, 2)
'''
    ),
}
