from smartlingApiSdk.UrlV2Helper import UrlV2Helper
from smartlingApiSdk.ApiV2 import ApiV2

class EstimatesApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, proxySettings, permanentHeaders=permanentHeaders, env=env)
        self.urlHelper = UrlV2Helper(projectId)

    def getJobFuzzyEstimateReports(self, translationJobUid, reportStatus='', contentCoverage='', creatorUserUids=[], translationJobSchemaContents=[], tags=[], createdFrom='', createdTo='', limit=0, offset=0):
        """
            get
            /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy
            for details check: https://api-reference.smartling.com/#operation/getJobFuzzyEstimateReports

            ------------------------------------------------------------------------------------------------------------------------
        """
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
        """
            post
            /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy
            for details check: https://api-reference.smartling.com/#operation/generateJobFuzzyEstimateReports

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'contentType':contentType,
            'tags':tags,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)




    def getJobCostEstimateReports(self, translationJobUid, reportStatus='', contentCoverage='', creatorUserUids=[], translationJobSchemaContents=[], tags=[], createdFrom='', createdTo='', limit=0, offset=0):
        """
            get
            /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost
            for details check: https://api-reference.smartling.com/#operation/getJobCostEstimateReports

            ------------------------------------------------------------------------------------------------------------------------
        """
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
        """
            post
            /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost
            for details check: https://api-reference.smartling.com/#operation/generateJobCostEstimateReports

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'contentType':contentType,
            'tags':tags,
            'localeWorkflows':localeWorkflows,
            'fuzzyProfileUid':fuzzyProfileUid,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost', translationJobUid=translationJobUid)
        return self.commandJson('POST', url, kw)




    def getJobEstimateReportStatus(self, reportUid, reportStatus='', reportType=''):
        """
            get
            /estimates-api/v2/projects/{projectId}/reports/{reportUid}/status
            for details check: https://api-reference.smartling.com/#operation/getJobEstimateReportStatus

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'reportStatus':reportStatus,
            'reportType':reportType,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}/status', reportUid=reportUid)
        return self.command('GET', url, kw)




    def getJobEstimateReport(self, reportUid, reportStatus='', reportType=''):
        """
            get
            /estimates-api/v2/projects/{projectId}/reports/{reportUid}
            for details check: https://api-reference.smartling.com/#operation/getJobEstimateReport

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'reportStatus':reportStatus,
            'reportType':reportType,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}', reportUid=reportUid)
        return self.command('GET', url, kw)




    def deleteJobEstimateReport(self, reportUid):
        """
            delete
            /estimates-api/v2/projects/{projectId}/reports/{reportUid}
            for details check: https://api-reference.smartling.com/#operation/deleteJobEstimateReport

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}', reportUid=reportUid)
        return self.command('DELETE', url, kw)




    def modifyJobEstimateReportTags(self, reportUid, tags):
        """
            put
            /estimates-api/v2/projects/{projectId}/reports/{reportUid}/tags
            for details check: https://api-reference.smartling.com/#operation/modifyJobEstimateReportTags

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'tags':tags,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}/tags', reportUid=reportUid)
        return self.commandJson('PUT', url, kw)




    def exportJobEstimationReport(self, projectUid, reportUid, format):
        """
            get
            /estimates-api/v2/projects/{projectUid}/reports/{reportUid}/download
            for details check: https://api-reference.smartling.com/#operation/exportJobEstimationReport

            ------------------------------------------------------------------------------------------------------------------------
        """
        kw = {
            'format':format,
        }
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectUid}/reports/{reportUid}/download', projectUid=projectUid, reportUid=reportUid)
        return self.command('GET', url, kw)



