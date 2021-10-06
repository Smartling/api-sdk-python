from smartlingApiSdk.ApiV2 import ApiV2

class ContextApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def uploadNewVisualContext(self, name='', content='', **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -F "content=@context1.png;type=image/png" -F "name=context1.png" "https://api.smartling.com/context-api/v2/projects/$smartlingProjectId/contexts"
            Responses:
                200 : OK
                400 : Validation error
            details :  https://api-reference.smartling.com/#operation/uploadNewVisualContext
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
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getVisualContextsListByProject
        '''
        kw = {
            'nameFilter':nameFilter,
            'offset':offset,
            'type':type,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getVisualContextInfo(self, contextUid, **kwargs):
        '''
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}
            Responses:
                200 : OK
                404 : Context not found
            details :  https://api-reference.smartling.com/#operation/getVisualContextInfo
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}', contextUid=contextUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def deleteVisualContext(self, contextUid, **kwargs):
        '''
            method  :  DELETE
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}
            Responses:
                200 : OK
                404 : Context not found
            details :  https://api-reference.smartling.com/#operation/deleteVisualContext
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}', contextUid=contextUid, **kwargs)
        response, status = self.command('DELETE', url, kw)
        return response, status


    def downloadVisualContextFileContent(self, contextUid, **kwargs):
        '''
            method  :  GET
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}/content
            Responses:
                200 : OK
                404 : Context not found
            details :  https://api-reference.smartling.com/#operation/downloadVisualContextFileContent
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}/content', contextUid=contextUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def runAutomaticContextMatching(self, contextUid, contentFileUri, stringHashcodes, overrideContextOlderThanDays, **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts/{contextUid}/match/async
            Responses:
                202 : ACCEPTED
                400 : Validation error
            details :  https://api-reference.smartling.com/#operation/runAutomaticContextMatching
        '''
        kw = {
            'contentFileUri':contentFileUri,
            'stringHashcodes':stringHashcodes,
            'overrideContextOlderThanDays':overrideContextOlderThanDays,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/contexts/{contextUid}/match/async', contextUid=contextUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def uploadAndMatchVisualContext(self, content, name='', matchParams='', **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/contexts/upload-and-match-async
            Responses:
                202 : ACCEPTED
                400 : Validation error
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
            Responses:
                200 : OK
                404 : Match request expired or does not exist
            details :  https://api-reference.smartling.com/#operation/getAsyncContextMatchResults
        '''
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/match/{matchId}', matchId=matchId, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def createStringToContextBindings(self, bindings, **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/bindings
            Responses:
                200 : OK
                400 : Validation error
            details :  https://api-reference.smartling.com/#operation/createStringToContextBindings
        '''
        kw = {
            'bindings':bindings,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/context-api/v2/projects/{projectId}/bindings', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getBindings(self, stringHashcodes, contentFileUri, contextUid, bindingUids, offset='', **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/bindings/list
            Responses:
                200 : OK
                400 : Validation error
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
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def deleteBindings(self, stringHashcodes, contentFileUri, contextUid, bindingUids, **kwargs):
        '''
            method  :  POST
            api url :  /context-api/v2/projects/{projectId}/bindings/remove
            Responses:
                200 : OK
                400 : Validation error
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
        response, status = self.commandJson('POST', url, kw)
        return response, status

