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

class Parameter():
    def __init__(self, param_dict):
        param_names = ['name', 'description', 'in', 'required', 'schema']
        self.processParams(param_names, param_dict)
        self._type = "string"
        if self._schema:
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
        else:
            return "%s=%s" % (self._name, self.getDefault())

    def getDefault(self):
        default = getattr(self, '_default', None)
        if default is None:
            default = "''"

        if 'array' == self._type:
            return '[]'
        if 'integer' == self._type:
            return '0'
        return default

class MuptipartProperty(Parameter):
    def __init__(self, name, param_dict):
        param_names = ['description', 'format', 'type', 'default', 'example']
        self.processParams(param_names, param_dict)
        self._required = False
        self._name = name.replace('[]','')

    def setRequired(self):
        self._required = True

    def __str__(self):
        if self._format:
            return "%s : %s-%s"  % (self._name, self._type, self._format)
        return "%s : %s" % (self._name, self._type)

