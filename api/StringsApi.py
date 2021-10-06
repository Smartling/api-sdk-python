from smartlingApiSdk.ApiV2 import ApiV2

class StringsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def addStringsToProject(self, strings, placeholderFormat, placeholderFormatCustom, namespace, **kwargs):
        '''
            method  :  POST
            api url :  /strings-api/v2/projects/{projectId}
            details :  https://api-reference.smartling.com/#operation/addStringsToProject
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringJSON" https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId
        '''
        kw = {
            'strings':strings,
            'placeholderFormat':placeholderFormat,
            'placeholderFormatCustom':placeholderFormatCustom,
            'namespace':namespace,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}', **kwargs)
        return self.commandJson('POST', url, kw)


    def getAddStringsToProjectRequestStatus(self, processUid, **kwargs):
        '''
            method  :  GET
            api url :  /strings-api/v2/projects/{projectId}/processes/{processUid}
            details :  https://api-reference.smartling.com/#operation/getAddStringsToProjectRequestStatus
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/processes/$processUid
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}/processes/{processUid}', processUid=processUid, **kwargs)
        return self.command('GET', url, kw)


    def getAllSourceStringsByProject(self, hashcodes=[], fileUri='', limit='', offset='', **kwargs):
        '''
            method  :  POST
            api url :  /strings-api/v2/projects/{projectId}/source-strings
            details :  https://api-reference.smartling.com/#operation/getAllSourceStringsByProject
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G -d "fileUri=$smartlingFileUri" https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/source-strings
        '''
        kw = {
            'hashcodes':hashcodes,
            'fileUri':fileUri,
            'limit':limit,
            'offset':offset,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}/source-strings', **kwargs)
        return self.commandJson('POST', url, kw)


    def getAllTranslationsByProject(self, targetLocaleId, hashcodes=[], retrievalType='', fileUri='', limit='', offset='', **kwargs):
        '''
            method  :  POST
            api url :  /strings-api/v2/projects/{projectId}/translations
            details :  https://api-reference.smartling.com/#operation/getAllTranslationsByProject
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/translations
        '''
        kw = {
            'targetLocaleId':targetLocaleId,
            'hashcodes':hashcodes,
            'retrievalType':retrievalType,
            'fileUri':fileUri,
            'limit':limit,
            'offset':offset,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}/translations', **kwargs)
        return self.commandJson('POST', url, kw)

