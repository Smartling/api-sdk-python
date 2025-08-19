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

from smartlingApiSdk.SmartlingDirective import SmartlingDirective
from smartlingApiSdk.version import version
from smartlingApiSdk.ApiV2 import ApiV2
import pytest




class TestSmartlingDirective(object):
    def test_init(self):
        d = SmartlingDirective("placeholder_format_custom", "%s")
        assert d.name == "placeholder_format_custom"
        assert d.value == "%s"

        d1 = SmartlingDirective("plaCeholder_Format_cusTom", None)
        assert d1.name == "placeholder_format_custom"
        assert d1.value == ""

    def test_init_empty_name(self):
        with pytest.raises(Exception):
            SmartlingDirective("", "%s")

    def test_init_None_name(self):
        with pytest.raises(Exception):
            SmartlingDirective(None, "%s")

    def test_remove_sl_prefix(self):
        d = SmartlingDirective("smartling.placeholder_format_custom", "%s")
        assert d.name == "placeholder_format_custom"

        d2 = SmartlingDirective("sl.placeholder_format_custom", "%s")
        assert d2.name == "sl.placeholder_format_custom"

        d3 = SmartlingDirective("smartling.placeholder_format_custom smartling.none", "%s")
        assert d3.name == "placeholder_format_custom smartling.none"

    def test_lib_id_directive(self):
        apiV2 = ApiV2("1", "2", "3")
        apiV2.clientUid = "test_test"
        params = {}
        apiV2.addLibIdDirective(params)
        assert True == (SmartlingDirective.SL_PREFIX + 'client_lib_id' in params)
        assert params[SmartlingDirective.SL_PREFIX + 'client_lib_id'] == "test_test"
