Smartling Python Translation Tool
=======

Command line tool to upload, download, and import translation to Smartling 

Usage
----------

```bash
$ python smartlingTool.py -h
usage: smartlingTool.py [-h] [-k APIKEY] [-p PROJECTID]
                        [-c CONFIGFILE]
                        {upload,download,import} ...

Smartling Translation Tool to upload, download, and import translation files

positional arguments:
  {upload,download,import}   To see individual sub command help: 'subcommand -h'
    upload              Upload the (English) source
    download            Download the translations
    import              Import translations

optional arguments:
  -h, --help            show this help message and exit
  -k APIKEY, --apiKey APIKEY
                        Smartling API key (overrides configuration file value)
  -p PROJECTID, --projectId PROJECTID
                        Smartling project ID (overrides configuration file
                        value)
  -c CONFIGFILE, --config CONFIGFILE
                        Configuration file (default ./translation.cfg)
```

### Upload

```bash
$ python smartlingTool.py upload -h
usage: smartlingTool.py upload [-h] -d DIR [-u URIPATH] [--run]

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Path to English source directory or file
  -u URIPATH, --uriPath URIPATH
                        File URI path used in Smartling system
  --run                 Run for real (default is noop)
```

### Download

Any translation that is not 100% complete will be skipped.
Translation which are not 100% and are download will include English in their place.

```bash
$ python smartlingTool.py download -h
usage: smartlingTool.py download [-h] -d DIR -o OUTPUTDIR [-u URIPATH]
                                 [-l LOCALE] [-p] [-s] [--run]

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Path to English source directory of file
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        Output directory where to save translated files.
                        Stores each translation in their own sub-directory.
  -u URIPATH, --uriPath URIPATH
                        File URI path used in Smartling system
  -l LOCALE, --locale LOCALE
                        Locale to download (default is all)
  -p, --allowPartial    Allow translation not 100% complete (default is false)
  -s, --pseudo          Download pseudo translations
  --run                 Run for real (default is noop)
```

### Import

```bash
$ python smartlingTool.py import -h
usage: smartlingTool.py import [-h] -d DIR [-u URIPATH] -l LOCALE
                               [-o] [--run]

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Path to translations directory or file
  -u URIPATH, --uriPath URIPATH
                        File URI path used in Smartling system
  -l LOCALE, --locale LOCALE
                        Locale to import
  -o, --overwrite       Overwrite previous translations
  --run                 Run for real (default is noop)
```

Configuration File
----------

Default location for configuration file: `translation.cfg`

```
[smartling]
# Project API Key
apiKey = XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX

# Project ID
projectId = XXXXXXXX

# Custom URI path (default "/files")
uriPath = /files/config-ui

[directives]
# Smartling directives
# See: https://docs.smartling.com/display/docs/Supported+File+Types
translate_mode = all
source_key_paths = {*}
placeholder_format_custom = __\w+__|\{{2,2}[\w\.]+\}{2,2}
variants_enabled = true

[locales]
# Locale Mapping - Use to map differences between project and Smartling locale codes
en = en-US
de = de-DE
es = es-ES
fr = fr-FR
ja = ja-JP
pt = pt-PT
pt_BR = pt-BR


[filters]
# Common delimited list of file extensions (default all files)
file_extensions =


[extensions]
# Extension Mapping - Use to map differences between file types and Smartling file types

# Gettext .pot and .po files
gettext = pot,po

# HTML files
html = html,htm

# Java Properties
javaProperties = properties

# Yaml files
yaml = yml

# Supports .xlf, .xliff, and .xml files that use the XML Localization Interchange File Format (XLIFF)
xliff = xlf,xliff

# Javascript files
json = json,js

# Qt Linguist TS format files
qt = ts

# MadCap Flare ZIP packages
madcap = zip
```

Examples
----------

### Upload

