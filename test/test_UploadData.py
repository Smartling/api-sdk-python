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

from smartlingApiSdk.UploadData import UploadData
from smartlingApiSdk.SmartlingDirective import SmartlingDirective



class TestUploadData(object):
    def test_init(self):
        ud = UploadData("path", "name", "type")
        assert ud.path == "path"
        assert ud.name == "name"
        assert ud.type == "type"
        assert ud.type == "type"
        assert ud.approveContent == "false"
        assert ud.callbackUrl == ""

    def test_setApproveContent(self):
        ud = UploadData("path", "name", "type")
        ud.setApproveContent("true")
        assert ud.approveContent == "true"

    def test_setCallbackUrl(self):
        ud = UploadData("path", "name", "type")
        ud.setCallbackUrl("smartling.com")
        assert ud.callbackUrl == "smartling.com"

    def test_addDirective(self):
        ud = UploadData("path", "name", "type")
        assert len(ud.directives) == 0

        ud.addDirective(SmartlingDirective("name", "value"))
        assert len(ud.directives) == 1
        assert ud.directives[0].name == "name"

        ud.addDirective(SmartlingDirective("name2", "value2"))
        assert len(ud.directives) == 2
        assert ud.directives[1].value == "value2"
