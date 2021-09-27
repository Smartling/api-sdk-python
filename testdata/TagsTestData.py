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
    'getTagsListByProject',
    'getAllTagsForStrings',
    'addTagToStrings',
    'removeTagsFromStrings',
    'addTagToStrings',
    'removeAllTagsFromStrings'
]

extra_initializations = '''
'''

test_evnironment = 'stg'

test_decortators = {
    'getTagsListByProject':TestData(
        {
        },
        custom_test_check = '''
assert_equal(True, hasattr(res.data, 'items'))
'''
    ),

   'getAllTagsForStrings' : TestData (
       {
           'stringHashcodes' : Code("['e1159037badca0a2a618f62c50eff1bb', ] # use your string hashcodes list here")
       },
       custom_test_check = '''
assert_equal(True, hasattr(res.data, 'items'))
assert_equal('e1159037badca0a2a618f62c50eff1bb', res.data.items[0]['stringHashcode'])
'''
   ),

   'addTagToStrings' : TestData (
       {
           'stringHashcodes' : Code("['e1159037badca0a2a618f62c50eff1bb', ] # use your string hashcodes list here"),
           'tags' : Code("['Uno', 'Dos']")
       },
       custom_test_check = '''
assert_equal([], res.errors)
'''
   ),

   'removeTagsFromStrings' : TestData (
       {
           'stringHashcodes' : Code("['e1159037badca0a2a618f62c50eff1bb', ] # use your string hashcodes list here"),
           'tags' : Code("['Uno', 'Dos']")
       },
       custom_test_check = '''
assert_equal([], res.errors)
'''
   ),

    'removeAllTagsFromStrings' : TestData (
    {
       'stringHashcodes' : Code("['e1159037badca0a2a618f62c50eff1bb', ] # use your string hashcodes list here"),
    },
       custom_test_check = '''
assert_equal([], res.errors)
'''
   ),

}