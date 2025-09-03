class UrlV2Helper:
    
    GET = "/files-api/v2/projects/{projectId}/locales/{localeId}/file"
    GET_MULTIPLE_LOCALES = "/files-api/v2/projects/{projectId}/files/zip"
    GET_ALL_LOCALES_ZIP = "/files-api/v2/projects/{projectId}/locales/all/file/zip"
    GET_ALL_LOCALES_CSV = "/files-api/v2/projects/{projectId}/locales/all/file"
    GET_ORIGINAL = "/files-api/v2/projects/{projectId}/file"
    LIST_FILES = "/files-api/v2/projects/{projectId}/files/list"
    LIST_FILE_TYPES = "/files-api/v2/projects/{projectId}/file-types"
    UPLOAD = "/files-api/v2/projects/{projectId}/file"
    DELETE = "/files-api/v2/projects/{projectId}/file/delete"
    PROJECT_DETAILS = "/projects-api/v2/projects/{projectId}"
    PROJECTS = "/accounts-api/v2/accounts/{accountUid}/projects"
    STATUS_ALL = "/files-api/v2/projects/{projectId}/file/status"
    STATUS_LOCALE = "/files-api/v2/projects/{projectId}/locales/{localeId}/file/status"
    RENAME = "/files-api/v2/projects/{projectId}/file/rename"
    LAST_MODIFIED = "/files-api/v2/projects/{projectId}/locales/{localeId}/file/last-modified"
    LAST_MODIFIED_ALL = "/files-api/v2/projects/{projectId}/file/last-modified"
    IMPORT = "/files-api/v2/projects/{projectId}/locales/{localeId}/file/import"
    GET_TRANSLATIONS = "/files-api/v2/projects/{projectId}/locales/{localeId}/file/get-translations"
    
    def __init__(self, projectId):
        self.projectId = projectId

    def getUrl(self, urlWithPlaceholders, localeId="", accountUid="", projectId="", **kw):
        
        url = urlWithPlaceholders
        if projectId:
            url = url.replace("{projectId}", projectId)
        else:
            url = url.replace("{projectId}", self.projectId)

        if localeId:
            url = url.replace("{localeId}", localeId)
        
        if accountUid:
            url = url.replace("{accountUid}", accountUid)

        for k in kw:
            url = url.replace("{%s}" % k, kw[k])
        
        if "{localeId}" in url:
            raise "Unhandled localeId placeholder:" + url
            
        if "{accountUid}" in url:
            raise "Unhandled accountUid placeholder:" + url
            
        if "{projectId}" in url:
            raise "Unhandled projectId placeholder:" + url
            
        return url
