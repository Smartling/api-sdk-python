from smartlingApiSdk.UrlV2Helper import UrlV2Helper
from smartlingApiSdk.ApiV2 import ApiV2

class ContextApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings, permanentHeaders=permanentHeaders, env=env)
        self.urlHelper = UrlV2Helper(projectId)

    def uploadNewVisualContext(self, name='', content=''):
        """
            post
            /context-api/v2/projects/{projectId}/contexts
            for details check: https://api-reference.smartling.com/#operation/uploadNewVisualContext
            curl -X POST -H "Authorization: Bearer $smartlingToken" -F "content=@context1.png;type=image/png" -F "name=context1.png" "https://api.smartling.com/context-api/v2/projects/$smartlingProjectId/contexts"

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'name':name,
            'content':self.processFile(content),
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts')
        return self.uploadMultipart(url, kw)




    def getVisualContextsListByProject(self, nameFilter='', offset='', type=''):
        """
            get
            /context-api/v2/projects/{projectId}/contexts
            for details check: https://api-reference.smartling.com/#operation/getVisualContextsListByProject

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'nameFilter':nameFilter,
            'offset':offset,
            'type':type,
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts')
        return self.command('GET', url, kw)




    def getVisualContextInfo(self, contextUid):
        """
            get
            /context-api/v2/projects/{projectId}/contexts/{contextUid}
            for details check: https://api-reference.smartling.com/#operation/getVisualContextInfo

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}', contextUid=contextUid)
        return self.command('GET', url, kw)




    def deleteVisualContext(self, contextUid):
        """
            delete
            /context-api/v2/projects/{projectId}/contexts/{contextUid}
            for details check: https://api-reference.smartling.com/#operation/deleteVisualContext

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}', contextUid=contextUid)
        return self.command('DELETE', url, kw)




    def downloadVisualContextFileContent(self, contextUid):
        """
            get
            /context-api/v2/projects/{projectId}/contexts/{contextUid}/content
            for details check: https://api-reference.smartling.com/#operation/downloadVisualContextFileContent

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}/content', contextUid=contextUid)
        return self.command('GET', url, kw)




    def runAutomaticContextMatching(self, contextUid, contentFileUri, stringHashcodes, overrideContextOlderThanDays):
        """
            post
            /context-api/v2/projects/{projectId}/contexts/{contextUid}/match/async
            for details check: https://api-reference.smartling.com/#operation/runAutomaticContextMatching

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'contentFileUri':contentFileUri,
            'stringHashcodes':stringHashcodes,
            'overrideContextOlderThanDays':overrideContextOlderThanDays,
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}/match/async', contextUid=contextUid)
        return self.commandJson('POST', url, kw)




    def uploadAndMatchVisualContext(self, content, name='', matchParams=''):
        """
            post
            /context-api/v2/projects/{projectId}/contexts/upload-and-match-async
            for details check: https://api-reference.smartling.com/#operation/uploadAndMatchVisualContext

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'content':self.processFile(content),
            'name':name,
            'matchParams':matchParams,
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/upload-and-match-async')
        return self.uploadMultipart(url, kw)




    def getAsyncContextMatchResults(self, matchId):
        """
            get
            /context-api/v2/projects/{projectId}/match/{matchId}
            for details check: https://api-reference.smartling.com/#operation/getAsyncContextMatchResults

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/match/{matchId}', matchId=matchId)
        return self.command('GET', url, kw)




    def createStringToContextBindings(self, bindings):
        """
            post
            /context-api/v2/projects/{projectId}/bindings
            for details check: https://api-reference.smartling.com/#operation/createStringToContextBindings

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'bindings':bindings,
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/bindings')
        return self.commandJson('POST', url, kw)




    def getBindings(self, batchBindingsRequest, offset=''):
        """
            post
            /context-api/v2/projects/{projectId}/bindings/list
            for details check: https://api-reference.smartling.com/#operation/getBindings

            ------------------------------------------------------------------------------------------------------------------------
            Parameters example:
            batchBindingsRequest: {
                "stringHashcodes": "[]",
                "contentFileUri": "''",
                "contextUid": "''",
                "bindingUids": "[]"
                }
        """
        kw = {
            'offset':offset,
            'batchBindingsRequest':batchBindingsRequest,
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/bindings/list')
        return self.commandJson('POST', url, kw)




    def deleteBindings(self, batchBindingsRequest):
        """
            post
            /context-api/v2/projects/{projectId}/bindings/remove
            for details check: https://api-reference.smartling.com/#operation/deleteBindings

            ------------------------------------------------------------------------------------------------------------------------
            Parameters example:
            batchBindingsRequest: {
                "stringHashcodes": "[]",
                "contentFileUri": "''",
                "contextUid": "''",
                "bindingUids": "[]"
                }
        """
        kw = {
            'batchBindingsRequest':batchBindingsRequest,
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/bindings/remove')
        return self.commandJson('POST', url, kw)



