#FileApi class implementation

import httplib
import urllib
import urllib2
from MultipartPostHandler import MultipartPostHandler
from Constants import Uri, Params

class FileApiBase:
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
 
    def __init__(self, host, apiKey, projectId):
        self.host   = host
        self.apiKey = apiKey
        self.projectId = projectId
  
    def addApiKeys(self, params):
        params [Params.API_KEY]    = self.apiKey
        params [Params.PROJECT_ID] = self.projectId 
     
    def uploadMultipart(self, params):
        self.addApiKeys(params) 
        params [Params.FILE] = open(params[Params.FILE_PATH],'rb')
        opener = urllib2.build_opener(MultipartPostHandler)
        urllib2.install_opener(opener)
        req = urllib2.Request('https://'+self.host + Uri.UPLOAD, params)
        response = urllib2.urlopen(req).read().strip()
        return response 

    def command(self, uri, params):
        self.addApiKeys(params)
        params_encoded = urllib.urlencode( params )
        conn = httplib.HTTPSConnection( self.host )
        conn.request("POST", uri, params_encoded, self.headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    

    # commands

    def commandUpload(self, path, name, type):
        params = { 
                    Params.FILE_URI  : name, 
                    Params.FILE_TYPE : type, 
                    Params.FILE_PATH : path + name, 
                  }
        return self.uploadMultipart( params )                  
    
    def commandList(self):
        return self.command( Uri.LIST, {} )

    def commandGet(self, fileUri, locale):
        params =  { 
            Params.FILE_URI : fileUri, 
            Params.LOCALE   : locale 
            }
        return self.command( Uri.GET, params )
        
    def commandStatus(self, fileUri, locale):
        params = { 
            Params.FILE_URI : fileUri, 
            Params.LOCALE   : locale 
            }
        return self.command( Uri.STATUS, params )   
