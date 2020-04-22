#
# Python command-line: Translation Tool
# Contributed by: Bazaarvoice
# Developers: Michael Goodnow
#

import os
import sys
import argparse
import logging
import ConfigParser

# allow to import ../smartlingApiSdk/SmartlingFileApi
lib_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + os.path.pardir + os.path.sep)
sys.path.append(lib_path)

from smartlingApiSdk.SmartlingFileApi import SmartlingFileApiFactory
from smartlingApiSdk.SmartlingDirective import SmartlingDirective
from smartlingApiSdk.UploadData import UploadData
from smartlingApiSdk.Constants import ReqMethod


class SmartlingApi:
    def __init__(self, apiKey, projectId):
        self.file_api = SmartlingFileApiFactory().getSmartlingTranslationApi(apiKey, projectId)

    # Upload a source file
    def uploadFile(self, uploadData):
        self.disableStdOut()
        response, code = self.file_api.upload(uploadData)
        self.enableStdOut()
        if code == 200 and response.code == "SUCCESS":
            return response.data
        else:
            raise IOError("Failed to upload ({0}), caused by: {1}".format(code, self._getMessages(response)))

    # Import a translation
    # ApiResponse: {"response":{"data":{"wordCount":10,"translationImportErrors":[{"contentFileId":238103,"stringHashcode":"851194c88c080f24ef257383841eb757","messages":["Information about import key was not found"],"importKey":null}],"stringCount":5},"code":"SUCCESS","messages":[]}}
    def importFile(self, uploadData, locale, overwrite=False):
        self.disableStdOut()
        response, code = self.file_api.import_call(uploadData, locale, translationState="PUBLISHED", overwrite=str(overwrite).lower())
        self.enableStdOut()
        if code == 200 and response.code == "SUCCESS":
            if response.data.translationImportErrors and len(response.data.translationImportErrors) > 0:
                logging.error("Error Importing translation (%s): %s, Caused by:\n%s",
                              locale,
                              uploadData.uriPath + uploadData.name,
                              self._getStringFromArray(response.data.translationImportErrors))
                raise IOError("Failed to import translation file: {0}".format(uploadData.uriPath + uploadData.name))
            return response.data
        else:
            raise IOError("Failed to import ({0}), caused by: {1}".format(code, self._getMessages(response)))

    # Get a translated files
    def getFile(self, fileUri, locale, isPseudo=False):
        self.disableStdOut()
        if isPseudo:
            data, code = self.file_api.get(fileUri, locale, retrievalType="pseudo")
        else:
            data, code = self.file_api.get(fileUri, locale)
        self.enableStdOut()
        if code == 200:
            return data
        else:
            raise IOError("Failed to get file ({0}): {1}".format(locale, fileUri))

    # Get file status
    # ApiResponse: {"response":{"data":{"fileUri":"common.json","wordCount":9,"fileType":"json","callbackUrl":null,"lastUploaded":"2014-10-30T19:09:36","stringCount":5,"approvedStringCount":0,"completedStringCount":0},"code":"SUCCESS","messages":[]}}
    def getStatus(self, fileUri, locale):
        self.disableStdOut()
        response, code = self.file_api.status(fileUri, locale)
        self.enableStdOut()
        if code == 200 and response.code == "SUCCESS":
            return response.data
        else:
            raise IOError("Failed to get file status ({0}): {1}, caused by: {2}".format(locale, fileUri, self._getMessages(response)))

    # Get list of the project locales
    # ApiResponse: [{'locale': 'de-DE', 'translated': 'Deutsch', 'name': 'German (Germany)'}, {'locale': 'pl-PL', 'translated': 'Polski', 'name': 'Polish (Poland)'}]
    def getProjectLocales(self):
        self.disableStdOut()
        response, code = self.file_api.command(ReqMethod.GET, "/v1/project/locale/list", params={})
        self.enableStdOut()
        if code != 200 or response.code != "SUCCESS":
            raise IOError("Failed to get project locales, caused by: {0}".format(self._getMessages(response)))
        return response.data.locales

    def _getMessages(self, response):
        if response and response.messages:
            return self._getStringFromArray(response.messages)

    def _getStringFromArray(self, array):
        message = ""
        for m in array:
            if len(message) > 0:
                message += "\n"
            message += str(m)
        return message

    def disableStdOut(self):
        self._stdout = sys.stdout
        null = open(os.devnull, 'wb')
        sys.stdout = null

    def enableStdOut(self):
        if self._stdout:
            sys.stdout = self._stdout


