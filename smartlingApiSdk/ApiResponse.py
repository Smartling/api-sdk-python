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
 * limitations under the License.
"""

import json


class Data:
    """ provides dictionary items to be object attributes """
    def __init__(self, dict):
        self.dict = dict

    def __getattr__(self, key):
        return self.dict[key]

    def __str__(self):
        return repr(self.dict)


class ApiResponse:
    """ response object to store parsed json response as python object, it also behaves like string for backward
        compatibility with previous SDK versions where response was a string """
    def __init__(self, responseString, statusCode, headers):
        self.statusCode = statusCode
        self.responseString = responseString
        self.responseDict = json.loads(responseString)
        self.isApiResonse = self.responseDict.get('response', None) and dict == type(self.responseDict['response'])
        self.headers = headers
        if self.isApiResonse:
            self.parseResponse(responseString)

    def parseResponse(self, responseString):
        """ parses json and fills object attributes according json attributes """

        for k, v in list(self.responseDict['response'].items()):
            if k == 'data':
                self.data = Data(v)
            else:
                setattr(self, k, v)

    def __getattr__(self, key):
        """ provides string object methods to be available for response to behave like a string """
        if hasattr(self.responseDict, key):
            return getattr(self.responseDict, key)

        try:
            return getattr(self, key)
        except:
            pass

    def __str__(self):
        return str(self.responseString)
