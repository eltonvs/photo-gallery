"""
  Define the project routes
"""


def includeme(config):
    config.add_route('index', '/')
    config.add_route('restrict', '/restrict')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    config.add_route('upload', '/upload')

    config.scan()
