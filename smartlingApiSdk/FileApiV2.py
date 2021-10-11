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

#FileApi class implementation

from .Constants import Params, ReqMethod
from .ApiV2 import ApiV2

class FileApiV2(ApiV2):
    """ basic class implementing file api calls """

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}):
        outdated = '''
This api is outdated and is not supported anymore!
You still can use it by commenting this exception.
But it is advised to use new api version.
Please check examples for current api usage.'''
        raise Exception(outdated)
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders)

    def commandGet(self, fileUri, locale, directives={}, **kw):
        """ https://developer.smartling.com/v1.0/reference#get_projects-projectid-locales-localeid-file """
        kw[Params.FILE_URI] = fileUri

        self.checkRetrievalType(kw)
        self.processDirectives(kw, directives)
        url = self.urlHelper.getUrl(self.urlHelper.GET, localeId=locale)

        resp, code, headers = self.getResponseAndStatus(ReqMethod.GET, url, kw)
        return resp, code

    def commandGetMultipleLocalesAsZip(self, fileUri, localeIds, directives={}, **kw):
        """ https://developer.smartling.com/v1.0/reference#get_projects-projectid-files-zip """
        kw[Params.FILE_URIS] = fileUri
        kw[Params.LOCALE_IDS] = localeIds

        self.checkRetrievalType(kw)
        self.processDirectives(kw, directives)

        resp, code, headers = self.getResponseAndStatus(ReqMethod.GET, self.urlHelper.getUrl(self.urlHelper.GET_MULTIPLE_LOCALES), kw)
        return resp, code

    def commandGetAllLocalesZip(self, fileUri, directives={}, **kw):
         """ http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/All-Locales """
         kw[Params.FILE_URI] = fileUri

         self.checkRetrievalType(kw)
         self.processDirectives(kw, directives)

         url = self.urlHelper.getUrl(self.urlHelper.GET_ALL_LOCALES_ZIP)

         resp, code, headers = self.getResponseAndStatus(ReqMethod.GET, url, kw)
         return resp, code


    def commandGetAllLocalesCsv(self, fileUri, directives={}, **kw):
         """  http://docs.smartling.com/pages/API/v2/FileAPI/Download-File/All-Locales-CSV """
         kw[Params.FILE_URI] = fileUri

         self.checkRetrievalType(kw)
         self.processDirectives(kw, directives)

         url = self.urlHelper.getUrl(self.urlHelper.GET_ALL_LOCALES_CSV)
         resp, code, headers = self.getResponseAndStatus(ReqMethod.GET, url, kw)
         return resp, code


    def commandGetOriginal(self, fileUri):
        """  https://developer.smartling.com/v1.0/reference#get_projects-projectid-file """
        kw = {}
        kw[Params.FILE_URI] = fileUri

        url = self.urlHelper.getUrl(self.urlHelper.GET_ORIGINAL)
        resp, code, headers = self.getResponseAndStatus(ReqMethod.GET, url, kw)
        return resp, code

    def commandList(self, **kw):
        """ https://developer.smartling.com/v1.0/reference#list """
        url = self.urlHelper.getUrl(self.urlHelper.LIST_FILES)
        self.validateFileTypes(kw)

        return self.command(ReqMethod.GET, url, kw)

    def commandListFileTypes(self, **kw):
        """ https://developer.smartling.com/v1.0/reference#get_projects-projectid-file-types """
        return self.command(ReqMethod.GET, self.urlHelper.getUrl(self.urlHelper.LIST_FILE_TYPES), kw)

    def commandUpload(self, filePath, fileType, directives={}, **kw):
        """ https://developer.smartling.com/v1.0/reference#upload """
        params = {
                Params.FILE_URI: filePath,
                Params.FILE_TYPE: fileType,
                Params.FILE_PATH: filePath
            }

        for k,v in list(kw.items()):
            params[k] = v

        self.addLibIdDirective(params)
        self.processDirectives(params, directives)

        url = self.urlHelper.getUrl(self.urlHelper.UPLOAD)
        return self.uploadMultipart(url, params)

    def commandDelete(self, fileUri, **kw):
        """ https://developer.smartling.com/v1.0/reference#delete """
        kw[Params.FILE_URI] = fileUri
        uri = self.urlHelper.getUrl(self.urlHelper.DELETE)

        return self.command(ReqMethod.POST, uri, kw)

    def commandStatus(self, fileUri):
        """ https://developer.smartling.com/v1.0/reference#get_projects-projectid-file-status """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.STATUS_ALL)
        return self.command(ReqMethod.GET, url, kw)

    def commandStatusLocale(self, fileUri, localeId):
        """ https://developer.smartling.com/v1.0/reference#get_projects-projectid-locales-localeid-file-status """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.STATUS_LOCALE, localeId = localeId)
        return self.command(ReqMethod.GET, url, kw)

    def commandRename(self, fileUri, newFileUrl):
        """ https://developer.smartling.com/v1.0/reference#rename """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        kw[Params.FILE_URI_NEW] = newFileUrl
        url = self.urlHelper.getUrl(self.urlHelper.RENAME)
        return self.command(ReqMethod.POST, url, kw)

    def commandLastModified(self, fileUri, localeId, **kw):
        """ https://developer.smartling.com/v1.0/reference#last-modified """
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.LAST_MODIFIED, localeId = localeId)
        return self.command(ReqMethod.GET, url, kw)

    def commandLastModifiedAll(self, fileUri, **kw):
        """ https://developer.smartling.com/v1.0/reference#get_projects-projectid-file-last-modified """
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.LAST_MODIFIED_ALL)
        return self.command(ReqMethod.GET, url, kw)

    def commandImport(self, fileUriOriginal, filePathTranslated, fileType, localeId, directives={}, **kw):
        self.validateFileTypes({"fileTypes":fileType})
        params = {}
        params[Params.FILE_URI]  = fileUriOriginal
        params[Params.FILE_TYPE] = fileType
        params[Params.FILE_PATH] = filePathTranslated
        params["file"] = filePathTranslated + ";type=text/plain"

        for k,v in list(kw.items()):
            params[k] = v

        self.processDirectives(params, directives)

        url = self.urlHelper.getUrl(self.urlHelper.IMPORT, localeId = localeId)
        return self.uploadMultipart(url, params)

    def commandListAuthorizedLocales(self, fileUri):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Authorize-Content/List-Authorized-Locales/ """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        url = self.urlHelper.getUrl(self.urlHelper.LIST_AUTHORIZED_LOCALES)
        return self.command(ReqMethod.GET, url, kw)

    def commandAuthorize(self, fileUri, localeIds):
        """ http://docs.smartling.com/pages/API/v2/FileAPI/Authorize-Content/Authorize/ """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE_IDS_BRACKET] = ",".join(localeIds)
        url = self.urlHelper.getUrl(self.urlHelper.AUTHORIZE)
        return self.command(ReqMethod.POST, url, kw)

    def commandUnauthorize(self, fileUri, localeIds):
        """  http://docs.smartling.com/pages/API/v2/FileAPI/Authorize-Content/Unauthorize/ """
        kw = {}
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE_IDS_BRACKET] = ",".join(localeIds)
        url = self.urlHelper.getUrl(self.urlHelper.UNAUTHORIZE)
        return self.command(ReqMethod.DELETE, url, kw)

    def commandGetTranslations(self, fileUri, filePath, localeId, directives={}, **kw):
        """  https://developer.smartling.com/v1.0/reference#post_projects-projectid-locales-localeid-file-import """
        kw[Params.FILE_URI]  = fileUri
        kw[Params.FILE_PATH] = filePath
        kw["file"] = filePath + ";type=text/plain"

        self.processDirectives(kw, directives)

        url = self.urlHelper.getUrl(self.urlHelper.GET_TRANSLATIONS, localeId = localeId)
        return self.uploadMultipart(url, kw, response_as_string=True)
