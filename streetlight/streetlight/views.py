from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
)

from pyramid.view import (
    view_config,
    forbidden_view_config,
)

from .models import (
    DBSession,
    MyModel,
    Admin,
    Group,
    Location,
    StreetLight,
    RootFactory,
)

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    has_permission,
    Allowed,
)

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import or_

from datetime import datetime


@view_config(route_name='home', renderer='templates/home.pt', permission='view')
def home(request):
    alert = False
    logged_in = authenticated_userid(request)

    home_url = request.route_url('home')
    login_url = request.route_url('login')
    view_url = request.route_url('view')
    alert_url = request.route_url('alert')
    admin_url = request.route_url('admin')
    add_admin_url = request.route_url('add_admin')
    edit_admin_url = request.route_url('edit_admin')
    add_streetlight_url = request.route_url('add_streetlight')
    logout_url = request.route_url('logout')

    alert = DBSession.query(StreetLight).filter(
        "voltage > 220.0 or current > 30.0").all()

    return dict(locals())


@view_config(route_name='view', renderer='templates/view.pt', permission='edit')
def view(request):
    all_streetlights = []
    logged_in = authenticated_userid(request)

    home_url = request.route_url('home')
    view_url = request.route_url('view')
    alert_url = request.route_url('alert')
    admin_url = request.route_url('admin')
    add_admin_url = request.route_url('add_admin')
    edit_admin_url = request.route_url('edit_admin')
    add_streetlight_url = request.route_url('add_streetlight')
    logout_url = request.route_url('logout')
    search_url = request.route_url('search')
    edit_streetlight = request.route_url('edit_streetlight')

    alert = DBSession.query(StreetLight).filter(
        "voltage > 220.0 or current > 30.0").all()

    for streetlight in DBSession.query(StreetLight).all():
        all_streetlights.append(streetlight)
    return dict(locals())


@view_config(route_name='search', renderer='templates/view.pt', permission='edit')
def search(request):
    all_streetlights = []
    logged_in = authenticated_userid(request)

    home_url = request.route_url('home')
    view_url = request.route_url('view')
    alert_url = request.route_url('alert')
    admin_url = request.route_url('admin')
    add_admin_url = request.route_url('add_admin')
    edit_admin_url = request.route_url('edit_admin')
    add_streetlight_url = request.route_url('add_streetlight')
    logout_url = request.route_url('logout')
    search_url = request.route_url('search')
    edit_streetlight = request.route_url('edit_streetlight')

    alert = DBSession.query(StreetLight).filter(
        "voltage > 220.0 or current > 30.0").all()

    if 'search_form' in request.params:
        search_way = request.params['search_way']
        keyword = request.params['keyword']
        if keyword == 'id':
            keyword = int(keyword)
        has_lights = DBSession.query(
            StreetLight).filter(
                or_(StreetLight.id == keyword, StreetLight.sn == keyword,
                    StreetLight.location == keyword)).all()
        for search_light in has_lights:
            all_streetlights.append(search_light)

    return dict(locals())


@view_config(route_name='alert', renderer='templates/view.pt', permission='edit')
def alert(request):
    all_streetlights = []
    logged_in = authenticated_userid(request)

    home_url = request.route_url('home')
    view_url = request.route_url('view')
    alert_url = request.route_url('alert')
    admin_url = request.route_url('admin')
    add_admin_url = request.route_url('add_admin')
    edit_admin_url = request.route_url('edit_admin')
    add_streetlight_url = request.route_url('add_streetlight')
    logout_url = request.route_url('logout')
    search_url = request.route_url('search')
    edit_streetlight = request.route_url('edit_streetlight')

    alert = DBSession.query(StreetLight).filter(
        "voltage > 220.0 or current > 30.0").all()
    for streetlight in alert:
        all_streetlights.append(streetlight)
    return dict(locals())


@view_config(route_name='admin', renderer='templates/admin.pt')
def admin(request):
    all_admins = []
    logged_in = authenticated_userid(request)

    home_url = request.route_url('home')
    login_url = request.route_url('login')
    view_url = request.route_url('view')
    alert_url = request.route_url('alert')
    admin_url = request.route_url('admin')
    add_admin_url = request.route_url('add_admin')
    edit_admin_url = request.route_url('edit_admin')
    add_streetlight_url = request.route_url('add_streetlight')
    logout_url = request.route_url('logout')
    delete_admin_url = request.route_url('delete_admin')

    alert = DBSession.query(StreetLight).filter(
        "voltage > 220.0 or current > 30.0").all()

    for admin in DBSession.query(Admin).all():
        all_admins.append(admin)
    return dict(locals())


@view_config(route_name='add_admin', renderer='templates/add_admin.pt', permission='add')
def add_admin(request):
    admin_saved = False
    all_group_names = []
    logged_in = authenticated_userid(request)

    home_url = request.route_url('home')
    login_url = request.route_url('login')
    view_url = request.route_url('view')
    alert_url = request.route_url('alert')
    admin_url = request.route_url('admin')
    add_admin_url = request.route_url('add_admin')
    edit_admin_url = request.route_url('edit_admin')
    add_streetlight_url = request.route_url('add_streetlight')
    logout_url = request.route_url('logout')
    delete_admin_url = request.route_url('delete_admin')

    alert = DBSession.query(StreetLight).filter(
        "voltage > 220.0 or current > 30.0").all()

    for group_name in DBSession.query(Group).all():
        all_group_names.append(group_name)

    if 'form.submitted' in request.params:
        user_name = request.params['user_name']
        password = request.params['password']
        user_group = request.params['user_group']
        DBSession.add(Admin(user_name, password, user_group))
        admin_saved = True
        return dict(locals())
    return dict(locals())


