
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
from smartlingApiSdk.api.JobBatchesV2Api import JobBatchesV2Api
from smartlingApiSdk.ProxySettings import ProxySettings
from smartlingApiSdk.Credentials import Credentials

isPython3 =  sys.version_info[:2] >= (3,0)

def assert_equal(a,b, comment=''):
    if a != b :
        err = "Assertion Failed: '%s' != '%s' %s" % (a,b, comment)
        if not isPython3 and type(err) == str:
            err = err.decode('utf-8', 'ignore')
        raise Exception(repr(err))

class testJobBatchesV2Api(object):

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

        self.job_batches_v2_api = JobBatchesV2Api(self.MY_USER_IDENTIFIER, self.MY_USER_SECRET, self.MY_PROJECT_ID, proxySettings, env='stg')

        print("setUp", "OK", "\n")


    def checkCreateJobBatchV2(self):
        """
            method  :  POST
            api url :  /job-batches-api/v2/projects/{projectId}/batches
            as curl :  curl -X POST "https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches" -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d '{"translationJobUid": "$translationJobUid", "authorize": true, "fileUris": ["example.json", "test.xml"]}'
            Responses:
                200 : OK
                404 : provided translationJobUid is not found in the TMS
            details :  https://api-reference.smartling.com/#operation/createJobBatchV2
        """
        self.file_uri = "java.properties.jb2.%d" % time.time()
        authorize=False
        translationJobUid="c4e4b14773bd"  #use real batch job here
        fileUris=[self.file_uri, "file_to_cancel_later"]
        localeWorkflows= [ { "targetLocaleId": "zh-TW", "workflowUid": "748398939979" } ]
        res, status = self.job_batches_v2_api.createJobBatchV2(authorize=authorize, translationJobUid=translationJobUid, fileUris=fileUris, localeWorkflows=localeWorkflows)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('createJobBatchV2', 'OK')
        self.batch_uid = res.data.batchUid


    def checkGetJobBatchesListV2(self):
        """
            method  :  GET
            api url :  /job-batches-api/v2/projects/{projectId}/batches
            as curl :  curl -X GET \'https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches?translationJobUid={translationJobUid}&status={status}&sortBy=createdDate&orderBy=desc&offset=0&limit=20' \-H "Authorization: Bearer $smartlingToken"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobBatchesListV2
        """
        res, status = self.job_batches_v2_api.getJobBatchesListV2()

        print('getJobBatchesListV2', 'OK')


    def checkGetJobBatchStatusV2(self):
        """
            method  :  GET
            api url :  /job-batches-api/v2/projects/{projectId}/batches/{batchUid}
            Responses:
                200 : OK
                404 : Batch provided in path is not found
            details :  https://api-reference.smartling.com/#operation/getJobBatchStatusV2
        """
        batchUid=self.batch_uid
        res, status = self.job_batches_v2_api.getJobBatchStatusV2(batchUid=batchUid)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('getJobBatchStatusV2', 'OK')


    def checkUploadFileToJobBatchV2(self):
        """
            method  :  POST
            api url :  /job-batches-api/v2/projects/{projectId}/batches/{batchUid}/file
            as curl :  curl -X POST \'https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches/{batchUid}/file' \-H "Authorization: Bearer $smartlingToken" \-F "file=@file.properties;type=text/plain" \-F "fileUri=file.properties" \-F "fileType=javaProperties" \-F "localeIdsToAuthorize[]=fr-FR" \-F "localeIdsToAuthorize[]=ru-RU"
            Responses:
                202 : ACCEPTED
                404 : Batch provided in path is not found
            details :  https://api-reference.smartling.com/#operation/uploadFileToJobBatchV2
        """
        textData = open(smartlingApiSdk.__path__[0]+'/resources/java.properties', 'rb').read().decode('utf-8', 'ignore')
        batchUid=self.batch_uid
        file=textData
        fileUri=self.file_uri
        fileType='javaProperties'
        authorize=False
        localeIdsToAuthorize=["zh-TW",]
        callbackUrl='https://www.callback.com/smartling/python/sdk/jb2.test'
        res, status = self.job_batches_v2_api.uploadFileToJobBatchV2(batchUid=batchUid, file=file, fileUri=fileUri, fileType=fileType, authorize=authorize, localeIdsToAuthorize=localeIdsToAuthorize, callbackUrl=callbackUrl)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('uploadFileToJobBatchV2', 'OK')


    def checkProcessBatchActionV2(self):
        """
            method  :  PUT
            api url :  /job-batches-api/v2/projects/{projectId}/batches/{batchUid}
            as curl :  curl -X PUT \'https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches/$batchUid' \-H "Authorization: Bearer $smartlingToken" \-H "Content-Type: application/json" \-d '{ "action": "CANCEL_FILE", "fileUri": "file1.xml", "reason": "Requested asset doesn't exist in Zendesk" }'
            Responses:
                200 : SUCCESS
                404 : Batch provided in path is not found
            details :  https://api-reference.smartling.com/#operation/processBatchActionV2
        """
        batchUid=self.batch_uid
        action='CANCEL_FILE'
        fileUri='file_to_cancel_later'
        reason='test reason'
        res, status = self.job_batches_v2_api.processBatchActionV2(batchUid=batchUid, action=action, fileUri=fileUri, reason=reason)

        assert_equal(True, status in [200,202])
        assert_equal(True, res.code in [self.CODE_SUCCESS_TOKEN, self.ACCEPTED_TOKEN])
        print('processBatchActionV2', 'OK')



def example():
    t = testJobBatchesV2Api()
    t.setUp()
    t.checkCreateJobBatchV2()
    t.checkGetJobBatchesListV2()
    t.checkGetJobBatchStatusV2()
    t.checkUploadFileToJobBatchV2()
    t.checkProcessBatchActionV2()
    t.tearDown()

if __name__ == '__main__':
    example()
