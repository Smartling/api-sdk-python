from .Constants import Uri, Params, ReqMethod
from .FileApiBase import FileApiBase

import warnings

class ApiV1(FileApiBase):
    """ Api v1 basic functionality. This API is deprecated. Please use ApiV2 instead. """
    def __init__(self, host, apiKey, projectId, proxySettings=None, permanentHeaders={}):
        warnings.warn("ApiV1 is deprecated, please use ApiV2 instead.", DeprecationWarning, stacklevel=2)
        super().__init__(host, proxySettings, permanentHeaders=permanentHeaders)
        self.apiKey = apiKey
        self.projectId = projectId

    def addAuth(self, params):
        params[Params.API_KEY] = self.apiKey
        params[Params.PROJECT_ID] = self.projectId
        return {}

    def commandUpload(self, uploadData):
        params = {
                    Params.FILE_URI: uploadData.uri or uploadData.name,
                    Params.FILE_TYPE: uploadData.type,
                    Params.FILE_PATH: uploadData.path + uploadData.name
                  }
        if (uploadData.approveContent):
            params[Params.APPROVED] = uploadData.approveContent

        if (uploadData.callbackUrl):
            params[Params.CALLBACK_URL] = uploadData.callbackUrl

        if (uploadData.directives):
            for index, directive in enumerate(uploadData.directives):
                params[directive.SL_PREFIX + directive.name] = directive.value
                
        if (uploadData.localesToApprove):
            for index, locale in enumerate(uploadData.localesToApprove):
                params['{0}[{1}]'.format(Params.LOCALES_TO_APPROVE, index)] = locale

        return self.uploadMultipart(Uri.UPLOAD, params)

    def commandList(self, **kw):
        return self.command(ReqMethod.POST, Uri.LIST, kw)

    def commandLastModified(self, fileUri, locale=None, **kw):
        kw[Params.FILE_URI] = fileUri
        if locale is not None:
            kw[Params.LOCALE] = locale
        return self.command(ReqMethod.GET, Uri.LAST_MODIFIED, kw)
        
    def commandGet(self, fileUri, locale, **kw):
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE] = locale
        if Params.RETRIEVAL_TYPE in kw and not kw[Params.RETRIEVAL_TYPE] in Params.allowedRetrievalTypes:
            raise "Not allowed value `%s` for parameter:%s try one of %s" % (kw[Params.RETRIEVAL_TYPE],
                                                                             Params.RETRIEVAL_TYPE,
                                                                             Params.allowedRetrievalTypes)

        resp, code, headers = self.getResponseAndStatus(ReqMethod.POST, Uri.GET, kw)
        return resp, code

    def commandDelete(self, fileUri, **kw):
        kw[Params.FILE_URI] = fileUri

        return self.command(ReqMethod.POST, Uri.DELETE, kw)
        
    def commandImport(self, uploadData, locale, **kw):
        kw[Params.FILE_URI]  = uploadData.uri
        kw[Params.FILE_TYPE] = uploadData.type
        kw[Params.FILE_PATH] = uploadData.path + uploadData.name
        kw["file"] = uploadData.path + uploadData.name + ";type=text/plain"
        kw[Params.LOCALE] = locale

        return self.uploadMultipart(Uri.IMPORT, kw)

    def commandStatus(self, fileUri, locale, **kw):
        kw[Params.FILE_URI] = fileUri
        kw[Params.LOCALE] = locale

        return self.command(ReqMethod.POST, Uri.STATUS, kw)

    def commandRename(self, fileUri, newUri, **kw):
        kw[Params.FILE_URI] = fileUri
        kw[Params.FILE_URI_NEW] = newUri

        return self.command(ReqMethod.POST, Uri.RENAME, kw)
