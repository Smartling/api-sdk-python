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
from Parameters import ApiCore, Parameter, MuptipartProperty

class Method(ApiCore):
    indent = '    '
    indent2 = indent*2
    indent3 = indent*3
    indent4 = indent*4

    def __init__(self, api_name, path, method, description_dict, opa_dict):
        ApiCore.__init__(self, opa_dict)
        for name in ['summary', 'description', 'tags', 'operationId', 'responses', 'x-code-samples', 'requestBody']:
            setattr(self, name, description_dict.get(name, None))
        self.api_name = api_name
        self.method = method
        self.path = path
        self.parameters = []
        self.oldSource = open('../smartlingApiSdk/FileApiV2.py').read().split('\n')
        self.UrlV2Helper = open('../smartlingApiSdk/UrlV2Helper.py').read().split('\n')
        for p in description_dict['parameters']:
            if 'projectId' == p['name'] : continue
            parameter = Parameter(p, opa_dict)
            self.parameters .append(parameter)

        self.need_multipart = False
        self.is_json = False
        self.getMultipartProps()
        self.custom_test_check = ""

    def build(self):
        rows = []

        rows.append(self.buildName())
        rows.append(self.buildDoc())

        if self.need_multipart:
            rows.append(self.buildMultipart())
        else:
            rows.append(self.buildBody())
        rows.append('')
        return '\n'.join(rows)

    def buildExample(self):
        rows = []

        rows.append(self.buildTestName())
        rows.append(self.buildDoc())


        rows.append(self.buildTestBody())
        rows.append('')
        return '\n'.join(rows)

    def buildTestName(self):
        return ''.join([
            self.indent,
            'def check',
            self.operationId[0].capitalize() + self.operationId[1:],
            '(self',
            '):',
            ]
        )
    def buildName(self):
        return ''.join([
            self.indent,
            'def ',
            self.operationId,
            '(self',
            self.buildPrarams(),
            '):',
        ]
        )

    def buildPrarams(self):
        result = ''
        joined = self.parameters + self.mp_params
        self.rearrangeRequired(joined)
        if joined:
            result += ", " + ", ".join(x.getParamForName() for x in joined)
        if self.hasDirectives:
            result += ', directives={}'
        return result

    def getOldMethod(self):
        UHMethod = ''
        result = [self.indent + '-'*120]
        pt = self.path + '"'
        self.oldMethodName = ''
        for line in self.UrlV2Helper:
            if not pt in line: continue
            UHMethod = line.split(' = ')[0].strip()
            UHMethod = 'urlHelper.' + UHMethod
        if not UHMethod:
            return self.joinWithIndent(result, self.indent2)
        old_method_lines = []
        start = end = 0
        for i in range(len(self.oldSource)):
            if UHMethod in self.oldSource[i]:
                end = i
                start = i
                while not 'def ' in self.oldSource[start]:
                    start -= 1
                while not 'return ' in self.oldSource[end]:
                    end += 1
                if 'return ' in self.oldSource[end]: end +=1
                result +=  self.oldSource[start:end]
                break
        if not 'def ' in self.oldSource[start]: return ''
        if start == end :
            result.append(self.indent+'Unable to get old method body')
        self.oldMethodName = self.oldSource[start].split('def ')[1]
        self.oldMethodName = '.'+self.oldMethodName.split('(')[0] + '('
        res_str = self.joinWithIndent(result, self.indent2)
        return res_str.replace('"""', "'''")

    def buildDoc(self):
        doc_lines = [
            self.indent2 + '"""',
            self.indent3 + self.method,
            self.indent3 + self.path,
            self.indent3 + 'for details check: https://api-reference.smartling.com/#operation/'+self.operationId,
            self.getCurlExample(),
            self.getOldMethod(),
        ]
        nested = self.listNestedValues()
        if nested:
            doc_lines.append(nested)
        doc_lines.append(self.indent2 + '"""')

        return '\n'.join(doc_lines)

    def getCurlExample(self):
        result = []
        samples = getattr(self, 'x-code-samples', [])
        if not samples:
            return ''

        for d in samples:
            result.append( self.indent + d['source'] )
        return self.joinWithIndent(result, self.indent2)

    def getPropertyDescription(self, prop):
        prop_dict = {}
        for m in prop.prop_list:
            prop_dict[m._name] = getattr(m, '_example', '') or m.getDefault()

        result = [ self.indent + 'Parameters example:'
        ]
        hdr = self.indent +  '%s: ' % prop._name
        dumped = json.dumps(prop_dict, indent=16)
        dumped = dumped.replace('}', self.indent4+'}')
        result.append( hdr + dumped)
        return result

    def listNestedValues(self):
        result = []
        for prop in self.mp_params:
            if not getattr(prop, 'prop_list', None):
                continue
            result += self.getPropertyDescription(prop)
        if result:
            return self.joinWithIndent(result, self.indent2)
        return ''

    def joinWithIndent(self, lst, indent):
        newline_plus_indent = '\n'+indent
        return indent + newline_plus_indent.join(lst)

    def buildPathParamsStr(self):
        path_params = [x for x in self.parameters if x._in == 'path']
        if not path_params:
            return ''
        pth_args = ['%s=%s' % (x._name,x._name) for x in path_params]
        return ', '+ ', '.join(pth_args)

    def buildBody(self):
        body_lines = []

        values_to_pass = "kw"
        body_lines.append('kw = {')
        #import pdb; pdb.set_trace()
        kw_params = [x for x in self.parameters if x._in == 'query']
        for p in kw_params:
            body_lines.append(self.indent + "'%s':%s," % (p._name, p._name))
        for m in self.mp_params:
            if m.is_request_body:
                values_to_pass = m._name
                continue
            if 'binary' == m._format:
                raise Exception("Uncomaptible parameter format for command")
            body_lines.append(self.indent + "'%s':%s," % (m._name, m._name))
        body_lines.append('}')
        body_lines.append("url = self.urlHelper.getUrl('%s'%s)" % (self.path, self.buildPathParamsStr()))
        cmd = "return self.command('%s', url, %s)" % (self.method.upper(), values_to_pass)
        if self.method.upper() in ('POST', 'PUT') and self.is_json:
            cmd = "return self.commandJson('%s', url, %s)" % (self.method.upper(), values_to_pass)

        body_lines.append(cmd)

        return self.joinWithIndent(body_lines, self.indent2)

    def buildTestBody(self):
        body_lines = []

        parameters = []
        initializers = {}

        testDataModule = __import__(self.api_name+'TestData')
        testData = getattr(testDataModule, 'test_decortators')

        jobs_test_data = None
        if self.operationId in testData.keys():
            jobs_test_data = testData[self.operationId]
            initializers = jobs_test_data.fields
            self.custom_test_check = jobs_test_data.custom_test_check
            for line in jobs_test_data.pre_calls:
                body_lines.append(line)
        if self.parameters:
            for p in self.parameters:
                if p._required or p._name in initializers:
                    parameters.append(p.getParamForMethodCall())
        if self.mp_params:
            for p in self.mp_params:
                if p._required or p._name in initializers:
                    parameters.append(p.getParamForMethodCall())

        kw_params = [x for x in self.parameters if x._in == 'query' or x._in == 'path']
        for p in kw_params:
            if p._required or p._name in initializers:
                body_lines.append(p.getParamForMethodCall(initializers))
        for p in self.mp_params:
            if p._required or p._name in initializers:
                body_lines.append(p.getParamForMethodCall(initializers))

        call_params = ', '.join(parameters)
        body_lines.append('res, status = self.api.%s(%s)' % (self.operationId, call_params))
        body_lines.append('')
        if self.custom_test_check:
            body_lines += self.custom_test_check.split('\n')
        else:
            body_lines.append('assert_equal(True, status in [200,202])')
            body_lines.append('assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])')
        body_lines.append('print("%s", "OK")' % self.operationId)
        if jobs_test_data:
            for line in jobs_test_data.post_calls:
                body_lines.append(line)

        return self.joinWithIndent(body_lines, self.indent2)

    def listPrtoperty(self, name, array):
        if not name:
            raise Exception("Can't determine property name")
        mp = MuptipartProperty(name, {'type':'array'}, self.opa_dict)
        mp.setRequired()
        mp.is_request_body = True
        self.mp_params.insert(0, mp)

    def getMultipartProps(self):
        self.mp_params = []
        self.hasDirectives = False
        if not self.requestBody: return
        self.type = list(self.requestBody['content'].keys())[0]
        if 'application/json' == self.type:
            self.is_json = True

        schema = self.requestBody['content'][self.type]['schema']

        refname = ''
        if '$ref' == list(schema.keys())[0]:
            schema, refname = self.resolveRef(schema['$ref'])

        props = schema.get('properties', None)
        if props is None:
            type = schema['type']
            if 'array' == type:
                self.listPrtoperty(refname, schema['items'])
                return
            else:
                print (schema)

        self.mp_params = self.parseProperties(props)

        for req in schema.get('required',[]):
            for mp in self.mp_params:
                if req == mp._name:
                    mp.setRequired()

        self.rearrangeRequired(self.mp_params)

    def rearrangeRequired(self, params):
        need_rearrange_idx = []
        has_optional = False
        pos_to_insert = 0
        for p in params:
            if not p._required:
                has_optional = True
                if not has_optional:
                    pos_to_insert = params.index(p)
                continue
            if has_optional:
                need_rearrange_idx.append( params.index(p) )
        for idx in need_rearrange_idx:
            p = params[idx]
            del params[idx]
            params.insert(pos_to_insert, p)
            pos_to_insert += 1

    def parseProperties(self, props):
        prop_list = []
        for k in props.keys():
            prop_dict = props[k]
            if k.startswith('smartling.'):
                self.hasDirectives = True
                continue

            mp = MuptipartProperty(k, prop_dict, self.opa_dict)
            prop_list.append(mp)

            if 'application/json' == self.type:
                mp.setRequired()

            if prop_dict.get('properties', None):
                mp.prop_list = self.parseProperties(prop_dict['properties'])

            if mp._format == 'binary':
                self.need_multipart = True
        return prop_list

    def buildMultipart(self):
        body_lines = []

        body_lines.append('kw = {')
        kw_params = [x for x in self.parameters if x._in == 'query']
        for p in kw_params:
            body_lines.append(self.indent + "'%s':%s," % (p._name, p._name))
        for m in self.mp_params:
            if 'binary' == m._format:
                body_lines.append(self.indent + "'%s':self.processFile(%s)," % (m._name, m._name))
            elif not 'directives' == m._name:
                body_lines.append(self.indent + "'%s':%s," % (m._name, m._name))
        body_lines.append('}')

        body_lines += self.addDirectives()
        body_lines.append("url = self.urlHelper.getUrl('%s'%s)" % (self.path, self.buildPathParamsStr()))
        body_lines.append("return self.uploadMultipart(url, kw)")

        return self.joinWithIndent(body_lines, self.indent2)

    def addDirectives(self):
        if self.hasDirectives:
            return ["self.addLibIdDirective(kw)",
                    'self.processDirectives(kw, directives)']
        else:
            return []
