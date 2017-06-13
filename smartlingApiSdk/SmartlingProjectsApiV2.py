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

from .ProjectsApiV2 import ProjectsApiV2

class SmartlingProjectsApiV2(ProjectsApiV2):
    """ Wrapper class providing access to projects API commands, all methods below represent API commands.
        Each command returns tuple = (response, status_code) 
        where response is ApiResponse object and status code = HTTP response status code
        
        ApiResponse object is python object as a result of json response parsing
        ApiResponse attributes depend on response json.
        To view all attributes of response use:
        for k,v in response.items(): print k, ':' ,v
        
        Response also can be a string to provide backward compatibility with previous versions
        in case you need json response as a string use :
        api = SmartlingFileApi(userIdentifier, userSecret, projectId)
        api.response_as_string = True
        
        Some of methods may be called with optional parameters
        like `list` method may have locale optional parameter or offset parameter
        simple list:
             api.list()
        list with additional parameters:
             api.list(limit=100, offset=50)
        """

    def __init__(self, userIdentifier, userSecret, proxySettings=None):
        ProjectsApiV2.__init__(self, userIdentifier, userSecret, proxySettings)

    def projects(self, accountUid):
        """
        Returns a list of all projects in an account, including basic project details.
        returns (response, status_code) tuple
        http://docs.smartling.com/pages/API/v2/Projects/List-Projects/
        """
        return self.commandProjects(accountUid)

    def project_details(self, projectId):
        """
        Returns basic details on a specific Smartling project.
        returns (response, status_code) tuple
        for details see http://docs.smartling.com/pages/API/v2/Projects/Project-Details/
        """
        return self.commandProjectDetails(projectId)

