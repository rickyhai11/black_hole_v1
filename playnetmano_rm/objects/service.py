"""Service object."""

from playnetmano_rm.db import api as db_api
from playnetmano_rm.objects import base
from oslo_versionedobjects import fields


@base.Playnetmano_rmObjectRegistry.register
class Service(base.Playnetmano_rmObject, base.VersionedObjectDictCompat):
    """Playnetmano_rm service object."""

    fields = {
        'id': fields.UUIDField(),
        'host': fields.StringField(),
        'binary': fields.StringField(),
        'topic': fields.StringField(),
        'disabled': fields.BooleanField(),
        'disabled_reason': fields.StringField(nullable=True),
        'created_at': fields.DateTimeField(),
        'updated_at': fields.DateTimeField(),
        'deleted_at': fields.DateTimeField(nullable=True),
        'deleted': fields.IntegerField(nullable=True),
    }

    @classmethod
    def create(cls, context, service_id, host=None, binary=None, topic=None):
        obj = db_api.service_create(context, service_id=service_id, host=host,
                                    binary=binary, topic=topic)
        return cls._from_db_object(context, cls(context), obj)

    @classmethod
    def get(cls, context, service_id):
        obj = db_api.service_get(context, service_id)
        return cls._from_db_object(context, cls(), obj)

    @classmethod
    def get_all(cls, context):
        objs = db_api.service_get_all(context)
        return [cls._from_db_object(context, cls(), obj) for obj in objs]

    @classmethod
    def update(cls, context, obj_id, values=None):
        obj = db_api.service_update(context, obj_id, values=values)
        return cls._from_db_object(context, cls(), obj)

    @classmethod
    def delete(cls, context, obj_id):
        db_api.service_delete(context, obj_id)
