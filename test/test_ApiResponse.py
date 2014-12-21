#!/usr/bin/python
# -*- coding: utf-8 -*-


''' Copyright 2013 Smartling, Inc.
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
 * limitations under the License.
'''

import os
import sys

lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from smartlingApiSdk.ApiResponse import ApiResponse
from nose.tools import assert_equal


class test_ApiResponse(object):
    JSON_STATUS = '{"response":{"data":{"fileUri":"javaUTF16.properties","wordCount":4,"fileType":"javaProperties","callbackUrl":"http://yourdomain.com/callback","lastUploaded":"2014-06-10T12:29:17","stringCount":4,"approvedStringCount":4,"completedStringCount":0},"code":"SUCCESS","messages":[]}}'
    def test_init(self):
        pass
        
    def test_ApiResponse_status(self):
        ar = ApiResponse(self.JSON_STATUS, "200")

        assert_equal(ar.status_code, "200")
        assert_equal(ar.code, "SUCCESS")
        assert_equal(ar.messages, [])

        assert_equal(ar.data.lastUploaded, '2014-06-10T12:29:17')
        assert_equal(ar.data.fileType, 'javaProperties')
        assert_equal(ar.data.stringCount, 4)
        assert_equal(ar.data.wordCount, 4)
        assert_equal(ar.data.approvedStringCount, 4)
        assert_equal(ar.data.fileUri, 'javaUTF16.properties')
        assert_equal(ar.data.completedStringCount, 0)
        assert_equal(ar.data.callbackUrl, 'http://yourdomain.com/callback')
