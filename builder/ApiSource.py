#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012-2021 Smartling, Inc.
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
 """

import importlib
from builder.Parameters import MultipartProperty
from builder.Method import Method
from builder.ExampleData import EXAMPLE_HEADER, EXAMPLE_FOOTER, TESTS_FOOTER, COPYRIGHT_HEADER


class ApiSource():
    def __init__(self, fullName, apiName):
        self.fullName = fullName
        self.methods = []
        self.apiName = apiName
        self.apiNameUnderscore = fullName.replace(' ', '_').replace('&', '').replace('__', '_').lower()

    def collectMethods(self, swaggerDict):
        toBuild = []
        for k, v in swaggerDict['paths'].items():
            for method, descr in v.items():
                if method == '$ref':
                    continue
                if toBuild and descr['operationId'] not in toBuild:  # Debug build for specific methods only
                    continue
                if self.fullName in descr['tags']:
                    m = Method(self.apiName, self.apiNameUnderscore, k, method, descr, swaggerDict)
                    self.patchMethods(descr, m, swaggerDict)
                    self.methods.append(m)

    def patchMethods(self, descr, m, swaggerDict):
        if descr['operationId'] == 'exportFileTranslations':
            propDict = {
                "type": "string",
                "format": "binary",
                "description": "The file contents to upload."
            }
            mp = MultipartProperty('file', propDict, swaggerDict)
            mp.setRequired()
            m.needMultipart = True
            m.multipartParameters.insert(0, mp)
        if descr['operationId'] in ('getAllSourceStringsByProject'):
            m.method = 'post'
            m.isJson = True
        if descr['operationId'] in ('addStringsToProject'):
            for p in m.parameters+m.multipartParameters:
                if p._name == 'namespace':
                    p._default = 'smartling.strings-api.default.namespace'
        if descr['operationId'] in ('getAllTranslationsByProject'):
            m.method = 'post'
            m.isJson = True
            if m.parameters[0]._name == 'hashcodes':
                p = m.parameters[0]
                del (m.parameters[0])
                m.parameters.insert(1, p)

    def build(self):

        header = COPYRIGHT_HEADER + '''

from smartlingApiSdk.ApiV2 import ApiV2

class %sApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)
''' % self.apiName
        rows = header.split('\n')
        for m in self.methods[:]:
            if m.deprecated: continue
            built = m.build()
            if built:
                rows.append(built)
                rows.append('')
                rows.append('')
        return '\n'.join(rows)

    def methodByName(self, name):
        for m in self.methods:
            if m.operationId == name:
                return m
        raise Exception("Can't find method:"+name)

    def buildExampleHeader(self):
        # Do dynamic imports based on apy_name
        testDataModule = importlib.import_module('testdata.'+self.apiName+'TestData')
        imports = getattr(testDataModule, 'imports', '')
        extraInitializations = getattr(testDataModule, 'extraInitializations')
        tearDown = getattr(testDataModule, 'tearDown', '')
        testsOrder = getattr(testDataModule, 'testsOrder')
        testEnvironment = getattr(testDataModule, 'testEnvironment', 'prod')

        hdr = EXAMPLE_HEADER
        if 'stg' == testEnvironment:
            hdr = hdr.replace('Credentials()', "Credentials('stg')")
            hdr = hdr.replace('proxySettings)', "proxySettings, env='stg')")
        tearDownMarker = '        print("tearDown", "OK")'
        hdr = hdr.replace(tearDownMarker, tearDown+tearDownMarker)
        hdr = hdr.replace("{EXTRA_IMPORTS}\n", imports)
        hdr += extraInitializations

        return hdr, testsOrder

    def buildTestOrExample(self, footer, indent):
        rows = []

        hdr, testsOrder = self.buildExampleHeader()

        apiNameApi = self.apiName + "Api"
        hdr = hdr.replace('{API_NAME}', apiNameApi)
        hdr = hdr.replace('{api_name}', self.apiNameUnderscore)
        ftr = footer.replace('{API_NAME}', apiNameApi)

        notTestedCalls = [m.operationId for m in self.methods if not m.deprecated]
        notTestedCalls.insert(0, "'''")
        notTestedCalls.insert(0, '# not covered by tests #')
        rows.append(hdr)
        testCalls = []

        for name in testsOrder:
            m = self.methodByName(name)
            if name in notTestedCalls:  # Test may occur twice in tests list
                notTestedCalls.remove(name)

            built = m.buildExample()
            capitalized = m.operationId[0].capitalize() + m.operationId[1:]

            testCalls.append('t.check%s()' % capitalized)

            if built:
                rows.append(built)
                rows.append('')

        notTestedCalls.append("'''")
        if len(notTestedCalls) > 3:
            testCalls += notTestedCalls

        newlineWithIndent = '\n' + '    ' * indent
        rows.append(ftr % newlineWithIndent.join(testCalls))
        return '\n'.join(rows)

    def buildExample(self):
        return self.buildTestOrExample(EXAMPLE_FOOTER, indent=1)

    def buildTest(self):
        return self.buildTestOrExample(TESTS_FOOTER, indent=2)


