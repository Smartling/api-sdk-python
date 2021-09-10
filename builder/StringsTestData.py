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
    'addStringsToProject',
    'getAddStringsToProjectRequestStatus',
    'getAllSourceStringsByProject',
    'getAllTranslationsByProject',
]

extra_initializations = '''
'''

test_evnironment = 'stg'

test_decortators = {
    'addStringsToProject':TestData(
        {
            'strings' : [
                {
                    "stringText": 'Strings API test from python api sdk',
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
                {
                    "stringText": 'Another Strings API test from python api sdk',
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
            ],
            'placeholderFormat' : 'none',
            'placeholderFormatCustom' : '',
            'namespace' : '',

        },
        [],
        [
            'self.processUid = res.data.processUid',
            "self.hashcode_0 = res.data.items[0]['hashcode']",
            "self.hashcode_1 = res.data.items[1]['hashcode']",
        ],
        custom_test_check = '''
assert_equal(res.data.wordCount, 15)
assert_equal(res.data.stringCount, 2)
assert_equal(res.data.items[0]['stringText'], 'Strings API test from python api sdk')
assert_equal(res.data.items[1]['stringText'], 'Another Strings API test from python api sdk')
'''
    ),

    'getAddStringsToProjectRequestStatus': TestData(
        {'processUid':Code('self.processUid')},
        custom_test_check = '''
assert_equal(res.data.processUid, self.processUid)
assert_equal(res.data.processStatistics['requested'], 2)
assert_equal(res.data.processStatistics['errored'], 0)
'''
    ),

    'getAllSourceStringsByProject': TestData(
        {'hashcodes':Code('[self.hashcode_0,self.hashcode_1]')},
         custom_test_check = '''
assert_equal(res.data.totalCount, 2)
assert_equal(res.data.items[0]['stringText'], 'Strings API test from python api sdk')
assert_equal(res.data.items[1]['stringText'], 'Another Strings API test from python api sdk')
'''
    ),

    'getAllTranslationsByProject': TestData(
        {
            'hashcodes':Code('[self.hashcode_0,self.hashcode_1]'),
            'targetLocaleId': 'zh-TW'
        },
        custom_test_check = '''
assert_equal(res.data.totalCount, 0)
'''
    ),
}