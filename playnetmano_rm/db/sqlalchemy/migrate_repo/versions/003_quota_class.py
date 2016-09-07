import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    quota_classes = sqlalchemy.Table(
        'quota_classes', meta,
        sqlalchemy.Column('id', sqlalchemy.Integer,
                          primary_key=True, nullable=False),
        sqlalchemy.Column('class_name', sqlalchemy.String(length=255),
                          index=True),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted', sqlalchemy.Integer),
        sqlalchemy.Column('resource', sqlalchemy.String(length=255)),
        sqlalchemy.Column('hard_limit', sqlalchemy.Integer,
                          nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )
    quota_classes.create()
