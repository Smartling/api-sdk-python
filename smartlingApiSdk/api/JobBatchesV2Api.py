
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


from smartlingApiSdk.ApiV2 import ApiV2

class JobBatchesV2Api(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def createJobBatchV2(self, authorize, translationJobUid, fileUris, localeWorkflows=[], **kwargs):
        """
            method  :  POST
            api url :  /job-batches-api/v2/projects/{projectId}/batches
            as curl :  curl -X POST "https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches" -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d '{"translationJobUid": "$translationJobUid", "authorize": true, "fileUris": ["example.json", "test.xml"]}'
            Responses:
                200 : OK
                404 : provided translationJobUid is not found in the TMS
            details :  https://api-reference.smartling.com/#operation/createJobBatchV2
        """
        kw = {
            'authorize':authorize,
            'translationJobUid':translationJobUid,
            'fileUris':fileUris,
            'localeWorkflows':localeWorkflows,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/job-batches-api/v2/projects/{projectId}/batches', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getJobBatchesListV2(self, translationJobUid='', status='', sortBy='createdDate', orderBy='desc', offset=0, limit=20, **kwargs):
        """
            method  :  GET
            api url :  /job-batches-api/v2/projects/{projectId}/batches
            as curl :  curl -X GET \'https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches?translationJobUid={translationJobUid}&status={status}&sortBy=createdDate&orderBy=desc&offset=0&limit=20' \-H "Authorization: Bearer $smartlingToken"
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobBatchesListV2
        """
        kw = {
            'translationJobUid':translationJobUid,
            'status':status,
            'sortBy':sortBy,
            'orderBy':orderBy,
            'offset':offset,
            'limit':limit,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/job-batches-api/v2/projects/{projectId}/batches', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getJobBatchStatusV2(self, batchUid, **kwargs):
        """
            method  :  GET
            api url :  /job-batches-api/v2/projects/{projectId}/batches/{batchUid}
            Responses:
                200 : OK
                404 : Batch provided in path is not found
            details :  https://api-reference.smartling.com/#operation/getJobBatchStatusV2
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/job-batches-api/v2/projects/{projectId}/batches/{batchUid}', batchUid=batchUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def processBatchActionV2(self, batchUid, action, fileUri, reason='', **kwargs):
        """
            method  :  PUT
            api url :  /job-batches-api/v2/projects/{projectId}/batches/{batchUid}
            as curl :  curl -X PUT \'https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches/$batchUid' \-H "Authorization: Bearer $smartlingToken" \-H "Content-Type: application/json" \-d '{ "action": "CANCEL_FILE", "fileUri": "file1.xml", "reason": "Requested asset doesn't exist in Zendesk" }'
            Responses:
                200 : SUCCESS
                404 : Batch provided in path is not found
            details :  https://api-reference.smartling.com/#operation/processBatchActionV2
        """
        kw = {
            'action':action,
            'fileUri':fileUri,
            'reason':reason,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/job-batches-api/v2/projects/{projectId}/batches/{batchUid}', batchUid=batchUid, **kwargs)
        response, status = self.commandJson('PUT', url, kw)
        return response, status


    def uploadFileToJobBatchV2(self, batchUid, file, fileUri, fileType, authorize=False, localeIdsToAuthorize=[], callbackUrl='', directives={}, **kwargs):
        """
            method  :  POST
            api url :  /job-batches-api/v2/projects/{projectId}/batches/{batchUid}/file
            as curl :  curl -X POST \'https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches/{batchUid}/file' \-H "Authorization: Bearer $smartlingToken" \-F "file=@file.properties;type=text/plain" \-F "fileUri=file.properties" \-F "fileType=javaProperties" \-F "localeIdsToAuthorize[]=fr-FR" \-F "localeIdsToAuthorize[]=ru-RU"
            Responses:
                202 : ACCEPTED
                404 : Batch provided in path is not found
            details :  https://api-reference.smartling.com/#operation/uploadFileToJobBatchV2
        """
        kw = {
            'file':self.processFile(file),
            'fileUri':fileUri,
            'fileType':fileType,
            'authorize':authorize,
            'localeIdsToAuthorize':localeIdsToAuthorize,
            'callbackUrl':callbackUrl,
        }
        self.addLibIdDirective(kw)
        self.processDirectives(kw, directives)
        url = self.urlHelper.getUrl('/job-batches-api/v2/projects/{projectId}/batches/{batchUid}/file', batchUid=batchUid)
        return self.uploadMultipart(url, kw)

