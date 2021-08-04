import json

class Parameter():
    def __init__(self, param_dict):
        param_names = ['name', 'description', 'in', 'required', 'schema']
        self.processParams(param_names, param_dict)
        self._type = "string"
        if self._schema:
            self._type = self._schema['type']
й            self._default = self._schema.get('default', None)

    def processParams(self, param_names, param_dict):

        for name in param_names:
            n = param_dict.get(name, None)
            if 'name' == name:
                #import pdb; pdb.set_trace()
                n = n.replace('[]', '')
            setattr(self, '_' + name, n)

    def getParamForName(self):
        if self._required:
            return self._name
        else:
            return "%s=%s" % (self._name, self.getDefault())

    def getDefault(self):
        default = getattr(self, '_default', None)
        if default is None:
            default = "''"

        if 'array' == self._type:
            return '[]'
        if 'integer' == self._type:
            return '0'
        return default

class MuptipartProperty(Parameter):
    def __init__(self, name, param_dict):
        param_names = ['type', 'description', 'format', 'type', 'default']
        #import pdb; pdb.set_trace()
        self.processParams(param_names, param_dict)
        self._required = False
        self._name = name.replace('[]','')

    def setRequired(self):
        self._required = True

    def __str__(self):
        if self._format:
            return "%s : %s-%s"  % (self._name, self._type, self._format)
        return "%s : %s" % (self._name, self._type)

