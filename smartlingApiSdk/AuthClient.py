#!/usr/bin/python
# -*- coding: utf-8 -*-




from .HttpClient import HttpClient
from .ApiResponse import ApiResponse
from .Constants import ReqMethod
import logging
import time


class AuthClient:
    authUri = "/auth-api/v2/authenticate"
    refreshUri = "/auth-api/v2/authenticate/refresh"
    timeJitter = 5  # Seconds off server expiration time

    def __init__(self, host, userIdentifier, userSecret, proxySettings=None):
        self.httpClient = HttpClient(host, proxySettings)
        self.userIdentifier = userIdentifier
        self.userSecret = userSecret
        self.accessExpiresAt = 0
        self.refreshExpiresAt = 0

    def request(self, uri, body):
        header = {"Content-Type": "application/json"}
        body = body.encode()
        response_data, status_code, headers = self.httpClient.getHttpResponseAndStatus(
            ReqMethod.POST, uri, params={}, extraHeaders=header, requestBody=body)
        apiResponse = ApiResponse(response_data, status_code, headers)

        now = time.time()
        try:
            self.accessToken = apiResponse.data.accessToken
            self.refreshToken = apiResponse.data.refreshToken
            self.accessExpiresAt = now + apiResponse.data.expiresIn - self.timeJitter
            self.refreshExpiresAt = now + apiResponse.data.refreshExpiresIn - self.timeJitter
        except Exception as e:
            logging.error(e)
            self.accessToken = None

    def authenticate(self):
        body = '{"userIdentifier": "%s", "userSecret": "%s"}' % (self.userIdentifier, self.userSecret)
        if '@smartling.com' in self.userIdentifier:
            self.request(self.authUri + '/user', body)
        else:
            self.request(self.authUri, body)

    def refresh(self):
        body = '{"refreshToken":"%s"}' % self.refreshToken
        self.request(self.refreshUri, body)

    def getToken(self):
        if not getattr(self, 'accessToken', None):
            self.authenticate()
            return self.accessToken

        now = time.time()
        if now >= self.accessExpiresAt:
            if now < self.refreshExpiresAt:
                self.refresh()
            else:
                self.authenticate()
        return self.accessToken
