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
from ExampleData import exampleHeader, exampleFooter

class ApiSource():
    def __init__(self, name):
        self.name = name
        self.methods = []
        self.api_name = name.replace(' ','').replace('&','')

    def collectMethods(self, opaDict):
        pt = opaDict['paths']
        all_tags = []
        for k,v  in opaDict['paths'].items():
            for method, descr in v.items():
                if method == '$ref': continue
                #if descr['operationId'] != 'assignCustomFieldsToProject': continue
                if self.name in descr['tags']:
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
        rows.append('from .UrlV2Helper import UrlV2Helper')
        rows.append('from .ApiV2 import ApiV2')
        rows.append('')
        rows.append('class %sApiAuto(ApiV2):' % self.api_name)
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

    def buildExample(self):
        rows = []

        myname = self.api_name + "ApiAuto"

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

        ftr = exampleFooter.replace('{API_NAME}', myname)
        rows.append(ftr % "\n    ".join(test_calls + mnmes))
        return '\n'.join(rows)



