#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Copyright 2012-2025 Smartling, Inc.
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

import requests
from requests.exceptions import ConnectionError, Timeout, RequestException, HTTPError
from .Constants import ReqMethod
from .Settings import Settings
from .exceptions import SmartlingAuthError, SmartlingAPIError, SmartlingClientError, SmartlingServerError, SmartlingTimeoutError, SmartlingConnectionError
import logging

class HttpClient:
    protocol = 'https://'

    def __init__(self, host, proxySettings=None, permanentHeaders={}):
        self.host = host
        self.proxy = self.get_proxy(proxySettings)
        self.permanentHeaders = permanentHeaders
        self.base_url = f"{self.protocol}{self.host}"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": Settings.userAgent})
        self.session.headers.update(self.permanentHeaders)

    def get_proxy(self, proxySettings):
        if not proxySettings:
            return None
        
        proxy_url = "http://"
        if proxySettings.username:
            proxy_url += f'{proxySettings.username}:{proxySettings.passwd}@'
        
        proxy_url += f'{proxySettings.host}:{proxySettings.port}'
        
        return {"https": proxy_url}

    def getHttpResponseAndStatus(self, method, uri, params, files=None, extraHeaders={}, requestBody=None, context=None):
        url = f"{self.base_url}{uri}"
        headers = extraHeaders.copy()

        try:
            response = self.session.request(
                method,
                url,
                params=params,
                data=requestBody,
                files=files,
                headers=headers,
                proxies=self.proxy,
                timeout=Settings.requestTimeoutSeconds,
            )
            response.raise_for_status()
            return response.content, response.status_code, response.headers
        except Timeout as e:
            raise SmartlingTimeoutError(f"Request timed out: {e}") from e
        except ConnectionError as e:
            raise SmartlingConnectionError(f"Connection error: {e}") from e
        except HTTPError as e:
            status_code = e.response.status_code
            request_id = e.response.headers.get("X-SL-RequestId", "Unknown")
            error_message = f"Request failed with status {status_code}: {e.response.text}"
            if 400 <= status_code < 500:
                if status_code == 401:
                    raise SmartlingAuthError(error_message, status_code, request_id) from e
                raise SmartlingClientError(error_message, status_code, request_id) from e
            elif 500 <= status_code < 600:
                raise SmartlingServerError(error_message, status_code, request_id) from e
            else:
                raise SmartlingAPIError(error_message, status_code, request_id) from e
        except RequestException as e:
            logging.error(f"An unexpected request error occurred: {e}")
            raise SmartlingException(f"An unexpected request error occurred: {e}") from e
