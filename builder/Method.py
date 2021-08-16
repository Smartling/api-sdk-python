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

    def __init__(self, path, method, description_dict):
        for name in ['summary', 'description', 'tags', 'operationId', 'responses', 'x-code-samples', 'requestBody']:
            setattr(self, name, description_dict.get(name, None))
        self.method = method
        self.path = path
        self.parameters = []
        self.oldSource = open('../smartlingApiSdk/FileApiV2.py').read().split('\n')
        self.UrlV2Helper = open('../smartlingApiSdk/UrlV2Helper.py').read().split('\n')
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
            result.append(self.indent+'Not FOUND')
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
        return '\n'.join([
            self.indent2 + '"""',
            self.indent3 + self.method,
            self.indent3 + self.path,
            self.indent3 + 'for details check: https://api-reference.smartling.com/#operation/'+self.operationId,
            self.getCurlExample(),
            self.getOldMethod(),
            self.indent2 + '"""'
        ]
        )

    def getCurlExample(self):
        result = []
        samples = getattr(self, 'x-code-samples', [])
        if not samples:
            return ''

        for d in samples:
            result.append( self.indent + d['source'] )
        return self.joinWithIndent(result, self.indent2)

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

    def getMultipartProps(self):
        self.mp_params = []
        self.hasDirectives = False
        if not self.requestBody: return
        self.type = list(self.requestBody['content'].keys())[0]

        schema = self.requestBody['content'][self.type]['schema']
        for k in schema['properties'].keys():
            prop_dict = schema['properties'][k]
            if k.startswith('smartling.'):
                self.hasDirectives = True
                continue
            mp = MuptipartProperty(k, prop_dict)
            self.mp_params.append(mp)

            if 'application/json' == self.type:
                mp.setRequired()

            if mp._format == 'binary':
                self.need_multipart = True

        for req in schema.get('required',[]):
            for mp in self.mp_params:
                if req == mp._name:
                    mp.setRequired()

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
