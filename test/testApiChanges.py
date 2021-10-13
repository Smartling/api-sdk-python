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

import os
import sys
from os import listdir
from os.path import isfile, join
import subprocess

lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from builder.ApiBuilder import ApiBuilder
from smartlingApiSdk.Logger import Logger
from smartlingApiSdk.Settings import Settings
import logging

isPython3 =  sys.version_info[:2] >= (3,0)

def assert_diff_is_empty(diff, cmd):
    if diff :
        print ("diff command is:", cmd)
        print (diff)
        err = "Api is changed"
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testApiChanges:
    api_path = '../smartlingApiSdk/api'
    example_path = '../smartlingApiSdk/example'

    def setUp(self):
        sys.stdout = Logger('python-sdk', Settings.logLevel)

    def tearDown(self):
        pass

    def command(self, cmd):
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output

    def fullPath(self, f):
        return join(self.api_path, f)

    def listApis(self):
        return [f for f in os.listdir(self.api_path) if isfile(self.fullPath(f)) and f.endswith('Api.py')]

    def testAll(self):
        for api_file_name in self.listApis():
            api_name = api_file_name[:-6]
            if 'AccountProjects' == api_name:
                api_name = 'Account & Projects'

            if 'JobBatchesV2' == api_name:
                api_name = 'Job Batches V2'

            print ("Cheking:%s" % api_name)
            apisrc = ApiBuilder(api_name).apisrc
            built_api = apisrc.build()
            self.checkDiff(api_file_name, self.api_path, built_api)
            built_example = apisrc.buildExample()
            example_file_name = api_file_name.replace('Api','Example')
            self.checkDiff(example_file_name, self.example_path, built_example)
            print ("isOk")

    def checkDiff(self, api_file_name, api_dir, built):
        outPath = '/tmp/'+api_file_name
        self.storeToFile(built, outPath)
        cmd = 'diff -u %s/%s %s' % (api_dir, api_file_name, outPath)
        diff = self.command(cmd)
        assert_diff_is_empty(diff.decode('utf8'), cmd)

    def storeToFile(self, data, path):
        out = open(path, 'w')
        out.write(data)
        out.close()


if __name__ == '__main__':
    t = testApiChanges()
    t.setUp()
    t.testAll()
    t.tearDown()