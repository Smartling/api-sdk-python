#!/usr/bin/python
# -*- coding: utf-8 -*-





class ProxySettings:
    """ settings for http proxy to be used to pass api requests, !!! Only basic authentication is supported for restricted proxy access !!! """
    def __init__(self, username, passwd, host, port):
        self.username = username
        self.passwd = passwd
        self.host = host
        self.port = port