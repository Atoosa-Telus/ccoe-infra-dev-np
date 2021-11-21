class ProjectClass:
    env = ''
    name =''
    id = ''
    number = ''
    parent = ''
    aliases = []

    def __init__(self, project, alias):
        self.name = project[alias]['name']
        self.env = project[alias]['labels']['env']
        self.number = project[alias]['projectNumber']
        self.id = project[alias]['projectId']
        self.parent = project[alias]['parent']['id']

    def list_valid_aliases(self, project):
        for element in project:
            aliases = aliases.append(element)
        self.aliases = aliases

class RestfulClass:
    get =''
    put = ''

    def __init__(self, method, request):
        self.get = method[request]['get']
        self.put = method[request]['put']