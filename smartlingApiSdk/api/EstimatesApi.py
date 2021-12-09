
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


from smartlingApiSdk.ApiV2 import ApiV2

class EstimatesApi(ApiV2):

    def __init__(self, userIdentifier, userSecret, projectId, proxySettings=None, permanentHeaders={}, env='prod'):
        ApiV2.__init__(self, userIdentifier, userSecret, projectId, proxySettings, permanentHeaders=permanentHeaders, env=env)

    def getJobFuzzyEstimateReports(self, translationJobUid, reportStatus='', contentCoverage='', creatorUserUids=[], translationJobSchemaContents=[], tags=[], createdFrom='', createdTo='', limit=0, offset=0, **kwargs):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobFuzzyEstimateReports
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def generateJobFuzzyEstimateReports(self, translationJobUid, contentType='', tags=[], **kwargs):
        """
            method  :  POST
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/generateJobFuzzyEstimateReports
        """
        kw = {
            'contentType':contentType,
            'tags':tags,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/fuzzy', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getJobCostEstimateReports(self, translationJobUid, reportStatus='', contentCoverage='', creatorUserUids=[], translationJobSchemaContents=[], tags=[], createdFrom='', createdTo='', limit=0, offset=0, **kwargs):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobCostEstimateReports
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
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost', translationJobUid=translationJobUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def generateJobCostEstimateReports(self, translationJobUid, contentType='', tags=[], localeWorkflows=[], fuzzyProfileUid='', **kwargs):
        """
            method  :  POST
            api url :  /estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/generateJobCostEstimateReports
        """
        kw = {
            'contentType':contentType,
            'tags':tags,
            'localeWorkflows':localeWorkflows,
            'fuzzyProfileUid':fuzzyProfileUid,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/jobs/{translationJobUid}/reports/cost', translationJobUid=translationJobUid, **kwargs)
        response, status = self.commandJson('POST', url, kw)
        return response, status


    def getJobEstimateReportStatus(self, reportUid, reportStatus='', reportType='', **kwargs):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}/status
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobEstimateReportStatus
        """
        kw = {
            'reportStatus':reportStatus,
            'reportType':reportType,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}/status', reportUid=reportUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def getJobEstimateReport(self, reportUid, reportStatus='', reportType='', **kwargs):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/getJobEstimateReport
        """
        kw = {
            'reportStatus':reportStatus,
            'reportType':reportType,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}', reportUid=reportUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status


    def deleteJobEstimateReport(self, reportUid, **kwargs):
        """
            method  :  DELETE
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/deleteJobEstimateReport
        """
        kw = {
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}', reportUid=reportUid, **kwargs)
        response, status = self.command('DELETE', url, kw)
        return response, status


    def modifyJobEstimateReportTags(self, reportUid, tags=[], **kwargs):
        """
            method  :  PUT
            api url :  /estimates-api/v2/projects/{projectId}/reports/{reportUid}/tags
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/modifyJobEstimateReportTags
        """
        kw = {
            'tags':tags,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectId}/reports/{reportUid}/tags', reportUid=reportUid, **kwargs)
        response, status = self.commandJson('PUT', url, kw)
        return response, status


    def exportJobEstimationReport(self, projectUid, reportUid, format, **kwargs):
        """
            method  :  GET
            api url :  /estimates-api/v2/projects/{projectUid}/reports/{reportUid}/download
            Responses:
                200 : OK
            details :  https://api-reference.smartling.com/#operation/exportJobEstimationReport
        """
        kw = {
            'format':format,
        }
        kw.update(kwargs)
        url = self.urlHelper.getUrl('/estimates-api/v2/projects/{projectUid}/reports/{reportUid}/download', projectUid=projectUid, reportUid=reportUid, **kwargs)
        response, status = self.command('GET', url, kw)
        return response, status

