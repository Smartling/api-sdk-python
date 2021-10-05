from smartlingApiSdk.ApiV2 import ApiV2

class JobsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def getJobsByAccount(self, accountUid, jobName='', projectIds=[], translationJobStatus=[], withPriority='', limit=0, offset=0, sortBy='', sortDirection='', **kwargs):
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/jobs', accountUid=accountUid, **kwargs)
        return self.command('GET', url, kw)


    def getJobsByProject(self, jobName='', jobNumber='', translationJobUids=[], translationJobStatus=[], limit=0, offset=0, sortBy='', sortDirection='', **kwargs):
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs', **kwargs)
        return self.command('GET', url, kw)


    def addJob(self, jobName, targetLocaleIds, description, dueDate, referenceNumber, callbackUrl, callbackMethod, customFields, **kwargs):
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs', **kwargs)
        return self.commandJson('POST', url, kw)


    def findJobsByStrings(self, hashcodes, localeIds, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings
            details :  https://api-reference.smartling.com/#operation/findJobsByStrings
        '''
        kw = {
            'hashcodes':hashcodes,
            'localeIds':localeIds,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings', **kwargs)
        return self.commandJson('POST', url, kw)


    def getStringsForTranslationJob(self, translationJobUid, targetLocaleId='', limit=0, offset=0, **kwargs):
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings', translationJobUid=translationJobUid, **kwargs)
        return self.command('GET', url, kw)


    def addStringsToJob(self, translationJobUid, hashcodes, moveEnabled, targetLocaleIds, **kwargs):
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/add', translationJobUid=translationJobUid, **kwargs)
        return self.commandJson('POST', url, kw)


    def removeStringsFromJob(self, translationJobUid, hashcodes, localeIds, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove
            details :  https://api-reference.smartling.com/#operation/removeStringsFromJob
        '''
        kw = {
            'hashcodes':hashcodes,
            'localeIds':localeIds,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove', translationJobUid=translationJobUid, **kwargs)
        return self.commandJson('POST', url, kw)


    def closeJob(self, translationJobUid, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/close
            details :  https://api-reference.smartling.com/#operation/closeJob
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/close', translationJobUid=translationJobUid, **kwargs)
        return self.command('POST', url, kw)


    def cancelJob(self, translationJobUid, reason, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel
            details :  https://api-reference.smartling.com/#operation/cancelJob
        '''
        kw = {
            'reason':reason,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel', translationJobUid=translationJobUid, **kwargs)
        return self.commandJson('POST', url, kw)


    def authorizeJob(self, translationJobUid, localeWorkflows, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize
            details :  https://api-reference.smartling.com/#operation/authorizeJob
        '''
        kw = {
            'localeWorkflows':localeWorkflows,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize', translationJobUid=translationJobUid, **kwargs)
        return self.commandJson('POST', url, kw)


    def getJobDetails(self, translationJobUid, **kwargs):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            details :  https://api-reference.smartling.com/#operation/getJobDetails
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid, **kwargs)
        return self.command('GET', url, kw)


    def updateJob(self, translationJobUid, jobName, description, dueDate, referenceNumber, callbackUrl, callbackMethod, customFields, **kwargs):
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid, **kwargs)
        return self.commandJson('PUT', url, kw)


    def deleteJob(self, translationJobUid, **kwargs):
        '''
            method  :  DELETE
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            details :  https://api-reference.smartling.com/#operation/deleteJob
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid, **kwargs)
        return self.command('DELETE', url, kw)


    def searchForJob(self, fileUris, hashcodes, translationJobUids, **kwargs):
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/search', **kwargs)
        return self.commandJson('POST', url, kw)


    def getJobAsyncProcessStatus(self, translationJobUid, processUid, **kwargs):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/processes/{processUid}
            details :  https://api-reference.smartling.com/#operation/getJobAsyncProcessStatus
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/processes/{processUid}', translationJobUid=translationJobUid, processUid=processUid, **kwargs)
        return self.command('GET', url, kw)


    def addFileToJob(self, translationJobUid, fileUri, targetLocaleIds, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add
            details :  https://api-reference.smartling.com/#operation/addFileToJob
        '''
        kw = {
            'fileUri':fileUri,
            'targetLocaleIds':targetLocaleIds,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add', translationJobUid=translationJobUid, **kwargs)
        return self.commandJson('POST', url, kw)


    def removeFileFromJob(self, translationJobUid, fileUri, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove
            details :  https://api-reference.smartling.com/#operation/removeFileFromJob
        '''
        kw = {
            'fileUri':fileUri,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove', translationJobUid=translationJobUid, **kwargs)
        return self.commandJson('POST', url, kw)


    def getJobFilesList(self, translationJobUid, limit=0, offset=0, **kwargs):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files
            details :  https://api-reference.smartling.com/#operation/getJobFilesList
        '''
        kw = {
            'limit':limit,
            'offset':offset,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files', translationJobUid=translationJobUid, **kwargs)
        return self.command('GET', url, kw)


    def addLocaleToJob(self, translationJobUid, targetLocaleId, syncContent, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            details :  https://api-reference.smartling.com/#operation/addLocaleToJob
        '''
        kw = {
            'syncContent':syncContent,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}', translationJobUid=translationJobUid, targetLocaleId=targetLocaleId, **kwargs)
        return self.commandJson('POST', url, kw)


    def removeLocaleFromJob(self, translationJobUid, targetLocaleId, **kwargs):
        '''
            method  :  DELETE
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            details :  https://api-reference.smartling.com/#operation/removeLocaleFromJob
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}', translationJobUid=translationJobUid, targetLocaleId=targetLocaleId, **kwargs)
        return self.command('DELETE', url, kw)


    def getJobFileProgress(self, translationJobUid, fileUri, **kwargs):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress
            details :  https://api-reference.smartling.com/#operation/getJobFileProgress
        '''
        kw = {
            'fileUri':fileUri,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress', translationJobUid=translationJobUid, **kwargs)
        return self.command('GET', url, kw)


    def getJobProgress(self, translationJobUid, targetLocaleId='', **kwargs):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress
            details :  https://api-reference.smartling.com/#operation/getJobProgress
        '''
        kw = {
            'targetLocaleId':targetLocaleId,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress', translationJobUid=translationJobUid, **kwargs)
        return self.command('GET', url, kw)


    def getJobLastCompletionDatesPerLocale(self, translationJobUid, **kwargs):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates
            details :  https://api-reference.smartling.com/#operation/getJobLastCompletionDatesPerLocale
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates', translationJobUid=translationJobUid, **kwargs)
        return self.command('GET', url, kw)


    def findScheduleForTranslationJob(self, translationJobUid, **kwargs):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            details :  https://api-reference.smartling.com/#operation/findScheduleForTranslationJob
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule', translationJobUid=translationJobUid, **kwargs)
        return self.command('GET', url, kw)


    def modifyScheduleItemsForTranslationJob(self, translationJobUid, schedules, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            details :  https://api-reference.smartling.com/#operation/modifyScheduleItemsForTranslationJob
        '''
        kw = {
            'schedules':schedules,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule', translationJobUid=translationJobUid, **kwargs)
        return self.commandJson('POST', url, kw)


    def getProjectCustomFields(self, **kwargs):
        '''
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/custom-fields
            details :  https://api-reference.smartling.com/#operation/getProjectCustomFields
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/custom-fields', **kwargs)
        return self.command('GET', url, kw)


    def assignCustomFieldsToProject(self, CustomFieldAssignmentList, **kwargs):
        '''
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/custom-fields
            details :  https://api-reference.smartling.com/#operation/assignCustomFieldsToProject
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/custom-fields', **kwargs)
        return self.commandJson('POST', url, CustomFieldAssignmentList)


    def getAccountCustomFields(self, accountUid, searchableOnly='', enabledOnly='', **kwargs):
        '''
            method  :  GET
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields
            details :  https://api-reference.smartling.com/#operation/getAccountCustomFields
        '''
        kw = {
            'searchableOnly':searchableOnly,
            'enabledOnly':enabledOnly,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields', accountUid=accountUid, **kwargs)
        return self.command('GET', url, kw)


    def createCustomField(self, accountUid, type, fieldName, enabled, required, searchable, displayToTranslators, options, defaultValue, description, **kwargs):
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields', accountUid=accountUid, **kwargs)
        return self.commandJson('POST', url, kw)


    def updateCustomField(self, accountUid, fieldUid, fieldName, enabled, required, searchable, displayToTranslators, options, defaultValue, description, **kwargs):
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields/{fieldUid}', accountUid=accountUid, fieldUid=fieldUid, **kwargs)
        return self.commandJson('PUT', url, kw)

