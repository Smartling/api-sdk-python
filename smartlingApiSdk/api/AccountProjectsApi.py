
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

class AccountProjectsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def getProjectsByAccount(self, accountUid, projectNameFilter='', includeArchived='', offset=0, limit=0, **kwargs):
        """
            method  :  GET
            api url :  /accounts-api/v2/accounts/{accountUid}/projects
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/accounts-api/v2/accounts/$smartlingAccountId/projects
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getProjectsByAccount
        """
        kw = {
            'projectNameFilter':projectNameFilter,
            'includeArchived':includeArchived,
            'offset':offset,
            'limit':limit,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/accounts-api/v2/accounts/{accountUid}/projects', accountUid=accountUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getProjectDetails(self, includeDisabledLocales='', **kwargs):
        """
            method  :  GET
            api url :  /projects-api/v2/projects/{projectId}
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/projects-api/v2/projects/$smartlingProjectId
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getProjectDetails
        """
        kw = {
            'includeDisabledLocales':includeDisabledLocales,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def addLocaleToProject(self, defaultWorkflowUid='', localeId='', **kwargs):
        """
            method  :  POST
            api url :  /projects-api/v2/projects/{projectId}/targetLocales
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/addLocaleToProject
        """
        kw = {
            'defaultWorkflowUid':defaultWorkflowUid,
            'localeId':localeId,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}/targetLocales', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def copyProject(self, projectName='', targetLocaleIds=[], **kwargs):
        """
            method  :  POST
            api url :  /projects-api/v2/projects/{projectId}/copy
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/copyProject
        """
        kw = {
            'projectName':projectName,
            'targetLocaleIds':targetLocaleIds,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}/copy', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getProjectCopyRequestStatus(self, processUid, **kwargs):
        """
            method  :  GET
            api url :  /projects-api/v2/projects/{projectId}/copy/{processUid}
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getProjectCopyRequestStatus
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}/copy/{processUid}', processUid=processUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status

