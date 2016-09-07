import datetime
from oslo_config import cfg
import six
import sqlalchemy

CLASS_NAME = 'default'
CREATED_AT = datetime.datetime.now()

CONF = cfg.CONF
CONF.import_group('playnetmano_rm_global_limit', 'playnetmano_rm.common.config')


def upgrade(migrate_engine):
    """Add default quota class data into DB."""
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    quota_classes = sqlalchemy.Table('quota_classes', meta, autoload=True)

    rows = quota_classes.count(). \
        where(quota_classes.c.class_name == 'default').execute().scalar()

    # Do not add entries if there are already 'default' entries.  We don't
    # want to write over something the user added.
    if rows:
        return

    # Set default quota limits
    qci = quota_classes.insert()
    for resource, default in six.iteritems(CONF.playnetmano_rm_global_limit):
        qci.execute({'created_at': CREATED_AT,
                     'class_name': CLASS_NAME,
                     'resource': resource[6:], # remove 'quota_' characters in "quota_security_groups" that is read from playnetmano_rm_global_limit config file
                     'hard_limit': default,
                     'deleted': False})
