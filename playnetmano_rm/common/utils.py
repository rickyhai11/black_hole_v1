
import itertools

from playnetmano_rm.common import consts
from playnetmano_rm.common import exceptions


def get_import_path(cls):
    return cls.__module__ + "." + cls.__name__


# Returns a iterator of tuples containing batch_size number of objects in each
def get_batch_projects(batch_size, project_list, fillvalue=None):
    # look at this link to see what happened
    # http://stackoverflow.com/questions/28847334/how-to-unserstand-the-code-using-izip-longest-to-chunk-a-list
    args = [iter(project_list)] * batch_size
    return itertools.izip_longest(fillvalue=fillvalue, *args)


# to do validate the quota limits
def validate_quota_limits(payload):
    for resource in payload:
        # Check valid resource name
        if resource not in itertools.chain(consts.CINDER_QUOTA_FIELDS,
                                           consts.NOVA_QUOTA_FIELDS,
                                           consts.NEUTRON_QUOTA_FIELDS):
            raise exceptions.InvalidInputError
        # Check valid quota limit value in case for put/post
        if isinstance(payload, dict) and (not isinstance(
                payload[resource], int) or payload[resource] <= 0):
            raise exceptions.InvalidInputError
