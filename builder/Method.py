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

import json
import importlib
from builder.Parameters import ApiCore, Parameter, MultipartProperty


class Method(ApiCore):
    indent = '    '
    indent2 = indent*2
    indent3 = indent*3
    indent4 = indent*4

    def __init__(self, apiName, apiNameUnderscore, path, method, descriptionDict, swaggerDict):
        ApiCore.__init__(self, swaggerDict)
        self.operationId = ''
        self.type = ''
        self.multipartParameters = []
        self.requestBody = ''
        for name in ['summary', 'description', 'tags', 'operationId', 'responses', 'x-code-samples', 'requestBody', 'deprecated']:
            setattr(self, name, descriptionDict.get(name, None))
        self.apiName = apiName
        self.apiNameUnderscore = apiNameUnderscore
        self.method = method
        self.path = path
        self.parameters = []

        for p in descriptionDict['parameters']:
            if 'projectId' == p['name']:
                continue  # We have projectId as api class member
            parameter = Parameter(p, swaggerDict)
            self.parameters .append(parameter)

        self.needMultipart = False
        self.isJson = False
        self.hasDirectives = False
        self.getMultipartProps()

    def build(self):
        rows = [
            self.buildName(),
            self.buildDoc()
        ]

        if self.needMultipart:
            rows.append(self.buildMultipart())
        else:
            rows.append(self.buildBody())

        return '\n'.join(rows)

    def buildExample(self):
        rows = [
            self.buildTestName(),
            self.buildDoc(),
            self.buildTestBody(),
            ''
        ]
        joined = '\n'.join(rows)
        joined = joined.replace(self.indent2 + '\n', '\n')  # Remove whitespaces for separator line
        return joined

    def buildTestName(self):
        return ''.join([
            self.indent,
            'def check',
            self.operationId[0].capitalize() + self.operationId[1:],
            '(self):',
            ]
        )

    def buildName(self):
        return ''.join([
            self.indent,
            'def ',
            self.operationId,
            '(self',
            self.buildParams(),
            ', **kwargs):',
        ]
        )

    def buildParams(self):
        result = ''
        joined = self.parameters + self.multipartParameters
        self.rearrangeRequired(joined)
        if joined:
            result += ", " + ", ".join(x.getParamForName() for x in joined)
        if self.hasDirectives:
            result += ', directives={}'
        return result

    def buildDoc(self):
        commentMarker = self.indent2 + '"""'
        docLines = [
            commentMarker,
            self.indent3 + 'method  :  ' + self.method.upper(),
            self.indent3 + 'api url :  ' + self.path,
        ]
        curl_example = self.getCurlExample()
        if curl_example:
            docLines.append(curl_example)

        nested = self.listNestedValues()
        if nested:
            docLines.append(nested)
        docLines = self.getResponsesDescription(docLines)
        details = self.indent3 + 'details :  https://api-reference.smartling.com/#operation/' + self.operationId
        docLines.append(details)
        docLines.append(commentMarker)

        return '\n'.join(docLines)

    def getResponsesDescription(self, docLines):
        result = []
        responses = getattr(self, 'responses', {})
        for code, codeDict in responses.items():
            descr = codeDict.get('description', '')
            if descr:
                result.append(self.indent2 + '%s : %s' % (code, descr))
        if result:
            result.insert(0, self.indent + "Responses:")
            responses = self.joinWithIndent(result, self.indent2)
            docLines.append(responses)
        return docLines

    def getCurlExample(self):
        result = []
        samples = getattr(self, 'x-code-samples', [])
        if not samples:
            return ''

        for d in samples:
            result.append(self.indent + 'as curl :  ' + d['source'].replace('\n', ''))
        return self.joinWithIndent(result, self.indent2)

    def getPropertyDescription(self, prop):
        prop_dict = {}
        for m in prop.prop_list:
            prop_dict[m._name] = getattr(m, '_example', '') or m.getDefault()

        result = [self.indent + 'Parameters example:']
        hdr = self.indent + '%s: ' % prop._name
        dumped = json.dumps(prop_dict, indent=16)
        dumped = dumped.replace('}', self.indent4+'}')
        result.append(hdr + dumped)
        return result

    def listNestedValues(self):
        result = []
        for prop in self.multipartParameters:
            if not getattr(prop, 'prop_list', None):
                continue
            result += self.getPropertyDescription(prop)
        if result:
            return self.joinWithIndent(result, self.indent2)
        return ''

    def joinWithIndent(self, lst, indent):
        newlinePlusIndent = '\n'+indent
        return indent + newlinePlusIndent.join(lst)

    def buildPathParamsStr(self):
        pathParameters = [x for x in self.parameters if x._in == 'path']
        if not pathParameters:
            return ''
        pthArgs = ['%s=%s' % (x._name, x._name) for x in pathParameters]
        return ', ' + ', '.join(pthArgs)

    def buildBody(self):
        bodyLines = []

        valuesToPass = "kw"
        bodyLines.append('kw = {')

        kw_params = [x for x in self.parameters if x._in == 'query']
        for p in kw_params:
            bodyLines.append(self.indent + "'%s':%s," % (p._name, p._name))
        for m in self.multipartParameters:
            if m.isRequestBody:
                valuesToPass = m._name
                continue
            if 'binary' == m._format:
                raise Exception("Incompatible parameter format for command")
            bodyLines.append(self.indent + "'%s':%s," % (m._name, m._name))
        bodyLines.append('}')
        bodyLines.append('kw.update(kwargs)')
        bodyLines.append("url = self.urlHelper.getUrl('%s'%s, **kwargs)" % (self.path, self.buildPathParamsStr()))
        cmd = "response, status = self.command('%s', url, %s)" % (self.method.upper(), valuesToPass)
        if self.method.upper() in ('POST', 'PUT') and self.isJson:
            cmd = "response, status = self.commandJson('%s', url, %s)" % (self.method.upper(), valuesToPass)
        bodyLines.append(cmd)
        bodyLines.append("return response, status")

        return self.joinWithIndent(bodyLines, self.indent2)

    def buildTestBody(self):
        bodyLines = []

        parameters = []
        initialisers = {}

        testDataModule = importlib.import_module('testdata.'+self.apiName+'TestData')
        decorators = getattr(testDataModule, 'testDecorators')

        jobsTestData = None
        if self.operationId in decorators.keys():
            jobsTestData = decorators[self.operationId]
            initialisers = jobsTestData.fields
            for line in jobsTestData.preCalls:
                bodyLines.append(line)
        for p in self.parameters + self.multipartParameters:
            if p._required or p._name in initialisers:
                parameters.append(p.getParamForMethodCall())

        kwParams = [x for x in self.parameters if x._in == 'query' or x._in == 'path']
        for p in kwParams + self.multipartParameters:
            if p._required or p._name in initialisers:
                bodyLines.append(p.getParamForMethodCall(initialisers))

        callParams = ', '.join(parameters)
        bodyLines.append('res, status = self.%s_api.%s(%s)' % (self.apiNameUnderscore, self.operationId, callParams))
        bodyLines.append('')

        if jobsTestData and jobsTestData.customTestCheck:
            bodyLines += jobsTestData.customTestCheck.split('\n')

        if jobsTestData and jobsTestData.is_apiv2_response:
            bodyLines.append('assert_equal(True, status in [200,202])')
            bodyLines.append('assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])')
        bodyLines.append("print('%s', 'OK')" % self.operationId)
        if jobsTestData:
            for line in jobsTestData.postCalls:
                bodyLines.append(line)

        return self.joinWithIndent(bodyLines, self.indent2)

    def listProperty(self, name):
        if not name:
            raise Exception("Can't determine property name")
        mp = MultipartProperty(name, {'type': 'array'}, self.swaggerDict)
        mp.setRequired()
        mp.isRequestBody = True
        self.multipartParameters.insert(0, mp)

    def getMultipartProps(self):
        self.multipartParameters = []
        if not self.requestBody:
            return
        self.resolveRequestBodyRef()
        self.type = list(self.requestBody['content'].keys())[0]
        if 'application/json' == self.type:
            self.isJson = True

        schema = self.requestBody['content'][self.type]['schema']

        refname = ''
        if '$ref' == list(schema.keys())[0]:
            schema, refname = self.resolveRef(schema['$ref'])

        props = schema.get('properties', None)
        if props is None:
            if 'array' == schema['type']:
                self.listProperty(refname)
                return
            else:
                print (schema)

        self.multipartParameters = self.parseProperties(props)

        for req in schema.get('required', []):
            for mp in self.multipartParameters:
                if req == mp._name:
                    mp.setRequired()

        self.rearrangeRequired(self.multipartParameters)

    def resolveRequestBodyRef(self):
        for key in self.requestBody:
            if '$ref' == key:
                resolved, refname = self.resolveRef(self.requestBody['$ref'])
                self.requestBody = resolved
                return

    def rearrangeRequired(self, params):
        needRearrangeIndex = []
        hasOptional = False
        positionToInsert = 0
        for p in params:
            if not p._required:
                hasOptional = True
                if not hasOptional:
                    positionToInsert = params.index(p)
                continue
            if hasOptional:
                needRearrangeIndex.append(params.index(p))
        for idx in needRearrangeIndex:
            p = params[idx]
            del params[idx]
            params.insert(positionToInsert, p)
            positionToInsert += 1

    def parseProperties(self, props):
        propList = []
        for k in props.keys():
            propDict = props[k]
            if k.startswith('smartling.'):
                self.hasDirectives = True
                continue

            mp = MultipartProperty(k, propDict, self.swaggerDict)
            propList.append(mp)

            if 'application/json' == self.type:
                if mp._description and 'required' in mp._description:
                    mp.setRequired()

            if propDict.get('properties', None):
                mp.prop_list = self.parseProperties(propDict['properties'])

            if mp._format == 'binary':
                self.needMultipart = True
        return propList

    def buildMultipart(self):
        result = [
            'kw = {',
        ]
        kw_params = [x for x in self.parameters if x._in == 'query']
        for p in kw_params:
            result.append(self.indent + "'%s':%s," % (p._name, p._name))
        for m in self.multipartParameters:
            if 'binary' == m._format:
                result.append(self.indent + "'%s':self.processFile(%s)," % (m._name, m._name))
            elif not 'directives' == m._name:
                result.append(self.indent + "'%s':%s," % (m._name, m._name))
        result.append('}')

        result += self.addDirectives()
        result.append("url = self.urlHelper.getUrl('%s'%s)" % (self.path, self.buildPathParamsStr()))
        result.append("return self.uploadMultipart(url, kw)")

        return self.joinWithIndent(result, self.indent2)

    def addDirectives(self):
        if self.hasDirectives:
            return ["self.addLibIdDirective(kw)",
                    'self.processDirectives(kw, directives)']
        else:
            return []
