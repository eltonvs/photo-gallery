from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

try:
    # for python 2
    from urlparse import urlparse
except ImportError:
    # for python 3
    from urllib.parse import urlparse

from gridfs import GridFS
from pymongo import MongoClient


def expandvars_dict(settings):
    """Expands all environment variables in a settings dictionary."""
    from os.path import expandvars
    return dict((key, expandvars(val)) for key, val in settings.items())


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings = expandvars_dict(settings)
    config = Configurator(settings=settings)

    # Security policies
    # config.include('.utils.auth')
    authn_policy = AuthTktAuthenticationPolicy(
        settings['app.secret'],
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # Jinja2 Settings
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Application Routes
    config.include('.routes')

    # Mongo Config
    db_url = urlparse(settings['mongo_uri'])
    config.registry.db = MongoClient(
        host=db_url.hostname,
        port=db_url.port,
    )

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db

    def add_fs(request):
        return GridFS(request.db)

    config.add_request_method(add_db, 'db', reify=True)
    config.add_request_method(add_fs, 'fs', reify=True)

    config.scan()
    return config.make_wsgi_app()
