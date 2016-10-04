import sqlalchemy


def upgrade(migrate_engine):
    meta = sqlalchemy.MetaData()
    meta.bind = migrate_engine

    reservations = sqlalchemy.Table(
        'reservations', meta,
        sqlalchemy.Column('id', sqlalchemy.Integer(), primary_key=True),
        sqlalchemy.Column('uuid', sqlalchemy.String(length=36), nullable=False),
        sqlalchemy.Column('usage_id', sqlalchemy.Integer(),
                   sqlalchemy.ForeignKey('quota_usages.id'),
                   nullable=False),
        sqlalchemy.Column('project_id',
                   sqlalchemy.String(length=255),
                   index=True),
        sqlalchemy.Column('resource',
                   sqlalchemy.String(length=255)),
        sqlalchemy.Column('delta', sqlalchemy.Integer(), nullable=False),
        sqlalchemy.Column('expire', sqlalchemy.DateTime),

        sqlalchemy.Column('created_at', sqlalchemy.DateTime),
        sqlalchemy.Column('updated_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted_at', sqlalchemy.DateTime),
        sqlalchemy.Column('deleted', sqlalchemy.Boolean(create_constraint=True,
                                          name=None)),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    reservations.create()