
"""Module with SQLAlchemy models."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

__all__ = [
    'User',
    'Service',
    'Access'
]

base = declarative_base()


class User(base):
    """Users table model."""

    id_ = Column(
        name='id',
        type_=Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    name = Column(
        name='name',
        type_=String(length=20),
        nullable=False,
        unique=True
    )
    password_hash = Column(
        name='password_hash',
        type_=String(length=100),
        nullable=False,
        unique=True
    )
    __tablename__ = 'users'


class Service(base):
    """Services table model."""

    id_ = Column(
        name='id',
        type_=Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    name = Column(
        name='name',
        type_=String(length=50),
        nullable=False,
        unique=True
    )
    __tablename__ = 'services'


class Access(base):
    """Accesses table model."""

    id_ = Column(
        name='id',
        type_=Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    user_id = Column(
        ForeignKey('users.id'),
        name='user_id',
        type_=Integer,
        nullable=False
    )
    service_id = Column(
        ForeignKey('services.id'),
        name='service_id',
        type_=Integer,
        nullable=False
    )
    __tablename__ = 'accesses'
