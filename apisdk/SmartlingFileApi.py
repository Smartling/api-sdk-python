#FileApi class implementation

from FileApiBase import FileApiBase

class SmartlingFileApi(FileApiBase):

    def __init__(self, host, apiKey, projectId):
        FileApiBase.__init__(self, host, apiKey, projectId)
        
    def upload(self, file_path, fname, ftype):
        return self.commandUpload( file_path, fname, ftype)                  
    
    def list(self):
        return self.commandList( )

    def get(self, fileUri, locale):
        return self.commandGet(fileUri, locale)
        
    def status(self, fileUri, locale):
        return self.commandStatus( fileUri, locale )  