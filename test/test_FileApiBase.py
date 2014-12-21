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

from smartlingApiSdk.SmartlingDirective import SmartlingDirective
from smartlingApiSdk.FileApiBase import FileApiBase
from smartlingApiSdk.UploadData import UploadData
from smartlingApiSdk.Constants import Params
from nose.tools import assert_equal


class test_UploadData(object):
    def mock_uploadMultipart(self, uri, params):
        return params

    def test_commandUpload(self):
        ud = UploadData("path", "name", "type")

        api = FileApiBase("host", "apiKey", "projectId")
        api.uploadMultipart = self.mock_uploadMultipart
        params = api.commandUpload(ud)

        assert_equal(len(params), 4)
        assert_equal(params[Params.FILE_URI], "name")
        assert_equal(params[Params.FILE_TYPE], "type")
        assert_equal(params[Params.FILE_PATH], "pathname")
        assert_equal(params[Params.APPROVED], "false")

    def test_commandUpload_Callback_Approved(self):
        ud = UploadData("path", "name", "type")
        ud.setApproveContent("true")
        ud.setCallbackUrl("smartling.com")

        api = FileApiBase("host", "apiKey", "projectId")
        api.uploadMultipart = self.mock_uploadMultipart
        params = api.commandUpload(ud)

        assert_equal(len(params), 5)
        assert_equal(params[Params.APPROVED], "true")
        assert_equal(params[Params.CALLBACK_URL], "smartling.com")

    def test_commandUpload_Directives(self):
        ud = UploadData("path", "name", "type")
        ud.setApproveContent("true")
        ud.setCallbackUrl("smartling.com")
        ud.addDirective(SmartlingDirective("placeholder_format_custom", "\[.+?\]"))
        ud.addDirective(SmartlingDirective("placeholder_format", "IOS"))

        api = FileApiBase("host", "apiKey", "projectId")
        api.uploadMultipart = self.mock_uploadMultipart
        params = api.commandUpload(ud)

        assert_equal(len(params), 7)
        assert_equal(params["smartling.placeholder_format_custom"], "\[.+?\]")
        assert_equal(params["smartling.placeholder_format"], "IOS")
