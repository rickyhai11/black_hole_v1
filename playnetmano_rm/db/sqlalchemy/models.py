
"""
SQLAlchemy models for playnetmano_rm data.
"""

from oslo_config import cfg
from oslo_db.sqlalchemy import models

from sqlalchemy.orm import session as orm_session
from sqlalchemy import (Column, Integer, String, Boolean, schema)
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
