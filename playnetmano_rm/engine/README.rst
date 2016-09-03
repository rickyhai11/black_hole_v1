===============================
Service
===============================

playnetmano_rm Service has responsibility for:

    Monitoring the job/smaller jobs status, and return the result to playnetmano_rm
    API if needed.

    Generate task to purge time-out jobs from playnetmano_rm Database

    Multiple playnetmano_rm API could run in parallel, and also can work in
    multi-worker mode.

    Multiple playnetmano_rm Engine will be designed and run in stateless mode,
    persistent data will be accessed (read and write) from the playnetmano_rm
    Database through the DAL module.

service.py:
    run KB service in multi-worker mode, and establish RPC server

engine_cfg.py:
    configuration and initialization for Engine service

quota_manager.py
    Manages all the quota related activies such as Periodic Quota Sync,
    One Demand Quota Sync, Get Total Usage for a Project, Read playnetmano_rm
    global limit from DB/Conf file etc..

    Quota sync happens based on below formula:
    Global_remaining_limit = playnetmano_rm_global_limit(from DB/Conf) -
                             Su(sum of all usages from all regions)
    Region_new_limit = Global_remaining_limit + resource_usage_in_that_region.

    Reference link: https://etherpad.opnfv.org/p/centralized_quota_management

    On Demand Quota Sync: Creates threads for each region and syncs
    the limits for each quota concurrently.

    Periodic Quota Sync: Creates threads for each Project and calls
    quota sync for project(On Demand Quota sync) for syncing project.

    Caches OpenStack region specific clients so reduced traffic.