class SmartlingTranslations:
    def __init__(self, args):
        self.args = args
        self.api = SmartlingApi(args.apiKey, args.projectId)

    #
    # Upload Source
    #
    def uploadSource(self, directives=None):
        args = self.args
        logging.info("Uploading source file(s) from: %s", args.dir)
        if not os.path.isdir(args.dir) and not os.path.isfile(args.dir):
            raise ValueError("Invalid source directory/file: {0}".format(args.dir))

        if os.path.isfile(args.dir):
            # Upload single file
            self._uploadSourceFile(os.path.dirname(args.dir), os.path.basename(args.dir), args.uriPath, directives)
        else:
            # Loop through files in directory recursively
            for root, dirs, files in os.walk(args.dir):
                for name in files:
                    if self._processFile(name):
                        relativeUri = args.uriPath + self._getRelativeUri(args.dir, root)
                        self._uploadSourceFile(root, name, relativeUri, directives)

    def _uploadSourceFile(self, path, fileName, uriPath, directives=None):
        absFile = os.path.join(path, fileName)
        logging.debug("Uploading: %s", absFile)

        if not path.endswith(os.path.sep):
            path += os.path.sep

        if self.args.run:
            uploadData = UploadData(path, fileName, self._getFileType(fileName))
            uploadData.setUri(uriPath + fileName)

            if directives:
                for directive, value in directives:
                    uploadData.addDirective(SmartlingDirective(directive, value))

            try:
                stats = self.api.uploadFile(uploadData)
                logging.info("Uploaded: %s -> %s (Word count = %s  New source = %s)",
                             absFile,
                             uriPath + fileName,
                             stats.wordCount,
                             "No" if stats.overWritten else "Yes")
            except IOError as ex:
                if "No source strings found" in str(ex):
                    logging.warn("No source strings found: %s", absFile)
                else:
                    raise ex
        else:
            logging.info("Upload (noop): %s -> %s", os.path.join(path, fileName), uriPath + fileName)

    #
    # Import Translations
    #
    def importTranslations(self, directives=None):
        args = self.args
        logging.info("Importing translation file(s) from: %s", args.dir)
        if not os.path.isdir(args.dir) and not os.path.isfile(args.dir):
            raise ValueError("Invalid translation directory/file: {0}".format(args.dir))

        if os.path.isfile(args.dir):
            # Upload single file
            self._importTranslationFile(os.path.dirname(args.dir), os.path.basename(args.dir), args.uriPath, args.locale, directives, args.overwrite)
        else:
            # Loop through files in directory recursively
            for root, dirs, files in os.walk(args.dir):
                for name in files:
                    if self._processFile(name):
                        relativeUri = args.uriPath + self._getRelativeUri(args.dir, root)
                        self._importTranslationFile(root, name, relativeUri, args.locale, directives, args.overwrite)

    def _importTranslationFile(self, path, fileName, uriPath, locale, directives=None, overwrite=False):
        smartlingLocale = self._getSmartlingLocale(locale)

        # Test if English source exists
        try:
            self.api.getStatus(uriPath + fileName, smartlingLocale)
        except IOError:
            logging.error("Failed to import translation as English source has not been uploaded: %s", uriPath + fileName)
            raise ValueError("No English source: {0}".format(uriPath + fileName))

        absFile = os.path.join(path, fileName)
        if self.args.run:
            logging.debug("Importing translation (%s): %s", smartlingLocale, absFile)
            if not path.endswith(os.path.sep):
                path += os.path.sep
            uploadData = UploadData(path, fileName, self._getFileType(fileName), uriPath)
            uploadData.uri = uriPath + fileName
            if directives:
                for directive, value in directives:
                    uploadData.addDirective(SmartlingDirective(directive, value))
            stats = self.api.importFile(uploadData, smartlingLocale, overwrite)
            logging.info("Imported translation (%s): %s -> %s (Word count = %s)",
                         smartlingLocale,
                         absFile,
                         uriPath + fileName,
                         stats.wordCount)
        else:
            logging.info("Import translation (noop): %s -> %s", absFile, uriPath + fileName)

    #
    # Download Translations
    #
    def downloadTranslations(self):
        args = self.args
        logging.info("Downloading translated file(s) for: %s", args.dir)
        if not os.path.isdir(args.dir) and not os.path.isfile(args.dir):
            raise ValueError("Invalid English source directory/file: {}".format(args.dir))

        if not os.path.isdir(args.outputDir):
            logging.debug("Creating output directory: %s", args.outputDir)
            os.makedirs(args.outputDir)

        projectLocales = self.api.getProjectLocales()

        allComplete = True
        for l in projectLocales:
            smartlingLocale = l['locale']
            if args.locale and args.locale != self._getLocaleFromSmartlingLocale(smartlingLocale):
                logging.debug("Skipping locale: %s", smartlingLocale)
                continue
            logging.info("Fetching translations%s for %s (%s)", "" if args.run else " (noop)", l['name'], smartlingLocale)
            if os.path.isfile(args.dir):
                # Get single file
                if not self._getTranslationsFile(args.outputDir, "", args.uriPath, os.path.basename(args.dir), smartlingLocale):
                    allComplete = False
            else:
                # Loop through files in directory recursively and get their translations from the server respectfully
                for root, dirs, files in os.walk(args.dir):
                    for name in files:
                        if self._processFile(name):
                            relativePath = self._getRelativePath(args.dir, root)
                            try:
                                if not self._getTranslationsFile(args.outputDir, relativePath, args.uriPath, name, smartlingLocale):
                                    allComplete = False
                            except IOError:
                                logging.warning("File hasn't been uploaded yet: " + args.uriPath + relativePath.replace('\\', '/') + name)
                                allComplete = False

        if allComplete:
            logging.info("Successfully - all source files translated!")
        else:
            logging.warn("Not all source files are translated!")

    def _getTranslationsFile(self, outputDir, relativePath, uriPath, fileName, smartlingLocale):
        args = self.args
        sourceFile = uriPath + relativePath.replace('\\', '/') + fileName
        outputFile = outputDir + os.path.sep + self._getLocaleFromSmartlingLocale(smartlingLocale) + os.path.sep + relativePath + fileName

        status = self.api.getStatus(sourceFile, smartlingLocale)
        percentComplete = self._getPercent(status.completedStringCount, status.stringCount)

        if percentComplete < 100 and not self.args.allowPartial:
            logging.info("Translated %s%% (%s): %s -> %s (skipping)", percentComplete, smartlingLocale, sourceFile, outputFile)
            return False

        logging.info("Translated %s%% (%s): %s -> %s", percentComplete, smartlingLocale, sourceFile, outputFile)
        if args.run:
            fileData = self.api.getFile(sourceFile, smartlingLocale, args.pseudo)
            if not os.path.isdir(os.path.dirname(outputFile)):
                os.makedirs(os.path.dirname(outputFile))
            f = open(outputFile, 'w')
            f.write(fileData)

        return percentComplete == 100

    # Get percentage
    def _getPercent(self, count, totalCount):
        if count == 0 and totalCount == 0:
            return 100
        if totalCount > 0:
            return int ((count / float(totalCount)) * 100)
        return 0

    # Get Smartling locale from locale
    def _getSmartlingLocale(self, locale):
        if hasattr(self.args, 'localeMap'):
            if self.args.localeMap[locale]:
                return self.args.localeMap[locale]
        return locale

    # Get locale from a Smartling locale
    def _getLocaleFromSmartlingLocale(self, smartlingLocale):
        if hasattr(self.args, 'localeMap'):
            for locale, slLocale in self.args.localeMap.iteritems():
                if slLocale == smartlingLocale:
                    return locale
        return smartlingLocale

    # Get relative path
    # rootDir = /root/path
    # fileDir = /root/path/subdir/path/file
    # returns subdir/path/file
    def _getRelativePath(self, rootDir, filePath):
        relativePath = filePath.replace(rootDir, "", 1)
        if relativePath.startswith(os.path.sep):
            relativePath = relativePath[1:]
        if len(relativePath) > 0 and not relativePath.endswith(os.path.sep):
            relativePath += os.path.sep
        return relativePath

    def _getRelativeUri(self, rootDir, filePath):
        return self._getRelativePath(rootDir, filePath).replace('\\', '/')

    # Determine if file should be processed based on file filters applied in configuration
    # returns boolean
    def _processFile(self, name):
        if not hasattr(self.args, 'filterFileExtensions'):
            return True
        extension = os.path.splitext(name)[1][1:]
        return extension in self.args.filterFileExtensions

    # Determine Smartling file type
    def _getFileType(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        if hasattr(self.args, 'extensionMap'):
            for key, value in self.args.extensionMap.iteritems():
                if extension in value.split(","):
                    return key
        return extension


def uploadSource(args, directives=None):
    tool = SmartlingTranslations(args)
    tool.uploadSource(directives)


def downloadTranslations(args):
    tool = SmartlingTranslations(args)
    tool.downloadTranslations()


def importTranslations(args, directives=None):
    tool = SmartlingTranslations(args)
    tool.importTranslations(directives)


def main():
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

    parser = argparse.ArgumentParser(description="Smartling Translation Tool to upload, download, and import translation files")
    parser.add_argument("-k", "--apiKey", dest="apiKey", help="Smartling API key (overrides configuration file value)")
    parser.add_argument("-p", "--projectId", dest="projectId",
                        help="Smartling project ID (overrides configuration file value)")
    parser.add_argument("-c", "--config", dest="configFile", default="translation.cfg", help="Configuration file (default ./translation.cfg)")

    subparsers = parser.add_subparsers(dest="sub_parser", help="To see individual sub command help: 'subcommand -h'")

    parser_upload = subparsers.add_parser("upload", help="Upload the (English) source")
    parser_upload.add_argument("-d", "--dir", dest="dir", required=True, help="Path to English source directory or file")
    parser_upload.add_argument("-u", "--uriPath", dest="uriPath", help="File URI path used in Smartling system")
    parser_upload.add_argument("--run", dest="run", action="store_true", help="Run for real (default is noop)")

    parser_download = subparsers.add_parser("download", help="Download the translations")
    parser_download.add_argument("-d", "--dir", dest="dir", required=True, help="Path to English source directory of file")
    parser_download.add_argument("-o", "--outputDir", dest="outputDir", required=True,
                            help="Output directory where to save translated files. Stores each translation in their own sub-directory.")
    parser_download.add_argument("-u", "--uriPath", dest="uriPath", help="File URI path used in Smartling system")
    parser_download.add_argument("-l", "--locale", dest="locale", help="Locale to download (default is all)")
    parser_download.add_argument("-p", "--allowPartial", dest="allowPartial", action="store_true", help="Allow translation not 100%% complete (default is false)")
    parser_download.add_argument("-s", "--pseudo", dest="pseudo", action="store_true", help="Download pseudo translations")
    parser_download.add_argument("--run", dest="run", action="store_true", help="Run for real (default is noop)")

    parser_import = subparsers.add_parser("import", help="Import translations")
    parser_import.add_argument("-d", "--dir", dest="dir", required=True, help="Path to translations directory or file")
    parser_import.add_argument("-u", "--uriPath", dest="uriPath", help="File URI path used in Smartling system")
    parser_import.add_argument("-l", "--locale", dest="locale", required=True, help="Locale to import")
    parser_import.add_argument("-o", "--overwrite", dest="overwrite", action="store_true", help="Overwrite previous translations")
    parser_import.add_argument("--run", dest="run", action="store_true", help="Run for real (default is noop)")

    args = parser.parse_args()

    config = ConfigParser.ConfigParser()
    # Allow case sensitive configuration keys
    config.optionxform = str
    config.read(args.configFile)

    if not args.uriPath and config.has_section("smartling"):
        args.uriPath = config.get("smartling", "uriPath")

    # Default uriPath
    if not args.uriPath:
        args.uriPath = "/files"

    # Fix URI path to include trailing slash (expected)
    if not args.uriPath.endswith('/'):
        args.uriPath += "/"

    # Get API Key
    if not args.apiKey and config.has_section("smartling"):
        args.apiKey = config.get("smartling", "apiKey")

    # Get Project ID
    if not args.projectId and config.has_section("smartling"):
        args.projectId = config.get("smartling", "projectId")
    if not args.apiKey or not args.projectId:
        raise ValueError("Smartling API Key and Project ID are required")

    # Get Locales
    if config.has_section("locales"):
        locales = {}
        for name, value in config.items("locales"):
            locales[name] = value
        args.localeMap = locales

    if config.has_section("extensions"):
        extensions = {}
        for name, value in config.items("extensions"):
            extensions[name] = value
        args.extensionMap = extensions

    # Get file extension filters
    if config.has_section("filters") and config.has_option("filters", "file_extensions"):
        fileExtensions = config.get("filters", "file_extensions")
        if fileExtensions and len(fileExtensions) > 0:
            fileExtensionArray = fileExtensions.split(",")
            if len(fileExtensionArray) > 0:
                args.filterFileExtensions = fileExtensionArray


    # Upload Command
    if args.sub_parser == "upload":
        directives = None
        if config.has_section("directives"):
            directives = config.items("directives")
        uploadSource(args, directives)

    # Get Command
    if args.sub_parser == "download":
        # Pseudo argument
        if args.pseudo:
            args.allowPartial = True
        downloadTranslations(args)

    # Import Command
    if args.sub_parser == "import":
        directives = None
        if config.has_section("directives"):
            directives = config.items("directives")
        importTranslations(args, directives)


main()

