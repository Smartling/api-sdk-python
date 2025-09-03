#!/usr/bin/python
# -*- coding: utf-8 -*-




import json


class Data:
    """ provides dictionary items to be object attributes """
    def __init__(self, dict):
        self.dict = dict

    def __getattr__(self, key):
        return self.dict[key]

    def __str__(self):
        return repr(self.dict)


class ApiResponse:
    """ response object to store parsed json response as python object, it also behaves like string for backward
        compatibility with previous SDK versions where response was a string """
    def __init__(self, responseString, statusCode, headers):
        self.statusCode = statusCode
        self.responseString = responseString
        self.responseDict = json.loads(responseString)
        self.isApiResonse = self.responseDict.get('response', None) and dict == type(self.responseDict['response'])
        self.headers = headers
        if self.isApiResonse:
            self.parseResponse()

    def parseResponse(self):
        """ parses json and fills object attributes according json attributes """

        for k, v in list(self.responseDict['response'].items()):
            if k == 'data':
                self.data = Data(v)
            else:
                setattr(self, k, v)

    def __getattr__(self, key):
        """ provides string object methods to be available for response to behave like a string """
        if hasattr(self.responseDict, key):
            return getattr(self.responseDict, key)

        try:
            return self.__dict__[key]
        except:
            raise AttributeError("ApiResponse has no attribute %r" % ( key ))

    def __str__(self):
        return str(self.responseString)
