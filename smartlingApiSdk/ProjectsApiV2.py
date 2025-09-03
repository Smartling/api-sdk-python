#!/usr/bin/python
# -*- coding: utf-8 -*-




#FileApi class implementation

from .Constants import ReqMethod
from .UrlV2Helper import UrlV2Helper
from .ApiV2 import ApiV2

class ProjectsApiV2(ApiV2):
    """ basic class implementing Projects/Accounts api calls """

    def __init__(self, userIdentifier, userSecret, proxySettings=None, permanentHeaders={}):
        outdated = '''
This api is outdated and is not supported anymore!
You still can use it by commenting this exception.
But it is advised to use new api version.
Please check examples for current api usage.'''
        raise Exception(outdated)
        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings, permanentHeaders=permanentHeaders)
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
        

       