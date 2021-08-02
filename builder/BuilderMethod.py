import json

class Parameter():
    def __init__(self, param_dict):
        for name in ['name', 'description', 'in', 'required', 'schema']:
            n = param_dict.get(name, 'NoEsta')
            if 'name' == name:
                n = n.replace('[]','List')
            setattr(self, '_'+name, n)

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
        for p in description_dict['parameters']:
            if 'projectId' == p['name'] : continue
            self.parameters .append( Parameter(p) )

    def build(self):
        rows = []
        rows.append(self.buildName())
        rows.append(self.buildDoc())
        if self.requestBody:
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
         if not self.parameters: return ''
         return ", " + ", ".join(x._name for x in self.parameters)

    def buildDoc(self):
        return '\n'.join([
            self.indent2 + '"""',
            self.indent3 + self.method,
            self.indent3 + self.path,
            self.indent3 + 'for details check: https://api-reference.smartling.com/#operation/'+self.operationId,
            self.indent2 + '"""'
            ]
        )

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

        newline_plus_indent = '\n'+self.indent2
        return self.indent2 + newline_plus_indent.join(body_lines)

    def buildMultipart(self):
        return str(self.requestBody)

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