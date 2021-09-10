from smartlingApiSdk.UrlV2Helper import UrlV2Helper
from smartlingApiSdk.ApiV2 import ApiV2

class StringsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings, permanentHeaders=permanentHeaders, env=env)
        self.urlHelper = UrlV2Helper(projectId)

    def addStringsToProject(self, strings, placeholderFormat, placeholderFormatCustom, namespace):
        """
            post
            /strings-api/v2/projects/{projectId}
            for details check: https://api-reference.smartling.com/#operation/addStringsToProject
            curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringJSON" https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'strings':strings,
            'placeholderFormat':placeholderFormat,
            'placeholderFormatCustom':placeholderFormatCustom,
            'namespace':namespace,
        }
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}')
        return self.commandJson('POST', url, kw)




    def getAddStringsToProjectRequestStatus(self, processUid):
        """
            get
            /strings-api/v2/projects/{projectId}/processes/{processUid}
            for details check: https://api-reference.smartling.com/#operation/getAddStringsToProjectRequestStatus
            curl -H "Authorization: Bearer $smartlingToken" -G https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/processes/$processUid

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}/processes/{processUid}', processUid=processUid)
        return self.command('GET', url, kw)




    def getAllSourceStringsByProject(self, hashcodes=[], fileUri='', limit='', offset=''):
        """
            post
            /strings-api/v2/projects/{projectId}/source-strings
            for details check: https://api-reference.smartling.com/#operation/getAllSourceStringsByProject
            curl -H "Authorization: Bearer $smartlingToken" -G -d "fileUri=$smartlingFileUri" https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/source-strings

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'hashcodes':hashcodes,
            'fileUri':fileUri,
            'limit':limit,
            'offset':offset,
        }
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}/source-strings')
        return self.commandJson('POST', url, kw)




    def getAllTranslationsByProject(self, targetLocaleId, hashcodes=[], retrievalType='', fileUri='', limit='', offset=''):
        """
            post
            /strings-api/v2/projects/{projectId}/translations
            for details check: https://api-reference.smartling.com/#operation/getAllTranslationsByProject
            curl -H "Authorization: Bearer $smartlingToken" -G https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/translations

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'targetLocaleId':targetLocaleId,
            'hashcodes':hashcodes,
            'retrievalType':retrievalType,
            'fileUri':fileUri,
            'limit':limit,
            'offset':offset,
        }
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}/translations')
        return self.commandJson('POST', url, kw)



