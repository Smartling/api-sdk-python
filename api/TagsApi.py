from smartlingApiSdk.ApiV2 import ApiV2

class TagsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def getTagsListByProject(self, tagMask='', limit=100, offset=0, **kwargs):
        '''
            method  :  GET
            api url :  /tags-api/v2/projects/{projectId}/tags
            details :  https://api-reference.smartling.com/#operation/getTagsListByProject
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/tags
        '''
        kw = {
            'tagMask':tagMask,
            'limit':limit,
            'offset':offset,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/tags', **kwargs)
        return self.command('GET', url, kw)


    def getAllTagsForStrings(self, stringHashcodes, **kwargs):
        '''
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/search
            details :  https://api-reference.smartling.com/#operation/getAllTagsForStrings
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/search
        '''
        kw = {
            'stringHashcodes':stringHashcodes,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/strings/tags/search', **kwargs)
        return self.commandJson('POST', url, kw)


    def addTagToStrings(self, tags, stringHashcodes, **kwargs):
        '''
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/add
            details :  https://api-reference.smartling.com/#operation/addTagToStrings
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/add
        '''
        kw = {
            'tags':tags,
            'stringHashcodes':stringHashcodes,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/strings/tags/add', **kwargs)
        return self.commandJson('POST', url, kw)


    def removeTagsFromStrings(self, tags, stringHashcodes, **kwargs):
        '''
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/remove
            details :  https://api-reference.smartling.com/#operation/removeTagsFromStrings
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/remove
        '''
        kw = {
            'tags':tags,
            'stringHashcodes':stringHashcodes,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/strings/tags/remove', **kwargs)
        return self.commandJson('POST', url, kw)


    def removeAllTagsFromStrings(self, stringHashcodes, **kwargs):
        '''
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/remove/all
            details :  https://api-reference.smartling.com/#operation/removeAllTagsFromStrings
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/remove/all
        '''
        kw = {
            'stringHashcodes':stringHashcodes,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/strings/tags/remove/all', **kwargs)
        return self.commandJson('POST', url, kw)
