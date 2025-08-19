#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012-2025 Smartling, Inc.
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
"""

import os
import sys

lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from smartlingApiSdk.ApiResponse import ApiResponse



class TestApiResponse(object):
    JSON_STATUS = '{"response":{"data":{"fileUri":"javaUTF16.properties","wordCount":4,"fileType":"javaProperties","callbackUrl":"http://yourdomain.com/callback","lastUploaded":"2014-06-10T12:29:17","stringCount":4,"approvedStringCount":4,"completedStringCount":0},"code":"SUCCESS","messages":[]}}'
    def test_init(self):
        pass
        
    def test_ApiResponse_status(self):
        ar = ApiResponse(self.JSON_STATUS, "200", {"Content-Type":"application-json"})

        assert ar.statusCode == "200"
        assert ar.code == "SUCCESS"
        assert ar.messages == []
        assert ar.headers.get("Content-Type") == "application-json"

        assert ar.data.lastUploaded == '2014-06-10T12:29:17'
        assert ar.data.fileType == 'javaProperties'
        assert ar.data.stringCount == 4
        assert ar.data.wordCount == 4
        assert ar.data.approvedStringCount == 4
        assert ar.data.fileUri == 'javaUTF16.properties'
        assert ar.data.completedStringCount == 0
        assert ar.data.callbackUrl == 'http://yourdomain.com/callback'

    def test_ApiResponse_failed(self):
        failed_json = '{"response":{"code":"VALIDATION_ERROR","errors":[{"key":null,"message":"File not found: test_import.xml_2.2.4_1629202583.584802","details":null}]}}'
        ar = ApiResponse(failed_json, "404", {"Content-Type":"application-json"})
        try:
            ua = ar.unexisting
        except AttributeError as e:
            assert str(e) == "ApiResponse has no attribute 'unexisting'"
        assert ar.code == "VALIDATION_ERROR"
