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

class Method():
    indent = '    '
    indent2 = indent*2
    indent3 = indent*3
    indent4 = indent*4

    def __init__(self, path, method, description_dict, opa_dict):
        for name in ['summary', 'description', 'tags', 'operationId', 'responses', 'x-code-samples', 'requestBody']:
            setattr(self, name, description_dict.get(name, None))
        self.method = method
        self.path = path
        self.parameters = []
        self.oldSource = open('../smartlingApiSdk/FileApiV2.py').read().split('\n')
        self.UrlV2Helper = open('../smartlingApiSdk/UrlV2Helper.py').read().split('\n')
        self.opa_dict = opa_dict
        for p in description_dict['parameters']:
            if 'projectId' == p['name'] : continue
            self.parameters .append( Parameter(p) )
        self.need_multipart = False
        self.getMultipartProps()
        self.newMethodName = '.'+self.operationId+'('

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
            'def test',
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
        if self.parameters:
            result += ", " + ", ".join(x.getParamForName() for x in self.parameters)
        if self.mp_params:
            result += ", " + ", ".join(x.getParamForName() for x in self.mp_params)
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

        body_lines.append('kw = {')
        kw_params = [x for x in self.parameters if x._in == 'query']
        for p in kw_params:
            body_lines.append(self.indent + "'%s':%s," % (p._name, p._name))
        for m in self.mp_params:
            if 'binary' == m._format:
                raise Exception("Uncomaptible parameter format for command")
            body_lines.append(self.indent + "'%s':%s," % (m._name, m._name))
        body_lines.append('}')
        body_lines.append("url = self.urlHelper.getUrl('%s'%s)" % (self.path, self.buildPathParamsStr()))
        body_lines.append("return self.command('%s', url, kw)" % self.method.upper())

        return self.joinWithIndent(body_lines, self.indent2)

    def buildTestBody(self):
        body_lines = []

        parameters = []
        if self.parameters:
            for p in self.parameters:
                if not p._required: continue
                parameters.append(p.getParamForMethodCall())
        if self.mp_params:
            for p in self.mp_params:
                if not p._required: continue
                parameters.append(p.getParamForMethodCall())

        kw_params = [x for x in self.parameters if x._in == 'query']
        for p in kw_params:
            if not p._required: continue
            body_lines.append(p.getParamInit())
        for m in self.mp_params:
            if not m._required: continue
            body_lines.append(m.getParamInit())

        call_params = ', '.join(parameters)
        body_lines.append('res, status = self.papi.%s(%s)' % (self.operationId, call_params))
        body_lines.append('')
        body_lines.append('assert_equal(200, status)')
        body_lines.append('assert_equal(self.CODE_SUCCESS_TOKEN, res.code)')
        body_lines.append('print("%s", "OK")' % self.operationId)

        return self.joinWithIndent(body_lines, self.indent2)

    def resolveRef(self, ref):
        #import pdb; pdb.set_trace()
        if not ref.startswith('#/'):
            raise Exception('Unknown $ref:%s' % ref)
        pth = ref[2:].split('/')
        dct = self.opa_dict
        lastname = ''
        for p in pth:
            dct = dct[p]
            lastname = p
        return dct, lastname

    def listPrtoperty(self, name, array):
        if not name:
            raise Exception("Can't determine property name")
        mp = MuptipartProperty(name, {'type':'array'})
        mp.setRequired()
        self.mp_params.insert(0, mp)

    def getMultipartProps(self):
        self.mp_params = []
        self.hasDirectives = False
        if not self.requestBody: return
        self.type = list(self.requestBody['content'].keys())[0]

        print (self.type)
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

    def parseProperties(self, props):
        prop_list = []
        for k in props.keys():
            prop_dict = props[k]
            if k.startswith('smartling.'):
                self.hasDirectives = True
                continue

            mp = MuptipartProperty(k, prop_dict)
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
