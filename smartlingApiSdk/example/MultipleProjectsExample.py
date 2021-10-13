    
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

from smartlingApiSdk.api.StringsApi import StringsApi
from smartlingApiSdk.api.FilesApi import FilesApi
from smartlingApiSdk.api.AccountProjectsApi import AccountProjectsApi
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class MultipeProjectsExample(object):

    def __init__(self):
        credentials = Credentials('stg') #Gets your Smartling credetnials from environment variables
        self.MY_USER_IDENTIFIER = credentials.MY_USER_IDENTIFIER
        self.MY_USER_SECRET = credentials.MY_USER_SECRET
        self.MY_PROJECT_ID = credentials.MY_PROJECT_ID

        #needed for testProjects
        self.MY_ACCOUNT_UID = credentials.MY_ACCOUNT_UID
        self.MY_LOCALE = credentials.MY_LOCALE

        if self.MY_ACCOUNT_UID == "CHANGE_ME":
            print("can't test projects api call, set self.MY_ACCOUNT_UID or export SL_ACCOUNT_UID=*********")
            return

        useProxy = False
        if useProxy :
            proxySettings = ProxySettings("login", "password", "proxy_host", "proxy_port or None")
        else:
            proxySettings = None

        self.strings_api = StringsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')
        self.files_api = FilesApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')
        self.projects_api = AccountProjectsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

    def filterResponseListValue(self, res, key):
        return [x[key] for x in res.data.items]

    def getAllSourceStringsByProject(self, projectId, fileUri):
        '''
            example of usage custom projectId - add it as named parameter to any api call
        '''
        res, status = self.strings_api.getAllSourceStringsByProject(fileUri = fileUri, projectId=projectId)
        return self.filterResponseListValue(res, 'parsedStringText')


    def getAllFilesByProject(self, projectId):
        '''
            anoher example of usage custom projectId - add it as named parameter to any api call
        '''
        res, code = self.files_api.getRecentlyUploadedSourceFilesList(projectId=projectId)
        return self.filterResponseListValue(res, 'fileUri')

    def getAccountProjects(self):
        res, code  = self.projects_api.getProjectsByAccount(self.MY_ACCOUNT_UID, limit=10)
        return self.filterResponseListValue(res, 'projectId')

def exampleMultipeProjects():
    '''
        note - to access multiple projects one should have access to all projects
        here 10 projects within same account are used to get urls and strings per url
    '''
    mpe = MultipeProjectsExample()
    project_uids = mpe.getAccountProjects()
    popularity = {}
    for uid in project_uids[:]:
        files = mpe.getAllFilesByProject(uid)
        print("processing %s : %d files" % (uid, len(files)))
        for file_uri in files:
            strings =  mpe.getAllSourceStringsByProject(uid, file_uri)
            for str in strings:
                projects = popularity.get(str,{})
                projects[uid] = 1
                popularity[str] = projects

    items = list(popularity.items())
    items.sort(key=lambda x:len(x[1]) )
    items.reverse()
    print ("."*120)
    print ("top 5 popular strings:")
    print ("."*120)
    for str, uids in items[:5]:
        print("%s : %d projects : %s" % (str, len(uids), list(uids.keys())))
        print ("."*120)

exampleMultipeProjects()