@view_config(route_name='edit_admin', renderer='templates/edit_admin.pt')
def edit_admin(request):
    changed = False
    all_group_names = []
    user_name = authenticated_userid(request)
    logged_in = authenticated_userid(request)

    home_url = request.route_url('home')
    login_url = request.route_url('login')
    view_url = request.route_url('view')
    alert_url = request.route_url('alert')
    admin_url = request.route_url('admin')
    add_admin_url = request.route_url('add_admin')
    edit_admin_url = request.route_url('edit_admin')
    add_streetlight_url = request.route_url('add_streetlight')
    logout_url = request.route_url('logout')
    delete_admin_url = request.route_url('delete_admin')

    alert = DBSession.query(StreetLight).filter(
        "voltage > 220.0 or current > 30.0").all()

    for group_name in DBSession.query(Group).all():
        all_group_names.append(group_name)

    if 'form.submitted' in request.params:
        password = request.params['password']
        user_group = request.params['user_group']
        admin = DBSession.query(Admin).filter_by(user_name=user_name).one()
        admin.password = password
        admin.user_group = user_group
        DBSession.flush()
        headers = forget(request)
        return HTTPFound(location=request.route_url('login'),
                         headers=headers)

    return dict(locals())


@view_config(route_name='delete_admin', renderer='templates/admin.pt')
def delete_admin(request):
    user_id = int(request.params['id'])
    DBSession.query(Admin).filter_by(id=user_id).delete()

    return HTTPFound(location=request.route_url('admin'))


@view_config(route_name='add_streetlight', renderer='templates/add_streetlight.pt')
def add_light(request):
    admin_saved = False
    all_locations = []
    voltage = 0.0
    current = 0.0
    status = False
    logged_in = authenticated_userid(request)

    home_url = request.route_url('home')
    login_url = request.route_url('login')
    view_url = request.route_url('view')
    alert_url = request.route_url('alert')
    admin_url = request.route_url('admin')
    add_admin_url = request.route_url('add_admin')
    edit_admin_url = request.route_url('edit_admin')
    add_streetlight_url = request.route_url('add_streetlight')
    logout_url = request.route_url('logout')
    delete_admin_url = request.route_url('delete_admin')

    alert = DBSession.query(StreetLight).filter(
        "voltage > 220.0 or current > 30.0").all()

    for location in DBSession.query(Location).all():
        all_locations.append(location)

    if 'form.submitted' in request.params:
        sn = request.params['sn']
        location = request.params['location']
        installation_time = datetime.now()
        remark = request.params['remark']
        DBSession.add(
            StreetLight(
                sn=sn, voltage=voltage, current=current, location=location, status=status,
                installation_time=installation_time, remark=remark))
        admin_saved = True
        return dict(locals())
    return dict(locals())


@view_config(route_name='edit_streetlight', renderer='templates/edit_streetlight.pt', permission='add')
def edit_light(request):
    changed = False
    all_locations = []
    logged_in = authenticated_userid(request)

    home_url = request.route_url('home')
    view_url = request.route_url('view')
    alert_url = request.route_url('alert')
    admin_url = request.route_url('admin')
    add_admin_url = request.route_url('add_admin')
    edit_admin_url = request.route_url('edit_admin')
    add_streetlight_url = request.route_url('add_streetlight')
    logout_url = request.route_url('logout')

    has_alert = DBSession.query(StreetLight).filter(
        "voltage > 220.0 or current > 30.0").all()
    if has_alert:
        alert = True

    for location in DBSession.query(Location).all():
        all_locations.append(location)
    if 'edit.submitted' in request.params:
        light_id = int(request.params['id'])
        sn = request.params['sn']
        remark = request.params['remark']
        location = request.params['location']
        return dict(locals())
    if 'form.submitted' in request.params:
        light_id = int(request.params['id'])
        sn = request.params['sn']
        location = request.params['location']
        remark = request.params['remark']
        the_light = DBSession.query(
            StreetLight).filter_by(id=light_id).one()
        the_light.sn = sn
        the_light.location = location
        the_light.remark = remark
        DBSession.flush()
        changed = True
        return (locals())

    return dict(locals())


@view_config(route_name='delete_streetlight', renderer='templates/view.pt')
def delete_light(request):
    referrer = request.url
    if 'delete.submitted' in request.params:
        light_id = int(request.params['id'])
        DBSession.query(StreetLight).filter_by(id=light_id).delete()
        return HTTPFound(location=referrer)


@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    fail_message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        try:
            admin = DBSession.query(Admin).filter_by(user_name=login).one()
        except NoResultFound, e:
            print e
            return dict(
                locals()
            )
        if admin.password == password:
            headers = remember(request, login)
            return HTTPFound(location=came_from,
                             headers=headers)
        fail_message = 'Failed login'

    return dict(locals())


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'),
                     headers=headers)
