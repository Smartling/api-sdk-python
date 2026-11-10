#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Internal long-running auth check against stg - NOT part of the automated test suite.

Repeats the functional test suites with ONE shared AuthClient for longer than the access
token TTL (480s on stg), so token refresh happens for real in the middle of API traffic.

Usage (from repo root, stg credentials exported, see set_env.sh):
    SL_LONGRUN_MINUTES=17 python3 internal/longrun_auth_stg.py

Asserts: every suite pass is green, at least one refresh happened, exactly one authenticate
(stg refresh is not session-capped), no failed auth request. Files uploaded during the run
are deleted at the end. Per-pass output goes to $SL_LONGRUN_OUT (default /tmp/sdk-longrun-<ts>).
"""

import contextlib
import datetime
import importlib
import os
import sys
import time
import traceback

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEST_DIR = os.path.join(ROOT, 'test')
sys.path[:0] = [ROOT, TEST_DIR]

import smartlingApiSdk.ApiV2 as apiV2Module
from smartlingApiSdk.ApiV2 import ApiV2
from smartlingApiSdk.AuthClient import AuthClient
from smartlingApiSdk.Credentials import Credentials
from smartlingApiSdk.api.FilesApi import FilesApi

SUITES = [  # (module, class); Jobs and Estimates are forced to stg below
    ('testAccountProjects', 'testAccountProjectsApi'),
    ('testContext', 'testContextApi'),
    ('testFiles', 'testFilesApi'),
    ('testStrings', 'testStringsApi'),
    ('testTags', 'testTagsApi'),
    ('testJobBatchesV2', 'testJobBatchesV2Api'),
    ('testJobs', 'testJobsApi'),
    ('testEstimates', 'testEstimatesApi'),
]
TEST_FILE_PREFIXES = ('java.properties', 'javaUTF16.properties', 'test.csv', 'test_import.xml', '_')
KEEP_FILES = ('test_import.xml_2.2.4_1629202583.584802',)  # hardcoded in testJobs


def utcIso(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')


class AuthLog:
    """ single AuthClient shared by every Api instance, records each auth request """
    def __init__(self):
        self.client = None
        self.events = []  # (time, kind, ok, expiresIn, refreshExpiresIn)

    def factory(self, host, userIdentifier, userSecret, proxySettings=None, ignore_errors=False):
        if self.client is None:
            self.client = AuthClient(host, userIdentifier, userSecret, proxySettings, ignore_errors=ignore_errors)
            originalRequest = self.client.request

            def request(uri, body):
                originalRequest(uri, body)
                c = self.client
                kind = 'refresh' if uri.endswith('/refresh') else 'authenticate'
                expiresIn = round(c.accessExpiresAt - time.time() + c.timeJitter) if c.accessToken else None
                self.events.append((time.time(), kind, bool(c.accessToken), expiresIn, c.refreshExpiresIn))
                print('[auth] %s %-12s ok=%s expiresIn=%s refreshExpiresIn=%s' % (
                    utcIso(time.time()), kind, bool(c.accessToken), expiresIn, c.refreshExpiresIn), file=sys.__stdout__)
            self.client.request = request
        return self.client

    def count(self, kind):
        return len([e for e in self.events if e[1] == kind])


def patchForStg(authLog):
    apiV2Module.AuthClient = authLog.factory

    originalApiInit = ApiV2.__init__
    def apiInit(self, *args, **kwargs):
        kwargs['env'] = 'stg'
        originalApiInit(self, *args, **kwargs)
    ApiV2.__init__ = apiInit

    originalCredentialsInit = Credentials.__init__
    def credentialsInit(self, env='stg'):
        originalCredentialsInit(self, 'stg')
    Credentials.__init__ = credentialsInit


def runSuite(moduleName, className, logFile):
    suite = getattr(importlib.import_module(moduleName), className)()
    with open(logFile, 'a') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        print('===== %s %s' % (utcIso(time.time()), moduleName))
        try:
            suite.setUp()
            try:
                suite.test_all()
            finally:
                suite.tearDown()
            return True
        except Exception:
            traceback.print_exc()
            return False


def cleanupFiles(startedAt):
    credentials = Credentials()
    api = FilesApi(credentials.MY_USER_IDENTIFIER, credentials.MY_USER_SECRET, credentials.MY_PROJECT_ID)
    items, offset = [], 0
    while True:
        res, status = api.getRecentlyUploadedSourceFilesList(limit=100, offset=offset)
        items += res.data.items
        if len(res.data.items) < 100:
            break
        offset += 100
    since = utcIso(startedAt - 60)
    stale = [i['fileUri'] for i in items if i['lastUploaded'] >= since and i['fileUri'] not in KEEP_FILES
             and i['fileUri'].startswith(TEST_FILE_PREFIXES)]
    deleted = len([u for u in stale if api.deleteUploadedSourceFile(u)[1] == 200])
    return deleted, len(stale)


def main():
    minutes = float(os.environ.get('SL_LONGRUN_MINUTES', '17'))
    startedAt = time.time()
    outDir = os.environ.get('SL_LONGRUN_OUT', '/tmp/sdk-longrun-%d' % startedAt)
    os.makedirs(outDir, exist_ok=True)
    os.chdir(TEST_DIR)  # suites resolve some paths relative to test/

    authLog = AuthLog()
    patchForStg(authLog)

    results = []  # (pass, suite, ok)
    passNo = 0
    print('long run: %.1f min, output in %s' % (minutes, outDir))
    while time.time() - startedAt < minutes * 60:
        passNo += 1
        logFile = os.path.join(outDir, 'pass_%02d.log' % passNo)
        for moduleName, className in SUITES:
            ok = runSuite(moduleName, className, logFile)
            results.append((passNo, moduleName, ok))
            print('%s pass %d %-20s %s' % (utcIso(time.time()), passNo, moduleName, 'OK' if ok else 'FAILED -> ' + logFile))

    elapsed = time.time() - startedAt
    deleted, stale = cleanupFiles(startedAt)
    failures = [r for r in results if not r[2]]
    accessTtl = authLog.events[0][3] if authLog.events else None

    print('\n===== summary')
    print('elapsed: %.0fs, passes: %d, suite runs: %d, failed: %d' % (elapsed, passNo, len(results), len(failures)))
    print('access TTL: %ss, authenticate: %d, refresh: %d, failed auth requests: %d' % (
        accessTtl, authLog.count('authenticate'), authLog.count('refresh'), len([e for e in authLog.events if not e[2]])))
    print('cleanup: deleted %d of %d files uploaded during the run' % (deleted, stale))

    checks = [
        ('all suite runs green', not failures),
        ('ran longer than access TTL', accessTtl is not None and elapsed > accessTtl),
        ('at least one refresh', authLog.count('refresh') >= 1),
        ('exactly one authenticate', authLog.count('authenticate') == 1),
        ('no failed auth request', all(e[2] for e in authLog.events)),
    ]
    for name, ok in checks:
        print('%-28s %s' % (name, 'OK' if ok else 'FAILED'))
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == '__main__':
    sys.exit(main())
