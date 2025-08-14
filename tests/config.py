class Config:
    def __init__(self, env):

        self.base_url = {
            'dev': 'https://myapp.dev.com',
            'qa' : 'https://myapp.qa.com',
            'stag' : 'https://web-stag.hispasatprod.opentv.com/'
        }[env]

        self.app_port = {
            'dev':'8080',
            'qa':'80',
            'stag':''
        }[env]