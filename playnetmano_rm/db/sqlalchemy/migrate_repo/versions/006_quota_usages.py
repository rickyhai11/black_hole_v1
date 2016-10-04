import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    quota_usages = sqlalchemy.Table(
        'quota_usages', meta,
        sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column('project_id', sqlalchemy.String(255), index=True),
        sqlalchemy.Column('user_id', sqlalchemy.String(255), index=True),
        sqlalchemy.Column('resource', sqlalchemy.String(255), nullable=False),
        sqlalchemy.Column('in_use', sqlalchemy.Integer),
        sqlalchemy.Column('allocated', sqlalchemy.Integer),
        sqlalchemy.Column('reserved', sqlalchemy.Integer),
        sqlalchemy.Column('available', sqlalchemy.Integer),
        sqlalchemy.Column('until_refresh', sqlalchemy.Integer),
        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted', sqlalchemy.Integer),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    quota_usages.create()
