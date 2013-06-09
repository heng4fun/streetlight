from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from .security import groupfinder

from .models import (
    DBSession,
    Base,
)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings, root_factory='streetlight.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('view', '/view')
    config.add_route('search', '/search')
    config.add_route('alert', '/alert')
    config.add_route('admin', '/admin')
    config.add_route('add_admin', '/add_admin')
    config.add_route('edit_admin', '/edit_admin')
    config.add_route('delete_admin', '/delete_admin')
    config.add_route('add_streetlight', '/add_streetlight')
    config.add_route('edit_streetlight', '/edit_streetlight')
    config.add_route('delete_streetlight', '/delete_streetlight')

    config.scan()
    return config.make_wsgi_app()
