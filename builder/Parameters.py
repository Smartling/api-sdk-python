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


class Code:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class ApiCore:
    def __init__(self, swaggerDict):
        self.swaggerDict = swaggerDict

    def resolveRef(self, ref):
        if not ref.startswith('#/'):
            raise Exception('Unknown $ref:%s' % ref)
        pth = ref[2:].split('/')
        dct = self.swaggerDict
        lastname = ''
        for p in pth:
            dct = dct[p]
            lastname = p
        return dct, lastname


class Parameter(ApiCore):
    def __init__(self, param_dict, swaggerDict):
        ApiCore.__init__(self, swaggerDict)
        self._required = False
        self._name = ""
        param_names = ['name', 'description', 'in', 'required', 'schema']
        self.processParams(param_names, param_dict)
        self._type = "string"

        if self._schema:
            if '$ref' == list(self._schema.keys())[0]:
                self._schema, refname = self.resolveRef(self._schema['$ref'])
            self._type = self._schema['type']
            self._default = self._schema.get('default', None)

    def processParams(self, param_names, param_dict):
        for name in param_names:
            n = param_dict.get(name, None)
            if 'name' == name:
                n = n.replace('[]', '')
            setattr(self, '_' + name, n)

    def getParamForName(self):
        if self._required:
            return self._name
        return "%s=%s" % (self._name, self.getDefault())

    def getParamForMethodCall(self, values={}):
        value = values.get(self._name, self._name)
        if type(value) == type(Code):
            pass
        elif value != self._name and type(value) == str:
            value = "'" + value + "'"
        if 'accountUid' == self._name:
            value = 'self.MY_ACCOUNT_UID'
        return "%s=%s" % (self._name, value)

    def getDefault(self):
        default = getattr(self, '_default', None)
        if default is None:
            default = "''"
        if "string" == self._type and default != "''":
            default = "'" + default + "'"
        if 'array' == self._type:
            return '[]'
        if 'integer' == self._type and default == "''":
            return '0'
        return default


class MultipartProperty(Parameter):
    def __init__(self, name, paramDict, swaggerDict):
        self._format = None
        self._type = None
        param_names = ['description', 'format', 'type', 'default', 'example']
        self.processParams(param_names, paramDict)
        self._required = False
        self._name = name.replace('[]', '').split(' ')[0]
        self.isRequestBody = False
        self.swaggerDict = swaggerDict

    def setRequired(self):
        self._required = True

    def __str__(self):
        if self._format:
            return "%s : %s-%s" % (self._name, self._type, self._format)
        return "%s : %s" % (self._name, self._type)

