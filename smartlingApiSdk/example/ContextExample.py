
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
from smartlingApiSdk.api.ContextApi import ContextApi
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testContextApi(object):

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

        self.context_api = ContextApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

        print("setUp", "OK", "\n")


    def checkUploadNewVisualContext(self):
        """
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -F "content=@context1.png;type=image/png" -F "name=context1.png" "https://api.smartling.com/context-api/v2/projects/$smartlingProjectId/contexts"
            Responses:
                200 : OK
                400 : Validation error
            details :  https://api-reference.smartling.com/#operation/uploadNewVisualContext
        """
        name='https://www.youtube.com/watch?v=0lJykuiS_9s'
        res, status = self.context_api.uploadNewVisualContext(name=name)


        assert_equal(res.data.contextType, 'VIDEO')
        assert_equal(res.data.name, 'https://www.youtube.com/watch?v=0lJykuiS_9s')

        content = smartlingApiSdk.__path__[0]+'/resources/ctx_api_test.png'
        res_img, status = self.context_api.uploadNewVisualContext(content=content)
        self.context_uid_img = res_img.data.contextUid

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('uploadNewVisualContext', 'OK')
        self.context_uid = res.data.contextUid


    def checkGetVisualContextsListByProject(self):
        """
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/contexts
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getVisualContextsListByProject
        """
        res, status = self.context_api.getVisualContextsListByProject()


        print('Total context count:',len(res.data.items))
        assert_equal(len(res.data.items) > 0, True)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getVisualContextsListByProject', 'OK')


    def checkGetVisualContextInfo(self):
        """
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}
            Responses:
                200 : OK
                404 : Context not found
            details :  https://api-reference.smartling.com/#operation/getVisualContextInfo
        """
        contextUid=self.context_uid
        res, status = self.context_api.getVisualContextInfo(contextUid=contextUid)


        assert_equal(res.data.contextType, 'VIDEO')
        assert_equal(res.data.name, 'https://www.youtube.com/watch?v=0lJykuiS_9s')

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getVisualContextInfo', 'OK')


    def checkDownloadVisualContextFileContent(self):
        """
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}/content
            Responses:
                200 : OK
                404 : Context not found
            details :  https://api-reference.smartling.com/#operation/downloadVisualContextFileContent
        """
        contextUid=self.context_uid_img
        res, status = self.context_api.downloadVisualContextFileContent(contextUid=contextUid)


        assert_equal(86324, len(res)) #empty for video context

        print('downloadVisualContextFileContent', 'OK')


    def checkRunAutomaticContextMatching(self):
        """
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}/match/async
            Responses:
                202 : ACCEPTED
                400 : Validation error
            details :  https://api-reference.smartling.com/#operation/runAutomaticContextMatching
        """
        contextUid=self.context_uid_img
        contentFileUri=''
        stringHashcodes=''
        overrideContextOlderThanDays=1
        res, status = self.context_api.runAutomaticContextMatching(contextUid=contextUid, contentFileUri=contentFileUri, stringHashcodes=stringHashcodes, overrideContextOlderThanDays=overrideContextOlderThanDays)


        self.match_id = res.data.matchId

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('runAutomaticContextMatching', 'OK')


    def checkUploadAndMatchVisualContext(self):
        """
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts/upload-and-match-async
            Responses:
                202 : ACCEPTED
                400 : Validation error
            details :  https://api-reference.smartling.com/#operation/uploadAndMatchVisualContext
        """
        content=smartlingApiSdk.__path__[0]+'/resources/ctx_api_test.png'
        res, status = self.context_api.uploadAndMatchVisualContext(content=content)


        self.match_id_upl_n_match = res.data.matchId

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('uploadAndMatchVisualContext', 'OK')


    def checkCreateStringToContextBindings(self):
        """
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/bindings
            Responses:
                200 : OK
                400 : Validation error
            details :  https://api-reference.smartling.com/#operation/createStringToContextBindings
        """
        bindings=[{'contextUid': self.context_uid, 'stringHashcode': 'ede6083ebd2594ca4e557612aaa05b2e'},
             {'contextUid': self.context_uid_img, 'stringHashcode': '4f25feab674accf572433f22dc516e2e'}]
        res, status = self.context_api.createStringToContextBindings(bindings=bindings)


        assert_equal(res.data.errors['totalCount'], 0)
        assert_equal(res.data.created['totalCount'], 2)
        items = res.data.created['items']
        self.binding_uno = items[0]['bindingUid']
        self.binding_dos = items[1]['bindingUid']

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('createStringToContextBindings', 'OK')


    def checkGetBindings(self):
        """
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/bindings/list
            Responses:
                200 : OK
                400 : Validation error
            details :  https://api-reference.smartling.com/#operation/getBindings
        """
        stringHashcodes=['ede6083ebd2594ca4e557612aaa05b2e', '4f25feab674accf572433f22dc516e2e']
        contentFileUri=''
        contextUid=''
        bindingUids=[]
        res, status = self.context_api.getBindings(stringHashcodes=stringHashcodes, contentFileUri=contentFileUri, contextUid=contextUid, bindingUids=bindingUids)


        print('Total bindings count:',len(res.data.items))
        assert_equal(len(res.data.items) >= 2, True)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getBindings', 'OK')


    def checkDeleteBindings(self):
        """
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/bindings/remove
            Responses:
                200 : OK
                400 : Validation error
            details :  https://api-reference.smartling.com/#operation/deleteBindings
        """
        stringHashcodes=[]
        contentFileUri=''
        contextUid=''
        bindingUids=[self.binding_uno, self.binding_dos]
        res, status = self.context_api.deleteBindings(stringHashcodes=stringHashcodes, contentFileUri=contentFileUri, contextUid=contextUid, bindingUids=bindingUids)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('deleteBindings', 'OK')


    def checkDeleteVisualContext(self):
        """
            method  :  DELETE
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}
            Responses:
                200 : OK
                404 : Context not found
            details :  https://api-reference.smartling.com/#operation/deleteVisualContext
        """
        contextUid=self.context_uid
        res, status = self.context_api.deleteVisualContext(contextUid=contextUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('deleteVisualContext', 'OK')


    def checkDeleteVisualContextsAsync(self):
        """
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts/remove/async
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/deleteVisualContextsAsync
        """
        contextUids=[self.context_uid_img,]
        res, status = self.context_api.deleteVisualContextsAsync(contextUids=contextUids)

        self.processUid = res.data.processUid

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('deleteVisualContextsAsync', 'OK')


    def checkGetAsyncProcessResults(self):
        """
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/processes/{processUid}
            Responses:
                200 : OK
                404 : Process request expired or does not exist
            details :  https://api-reference.smartling.com/#operation/getAsyncProcessResults
        """
        processUid=self.processUid
        res, status = self.context_api.getAsyncProcessResults(processUid=processUid)


        assert_equal(res.data.processUid, self.processUid)
        assert_equal(res.data.processType, 'DELETE_CONTEXTS')
        assert_equal(True, res.data.processState in ['IN_PROGRESS', 'COMPLETED'])

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getAsyncProcessResults', 'OK')



def example():
    t = testContextApi()
    t.setUp()
    t.checkUploadNewVisualContext()
    t.checkGetVisualContextsListByProject()
    t.checkGetVisualContextInfo()
    t.checkDownloadVisualContextFileContent()
    t.checkRunAutomaticContextMatching()
    t.checkUploadAndMatchVisualContext()
    t.checkCreateStringToContextBindings()
    t.checkGetBindings()
    t.checkDeleteBindings()
    t.checkDeleteVisualContext()
    t.checkDeleteVisualContextsAsync()
    t.checkGetAsyncProcessResults()
    t.tearDown()

if __name__ == '__main__':
    example()
