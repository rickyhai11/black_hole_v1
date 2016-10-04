
"""
SQLAlchemy models for playnetmano_rm data.
"""

from oslo_config import cfg
from oslo_db.sqlalchemy import models

from sqlalchemy.orm import relationship
from sqlalchemy.orm import session as orm_session
from sqlalchemy import (Column, Integer, String, Boolean, schema, ForeignKey, DateTime)
from sqlalchemy.ext.declarative import declarative_base

CONF = cfg.CONF
BASE = declarative_base()


def get_session():
    from playnetmano_rm.db.sqlalchemy import api as db_api

    return db_api.get_session()


class Playnetmano_rmBase(models.ModelBase,
                         models.SoftDeleteMixin,
                         models.TimestampMixin):
    """Base class for Playnetmano_rm Models."""
    __table_args__ = {'mysql_engine': 'InnoDB'}

    def expire(self, session=None, attrs=None):
        if not session:
            session = orm_session.Session.object_session(self)
            if not session:
                session = get_session()
        session.expire(self, attrs)

    def refresh(self, session=None, attrs=None):
        """Refresh this object."""
        if not session:
            session = orm_session.Session.object_session(self)
            if not session:
                session = get_session()
        session.refresh(self, attrs)

    def delete(self, session=None):
        """Delete this object."""
        if not session:
            session = orm_session.Session.object_session(self)
            if not session:
                session = get_session()
        session.begin()
        session.delete(self)
        session.commit()


class Quota(BASE, Playnetmano_rmBase):
    """Represents a single quota override for a project.

    If there is no row for a given project id and resource, then the
    default for the quota class is used.  If there is no row for a
    given quota class and resource, then the default for the
    deployment is used. If the row is present but the hard limit is
    Null, then the resource is unlimited.
    """

    __tablename__ = 'quotas'

    __table_args__ = (
        schema.UniqueConstraint("project_id", "resource", "deleted",
                                name="uniq_quotas0project_id0resource0deleted"
                                ),)

    id = Column(Integer, primary_key=True)

    project_id = Column(String(255), index=True)

    resource = Column(String(255), nullable=False)

    hard_limit = Column(Integer, nullable=True)

class QuotaUsages(BASE, Playnetmano_rmBase):
    """Quota_uages.

    store quota usages for project resource
    """
    __tablename__ = 'quota_usages'
    __table_args__ = ()
    attributes = ['id', 'project_id', 'user_id', 'resource',
                  'in_use', 'allocated','reserved', 'available', 'until_refresh',
                  'created_at', 'updated_at', 'deleted_at', 'deleted']

    id = Column(Integer, primary_key=True)
    project_id = Column(String(255), index=True)
    user_id = Column(String(255), index=True)
    resource = Column(String(255), nullable=False)

    in_use = Column(Integer)
    allocated = Column(Integer, default=0)
    reserved = Column(Integer, default=0)
    available = Column(Integer, default=0)

    until_refresh = Column(Integer, default=0)

    @property
    def total(self):
        return self.in_use + self.reserved
    
class Reservation(BASE, Playnetmano_rmBase):
    """Reservation.

    Represents a resource reservation service (for quotas)
    """
    __tablename__ = 'reservations'
    __table_args__ = ()
    attributes = ['id', 'uuid', 'usage_id', 'project_id', 'resource',
                  'delta', 'expire',
                  'created_at', 'updated_at', 'deleted_at', 'deleted']

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False)

    usage_id = Column(Integer,
                          ForeignKey('quota_usages.id'),
                          nullable=False)

    project_id = Column(String(255), index=True)
    resource = Column(String(255))

    delta = Column(Integer)
    expire = Column(DateTime, nullable=False)

    usage = relationship(
        "QuotaUsages",
        foreign_keys=usage_id,
        primaryjoin='and_(Reservation.usage_id == QuotaUsages.id,'
                    'QuotaUsages.deleted == 0)')

class QuotaClass(BASE, Playnetmano_rmBase):
    """Represents a single quota override for a quota class.

    If there is no row for a given quota class and resource, then the
    default for the deployment is used.  If the row is present but the
    hard limit is Null, then the resource is unlimited.
    """

    __tablename__ = "quota_classes"

    id = Column(Integer, primary_key=True)

    class_name = Column(String(255), index=True)

    resource = Column(String(255))

    hard_limit = Column(Integer, nullable=True)


class SyncLock(BASE, Playnetmano_rmBase):
    """Store locks to avoid overlapping of projects

    syncing during automatic periodic sync jobs with
    multiple-engines.
    """

    __tablename__ = 'sync_lock'

    id = Column(Integer, primary_key=True)

    engine_id = Column(String(36), nullable=False)

    timer_lock = Column(String(255), nullable=False)

    task_type = Column(String(36), nullable=False)


class Service(BASE, Playnetmano_rmBase):
    """"Playnetmano_rm service engine registry"""

    __tablename__ = 'service'

    id = Column('id', String(36), primary_key=True, nullable=False)

    host = Column(String(255))

    binary = Column(String(255))

    topic = Column(String(255))

    disabled = Column(Boolean, default=False)

    disabled_reason = Column(String(255))
