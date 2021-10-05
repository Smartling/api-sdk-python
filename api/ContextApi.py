from smartlingApiSdk.ApiV2 import ApiV2

class ContextApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def uploadNewVisualContext(self, name='', content='', **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts
            details :  https://api-reference.smartling.com/#operation/uploadNewVisualContext
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -F "content=@context1.png;type=image/png" -F "name=context1.png" "https://api.smartling.com/context-api/v2/projects/$smartlingProjectId/contexts"
        '''
        kw = {
            'name':name,
            'content':self.processFile(content),
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts')
        return self.uploadMultipart(url, kw)


    def getVisualContextsListByProject(self, nameFilter='', offset='', type='', **kwargs):
        '''
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/contexts
            details :  https://api-reference.smartling.com/#operation/getVisualContextsListByProject
        '''
        kw = {
            'nameFilter':nameFilter,
            'offset':offset,
            'type':type,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts', **kwargs)
        return self.command('GET', url, kw)


    def getVisualContextInfo(self, contextUid, **kwargs):
        '''
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}
            details :  https://api-reference.smartling.com/#operation/getVisualContextInfo
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}', contextUid=contextUid, **kwargs)
        return self.command('GET', url, kw)


    def deleteVisualContext(self, contextUid, **kwargs):
        '''
            method  :  DELETE
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}
            details :  https://api-reference.smartling.com/#operation/deleteVisualContext
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}', contextUid=contextUid, **kwargs)
        return self.command('DELETE', url, kw)


    def downloadVisualContextFileContent(self, contextUid, **kwargs):
        '''
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}/content
            details :  https://api-reference.smartling.com/#operation/downloadVisualContextFileContent
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}/content', contextUid=contextUid, **kwargs)
        return self.command('GET', url, kw)


    def runAutomaticContextMatching(self, contextUid, contentFileUri, stringHashcodes, overrideContextOlderThanDays, **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}/match/async
            details :  https://api-reference.smartling.com/#operation/runAutomaticContextMatching
        '''
        kw = {
            'contentFileUri':contentFileUri,
            'stringHashcodes':stringHashcodes,
            'overrideContextOlderThanDays':overrideContextOlderThanDays,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}/match/async', contextUid=contextUid, **kwargs)
        return self.commandJson('POST', url, kw)


    def uploadAndMatchVisualContext(self, content, name='', matchParams='', **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts/upload-and-match-async
            details :  https://api-reference.smartling.com/#operation/uploadAndMatchVisualContext
        '''
        kw = {
            'content':self.processFile(content),
            'name':name,
            'matchParams':matchParams,
        }
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/upload-and-match-async')
        return self.uploadMultipart(url, kw)


    def getAsyncContextMatchResults(self, matchId, **kwargs):
        '''
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/match/{matchId}
            details :  https://api-reference.smartling.com/#operation/getAsyncContextMatchResults
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/match/{matchId}', matchId=matchId, **kwargs)
        return self.command('GET', url, kw)


    def createStringToContextBindings(self, bindings, **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/bindings
            details :  https://api-reference.smartling.com/#operation/createStringToContextBindings
        '''
        kw = {
            'bindings':bindings,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/bindings', **kwargs)
        return self.commandJson('POST', url, kw)


    def getBindings(self, stringHashcodes, contentFileUri, contextUid, bindingUids, offset='', **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/bindings/list
            details :  https://api-reference.smartling.com/#operation/getBindings
        '''
        kw = {
            'offset':offset,
            'stringHashcodes':stringHashcodes,
            'contentFileUri':contentFileUri,
            'contextUid':contextUid,
            'bindingUids':bindingUids,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/bindings/list', **kwargs)
        return self.commandJson('POST', url, kw)


    def deleteBindings(self, stringHashcodes, contentFileUri, contextUid, bindingUids, **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/bindings/remove
            details :  https://api-reference.smartling.com/#operation/deleteBindings
        '''
        kw = {
            'stringHashcodes':stringHashcodes,
            'contentFileUri':contentFileUri,
            'contextUid':contextUid,
            'bindingUids':bindingUids,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/bindings/remove', **kwargs)
        return self.commandJson('POST', url, kw)

