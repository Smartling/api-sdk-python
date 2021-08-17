from .UrlV2Helper import UrlV2Helper
from .ApiV2 import ApiV2

class AccountProjectsApiAuto(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None):
        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings)
        self.urlHelper = UrlV2Helper(projectId)

    def getProjectsByAccount(self, accountUid, projectNameFilter='', includeArchived='', offset=0, limit=0):
        """
            get
            /accounts-api/v2/accounts/{accountUid}/projects
            for details check: https://api-reference.smartling.com/#operation/getProjectsByAccount
            curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/accounts-api/v2/accounts/$smartlingAccountId/projects


        """
        kw = {
            'projectNameFilter':projectNameFilter,
            'includeArchived':includeArchived,
            'offset':offset,
            'limit':limit,
        }
        url = self.urlHelper.getUrl('/accounts-api/v2/accounts/{accountUid}/projects', accountUid=accountUid)
        return self.command('GET', url, kw)




    def getProjectDetails(self, includeDisabledLocales=''):
        """
            get
            /projects-api/v2/projects/{projectId}
            for details check: https://api-reference.smartling.com/#operation/getProjectDetails
            curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/projects-api/v2/projects/$smartlingProjectId


        """
        kw = {
            'includeDisabledLocales':includeDisabledLocales,
        }
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}')
        return self.command('GET', url, kw)




    def addLocaleToProject(self, defaultWorkflowUid, localeId):
        """
            post
            /projects-api/v2/projects/{projectId}/targetLocales
            for details check: https://api-reference.smartling.com/#operation/addLocaleToProject

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'defaultWorkflowUid':defaultWorkflowUid,
            'localeId':localeId,
        }
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}/targetLocales')
        return self.command('POST', url, kw)




    def copyProject(self, projectName, targetLocaleIds):
        """
            post
            /projects-api/v2/projects/{projectId}/copy
            for details check: https://api-reference.smartling.com/#operation/copyProject

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'projectName':projectName,
            'targetLocaleIds':targetLocaleIds,
        }
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}/copy')
        return self.command('POST', url, kw)




    def getProjectCopyRequestStatus(self, processUid):
        """
            get
            /projects-api/v2/projects/{projectId}/copy/{processUid}
            for details check: https://api-reference.smartling.com/#operation/getProjectCopyRequestStatus

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/projects-api/v2/projects/{projectId}/copy/{processUid}', processUid=processUid)
        return self.command('GET', url, kw)



