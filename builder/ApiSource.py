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
    def __init__(self, full_name, api_name, test_evnironment='prod'):
        self.full_name = full_name
        self.methods = []
        self.api_name = api_name

    def collectMethods(self, opaDict):
        pt = opaDict['paths']
        all_tags = []
        methods_to_build = []
        for k,v  in opaDict['paths'].items():
            for method, descr in v.items():
                if method == '$ref': continue
                if methods_to_build and descr['operationId'] not in methods_to_build: #debug build for specific methods only
                    continue
                if self.full_name in descr['tags']:
                    m = Method(self.api_name, k, method, descr, opaDict)
                    self.patchMethods(descr, m, opaDict)
                    self.methods.append(m)

    def patchMethods(self, descr, m, opa_dict):
        if descr['operationId'] == 'exportFileTranslations':
            prop_dict = {
                "type": "string",
                "format": "binary",
                "description": "The file contents to upload."
            }
            mp = MuptipartProperty('file', prop_dict, opa_dict)
            mp.setRequired()
            m.need_multipart = True
            m.mp_params.insert(0, mp)
        if descr['operationId'] in ('getAllSourceStringsByProject'):
            m.method = 'post'
            m.is_json = True
        if descr['operationId'] in ('getAllTranslationsByProject'):
            m.method = 'post'
            m.is_json = True
            #import pdb; pdb.set_trace()
            if m.parameters[0]._name == 'hashcodes':
                p = m.parameters[0]
                del (m.parameters[0])
                m.parameters.insert(1, p)


    def build(self):
        rows = []
        rows.append('from smartlingApiSdk.UrlV2Helper import UrlV2Helper')
        rows.append('from smartlingApiSdk.ApiV2 import ApiV2')
        rows.append('')
        rows.append('class %sApi(ApiV2):' % self.api_name)
        rows.append('')
        if self.api_name in ['JobBatchesV2', 'Strings']:
            rows.append("    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):")
            rows.append('        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings, permanentHeaders=permanentHeaders, env=env)')
        else:
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
        test_evnironment = getattr(testDataModule, 'test_evnironment', 'prod')
        return extra_initializations, tests_order, test_evnironment

    def buildTestOrExample(self, footer, indent):
        rows = []

        myname = self.api_name + "Api"

        extra_initializations, tests_order, test_evnironment = self.importTestData()
        hdr = exampleHeader.replace('{API_NAME}', myname)
        if 'stg' == test_evnironment:
            hdr = hdr.replace('Credentials()', "Credentials('stg')")
            hdr = hdr.replace('proxySettings)', "proxySettings, env='stg')")
        hdr += extra_initializations

        not_tested_calls = [m.operationId for m in self.methods]
        not_tested_calls.insert(0, "'''")
        not_tested_calls.insert(0, '# not covered by tests #')
        rows.append(hdr)
        test_calls = []

        for name in tests_order:
            m = self.methodByName(name)
            not_tested_calls.remove(name)

            built = m.buildExample()
            capitalized = m.operationId[0].capitalize() + m.operationId[1:]

            test_call = 't.check%s()' % capitalized
            test_calls.append(test_call)

            if built:
                rows.append(built)
                rows.append('')

        not_tested_calls.append("'''")
        if len(not_tested_calls) > 3:
            test_calls += not_tested_calls

        ftr = footer.replace('{API_NAME}', myname)
        newline_w_indent = '\n'+ '    ' * indent
        rows.append(ftr % newline_w_indent.join(test_calls))
        return '\n'.join(rows)

    def buildExample(self):
        return self.buildTestOrExample(exampleFooter, indent=1)

    def buildTest(self):
        return self.buildTestOrExample(testsFooter, indent=2)

