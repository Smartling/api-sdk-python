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

import os
import sys

sys.path.append(os.path.abspath('../'))
isPython3 = sys.version_info[:2] >= (3, 0)

import json
import collections
from builder.ApiSource import ApiSource
from smartlingApiSdk.HttpClient import HttpClient
from smartlingApiSdk.Logger import Logger
from smartlingApiSdk.Settings import Settings


class ApiBuilder:
    """
    builds api based in openapi description for specific Api family defined as full_name
    """

    def __init__(self, fullName):
        self.api_name = fullName.replace(' ', '').replace('&', '')
        json_dict = self.getApiJson()
        self.apisrc = ApiSource(fullName, self.api_name)
        self.apisrc.collectMethods(json_dict)

    def getApiJson(self):
        httpLoader = HttpClient('api-reference.smartling.com')
        responseData, statusCode, headers = httpLoader.getHttpResponseAndStatus('GET', '/swagger.json', {})
        if 200 != statusCode:
            raise Exception('Can not load openapi description')
        if isPython3:
            responseData = responseData.decode('utf8')
        open("openapi3.json", 'w').write(responseData)
        jsonString = responseData
        return json.loads(jsonString, object_pairs_hook=collections.OrderedDict)

    def build(self):
        built = self.apisrc.build()
        outPath = '../smartlingApiSdk/api/%sApi.py' % self.api_name
        open(outPath, 'w').write(built)
        print (built)
        return self  # Allow tagged calls : build().buildExample().buildTest()

    def buildExample(self):
        built = self.apisrc.buildExample()

        outPath = '../smartlingApiSdk/example/%sExample.py' % self.api_name
        open(outPath, 'w').write(built)
        print (built)
        return self  # Allow tagged calls : build().buildExample().buildTest()

    def buildTest(self):
        built = self.apisrc.buildTest()

        outPath = '../test/test%s.py' % self.api_name
        open(outPath, 'w').write(built)
        print (built)
        return self  # Allow tagged calls : build().buildExample().buildTest()


def main():
    sys.stdout = Logger('python-sdk', Settings.logLevel)
    ApiBuilder("Jobs").build().buildExample().buildTest()
    ApiBuilder("Job Batches V2").build().buildExample().buildTest()
    ApiBuilder("Strings").build().buildExample().buildTest()
    ApiBuilder("Context").build().buildExample().buildTest()
    ApiBuilder("Estimates").build().buildExample().buildTest()
    ApiBuilder("Account & Projects").build().buildExample().buildTest()
    ApiBuilder("Files").build().buildExample().buildTest()
    ApiBuilder("Tags").build().buildExample().buildTest()

if __name__ == '__main__':
    main()
