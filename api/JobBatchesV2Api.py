from smartlingApiSdk.ApiV2 import ApiV2

class JobBatchesV2Api(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def createJobBatchV2(self, authorize, translationJobUid, fileUris, localeWorkflows):
        '''
            method  :  POST
            api url :  /job-batches-api/v2/projects/{projectId}/batches
            details :  https://api-reference.smartling.com/#operation/createJobBatchV2
            as curl :  curl -X POST "https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches" -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d '{"translationJobUid": "$translationJobUid", "authorize": true, "fileUris": ["example.json", "test.xml"]}'
        '''
        kw = {
            'authorize':authorize,
            'translationJobUid':translationJobUid,
            'fileUris':fileUris,
            'localeWorkflows':localeWorkflows,
        }
        url = self.urlHelper.getUrl('/job-batches-api/v2/projects/{projectId}/batches')
        return self.commandJson('POST', url, kw)


    def getJobBatchesListV2(self, translationJobUid='', status='', sortBy='createdDate', orderBy='desc', offset=0, limit=20):
        '''
            method  :  GET
            api url :  /job-batches-api/v2/projects/{projectId}/batches
            details :  https://api-reference.smartling.com/#operation/getJobBatchesListV2
            as curl :  curl -X GET \'https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches?translationJobUid={translationJobUid}&status={status}&sortBy=createdDate&orderBy=desc&offset=0&limit=20' \-H "Authorization: Bearer $smartlingToken"
        '''
        kw = {
            'translationJobUid':translationJobUid,
            'status':status,
            'sortBy':sortBy,
            'orderBy':orderBy,
            'offset':offset,
            'limit':limit,
        }
        url = self.urlHelper.getUrl('/job-batches-api/v2/projects/{projectId}/batches')
        return self.command('GET', url, kw)


    def getJobBatchStatusV2(self, batchUid):
        '''
            method  :  GET
            api url :  /job-batches-api/v2/projects/{projectId}/batches/{batchUid}
            details :  https://api-reference.smartling.com/#operation/getJobBatchStatusV2
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/job-batches-api/v2/projects/{projectId}/batches/{batchUid}', batchUid=batchUid)
        return self.command('GET', url, kw)


    def processBatchActionV2(self, batchUid, action, fileUri, reason):
        '''
            method  :  PUT
            api url :  /job-batches-api/v2/projects/{projectId}/batches/{batchUid}
            details :  https://api-reference.smartling.com/#operation/processBatchActionV2
            as curl :  curl -X PUT \'https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches/$batchUid' \-H "Authorization: Bearer $smartlingToken" \-H "Content-Type: application/json" \-d '{ "action": "CANCEL_FILE", "fileUri": "file1.xml", "reason": "Requested asset doesn't exist in Zendesk" }'
        '''
        kw = {
            'action':action,
            'fileUri':fileUri,
            'reason':reason,
        }
        url = self.urlHelper.getUrl('/job-batches-api/v2/projects/{projectId}/batches/{batchUid}', batchUid=batchUid)
        return self.commandJson('PUT', url, kw)


    def uploadFileToJobBatchV2(self, batchUid, file, fileUri, fileType, authorize=False, localeIdsToAuthorize=[], callbackUrl='', directives={}):
        '''
            method  :  POST
            api url :  /job-batches-api/v2/projects/{projectId}/batches/{batchUid}/file
            details :  https://api-reference.smartling.com/#operation/uploadFileToJobBatchV2
            as curl :  curl -X POST \'https://api.smartling.com/job-batches-api/v2/projects/$smartlingProjectId/batches/{batchUid}/file' \-H "Authorization: Bearer $smartlingToken" \-F "file=@file.properties;type=text/plain" \-F "fileUri=file.properties" \-F "fileType=javaProperties" \-F "localeIdsToAuthorize[]=fr-FR" \-F "localeIdsToAuthorize[]=ru-RU"
        '''
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

