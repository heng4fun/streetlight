from pyramid.security import (
    Allow,
    Everyone,
)

from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value


class StreetLight(Base):
    __tablename__ = 'streetlamps'
    id = Column(Integer, primary_key=True)
    sn = Column(String(50))
    voltage = Column(Float)
    current = Column(Float)
    location = Column(String(100))
    status = Column(Boolean)
    installation_time = Column(DateTime)
    remark = Column(Text)

    def __init__(self, sn, voltage, current, location, status, installation_time, remark):
        self.sn = sn
        self.voltage = voltage
        self.current = current
        self.location = location
        self.status = status
        self.installation_time = installation_time
        self.remark = remark


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(50), unique=True)
    password = Column(String(50))
    user_group = Column(String(50), ForeignKey('groups.group_name'))

    def __init__(self, user_name, password, user_group):
        self.user_name = user_name
        self.password = password
        self.user_group = user_group


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String(50), unique=True)

    def __init__(self, group_name):
        self.group_name = group_name


class Location(Base):

    """docstring for Location"""
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    location = Column(String(50), unique=True)

    def __init__(self, location):
        self.location = location


class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'view'), (
        Allow, 'group:admins', 'edit'), (Allow, 'group:supers', 'add'), (Allow, 'group:supers', 'edit')]

    def __init__(self, request):
        pass
