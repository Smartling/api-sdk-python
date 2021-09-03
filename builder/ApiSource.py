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

import json
import collections
from Parameters import Parameter, MuptipartProperty
from Method import Method
from ExampleData import exampleHeader, exampleFooter, testsFooter

class ApiSource():
    def __init__(self, full_name, api_name):
        self.full_name = full_name
        self.methods = []
        self.api_name = api_name

    def collectMethods(self, opaDict):
        pt = opaDict['paths']
        all_tags = []
        for k,v  in opaDict['paths'].items():
            for method, descr in v.items():
                if method == '$ref': continue
                #if descr['operationId'] != 'assignCustomFieldsToProject': continue
                if self.full_name in descr['tags']:
                    m = Method(self.api_name, k, method, descr, opaDict)
                    self.patchExportTranslations(descr, m)
                    self.methods.append(m)

    def patchExportTranslations(self, descr, m):
        if descr['operationId'] == 'exportFileTranslations':
            prop_dict = {
                "type": "string",
                "format": "binary",
                "description": "The file contents to upload."
            }
            mp = MuptipartProperty('file', prop_dict)
            mp.setRequired()
            m.need_multipart = True
            m.mp_params.insert(0, mp)

    def build(self):
        rows = []
        rows.append('from smartlingApiSdk.UrlV2Helper import UrlV2Helper')
        rows.append('from .ApiV2 import ApiV2')
        rows.append('')
        rows.append('class %sApi(ApiV2):' % self.api_name)
        rows.append('')
        rows.append('    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None):')
        rows.append('        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings)')
        rows.append('        self.urlHelper = UrlV2Helper(projectId)')
        rows.append('')

        for m in self.methods[:]:
            built = m.build()
            if built:
                rows.append(built)
                rows.append('')
                rows.append('')
                rows.append('')
        return '\n'.join(rows)


    def methodByName(self, name):
        for m in self.methods:
            if m.operationId == name:
                return m
        raise Exception("Can't find method:"+name)

    def importTestData(self):
        testDataModule = __import__(self.api_name+'TestData')
        extra_initializations = getattr(testDataModule, 'extra_initializations')
        tests_order = getattr(testDataModule, 'tests_order')
        return extra_initializations, tests_order

    def buildTestOrExample(self, footer, indent):
        rows = []

        myname = self.api_name + "Api"

        extra_initializations, tests_order = self.importTestData()
        hdr = exampleHeader.replace('{API_NAME}', myname)
        hdr += extra_initializations

        mnmes = [m.operationId for m in self.methods]
        mnmes.insert(0, "'''")
        mnmes.insert(0, '# not covered by tests #')
        rows.append(hdr)
        test_calls = []

        for name in tests_order:
            m = self.methodByName(name)
            mnmes.remove(name)

            built = m.buildExample()
            capitalized = m.operationId[0].capitalize() + m.operationId[1:]

            test_call = 't.check%s()' % capitalized
            test_calls.append(test_call)

            if built:
                rows.append(built)
                rows.append('')

        mnmes.append("'''")

        ftr = footer.replace('{API_NAME}', myname)
        newline_w_indent = '\n'+ '    ' * indent
        rows.append(ftr % newline_w_indent.join(test_calls + mnmes))
        return '\n'.join(rows)

    def buildExample(self):
        return self.buildTestOrExample(exampleFooter, indent=1)

    def buildTest(self):
        return self.buildTestOrExample(testsFooter, indent=2)

