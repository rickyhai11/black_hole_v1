import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    service = sqlalchemy.Table(
        'service', meta,
        sqlalchemy.Column('id', sqlalchemy.String(36),
                          primary_key=True, nullable=False),
        sqlalchemy.Column('host', sqlalchemy.String(length=255)),
        sqlalchemy.Column('binary', sqlalchemy.String(length=255)),
        sqlalchemy.Column('topic', sqlalchemy.String(length=255)),
        sqlalchemy.Column('disabled', sqlalchemy.Boolean, default=False),
        sqlalchemy.Column('disabled_reason', sqlalchemy.String(length=255)),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted', sqlalchemy.Integer),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )
    service.create()
