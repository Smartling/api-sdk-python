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
import os, sys
sys.path.append(os.path.abspath('../'))
isPython3 =  sys.version_info[:2] >= (3,0)

import json
import collections
from builder.ApiSource import ApiSource
from smartlingApiSdk.HttpClient import HttpClient
from smartlingApiSdk.Logger import Logger
import logging

class ApiBuilder:
    """
    builds api based in openapi description for specific Api familiy defined as full_name
    """
    def __init__(self, full_name):
        self.api_name = full_name.replace(' ','').replace('&','')
        json_dict = self.getApiJson()
        self.apisrc = ApiSource(full_name, self.api_name)
        self.apisrc.collectMethods(json_dict)

    def getApiJson(self):
        http_loader = HttpClient('api-reference.smartling.com')
        response_data, status_code, headers = http_loader.getHttpResponseAndStatus('GET', '/swagger.json', {})
        if 200 != status_code:
            raise Exception('Can not load openapi description')
        if isPython3:
            response_data = response_data.decode('utf8')
        open("openapi3.json",'w').write(response_data)
        json_string = response_data
        json_dict = json.loads(json_string, object_pairs_hook=collections.OrderedDict)
        return json_dict

    def build(self):
        built = self.apisrc.build()
        out_path = '../api/%sApi.py' % self.api_name
        open(out_path,'w').write(built)
        print (built)
        return self #allow tagged calls : build().buildExample().buildTest()

    def buildExample(self):
        built = self.apisrc.buildExample()

        out_path = '../example/%sExample.py' % self.api_name
        open(out_path,'w').write(built)
        print (built)
        return self #allow tagged calls : build().buildExample().buildTest()

    def buildTest(self):
        built = self.apisrc.buildTest()

        out_path = '../test/test%s.py' % self.api_name
        open(out_path,'w').write(built)
        print (built)
        return self #allow tagged calls : build().buildExample().buildTest()



def main():
    sys.stdout = Logger('python-sdk', logging.INFO)
    ApiBuilder("Jobs").build().buildExample().buildTest()
    ApiBuilder("Job Batches V2").build().buildExample().buildTest()
    ApiBuilder("Strings").build().buildExample().buildTest()
    ApiBuilder("Context").build().buildExample().buildTest()
    ApiBuilder("Estimates").build().buildExample().buildTest()
    ApiBuilder("Account & Projects").build().buildExample().buildTest()
    ApiBuilder("Files").build().buildExample().buildTest()

if __name__ == '__main__':
    main()