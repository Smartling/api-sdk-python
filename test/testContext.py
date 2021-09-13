
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
    ACCEPTED_TOKED = 'ACCEPTED'

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


    def checkDeleteVisualContext(self):
        """
            delete
            /context-api/v2/projects/{projectId}/contexts/{contextUid}
            for details check: https://api-reference.smartling.com/#operation/deleteVisualContext

            ------------------------------------------------------------------------------------------------------------------------
        """
        contextUid=self.context_uid
        res, status = self.api.deleteVisualContext(contextUid=contextUid)
        
        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKED])
        print("deleteVisualContext", "OK")



    def test_all(self):
        t = self
        t.checkUploadNewVisualContext()
        t.checkGetVisualContextsListByProject()
        t.checkDeleteVisualContext()
        # not covered by tests #
        '''
        getVisualContextInfo
        downloadVisualContextFileContent
        runAutomaticContextMatching
        uploadAndMatchVisualContext
        getAsyncContextMatchResults
        createStringToContextBindings
        getBindings
        deleteBindings
        '''