class Method():
    indent = '    '
    indent2 = indent*2
    indent3 = indent*3
    df = 'def '

    def __init__(self, path, method, description_dict):
        for name in ['summary', 'description', 'tags', 'operationId', 'responses', 'x-code-samples', 'requestBody']:
            setattr(self, name, description_dict.get(name, None))
        self.method = method
        self.path = path
        self.parameters = []
        self.oldSource = open('smartlingApiSdk/FileApiV2.py').read().split('\n')
        self.UrlV2Helper = open('smartlingApiSdk/UrlV2Helper.py').read().split('\n')
        for p in description_dict['parameters']:
            if 'projectId' == p['name'] : continue
            self.parameters .append( Parameter(p) )
        self.need_multipart = False
        self.getMultipartProps()

    def build(self):
        rows = []

        #if not self.requestBody: return ""

        rows.append(self.buildName())
        rows.append(self.buildDoc())

        if self.need_multipart:
            rows.append(self.buildMultipart())
        else:
            rows.append(self.buildBody())
        rows.append('')
        return '\n'.join(rows)

    def buildName(self):
        return ''.join([
            self.indent,
            self.df,
            self.operationId,
            '(self',
            self.buildPrarams(),
            '):',
            ]
        )

    def buildPrarams(self):
        result = ''
        #params = self.parameters +
        if self.parameters:
            result += ", " + ", ".join(x.getParamForName() for x in self.parameters)
        if self.mp_params:
            result += ", " + ", ".join(x.getParamForName() for x in self.mp_params)
        if self.hasDirectives:
            result += ', directives={}'
        return result

    def getOldMethod(self):
        UHMethod = ''
        result = [self.indent + '-'*120]
        pt = self.path + '"'
        for line in self.UrlV2Helper:
            if not pt in line: continue
            UHMethod = line.split(' = ')[0].strip()
            UHMethod = 'urlHelper.' + UHMethod
        if not UHMethod:
            result.append(self.indent+'Not FOUND')
            #result.append('-'*120)
            return self.joinWithIndent(result, self.indent2)
        old_method_lines = []
        start = end = 0
        for i in range(len(self.oldSource)):
            if UHMethod in self.oldSource[i]:
                end = i
                start = i
                while not 'def ' in self.oldSource[start]:
                    start -= 1
                while not 'return ' in self.oldSource[end]:
                    end += 1
                if 'return ' in self.oldSource[end]: end +=1
                result +=  self.oldSource[start:end]
                break
        if start == end :
            result.append(self.indent+'Unable to get old method body')
        #result.append('-'*120)
        res_str = self.joinWithIndent(result, self.indent2)
        return res_str.replace('"""', "'''")

    def buildDoc(self):
        return '\n'.join([
            self.indent2 + '"""',
            self.indent3 + self.method,
            self.indent3 + self.path,
            self.indent3 + 'for details check: https://api-reference.smartling.com/#operation/'+self.operationId,
            self.getCurlExample(),
            self.getOldMethod(),
            self.indent2 + '"""'
            ]
        )

    def getCurlExample(self):
        result = []
        samples = getattr(self, 'x-code-samples', [])
        if not samples:
            return ''

        for d in samples:
            result.append( self.indent + d['source'] )
        return self.joinWithIndent(result, self.indent2)

    def joinWithIndent(self, lst, indent):
        newline_plus_indent = '\n'+indent
        return indent + newline_plus_indent.join(lst)

    def buildPathParamsStr(self):
        path_params = [x for x in self.parameters if x._in == 'path']
        if not path_params:
            return ''
        pth_args = ['%s=%s' % (x._name,x._name) for x in path_params]
        return ', '+ ', '.join(pth_args)

    def buildBody(self):
        body_lines = []

        body_lines.append('kw = {')
        kw_params = [x for x in self.parameters if x._in == 'query']
        for p in kw_params:
            body_lines.append(self.indent + "'%s':%s," % (p._name, p._name))
        for m in self.mp_params:
            if 'binary' == m._format:
                raise Exception("Uncomaptible parameter format for command")
            body_lines.append(self.indent + "'%s':%s," % (m._name, m._name))
        body_lines.append('}')
        body_lines.append("url = self.urlHelper.getUrl('%s'%s)" % (self.path, self.buildPathParamsStr()))
        body_lines.append("return self.command('%s', url, kw)" % self.method.upper())

        return self.joinWithIndent(body_lines, self.indent2)

    def getMultipartProps(self):
        self.mp_params = []
        self.hasDirectives = False
        if not self.requestBody: return
        type = list(self.requestBody['content'].keys())[0]
        if "multipart/form-data" != type:
            return #self.indent2 + 'Cant process:' + type

        schema = self.requestBody['content'][type]['schema']
        #import pdb; pdb.set_trace()
        for k in schema['properties'].keys():
            prop_dict = schema['properties'][k]
            if k.startswith('smartling.'):
                self.hasDirectives = True
                continue
            mp = MuptipartProperty(k, prop_dict)
            self.mp_params.append(mp)
            if mp._format == 'binary':
                self.need_multipart = True

        for req in schema['required']:
            for mp in self.mp_params:
                if req == mp._name:
                    mp.setRequired()

    def buildMultipart(self):
        body_lines = []

        body_lines.append('kw = {')
        kw_params = [x for x in self.parameters if x._in == 'query']
        for p in kw_params:
            body_lines.append(self.indent + "'%s':%s," % (p._name, p._name))
        for m in self.mp_params:
            if 'binary' == m._format:
                body_lines.append(self.indent + "'%s':self.processFile(%s)," % (m._name, m._name))
            elif not 'directives' == m._name:
                body_lines.append(self.indent + "'%s':%s," % (m._name, m._name))
        body_lines.append('}')

        body_lines += self.addDirectives()
        body_lines.append("url = self.urlHelper.getUrl('%s'%s)" % (self.path, self.buildPathParamsStr()))
        body_lines.append("return self.uploadMultipart(url, kw)")

        return self.joinWithIndent(body_lines, self.indent2)

    def addDirectives(self):
        if self.hasDirectives:
            return ["self.addLibIdDirective(kw)",
                    'self.processDirectives(kw, directives)']
        else:
            return []

class ApiSource():
    def __init__(self, name):
        self.name = name
        self.methods = []

    def collectMethods(self, opaDict):
        #itms = list(dict['paths'])
        pt = opaDict['paths']
        #import pdb; pdb.set_trace()
        all_tags = []
        for k,v  in opaDict['paths'].items():
            for method, descr in v.items():
                if method == '$ref': continue
                #if descr['operationId'] != 'deleteUploadedSourceFile': continue
                if self.name in descr['tags']:
                    m = Method(k, method, descr)
                    self.methods.append(m)
                    #return

    def build(self):
        rows = []
        rows.append('from .UrlV2Helper import UrlV2Helper')
        rows.append('from .ApiV2 import ApiV2')
        rows.append('')
        rows.append('class %sApiAuto(ApiV2):' % self.name)
        for m in self.methods[:]:
            built = m.build()
            if built:
                rows.append(built)
                rows.append('')
                rows.append('')
                rows.append('')
        return '\n'.join(rows)


def main():
    dict = json.loads(open('builder/openapi3.json', 'rb').read())
    #apisrc = ApiSource("Jobs")
    apisrc = ApiSource("Files")
    apisrc.collectMethods(dict)
    built = apisrc.build()
    print (built)

main()