```bash
$ python smartlingTool.py upload --dir /workspace/config-ui/static/locales/en
2014-11-03 10:44:06,208 - INFO - Uploading source files from: /workspace/config-ui/static/locales/en
2014-11-03 10:44:06,209 - INFO - Upload (noop): /workspace/config-ui/static/locales/en/badges.json -> /files/config-ui/badges.json
2014-11-03 10:44:06,209 - INFO - Upload (noop): /workspace/config-ui/static/locales/en/common.json -> /files/config-ui/common.json
2014-11-03 10:44:06,209 - INFO - Upload (noop): /workspace/config-ui/static/locales/en/container.json -> /files/config-ui/container.json
2014-11-03 10:44:06,209 - INFO - Upload (noop): /workspace/config-ui/static/locales/en/editCopy.json -> /files/config-ui/editCopy.json
2014-11-03 10:44:06,209 - INFO - Upload (noop): /workspace/config-ui/static/locales/en/preview.json -> /files/config-ui/preview.json
2014-11-03 10:44:06,209 - INFO - Upload (noop): /workspace/config-ui/static/locales/en/submission.json -> /files/config-ui/submission.json
```

### Download

```bash
python smartlingTool.py download --dir /workspace/config-ui/static/locales/en --outputDir /workspace/config-ui/static/locales
2014-11-03 10:44:28,670 - INFO - Downloading translated files for: /workspace/config-ui/static/locales/en
2014-11-03 10:44:29,576 - INFO - Fetching translations (noop) for French (France) (fr-FR)
2014-11-03 10:44:30,172 - INFO - Translated 100% (fr-FR): /files/config-ui/badges.json -> /workspace/config-ui/static/locales/fr/badges.json
2014-11-03 10:44:30,734 - INFO - Translated 100% (fr-FR): /files/config-ui/common.json -> /workspace/config-ui/static/locales/fr/common.json
2014-11-03 10:44:31,228 - INFO - Translated 100% (fr-FR): /files/config-ui/container.json -> /workspace/config-ui/static/locales/fr/container.json
2014-11-03 10:44:32,506 - INFO - Translated 100% (fr-FR): /files/config-ui/editCopy.json -> /workspace/config-ui/static/locales/fr/editCopy.json
2014-11-03 10:44:32,965 - INFO - Translated 100% (fr-FR): /files/config-ui/preview.json -> /workspace/config-ui/static/locales/fr/preview.json
2014-11-03 10:44:33,774 - INFO - Translated 100% (fr-FR): /files/config-ui/submission.json -> /workspace/config-ui/static/locales/fr/submission.json
2014-11-03 10:44:33,774 - INFO - Fetching translations (noop) for German (Germany) (de-DE)
2014-11-03 10:44:34,455 - INFO - Translated 100% (de-DE): /files/config-ui/badges.json -> /workspace/config-ui/static/locales/de/badges.json
2014-11-03 10:44:34,993 - INFO - Translated 100% (de-DE): /files/config-ui/common.json -> /workspace/config-ui/static/locales/de/common.json
2014-11-03 10:44:35,563 - INFO - Translated 100% (de-DE): /files/config-ui/container.json -> /workspace/config-ui/static/locales/de/container.json
2014-11-03 10:44:36,065 - INFO - Translated 100% (de-DE): /files/config-ui/editCopy.json -> /workspace/config-ui/static/locales/de/editCopy.json
2014-11-03 10:44:36,488 - INFO - Translated 100% (de-DE): /files/config-ui/preview.json -> /workspace/config-ui/static/locales/de/preview.json
2014-11-03 10:44:37,085 - INFO - Translated 100% (de-DE): /files/config-ui/submission.json -> /workspace/config-ui/static/locales/de/submission.json
2014-11-03 10:44:37,085 - INFO - Fetching translations (noop) for Japanese (ja-JP)
2014-11-03 10:44:37,564 - INFO - Translated 100% (ja-JP): /files/config-ui/badges.json -> /workspace/config-ui/static/locales/ja/badges.json
2014-11-03 10:44:38,124 - INFO - Translated 100% (ja-JP): /files/config-ui/common.json -> /workspace/config-ui/static/locales/ja/common.json
2014-11-03 10:44:38,670 - INFO - Translated 100% (ja-JP): /files/config-ui/container.json -> /workspace/config-ui/static/locales/ja/container.json
2014-11-03 10:44:39,150 - INFO - Translated 100% (ja-JP): /files/config-ui/editCopy.json -> /workspace/config-ui/static/locales/ja/editCopy.json
2014-11-03 10:44:39,666 - INFO - Translated 100% (ja-JP): /files/config-ui/preview.json -> /workspace/config-ui/static/locales/ja/preview.json
2014-11-03 10:44:40,164 - INFO - Translated 100% (ja-JP): /files/config-ui/submission.json -> /workspace/config-ui/static/locales/ja/submission.json
2014-11-03 10:44:40,164 - INFO - Fetching translations (noop) for Portuguese (Portugal) (pt-PT)
2014-11-03 10:44:40,614 - INFO - Translated 100% (pt-PT): /files/config-ui/badges.json -> /workspace/config-ui/static/locales/pt/badges.json
2014-11-03 10:44:41,375 - INFO - Translated 100% (pt-PT): /files/config-ui/common.json -> /workspace/config-ui/static/locales/pt/common.json
2014-11-03 10:44:41,774 - INFO - Translated 100% (pt-PT): /files/config-ui/container.json -> /workspace/config-ui/static/locales/pt/container.json
2014-11-03 10:44:42,218 - INFO - Translated 100% (pt-PT): /files/config-ui/editCopy.json -> /workspace/config-ui/static/locales/pt/editCopy.json
2014-11-03 10:44:42,731 - INFO - Translated 100% (pt-PT): /files/config-ui/preview.json -> /workspace/config-ui/static/locales/pt/preview.json
2014-11-03 10:44:43,180 - INFO - Translated 100% (pt-PT): /files/config-ui/submission.json -> /workspace/config-ui/static/locales/pt/submission.json
2014-11-03 10:44:43,180 - INFO - Fetching translations (noop) for Spanish (Spain) (es-ES)
2014-11-03 10:44:43,864 - INFO - Translated 100% (es-ES): /files/config-ui/badges.json -> /workspace/config-ui/static/locales/es/badges.json
2014-11-03 10:44:44,288 - INFO - Translated 100% (es-ES): /files/config-ui/common.json -> /workspace/config-ui/static/locales/es/common.json
2014-11-03 10:44:44,739 - INFO - Translated 100% (es-ES): /files/config-ui/container.json -> /workspace/config-ui/static/locales/es/container.json
2014-11-03 10:44:45,142 - INFO - Translated 100% (es-ES): /files/config-ui/editCopy.json -> /workspace/config-ui/static/locales/es/editCopy.json
2014-11-03 10:44:45,528 - INFO - Translated 100% (es-ES): /files/config-ui/preview.json -> /workspace/config-ui/static/locales/es/preview.json
2014-11-03 10:44:45,968 - INFO - Translated 100% (es-ES): /files/config-ui/submission.json -> /workspace/config-ui/static/locales/es/submission.json
2014-11-03 10:44:45,968 - INFO - Successfully - all source files translated!
```

