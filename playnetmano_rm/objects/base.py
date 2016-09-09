"""playnetmano_rm common internal object model"""

from oslo_utils import versionutils
from oslo_versionedobjects import base

from playnetmano_rm import objects

VersionedObjectDictCompat = base.VersionedObjectDictCompat


class Playnetmano_rmObject(base.VersionedObject):
    """Base class for playnetmano_rm objects.

    This is the base class for all objects that can be remoted or instantiated
    via RPC. Simply defining a sub-class of this class would make it remotely
    instantiatable. Objects should implement the "get" class method and the
    "save" object method.
    """

    OBJ_PROJECT_NAMESPACE = 'playnetmano_rm'
    VERSION = '1.0'

    @staticmethod
    def _from_db_object(context, obj, db_obj):
        if db_obj is None:
            return None
        for field in obj.fields:
            if field == 'metadata':
                obj['metadata'] = db_obj['meta_data']
            else:
                obj[field] = db_obj[field]

        obj._context = context
        obj.obj_reset_changes()

        return obj


class Playnetmano_rmObjectRegistry(base.VersionedObjectRegistry):
    def registration_hook(self, cls, index):
        """Callback for object registration.

        When an object is registered, this function will be called for
        maintaining playnetmano_rm.objects.$OBJECT as the highest-versioned
        implementation of a given object.
        """
        version = versionutils.convert_version_to_tuple(cls.VERSION)
        if not hasattr(objects, cls.obj_name()):
            setattr(objects, cls.obj_name(), cls)
        else:
            curr_version = versionutils.convert_version_to_tuple(
                getattr(objects, cls.obj_name()).VERSION)
            if version >= curr_version:
                setattr(objects, cls.obj_name(), cls)
