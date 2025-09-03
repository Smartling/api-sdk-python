#!/usr/bin/python
# -*- coding: utf-8 -*-




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

        """

    def __init__(self, userIdentifier, userSecret, proxySettings=None, permanentHeaders={}):
        ProjectsApiV2.__init__(self, userIdentifier, userSecret, proxySettings, permanentHeaders=permanentHeaders)

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

