import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    sync_lock = sqlalchemy.Table(
        'sync_lock', meta,
        sqlalchemy.Column('id', sqlalchemy.Integer,
                          primary_key=True, nullable=False),
        sqlalchemy.Column('timer_lock', sqlalchemy.String(length=255),
                          nullable=False),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted', sqlalchemy.Integer),
        sqlalchemy.Column('engine_id', sqlalchemy.String(length=36),
                          nullable=False),
        sqlalchemy.Column('task_type', sqlalchemy.String(length=36),
                          nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )
    sync_lock.create()
