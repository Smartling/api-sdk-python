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

from smartlingApiSdk.api.FilesApi import FilesApi
from nose.tools import assert_equal


class test_FilesApiUrls(object):

    def setUp(self):
        self.calls = []
        self.api = FilesApi('userIdentifier', 'userSecret', 'prj123')
        self.api.command = self.mock_command

    def mock_command(self, method, url, params):
        self.calls.append((method, url, params))
        return None, 200

    def test_downloadTranslatedFile_single_locale(self):
        self.api.downloadTranslatedFile('de-DE', 'x')
        assert_equal(self.calls[0][:2], ('GET', '/files-api/v2/projects/prj123/locales/de-DE/file'))
        assert_equal(self.calls[0][2]['fileUri'], 'x')

    def test_downloadTranslatedFile_locale_list_is_joined(self):
        self.api.downloadTranslatedFile(['de-DE', 'fr-FR'], 'x')
        assert_equal(self.calls[0][1], '/files-api/v2/projects/prj123/locales/de-DE,fr-FR/file')

    def test_legacy_downloadTranslatedFileSingleLocale_alias(self):
        self.api.downloadTranslatedFileSingleLocale('de-DE', 'x', retrievalType='pseudo', includeOriginalStrings=True)
        method, url, params = self.calls[0]
        assert_equal((method, url), ('GET', '/files-api/v2/projects/prj123/locales/de-DE/file'))
        assert_equal(params['fileUri'], 'x')
        assert_equal(params['retrievalType'], 'pseudo')
        assert_equal(params['includeOriginalStrings'], True)
