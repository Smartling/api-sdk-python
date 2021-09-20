from smartlingApiSdk.UrlV2Helper import UrlV2Helper
from smartlingApiSdk.ApiV2 import ApiV2

class AccountProjectsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings, permanentHeaders=permanentHeaders, env=env)
        self.urlHelper = UrlV2Helper(projectId)

    def getProjectsByAccount(self, accountUid, projectNameFilter='', includeArchived='', offset=0, limit=0):
        '''
            method  :  GET
            api url :  /accounts-api/v2/accounts/{accountUid}/projects
            details :  https://api-reference.smartling.com/#operation/getProjectsByAccount
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/accounts-api/v2/accounts/$smartlingAccountId/projects
        '''
        kw = {
            'projectNameFilter':projectNameFilter,
            'includeArchived':includeArchived,
            'offset':offset,
            'limit':limit,
        }
        url = self.urlHelper.getUrl('/accounts-api/v2/accounts/{accountUid}/projects', accountUid=accountUid)
        return self.command('GET', url, kw)


    def getProjectDetails(self, includeDisabledLocales=''):
        '''
            method  :  GET
            api url :  /projects-api/v2/projects/{projectId}
            details :  https://api-reference.smartling.com/#operation/getProjectDetails
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/projects-api/v2/projects/$smartlingProjectId
        '''
        kw = {
            'includeDisabledLocales':includeDisabledLocales,
        }
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}')
        return self.command('GET', url, kw)


    def addLocaleToProject(self, defaultWorkflowUid, localeId):
        '''
            method  :  POST
            api url :  /projects-api/v2/projects/{projectId}/targetLocales
            details :  https://api-reference.smartling.com/#operation/addLocaleToProject
        '''
        kw = {
            'defaultWorkflowUid':defaultWorkflowUid,
            'localeId':localeId,
        }
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}/targetLocales')
        return self.commandJson('POST', url, kw)


    def copyProject(self, projectName, targetLocaleIds):
        '''
            method  :  POST
            api url :  /projects-api/v2/projects/{projectId}/copy
            details :  https://api-reference.smartling.com/#operation/copyProject
        '''
        kw = {
            'projectName':projectName,
            'targetLocaleIds':targetLocaleIds,
        }
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}/copy')
        return self.commandJson('POST', url, kw)


    def getProjectCopyRequestStatus(self, processUid):
        '''
            method  :  GET
            api url :  /projects-api/v2/projects/{projectId}/copy/{processUid}
            details :  https://api-reference.smartling.com/#operation/getProjectCopyRequestStatus
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}/copy/{processUid}', processUid=processUid)
        return self.command('GET', url, kw)

