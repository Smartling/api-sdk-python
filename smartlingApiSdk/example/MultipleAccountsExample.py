    
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

lib_path = os.path.abspath('../../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from smartlingApiSdk.api.FilesApi import FilesApi
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class MultipleAccountsExample(object):

    def __init__(self, userIdentifier, userSecret, userProjectId, env):
        proxySettings = None
        self.files_api = FilesApi(userIdentifier, userSecret, userProjectId, proxySettings, env=env)

    def filterResponseListValue(self, res, key):
        return [x[key] for x in res.data.items]

    def getAllFilesByProject(self):
        res, code = self.files_api.getRecentlyUploadedSourceFilesList()
        return self.filterResponseListValue(res, 'fileUri')


def exampleMultipeAccounts():
    '''
        multiple accounts require multiple instances of same api class, each with own account credentials
        here we compare files with prod credentials vs files with stg credentials
    '''
    credentials = Credentials('prod') #Gets your Smartling credetnials from environment variables
    mae_prod = MultipleAccountsExample(credentials.MY_USER_IDENTIFIER, credentials.MY_USER_SECRET, credentials.MY_PROJECT_ID, 'prod')

    credentials = Credentials('stg') #Gets your Smartling credetnials from environment variables, there are stg specific env varinbales checked
    mae_stg = MultipleAccountsExample(credentials.MY_USER_IDENTIFIER, credentials.MY_USER_SECRET, credentials.MY_PROJECT_ID, 'stg')

    prod_files = mae_prod.getAllFilesByProject()
    stg_files  = mae_stg.getAllFilesByProject()

    print ("."*120)
    print ("Files shared betweed prod and stg")
    print ("."*120)
    for f in prod_files:
        if f in stg_files:
            print (f)
    print ("."*120)
exampleMultipeAccounts()
