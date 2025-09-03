class UploadData:
    """ Helper class to store `upload` and `import` command attributes """
    approveContent = "false"
    callbackUrl = ""
    localesToApprove = []

    def __init__(self, path, name, type):
        self.path = path
        self.name = name
        self.type = type
        self.uri = name
        self.directives = []
 
    def setApproveContent(self, approveContent):
        self.approveContent = approveContent

    def setCallbackUrl(self, callbackUrl):
        self.callbackUrl = callbackUrl
        
    def setLocalesToApprove(self, localesToApprove):
        self.localesToApprove = localesToApprove

    def addDirective(self, directive):
        self.directives.append(directive)

    def setUri(self, uri):
        self.uri = uri