### Import Directory

```bash
$ python smartlingTool.py import --dir /workspace/config-ui/static/locales/fr --locale fr
2014-11-03 10:46:39,653 - INFO - Importing translation file(s) from: /workspace/config-ui/static/locales/fr
2014-11-03 10:46:40,624 - INFO - Import translation (noop): /workspace/config-ui/static/locales/fr/badges.json -> /files/config-ui/badges.json
2014-11-03 10:46:41,091 - INFO - Import translation (noop): /workspace/config-ui/static/locales/fr/common.json -> /files/config-ui/common.json
2014-11-03 10:46:41,480 - INFO - Import translation (noop): /workspace/config-ui/static/locales/fr/container.json -> /files/config-ui/container.json
2014-11-03 10:46:41,951 - INFO - Import translation (noop): /workspace/config-ui/static/locales/fr/editCopy.json -> /files/config-ui/editCopy.json
2014-11-03 10:46:42,433 - INFO - Import translation (noop): /workspace/config-ui/static/locales/fr/preview.json -> /files/config-ui/preview.json
2014-11-03 10:46:42,927 - INFO - Import translation (noop): /workspace/config-ui/static/locales/fr/submission.json -> /files/config-ui/submission.json
```

### Import File (with overwrite)

```bash
$ python smartlingTool.py import --dir /workspace/config-ui/static/locales/fr/badges.json --locale fr --overwrite
2014-11-03 10:47:22,401 - INFO - Importing translation file(s) from: /workspace/config-ui/static/locales/fr/badges.json
2014-11-03 10:47:22,910 - INFO - Import translation (noop): /workspace/config-ui/static/locales/fr/badges.json -> /files/config-ui/badges.json
```

