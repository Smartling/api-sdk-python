from .UrlV2Helper import UrlV2Helper
from .ApiV2 import ApiV2

class JobsApiAuto(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None):
        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings)
        self.urlHelper = UrlV2Helper(projectId)

    def getJobsByAccount(self, accountUid, jobName='', projectIds=[], translationJobStatus=[], withPriority='', limit=0, offset=0, sortBy='', sortDirection=''):
        """
            get
            /jobs-api/v3/accounts/{accountUid}/jobs
            for details check: https://api-reference.smartling.com/#operation/getJobsByAccount
            curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/accounts/$smartlingAccountId/jobs

            ------------------------------------------------------------------------------------------------------------------------
        """
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
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs
            for details check: https://api-reference.smartling.com/#operation/getJobsByProject
            curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs

            ------------------------------------------------------------------------------------------------------------------------
        """
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
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs
            for details check: https://api-reference.smartling.com/#operation/addJob
            curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingJobJSON" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs

            ------------------------------------------------------------------------------------------------------------------------
        """
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
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings
            for details check: https://api-reference.smartling.com/#operation/findJobsByStrings

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'hashcodes':hashcodes,
            'localeIds':localeIds,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings')
        return self.commandJson('POST', url, kw)




    def getStringsForTranslationJob(self, translationJobUid, targetLocaleId='', limit=0, offset=0):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings
            for details check: https://api-reference.smartling.com/#operation/getStringsForTranslationJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'targetLocaleId':targetLocaleId,
            'limit':limit,
            'offset':offset,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)




    def addStringsToJob(self, translationJobUid, hashcodes, moveEnabled, targetLocaleIds):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/add
            for details check: https://api-reference.smartling.com/#operation/addStringsToJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'hashcodes':hashcodes,
            'moveEnabled':moveEnabled,
            'targetLocaleIds':targetLocaleIds,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/add', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)




    def removeStringsFromJob(self, translationJobUid, hashcodes, localeIds):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove
            for details check: https://api-reference.smartling.com/#operation/removeStringsFromJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'hashcodes':hashcodes,
            'localeIds':localeIds,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)




    def closeJob(self, translationJobUid):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/close
            for details check: https://api-reference.smartling.com/#operation/closeJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/close', translationJobUid=translationJobUid)
        return self.command('POST', url, kw)




    def cancelJob(self, translationJobUid, reason):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel
            for details check: https://api-reference.smartling.com/#operation/cancelJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'reason':reason,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)




    def authorizeJob(self, translationJobUid, localeWorkflows):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize
            for details check: https://api-reference.smartling.com/#operation/authorizeJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'localeWorkflows':localeWorkflows,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)




    def getJobDetails(self, translationJobUid):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            for details check: https://api-reference.smartling.com/#operation/getJobDetails

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)




    def updateJob(self, translationJobUid, jobName, description, dueDate, referenceNumber, callbackUrl, callbackMethod, customFields):
        """
            put
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            for details check: https://api-reference.smartling.com/#operation/updateJob

            ------------------------------------------------------------------------------------------------------------------------
        """
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
        return self.command('PUT', url, kw)




    def deleteJob(self, translationJobUid):
        """
            delete
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            for details check: https://api-reference.smartling.com/#operation/deleteJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid)
        return self.command('DELETE', url, kw)




    def searchForJob(self, fileUris, hashcodes, translationJobUids):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/search
            for details check: https://api-reference.smartling.com/#operation/searchForJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'fileUris':fileUris,
            'hashcodes':hashcodes,
            'translationJobUids':translationJobUids,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/search')
        return self.commandJson('POST', url, kw)




    def getJobAsyncProcessStatus(self, translationJobUid, processUid):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/processes/{processUid}
            for details check: https://api-reference.smartling.com/#operation/getJobAsyncProcessStatus

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/processes/{processUid}', translationJobUid=translationJobUid, processUid=processUid)
        return self.command('GET', url, kw)




    def addFileToJob(self, translationJobUid, fileUri, targetLocaleIds):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add
            for details check: https://api-reference.smartling.com/#operation/addFileToJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'fileUri':fileUri,
            'targetLocaleIds':targetLocaleIds,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)




    def removeFileFromJob(self, translationJobUid, fileUri):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove
            for details check: https://api-reference.smartling.com/#operation/removeFileFromJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'fileUri':fileUri,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)




    def getJobFilesList(self, translationJobUid, limit=0, offset=0):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files
            for details check: https://api-reference.smartling.com/#operation/getJobFilesList

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'limit':limit,
            'offset':offset,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)




    def addLocaleToJob(self, translationJobUid, targetLocaleId, syncContent):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            for details check: https://api-reference.smartling.com/#operation/addLocaleToJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'syncContent':syncContent,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}', translationJobUid=translationJobUid, targetLocaleId=targetLocaleId)
        return self.commandJson('POST', url, kw)




    def removeLocaleFromJob(self, translationJobUid, targetLocaleId):
        """
            delete
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            for details check: https://api-reference.smartling.com/#operation/removeLocaleFromJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}', translationJobUid=translationJobUid, targetLocaleId=targetLocaleId)
        return self.command('DELETE', url, kw)




    def getJobFileProgress(self, translationJobUid, fileUri):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress
            for details check: https://api-reference.smartling.com/#operation/getJobFileProgress

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'fileUri':fileUri,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)




    def getJobProgress(self, translationJobUid, targetLocaleId=''):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress
            for details check: https://api-reference.smartling.com/#operation/getJobProgress

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'targetLocaleId':targetLocaleId,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)




    def getJobLastCompletionDatesPerLocale(self, translationJobUid):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates
            for details check: https://api-reference.smartling.com/#operation/getJobLastCompletionDatesPerLocale

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)




    def findScheduleForTranslationJob(self, translationJobUid):
        """
            get
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            for details check: https://api-reference.smartling.com/#operation/findScheduleForTranslationJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)




    def modifyScheduleItemsForTranslationJob(self, translationJobUid, schedules):
        """
            post
            /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            for details check: https://api-reference.smartling.com/#operation/modifyScheduleItemsForTranslationJob

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'schedules':schedules,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)




    def getProjectCustomFields(self):
        """
            get
            /jobs-api/v3/projects/{projectId}/custom-fields
            for details check: https://api-reference.smartling.com/#operation/getProjectCustomFields

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/custom-fields')
        return self.command('GET', url, kw)




    def assignCustomFieldsToProject(self, CustomFieldAssignmentList):
        """
            post
            /jobs-api/v3/projects/{projectId}/custom-fields
            for details check: https://api-reference.smartling.com/#operation/assignCustomFieldsToProject

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'CustomFieldAssignmentList':CustomFieldAssignmentList,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/custom-fields')
        return self.command('POST', url, kw)




    def getAccountCustomFields(self, accountUid, searchableOnly='', enabledOnly=''):
        """
            get
            /jobs-api/v3/accounts/{accountUid}/custom-fields
            for details check: https://api-reference.smartling.com/#operation/getAccountCustomFields

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'searchableOnly':searchableOnly,
            'enabledOnly':enabledOnly,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields', accountUid=accountUid)
        return self.command('GET', url, kw)




    def createCustomField(self, accountUid, data):
        """
            post
            /jobs-api/v3/accounts/{accountUid}/custom-fields
            for details check: https://api-reference.smartling.com/#operation/createCustomField

            ------------------------------------------------------------------------------------------------------------------------
            Parameters example:
            data: {
                "type": "SHORT_TEXT | LONG_TEXT | SELECTBOX | CHECKBOX",
                "fieldName": "field-name",
                "enabled": true,
                "required": true,
                "searchable": true,
                "displayToTranslators": true,
                "options": "[]",
                "defaultValue": "default field value",
                "description": "Custom field example"
                }
        """
        kw = {
            'data':data,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields', accountUid=accountUid)
        return self.commandJson('POST', url, kw)




    def updateCustomField(self, accountUid, fieldUid, data):
        """
            put
            /jobs-api/v3/accounts/{accountUid}/custom-fields/{fieldUid}
            for details check: https://api-reference.smartling.com/#operation/updateCustomField

            ------------------------------------------------------------------------------------------------------------------------
            Parameters example:
            data: {
                "fieldName": "field-name",
                "enabled": true,
                "required": true,
                "searchable": true,
                "displayToTranslators": true,
                "options": "[]",
                "defaultValue": "default field value",
                "description": "Custom field example"
                }
        """
        kw = {
            'data':data,
        }
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields/{fieldUid}', accountUid=accountUid, fieldUid=fieldUid)
        return self.command('PUT', url, kw)



