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
    'addStringsToProject',
    'getAddStringsToProjectRequestStatus',
    'getAllSourceStringsByProject',
    'getAllTranslationsByProject',
]

imports = '''
# example of custom user-agent setup
from smartlingApiSdk.Settings import Settings
Settings.userAgent = "My Custom User Agent"

# example of custom logger settings
from smartlingApiSdk.Settings import Settings
import logging
Settings.logPath = '/tmp/python.sdk.log'
Settings.logLevel = logging.DEBUG
'''

extraInitializations = ''

testEnvironment = 'stg'

testDecorators = {
    'addStringsToProject':TestData(
        {
            'strings' : Code('''[
                {
                    "stringText": "Strings API test from python api sdk",
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
                {
                    "stringText": "Another Strings API test from python api sdk",
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
                {
                    "stringText": 'Service',
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
                {
                    "stringText": 'Usability Testing',
                    "callbackUrl": "https://test.strings.smartling.com/test",
                    "callbackMethod": "GET",
                    "instruction": "Do nothing it's a test",
                    "maxLength": 4096,
                    "format": "auto",
                },
            ]'''),
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
        customTestCheck='''
assert_equal(res.data.wordCount, 18)
assert_equal(res.data.stringCount, 4)
stringTexts = [res.data.items[0]['stringText'], res.data.items[1]['stringText']]
assert_equal(True, 'Strings API test from python api sdk' in stringTexts)
assert_equal(True, 'Another Strings API test from python api sdk' in stringTexts)
'''
    ),

    'getAddStringsToProjectRequestStatus': TestData(
        {'processUid':Code('self.processUid')},
        customTestCheck='''
assert_equal(res.data.processUid, self.processUid)
assert_equal(res.data.processStatistics['requested'], 4)
assert_equal(res.data.processStatistics['errored'], 0)
'''
    ),

    'getAllSourceStringsByProject': TestData(
        {'hashcodes':Code('[self.hashcode_0,self.hashcode_1]')},
         customTestCheck='''
assert_equal(res.data.totalCount, 2)
stringTexts = [res.data.items[0]['stringText'], res.data.items[1]['stringText']]
assert_equal(True, 'Strings API test from python api sdk' in stringTexts)
assert_equal(True, 'Another Strings API test from python api sdk' in stringTexts)
'''
    ),

    'getAllTranslationsByProject': TestData(
        {
            'hashcodes':Code('[self.hashcode_0,self.hashcode_1]'),
            'targetLocaleId': 'zh-TW'
        },
        customTestCheck='''
assert_equal(res.data.totalCount, 0)
'''
    ),
}