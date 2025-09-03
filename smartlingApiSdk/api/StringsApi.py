
#!/usr/bin/python
# -*- coding: utf-8 -*-





from smartlingApiSdk.ApiV2 import ApiV2

class StringsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def addStringsToProject(self, strings, placeholderFormat='', placeholderFormatCustom='', namespace='smartling.strings-api.default.namespace', **kwargs):
        """
            method  :  POST
            api url :  /strings-api/v2/projects/{projectId}
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringJSON" https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId
            Responses:
                200 : OK
                202 : ACCEPTED
            details :  https://api-reference.smartling.com/#operation/addStringsToProject
        """
        kw = {
            'strings':strings,
            'placeholderFormat':placeholderFormat,
            'placeholderFormatCustom':placeholderFormatCustom,
            'namespace':namespace,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getAddStringsToProjectRequestStatus(self, processUid, **kwargs):
        """
            method  :  GET
            api url :  /strings-api/v2/projects/{projectId}/processes/{processUid}
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/processes/$processUid
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getAddStringsToProjectRequestStatus
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}/processes/{processUid}', processUid=processUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getAllSourceStringsByProject(self, hashcodes=[], fileUri='', limit='', offset='', **kwargs):
        """
            method  :  POST
            api url :  /strings-api/v2/projects/{projectId}/source-strings
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G -d "fileUri=$smartlingFileUri" https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/source-strings
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getAllSourceStringsByProject
        """
        kw = {
            'hashcodes':hashcodes,
            'fileUri':fileUri,
            'limit':limit,
            'offset':offset,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/strings-api/v2/projects/{projectId}/source-strings', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getAllTranslationsByProject(self, targetLocaleId, hashcodes=[], retrievalType='', fileUri='', limit='', offset='', **kwargs):
        """
            method  :  POST
            api url :  /strings-api/v2/projects/{projectId}/translations
            as curl :  curl -H "Authorization: Bearer $smartlingToken" -G https://api.smartling.com/strings-api/v2/projects/$smartlingProjectId/translations
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getAllTranslationsByProject
        """
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
        response, status = self.commandJson('POST', url, kw)
        return response, status

