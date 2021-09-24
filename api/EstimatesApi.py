from smartlingApiSdk.ApiV2 import ApiV2

class EstimatesApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def getJobFuzzyEstimateReports(self, translationJobUid, reportStatus='', contentCoverage='', creatorUserUids=[], translationJobSchemaContents=[], tags=[], createdFrom='', createdTo='', limit=0, offset=0):
        '''
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy
            details :  https://api-reference.smartling.com/#operation/getJobFuzzyEstimateReports
        '''
        kw = {
            'reportStatus':reportStatus,
            'contentCoverage':contentCoverage,
            'creatorUserUids':creatorUserUids,
            'translationJobSchemaContents':translationJobSchemaContents,
            'tags':tags,
            'createdFrom':createdFrom,
            'createdTo':createdTo,
            'limit':limit,
            'offset':offset,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)


    def generateJobFuzzyEstimateReports(self, translationJobUid, contentType, tags):
        '''
            method  :  POST
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy
            details :  https://api-reference.smartling.com/#operation/generateJobFuzzyEstimateReports
        '''
        kw = {
            'contentType':contentType,
            'tags':tags,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)


    def getJobCostEstimateReports(self, translationJobUid, reportStatus='', contentCoverage='', creatorUserUids=[], translationJobSchemaContents=[], tags=[], createdFrom='', createdTo='', limit=0, offset=0):
        '''
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost
            details :  https://api-reference.smartling.com/#operation/getJobCostEstimateReports
        '''
        kw = {
            'reportStatus':reportStatus,
            'contentCoverage':contentCoverage,
            'creatorUserUids':creatorUserUids,
            'translationJobSchemaContents':translationJobSchemaContents,
            'tags':tags,
            'createdFrom':createdFrom,
            'createdTo':createdTo,
            'limit':limit,
            'offset':offset,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost', translationJobUid=translationJobUid)
        return self.command('GET', url, kw)


    def generateJobCostEstimateReports(self, translationJobUid, contentType, tags, localeWorkflows, fuzzyProfileUid):
        '''
            method  :  POST
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost
            details :  https://api-reference.smartling.com/#operation/generateJobCostEstimateReports
        '''
        kw = {
            'contentType':contentType,
            'tags':tags,
            'localeWorkflows':localeWorkflows,
            'fuzzyProfileUid':fuzzyProfileUid,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)


    def getJobEstimateReportStatus(self, reportUid, reportStatus='', reportType=''):
        '''
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}/status
            details :  https://api-reference.smartling.com/#operation/getJobEstimateReportStatus
        '''
        kw = {
            'reportStatus':reportStatus,
            'reportType':reportType,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}/status', reportUid=reportUid)
        return self.command('GET', url, kw)


    def getJobEstimateReport(self, reportUid, reportStatus='', reportType=''):
        '''
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}
            details :  https://api-reference.smartling.com/#operation/getJobEstimateReport
        '''
        kw = {
            'reportStatus':reportStatus,
            'reportType':reportType,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}', reportUid=reportUid)
        return self.command('GET', url, kw)


    def deleteJobEstimateReport(self, reportUid):
        '''
            method  :  DELETE
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}
            details :  https://api-reference.smartling.com/#operation/deleteJobEstimateReport
        '''
        kw = {
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}', reportUid=reportUid)
        return self.command('DELETE', url, kw)


    def modifyJobEstimateReportTags(self, reportUid, tags):
        '''
            method  :  PUT
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}/tags
            details :  https://api-reference.smartling.com/#operation/modifyJobEstimateReportTags
        '''
        kw = {
            'tags':tags,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}/tags', reportUid=reportUid)
        return self.commandJson('PUT', url, kw)


    def exportJobEstimationReport(self, projectUid, reportUid, format):
        '''
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectUid}/reports/{reportUid}/download
            details :  https://api-reference.smartling.com/#operation/exportJobEstimationReport
        '''
        kw = {
            'format':format,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectUid}/reports/{reportUid}/download', projectUid=projectUid, reportUid=reportUid)
        return self.command('GET', url, kw)

