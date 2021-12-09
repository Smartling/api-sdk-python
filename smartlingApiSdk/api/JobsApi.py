
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

class JobsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def getJobsByAccount(self, accountUid, jobName='', projectIds=[], translationJobStatus=[], withPriority='', limit=0, offset=0, sortBy='', sortDirection='', **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/accounts/{accountUid}/jobs
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/accounts/$smartlingAccountId/jobs
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobsByAccount
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/jobs', accountUid=accountUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getJobsByProject(self, jobName='', jobNumber='', translationJobUids=[], translationJobStatus=[], limit=0, offset=0, sortBy='', sortDirection='', **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobsByProject
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def addJob(self, jobName, targetLocaleIds=[], description='', dueDate='', referenceNumber='', callbackUrl='', callbackMethod='', customFields=[], **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingJobJSON" https://api.smartling.com/jobs-api/v3/projects/$smartlingProjectId/jobs
            Responses:
                200 : OK
                400 : Validation error during job creation.
            details :  https://api-reference.smartling.com/#operation/addJob
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def findJobsByStrings(self, hashcodes=[], localeIds=[], **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings
            Responses:
                200 : OK
                400 : Validation error response
            details :  https://api-reference.smartling.com/#operation/findJobsByStrings
        """
        kw = {
            'hashcodes':hashcodes,
            'localeIds':localeIds,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/find-jobs-by-strings', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getStringsForTranslationJob(self, translationJobUid, targetLocaleId='', limit=0, offset=0, **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings
            Responses:
                200 : OK
                404 : Job not found error
            details :  https://api-reference.smartling.com/#operation/getStringsForTranslationJob
        """
        kw = {
            'targetLocaleId':targetLocaleId,
            'limit':limit,
            'offset':offset,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def addStringsToJob(self, translationJobUid, hashcodes, moveEnabled=False, targetLocaleIds=[], **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/add
            Responses:
                200 : OK
                202 : ACCEPTED
                400 : Validation error response
            details :  https://api-reference.smartling.com/#operation/addStringsToJob
        """
        kw = {
            'hashcodes':hashcodes,
            'moveEnabled':moveEnabled,
            'targetLocaleIds':targetLocaleIds,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/add', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def removeStringsFromJob(self, translationJobUid, hashcodes=[], localeIds=[], **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove
            Responses:
                200 : OK
                202 : ACCEPTED
            details :  https://api-reference.smartling.com/#operation/removeStringsFromJob
        """
        kw = {
            'hashcodes':hashcodes,
            'localeIds':localeIds,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/strings/remove', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def closeJob(self, translationJobUid, **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/close
            Responses:
                200 : OK
                400 : Validation error when closing a job
            details :  https://api-reference.smartling.com/#operation/closeJob
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/close', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('POST', url, kw)
        return response, status


    def cancelJob(self, translationJobUid, reason='', **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel
            Responses:
                200 : OK
                202 : ACCEPTED
                400 : Validation error when cancelling a job
                401 : Authentication error
            details :  https://api-reference.smartling.com/#operation/cancelJob
        """
        kw = {
            'reason':reason,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/cancel', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def authorizeJob(self, translationJobUid, localeWorkflows=[], **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize
            Responses:
                200 : OK
                400 : Validation error when authorizing a job
            details :  https://api-reference.smartling.com/#operation/authorizeJob
        """
        kw = {
            'localeWorkflows':localeWorkflows,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/authorize', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getJobDetails(self, translationJobUid, **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            Responses:
                200 : OK
                404 : Job not found error
            details :  https://api-reference.smartling.com/#operation/getJobDetails
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def updateJob(self, translationJobUid, jobName, description='', dueDate='', referenceNumber='', callbackUrl='', callbackMethod='', customFields=[], **kwargs):
        """
            method  :  PUT
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            Responses:
                200 : OK
                400 : Validation error on updating a job
                404 : Job not found error
            details :  https://api-reference.smartling.com/#operation/updateJob
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('PUT', url, kw)
        return response, status


    def deleteJob(self, translationJobUid, **kwargs):
        """
            method  :  DELETE
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}
            Responses:
                200 : OK
                400 : Validation error when deleting a job
                401 : Authentication error
            details :  https://api-reference.smartling.com/#operation/deleteJob
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('DELETE', url, kw)
        return response, status


    def searchForJob(self, fileUris=[], hashcodes=[], translationJobUids=[], **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/search
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/searchForJob
        """
        kw = {
            'fileUris':fileUris,
            'hashcodes':hashcodes,
            'translationJobUids':translationJobUids,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/search', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getJobAsyncProcessStatus(self, translationJobUid, processUid, **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/processes/{processUid}
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobAsyncProcessStatus
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/processes/{processUid}', translationJobUid=translationJobUid, processUid=processUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def addFileToJob(self, translationJobUid, fileUri, targetLocaleIds=[], **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add
            Responses:
                200 : OK
                202 : ACCEPTED
                400 : Validation error adding file to a job
                423 : The requested file is currently being processed by another operation. The file will be unlocked after the operation completes.
            details :  https://api-reference.smartling.com/#operation/addFileToJob
        """
        kw = {
            'fileUri':fileUri,
            'targetLocaleIds':targetLocaleIds,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/add', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def removeFileFromJob(self, translationJobUid, fileUri='', **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove
            Responses:
                200 : OK
                202 : ACCEPTED
                404 : Not found validation error
            details :  https://api-reference.smartling.com/#operation/removeFileFromJob
        """
        kw = {
            'fileUri':fileUri,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/remove', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getJobFilesList(self, translationJobUid, limit=0, offset=0, **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobFilesList
        """
        kw = {
            'limit':limit,
            'offset':offset,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/files', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def addLocaleToJob(self, translationJobUid, targetLocaleId, syncContent=True, **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            Responses:
                200 : OK
                202 : ACCEPTED
            details :  https://api-reference.smartling.com/#operation/addLocaleToJob
        """
        kw = {
            'syncContent':syncContent,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}', translationJobUid=translationJobUid, targetLocaleId=targetLocaleId, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def removeLocaleFromJob(self, translationJobUid, targetLocaleId, **kwargs):
        """
            method  :  DELETE
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}
            Responses:
                200 : OK
                202 : ACCEPTED
            details :  https://api-reference.smartling.com/#operation/removeLocaleFromJob
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales/{targetLocaleId}', translationJobUid=translationJobUid, targetLocaleId=targetLocaleId, **kwargs)
        response, status = self.command('DELETE', url, kw)
        return response, status


    def getJobFileProgress(self, translationJobUid, fileUri, **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobFileProgress
        """
        kw = {
            'fileUri':fileUri,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/file/progress', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getJobProgress(self, translationJobUid, targetLocaleId='', **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/getJobProgress
        """
        kw = {
            'targetLocaleId':targetLocaleId,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/progress', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getJobLastCompletionDatesPerLocale(self, translationJobUid, **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/getJobLastCompletionDatesPerLocale
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/locales-completion-dates', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def findScheduleForTranslationJob(self, translationJobUid, **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/findScheduleForTranslationJob
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def modifyScheduleItemsForTranslationJob(self, translationJobUid, schedules=[], **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/modifyScheduleItemsForTranslationJob
        """
        kw = {
            'schedules':schedules,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/jobs/{translationJobUid}/schedule', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getProjectCustomFields(self, **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/projects/{projectId}/custom-fields
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/getProjectCustomFields
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/custom-fields', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def assignCustomFieldsToProject(self, CustomFieldAssignmentList, **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/projects/{projectId}/custom-fields
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/assignCustomFieldsToProject
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/projects/{projectId}/custom-fields', **kwargs)
        response, status = self.commandJson('POST', url, CustomFieldAssignmentList)
        return response, status


    def getAccountCustomFields(self, accountUid, searchableOnly='', enabledOnly='', **kwargs):
        """
            method  :  GET
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields
            Responses:
                200 : OK
                404 : Not found error
            details :  https://api-reference.smartling.com/#operation/getAccountCustomFields
        """
        kw = {
            'searchableOnly':searchableOnly,
            'enabledOnly':enabledOnly,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields', accountUid=accountUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def createCustomField(self, accountUid, required, type='', fieldName='', enabled='', searchable='', displayToTranslators='', options=[], defaultValue='', description='', **kwargs):
        """
            method  :  POST
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/createCustomField
        """
        kw = {
            'required':required,
            'type':type,
            'fieldName':fieldName,
            'enabled':enabled,
            'searchable':searchable,
            'displayToTranslators':displayToTranslators,
            'options':options,
            'defaultValue':defaultValue,
            'description':description,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields', accountUid=accountUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def updateCustomField(self, accountUid, fieldUid, required, fieldName='', enabled='', searchable='', displayToTranslators='', options=[], defaultValue='', description='', **kwargs):
        """
            method  :  PUT
            api url :  /jobs-api/v3/accounts/{accountUid}/custom-fields/{fieldUid}
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/updateCustomField
        """
        kw = {
            'required':required,
            'fieldName':fieldName,
            'enabled':enabled,
            'searchable':searchable,
            'displayToTranslators':displayToTranslators,
            'options':options,
            'defaultValue':defaultValue,
            'description':description,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/jobs-api/v3/accounts/{accountUid}/custom-fields/{fieldUid}', accountUid=accountUid, fieldUid=fieldUid, **kwargs)
        response, status = self.commandJson('PUT', url, kw)
        return response, status

