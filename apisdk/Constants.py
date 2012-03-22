#constants for File API

class Params:
    API_KEY    = 'apiKey'
    PROJECT_ID = 'projectId'
    FILE_PATH  = 'file_path'
    FILE_URI   = 'fileUri'
    FILE_TYPE  = 'fileType'
    LOCALE     = 'locale'
    FILE       = 'file'
    
class Uri:
    base = '/v1/file/'
    UPLOAD = base + 'upload'
    LIST   = base + 'list'
    GET    = base + 'get'
    STATUS = base + 'status'