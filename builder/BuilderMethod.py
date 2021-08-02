import json

class Parameter():
    def __init__(self, param_dict):
        param_names = ['name', 'description', 'in', 'required', 'schema']
        self.processParams(param_names, param_dict)
        if self._schema:
            self._type = self._schema['type']

    def processParams(self, param_names, param_dict):
        for name in param_names:
            n = param_dict.get(name, None)
            if 'name' == name:
                n = n.replace('[]', 'List')
            setattr(self, '_' + name, n)

    def getParamForName(self):
        if self._required:
            return self._name
        else:
            return "%s=%s" % (self._name, self.getDefault())

    def getDefault(self):
        if 'array' == self._type:
            return '[]'
        if 'integer' == self._type:
            return '0'
        return "''"

class MuptipartProperty(Parameter):
    def __init__(self, name, param_dict):
        param_names = ['type', 'description', 'format']
        self.processParams(param_names, param_dict)
        self._required = False
        self._name = name
        self._type =self._format

    def setRequired(self):
        self._required = True

    def __str__(self):
        return "%s : %s" % (self._name, self._required)

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
        self.getMultipartProps()

    def build(self):
        rows = []

        if self.requestBody:
            rows.append(self.buildName())
            rows.append(self.buildDoc())
            rows.append(self.buildMultipart())
        else:
            if 0:
                rows.append(self.buildName())
                rows.append(self.buildDoc())
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
        return result

    def getOldMethod(self):
        UHMethod = ''
        result = ['-'*120]
        pt = self.path + '"'
        for line in self.UrlV2Helper:
            if not pt in line: continue
            UHMethod = line.split(' = ')[0].strip()
            UHMethod = 'urlHelper.' + UHMethod
        if not UHMethod:
            result.append(self.indent+'Not FOUND')
            result.append('-'*120)
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
                result +=  self.oldSource[start:end]
                break
        if start == end :
            result.append(self.indent+'Unable to get old method body')
        result.append('-'*120)
        return self.joinWithIndent(result, self.indent2)

    def buildDoc(self):
        return '\n'.join([
            self.indent2 + '"""',
            self.indent3 + self.method,
            self.indent3 + self.path,
            self.indent3 + 'for details check: https://api-reference.smartling.com/#operation/'+self.operationId,
            self.getOldMethod(),
            self.indent2 + '"""'
            ]
        )

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
        has_kw = 0
        body_lines = []

        body_lines.append('kw = {')
        kw_params = [x for x in self.parameters if x._in == 'query']
        for p in kw_params:
            body_lines.append(self.indent + "'%s':%s," % (p._name, p._name))
        body_lines.append('}')
        body_lines.append("url = self.urlHelper.getUrl('%s'%s)" % (self.path, self.buildPathParamsStr()))
        body_lines.append("return self.command('%s', url, kw)" % self.method.upper())

        return self.joinWithIndent(body_lines, self.indent2)

    def getMultipartProps(self):
        self.mp_params = []
        if not self.requestBody: return
        type = list(self.requestBody['content'].keys())[0]
        if "multipart/form-data" != type:
            return #self.indent2 + 'Cant process:' + type

        schema = self.requestBody['content'][type]['schema']

        for k in schema['properties'].keys():
            prop_dict = schema['properties'][k]
            self.mp_params.append(MuptipartProperty(k, prop_dict))

        for req in schema['required']:
            for mp in self.mp_params:
                if req == mp._name:
                    mp.setRequired()

    def buildMultipart(self):
        self.mp_params_str = [str(x) for x in self.mp_params]
        return self.joinWithIndent(self.mp_params_str, self.indent2)

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
                try:
                    if self.name in descr['tags']:
                        m = Method(k, method, descr)
                        self.methods.append(m)
                except:
                    print(method, descr)

    def build(self):
        rows = []
        rows.append('')
        rows.append('class %sApi:' % self.name)
        for m in self.methods[:]:
            rows.append(m.build())
        return '\n'.join(rows)


def main():
    dict = json.loads(open('builder/openapi3.json', 'rb').read())

    #apisrc = ApiSource("Jobs")
    apisrc = ApiSource("Files")
    apisrc.collectMethods(dict)
    built = apisrc.build()
    print (built)

main()