
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
 * limitations under the License.
'''

import os
import sys
import time, datetime

lib_path = os.path.abspath('../')
sys.path.append(lib_path)  # allow to import ../smartlingApiSdk/SmartlingFileApi

from api.ContextApi import ContextApi
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

        self.api = ContextApi(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

        print("setUp", "OK", "\n")


    def checkUploadNewVisualContext(self):
        """
            post
            /context-api/v2/projects/{projectId}/contexts
            for details check: https://api-reference.smartling.com/#operation/uploadNewVisualContext
            curl -X POST -H "Authorization: Bearer $smartlingToken" -F "content=@context1.png;type=image/png" -F "name=context1.png" "https://api.smartling.com/context-api/v2/projects/$smartlingProjectId/contexts"

            ------------------------------------------------------------------------------------------------------------------------
        """
        name='https://www.youtube.com/watch?v=0lJykuiS_9s'
        res, status = self.api.uploadNewVisualContext(name=name)
        
        
        assert_equal(res.data.contextType, 'VIDEO')
        assert_equal(res.data.name, 'https://www.youtube.com/watch?v=0lJykuiS_9s')
        
        res_img, status = self.api.uploadNewVisualContext(content='../resources/ctx_api_test.png')
        self.context_uid_img = res_img.data.contextUid
        
        print("uploadNewVisualContext", "OK")
        self.context_uid = res.data.contextUid


    def checkGetVisualContextsListByProject(self):
        """
            get
            /context-api/v2/projects/{projectId}/contexts
            for details check: https://api-reference.smartling.com/#operation/getVisualContextsListByProject

            ------------------------------------------------------------------------------------------------------------------------
        """
        res, status = self.api.getVisualContextsListByProject()
        
        
        print('Total context count:',len(res.data.items))
        assert_equal(len(res.data.items) > 0, True)
        
        print("getVisualContextsListByProject", "OK")


    def checkGetVisualContextInfo(self):
        """
            get
            /context-api/v2/projects/{projectId}/contexts/{contextUid}
            for details check: https://api-reference.smartling.com/#operation/getVisualContextInfo

            ------------------------------------------------------------------------------------------------------------------------
        """
        contextUid=self.context_uid
        res, status = self.api.getVisualContextInfo(contextUid=contextUid)
        
        
        assert_equal(res.data.contextType, 'VIDEO')
        assert_equal(res.data.name, 'https://www.youtube.com/watch?v=0lJykuiS_9s')
        
        print("getVisualContextInfo", "OK")


    def checkDownloadVisualContextFileContent(self):
        """
            get
            /context-api/v2/projects/{projectId}/contexts/{contextUid}/content
            for details check: https://api-reference.smartling.com/#operation/downloadVisualContextFileContent

            ------------------------------------------------------------------------------------------------------------------------
        """
        contextUid=self.context_uid_img
        res, status = self.api.downloadVisualContextFileContent(contextUid=contextUid)
        
        
        assert_equal(86324, len(res)) #empty for video context
        
        print("downloadVisualContextFileContent", "OK")


    def checkRunAutomaticContextMatching(self):
        """
            post
            /context-api/v2/projects/{projectId}/contexts/{contextUid}/match/async
            for details check: https://api-reference.smartling.com/#operation/runAutomaticContextMatching

            ------------------------------------------------------------------------------------------------------------------------
        """
        contextUid=self.context_uid_img
        contentFileUri=''
        stringHashcodes=''
        overrideContextOlderThanDays=1
        res, status = self.api.runAutomaticContextMatching(contextUid=contextUid, contentFileUri=contentFileUri, stringHashcodes=stringHashcodes, overrideContextOlderThanDays=overrideContextOlderThanDays)
        
        
        self.match_id = res.data.matchId
        
        print("runAutomaticContextMatching", "OK")


    def checkUploadAndMatchVisualContext(self):
        """
            post
            /context-api/v2/projects/{projectId}/contexts/upload-and-match-async
            for details check: https://api-reference.smartling.com/#operation/uploadAndMatchVisualContext

            ------------------------------------------------------------------------------------------------------------------------
        """
        content='../resources/ctx_api_test.png'
        res, status = self.api.uploadAndMatchVisualContext(content=content)
        
        
        self.match_id_upl_n_match = res.data.matchId
        
        print("uploadAndMatchVisualContext", "OK")


    def checkGetAsyncContextMatchResults(self):
        """
            get
            /context-api/v2/projects/{projectId}/match/{matchId}
            for details check: https://api-reference.smartling.com/#operation/getAsyncContextMatchResults

            ------------------------------------------------------------------------------------------------------------------------
        """
        matchId=self.match_id_upl_n_match
        res, status = self.api.getAsyncContextMatchResults(matchId=matchId)
        
        
        
        print("getAsyncContextMatchResults", "OK")


    def checkCreateStringToContextBindings(self):
        """
            post
            /context-api/v2/projects/{projectId}/bindings
            for details check: https://api-reference.smartling.com/#operation/createStringToContextBindings

            ------------------------------------------------------------------------------------------------------------------------
        """
        bindings=[{'contextUid': self.context_uid, 'stringHashcode': 'ede6083ebd2594ca4e557612aaa05b2e'},
             {'contextUid': self.context_uid_img, 'stringHashcode': '4f25feab674accf572433f22dc516e2e'}]
        res, status = self.api.createStringToContextBindings(bindings=bindings)
        
        
        assert_equal(res.data.errors['totalCount'], 0)
        assert_equal(res.data.created['totalCount'], 2)
        items = res.data.created['items']
        self.binding_uno = items[0]['bindingUid']
        self.binding_dos = items[1]['bindingUid']
        
        print("createStringToContextBindings", "OK")


    def checkGetBindings(self):
        """
            post
            /context-api/v2/projects/{projectId}/bindings/list
            for details check: https://api-reference.smartling.com/#operation/getBindings

            ------------------------------------------------------------------------------------------------------------------------
        """
        stringHashcodes=['ede6083ebd2594ca4e557612aaa05b2e', '4f25feab674accf572433f22dc516e2e']
        contentFileUri=''
        contextUid=''
        bindingUids=[]
        res, status = self.api.getBindings(stringHashcodes=stringHashcodes, contentFileUri=contentFileUri, contextUid=contextUid, bindingUids=bindingUids)
        
        
        print('Total bindings count:',len(res.data.items))
        assert_equal(len(res.data.items), 2)
        
        print("getBindings", "OK")


    def checkDeleteBindings(self):
        """
            post
            /context-api/v2/projects/{projectId}/bindings/remove
            for details check: https://api-reference.smartling.com/#operation/deleteBindings

            ------------------------------------------------------------------------------------------------------------------------
        """
        stringHashcodes=[]
        contentFileUri=''
        contextUid=''
        bindingUids=[self.binding_uno, self.binding_dos]
        res, status = self.api.deleteBindings(stringHashcodes=stringHashcodes, contentFileUri=contentFileUri, contextUid=contextUid, bindingUids=bindingUids)
        
        
        assert_equal(res.data.totalCount, 2)
        
        print("deleteBindings", "OK")


    def checkDeleteVisualContext(self):
        """
            delete
            /context-api/v2/projects/{projectId}/contexts/{contextUid}
            for details check: https://api-reference.smartling.com/#operation/deleteVisualContext

            ------------------------------------------------------------------------------------------------------------------------
        """
        contextUid=self.context_uid
        res, status = self.api.deleteVisualContext(contextUid=contextUid)
        
        
        res2, status = self.api.deleteVisualContext(contextUid=self.context_uid_img)
        
        print("deleteVisualContext", "OK")



def example():
    t = testContextApi()
    t.setUp()
    t.checkUploadNewVisualContext()
    t.checkGetVisualContextsListByProject()
    t.checkGetVisualContextInfo()
    t.checkDownloadVisualContextFileContent()
    t.checkRunAutomaticContextMatching()
    t.checkUploadAndMatchVisualContext()
    t.checkGetAsyncContextMatchResults()
    t.checkCreateStringToContextBindings()
    t.checkGetBindings()
    t.checkDeleteBindings()
    t.checkDeleteVisualContext()
    t.tearDown()

example()
