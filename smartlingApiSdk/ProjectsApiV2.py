#!/usr/bin/python
# -*- coding: utf-8 -*-


''' Copyright 2012 Smartling, Inc.
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
'''

#FileApi class implementation

from .Constants import ReqMethod
from .UrlV2Helper import UrlV2Helper
from .ApiV2 import ApiV2

class ProjectsApiV2(ApiV2):
    """ basic class implementing Projects/Accounts api calls """

    def __init__(self, userIdentifier, userSecret, proxySettings=None):
        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings)
        self.urlHelper = UrlV2Helper(None)

    def commandProjectDetails(self, projectId):    
        """ http://docs.smartling.com/pages/API/v2/Projects/Project-Details/ """
        kw = {}
        url = self.urlHelper.getUrl(self.urlHelper.PROJECT_DETAILS, projectId=projectId)
        return self.command(ReqMethod.GET, url, kw)

    def commandProjects(self, accountUid):    
        """ http://docs.smartling.com/pages/API/v2/Projects/List-Projects/ """
        kw = {}
        url = self.urlHelper.getUrl(self.urlHelper.PROJECTS, accountUid = accountUid)
        return self.command(ReqMethod.GET, url, kw)
        

       