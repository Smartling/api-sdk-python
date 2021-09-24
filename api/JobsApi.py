from smartlingApiSdk.ApiV2 import ApiV2

class JobsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def getJobsByAccount(self, accountUid, jobName='', projectIds=[], translationJobStatus=[], withPriority='', limit=0, offset=0, sortBy='', sortDirection=''):
        '''
            method  :  GET
            api url :  /jobs-api/v3/accounts/{accountUid}/jobs
            details :  https://api-reference.smartling.com/#operation/getJobsByAccount
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/accounts/$smartlingAccountId/jobs
        '''
        kw = {
            'jobName':jobName,
            'projectIds':projectIds,
            'translationJobStatus':translationJobStatus,
            'withPriority':withPriority,
            'limit':limit,
            'offset':offset,
            'sortBy':sortBy,
            'sortDirection':sortDirection,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/jobs', accountUid=accountUid)
        return self.command('GET', url, kw)


    def getJobsByProject(self, jobName='', jobNumber='', translationJobUids=[], translationJobStatus=[], limit=0, offset=0, sortBy='', sortDirection=''):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs
            details :  https://api-reference.smartling.com/#operation/getJobsByProject
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs
        '''
        kw = {
            'jobName':jobName,
            'jobNumber':jobNumber,
            'translationJobUids':translationJobUids,
            'translationJobStatus':translationJobStatus,
            'limit':limit,
            'offset':offset,
            'sortBy':sortBy,
            'sortDirection':sortDirection,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs')
        return self.command('GET', url, kw)


    def addJob(self, jobName, targetLocaleIds, description, dueDate, referenceNumber, callbackUrl, callbackMethod, customFields):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs
            details :  https://api-reference.smartling.com/#operation/addJob
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingJobJSON" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs
        '''
        kw = {
            'jobName':jobName,
            'targetLocaleIds':targetLocaleIds,
            'description':description,
            'dueDate':dueDate,
            'referenceNumber':referenceNumber,
            'callbackUrl':callbackUrl,
            'callbackMethod':callbackMethod,
            'customFields':customFields,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs')
        return self.commandJson('POST', url, kw)


    def findJobsByStrings(self, hashcodes, localeIds):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings
            details :  https://api-reference.smartling.com/#operation/findJobsByStrings
        '''
        kw = {
            'hashcodes':hashcodes,
            'localeIds':localeIds,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings')
        return self.commandJson('POST', url, kw)


    def getStringsForTranslationJob(self, translationJobUid, targetLocaleId='', limit=0, offset=0):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings
            details :  https://api-reference.smartling.com/#operation/getStringsForTranslationJob
        '''
        kw = {
            'targetLocaleId':targetLocaleId,
            'limit':limit,
            'offset':offset,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)


    def addStringsToJob(self, translationJobUid, hashcodes, moveEnabled, targetLocaleIds):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/add
            details :  https://api-reference.smartling.com/#operation/addStringsToJob
        '''
        kw = {
            'hashcodes':hashcodes,
            'moveEnabled':moveEnabled,
            'targetLocaleIds':targetLocaleIds,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/add', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)


    def removeStringsFromJob(self, translationJobUid, hashcodes, localeIds):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove
            details :  https://api-reference.smartling.com/#operation/removeStringsFromJob
        '''
        kw = {
            'hashcodes':hashcodes,
            'localeIds':localeIds,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)


    def closeJob(self, translationJobUid):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/close
            details :  https://api-reference.smartling.com/#operation/closeJob
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/close', translationJobUid=translationJobUid)
        return self.command('POST', url, kw)


    def cancelJob(self, translationJobUid, reason):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel
            details :  https://api-reference.smartling.com/#operation/cancelJob
        '''
        kw = {
            'reason':reason,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)


    def authorizeJob(self, translationJobUid, localeWorkflows):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize
            details :  https://api-reference.smartling.com/#operation/authorizeJob
        '''
        kw = {
            'localeWorkflows':localeWorkflows,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)


    def getJobDetails(self, translationJobUid):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            details :  https://api-reference.smartling.com/#operation/getJobDetails
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)


    def updateJob(self, translationJobUid, jobName, description, dueDate, referenceNumber, callbackUrl, callbackMethod, customFields):
        '''
            method  :  PUT
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            details :  https://api-reference.smartling.com/#operation/updateJob
        '''
        kw = {
            'jobName':jobName,
            'description':description,
            'dueDate':dueDate,
            'referenceNumber':referenceNumber,
            'callbackUrl':callbackUrl,
            'callbackMethod':callbackMethod,
            'customFields':customFields,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid)
        return self.commandJson('PUT', url, kw)


    def deleteJob(self, translationJobUid):
        '''
            method  :  DELETE
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            details :  https://api-reference.smartling.com/#operation/deleteJob
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid)
        return self.command('DELETE', url, kw)


    def searchForJob(self, fileUris, hashcodes, translationJobUids):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/search
            details :  https://api-reference.smartling.com/#operation/searchForJob
        '''
        kw = {
            'fileUris':fileUris,
            'hashcodes':hashcodes,
            'translationJobUids':translationJobUids,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/search')
        return self.commandJson('POST', url, kw)


    def getJobAsyncProcessStatus(self, translationJobUid, processUid):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/processes/{processUid}
            details :  https://api-reference.smartling.com/#operation/getJobAsyncProcessStatus
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/processes/{processUid}', translationJobUid=translationJobUid, processUid=processUid)
        return self.command('GET', url, kw)


    def addFileToJob(self, translationJobUid, fileUri, targetLocaleIds):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add
            details :  https://api-reference.smartling.com/#operation/addFileToJob
        '''
        kw = {
            'fileUri':fileUri,
            'targetLocaleIds':targetLocaleIds,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)


    def removeFileFromJob(self, translationJobUid, fileUri):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove
            details :  https://api-reference.smartling.com/#operation/removeFileFromJob
        '''
        kw = {
            'fileUri':fileUri,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)


    def getJobFilesList(self, translationJobUid, limit=0, offset=0):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files
            details :  https://api-reference.smartling.com/#operation/getJobFilesList
        '''
        kw = {
            'limit':limit,
            'offset':offset,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)


    def addLocaleToJob(self, translationJobUid, targetLocaleId, syncContent):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            details :  https://api-reference.smartling.com/#operation/addLocaleToJob
        '''
        kw = {
            'syncContent':syncContent,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}', translationJobUid=translationJobUid, targetLocaleId=targetLocaleId)
        return self.commandJson('POST', url, kw)


    def removeLocaleFromJob(self, translationJobUid, targetLocaleId):
        '''
            method  :  DELETE
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            details :  https://api-reference.smartling.com/#operation/removeLocaleFromJob
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}', translationJobUid=translationJobUid, targetLocaleId=targetLocaleId)
        return self.command('DELETE', url, kw)


    def getJobFileProgress(self, translationJobUid, fileUri):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress
            details :  https://api-reference.smartling.com/#operation/getJobFileProgress
        '''
        kw = {
            'fileUri':fileUri,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)


    def getJobProgress(self, translationJobUid, targetLocaleId=''):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress
            details :  https://api-reference.smartling.com/#operation/getJobProgress
        '''
        kw = {
            'targetLocaleId':targetLocaleId,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)


    def getJobLastCompletionDatesPerLocale(self, translationJobUid):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates
            details :  https://api-reference.smartling.com/#operation/getJobLastCompletionDatesPerLocale
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)


    def findScheduleForTranslationJob(self, translationJobUid):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            details :  https://api-reference.smartling.com/#operation/findScheduleForTranslationJob
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)


    def modifyScheduleItemsForTranslationJob(self, translationJobUid, schedules):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            details :  https://api-reference.smartling.com/#operation/modifyScheduleItemsForTranslationJob
        '''
        kw = {
            'schedules':schedules,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)


    def getProjectCustomFields(self):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/custom-fields
            details :  https://api-reference.smartling.com/#operation/getProjectCustomFields
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/custom-fields')
        return self.command('GET', url, kw)


    def assignCustomFieldsToProject(self, CustomFieldAssignmentList):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/custom-fields
            details :  https://api-reference.smartling.com/#operation/assignCustomFieldsToProject
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/custom-fields')
        return self.commandJson('POST', url, CustomFieldAssignmentList)


    def getAccountCustomFields(self, accountUid, searchableOnly='', enabledOnly=''):
        '''
            method  :  GET
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields
            details :  https://api-reference.smartling.com/#operation/getAccountCustomFields
        '''
        kw = {
            'searchableOnly':searchableOnly,
            'enabledOnly':enabledOnly,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields', accountUid=accountUid)
        return self.command('GET', url, kw)


    def createCustomField(self, accountUid, type, fieldName, enabled, required, searchable, displayToTranslators, options, defaultValue, description):
        '''
            method  :  POST
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields
            details :  https://api-reference.smartling.com/#operation/createCustomField
        '''
        kw = {
            'type':type,
            'fieldName':fieldName,
            'enabled':enabled,
            'required':required,
            'searchable':searchable,
            'displayToTranslators':displayToTranslators,
            'options':options,
            'defaultValue':defaultValue,
            'description':description,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields', accountUid=accountUid)
        return self.commandJson('POST', url, kw)


    def updateCustomField(self, accountUid, fieldUid, fieldName, enabled, required, searchable, displayToTranslators, options, defaultValue, description):
        '''
            method  :  PUT
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields/{fieldUid}
            details :  https://api-reference.smartling.com/#operation/updateCustomField
        '''
        kw = {
            'fieldName':fieldName,
            'enabled':enabled,
            'required':required,
            'searchable':searchable,
            'displayToTranslators':displayToTranslators,
            'options':options,
            'defaultValue':defaultValue,
            'description':description,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields/{fieldUid}', accountUid=accountUid, fieldUid=fieldUid)
        return self.commandJson('PUT', url, kw)

