
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
import time, datetime

sys.path += [os.path.abspath('../'), os.path.abspath('../../')]  # allow to import ../smartlingApiSdk.api

import smartlingApiSdk
from smartlingApiSdk.api.TagsApi import TagsApi
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testTagsApi(object):

    CODE_SUCCESS_TOKEN = 'SUCCESS'
    ACCEPTED_TOKEN = 'ACCEPTED'

    def tearDown(self):
        print("tearDown", "OK")

    def setUp(self):
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

        self.tags_api = TagsApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

        print("setUp", "OK", "\n")


    def checkGetTagsListByProject(self):
        """
            method  :  GET
            api url :  /tags-api/v2/projects/{projectId}/tags
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/tags
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getTagsListByProject
        """
        res, status = self.tags_api.getTagsListByProject()


        assert_equal(True, hasattr(res.data, 'items'))

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getTagsListByProject', 'OK')


    def checkGetAllTagsForStrings(self):
        """
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/search
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/search
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getAllTagsForStrings
        """
        stringHashcodes=['e1159037badca0a2a618f62c50eff1bb', ] # use your string hashcodes list here
        res, status = self.tags_api.getAllTagsForStrings(stringHashcodes=stringHashcodes)


        assert_equal(True, hasattr(res.data, 'items'))
        assert_equal('e1159037badca0a2a618f62c50eff1bb', res.data.items[0]['stringHashcode'])

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getAllTagsForStrings', 'OK')


    def checkAddTagToStrings(self):
        """
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/add
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/add
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/addTagToStrings
        """
        tags=['Uno', 'Dos']
        stringHashcodes=['e1159037badca0a2a618f62c50eff1bb', ] # use your string hashcodes list here
        res, status = self.tags_api.addTagToStrings(tags=tags, stringHashcodes=stringHashcodes)


        assert_equal([], res.errors)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('addTagToStrings', 'OK')


    def checkRemoveTagsFromStrings(self):
        """
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/remove
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/remove
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/removeTagsFromStrings
        """
        tags=['Uno', 'Dos']
        stringHashcodes=['e1159037badca0a2a618f62c50eff1bb', ] # use your string hashcodes list here
        res, status = self.tags_api.removeTagsFromStrings(tags=tags, stringHashcodes=stringHashcodes)


        assert_equal([], res.errors)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('removeTagsFromStrings', 'OK')


    def checkAddTagToStrings(self):
        """
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/add
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/add
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/addTagToStrings
        """
        tags=['Uno', 'Dos']
        stringHashcodes=['e1159037badca0a2a618f62c50eff1bb', ] # use your string hashcodes list here
        res, status = self.tags_api.addTagToStrings(tags=tags, stringHashcodes=stringHashcodes)


        assert_equal([], res.errors)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('addTagToStrings', 'OK')


    def checkRemoveAllTagsFromStrings(self):
        """
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/remove/all
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/remove/all
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/removeAllTagsFromStrings
        """
        stringHashcodes=['e1159037badca0a2a618f62c50eff1bb', ] # use your string hashcodes list here
        res, status = self.tags_api.removeAllTagsFromStrings(stringHashcodes=stringHashcodes)


        assert_equal([], res.errors)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('removeAllTagsFromStrings', 'OK')



def example():
    t = testTagsApi()
    t.setUp()
    t.checkGetTagsListByProject()
    t.checkGetAllTagsForStrings()
    t.checkAddTagToStrings()
    t.checkRemoveTagsFromStrings()
    t.checkAddTagToStrings()
    t.checkRemoveAllTagsFromStrings()
    t.tearDown()

if __name__ == '__main__':
    example()
