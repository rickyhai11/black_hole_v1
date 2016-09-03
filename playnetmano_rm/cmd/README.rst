===============================
cmd
===============================

Scripts to start the playnetmano_rm API and Engine services

api.py:
    start API service
    python api.py --config-file=/etc/playnetmano_rm.conf

engine.py:
    start Engine service
    python engine.py --config-file=/etc/playnetmano_rm.conf

manage.py:
    CLI interface for playnetmano_rm management
    playnetmano_rm-manage --config-file /etc/playnetmano_rm.conf db_sync
    playnetmano_rm-manage --config-file /etc/playnetmano_rm.conf db_version