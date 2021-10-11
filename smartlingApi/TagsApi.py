
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

class TagsApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def getTagsListByProject(self, tagMask='', limit=100, offset=0, **kwargs):
        """
            method  :  GET
            api url :  /tags-api/v2/projects/{projectId}/tags
            as curl :  curl -H "Authorization: Bearer $smartlingToken" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/tags
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getTagsListByProject
        """
        kw = {
            'tagMask':tagMask,
            'limit':limit,
            'offset':offset,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/tags', **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getAllTagsForStrings(self, stringHashcodes, **kwargs):
        """
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/search
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/search
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getAllTagsForStrings
        """
        kw = {
            'stringHashcodes':stringHashcodes,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/strings/tags/search', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def addTagToStrings(self, tags, stringHashcodes, **kwargs):
        """
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/add
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/add
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/addTagToStrings
        """
        kw = {
            'tags':tags,
            'stringHashcodes':stringHashcodes,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/strings/tags/add', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def removeTagsFromStrings(self, tags, stringHashcodes, **kwargs):
        """
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/remove
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/remove
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/removeTagsFromStrings
        """
        kw = {
            'tags':tags,
            'stringHashcodes':stringHashcodes,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/strings/tags/remove', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def removeAllTagsFromStrings(self, stringHashcodes, **kwargs):
        """
            method  :  POST
            api url :  /tags-api/v2/projects/{projectId}/strings/tags/remove/all
            as curl :  curl -X POST -H "Authorization: Bearer $smartlingToken" -H "Content-Type: application/json" -d "$smartlingStringTagJSON" https://api.smartling.com/tags-api/v2/projects/$smartlingProjectId/strings/tags/remove/all
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/removeAllTagsFromStrings
        """
        kw = {
            'stringHashcodes':stringHashcodes,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/tags-api/v2/projects/{projectId}/strings/tags/remove/all', **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status

