===========================
playnetmano_rm Installation Guide
===========================

Preparing the installation
--------------------------
playnetmano_rm is centralized synchronization service for multi-region OpenStack
deployments. In OPNFV Colorado release, playnetmano_rm provides centralized quota
management feature. At least two OpenStack regions with shared KeyStone should
be installed first.

playnetmano_rm includes playnetmano_rm-api and playnetmano_rm-engine, playnetmano_rm-api and
playnetmano_rm-engine which talk to each other through message bus, and both
services access the database. playnetmano_rm-api receives the RESTful
API request for quota management and forward the request to playnetmano_rm-engine
to do quota synchronization etc task.

Therefore install playnetmano_rm on the controller nodes of one of the OpenStack
region, these two services could be deployed in same node or different node.
Both playnetmano_rm-api and playnetmano_rm-engine can run in multiple nodes with
multi-workers mode. It's up to you how many nodes you want to deploy
playnetmano_rm-api and playnetmano_rm-engine and they can work in same node or
different nodes.

HW requirements
---------------
No special hardware requirements

Installation instruction
------------------------

In colorado release, playnetmano_rm is recommended to be installed in a python
virtual environment. So install and activate virtualenv first.

.. code-block:: bash

    sudo pip install virtualenv
    virtualenv venv
    source venv/bin/activate

Get the latest code of playnetmano_rm from git repository:

.. code-block:: bash

    git clone https://github.com/openstack/playnetmano_rm.git
    cd playnetmano_rm/
    pip install -e .


or get the stable release from PyPI repository:

.. code-block:: bash

    pip install playnetmano_rm

In case of the database package are not installed, you may need to install:

.. code-block:: bash

    pip install mysql
    pip install pymysql

In the playnetmano_rm root folder, where you can find the source code of playnetmano_rm,
generate the configuration sample file for playnetmano_rm:

.. code-block:: bash

    oslo-config-generator --config-file=./tools/config-generator.conf

prepare the folder used for cache, log and configuration for playnetmano_rm:

.. code-block:: bash

    sudo rm -rf /var/cache/playnetmano_rm
    sudo mkdir -p /var/cache/playnetmano_rm
    sudo chown `whoami` /var/cache/playnetmano_rm
    sudo rm -rf /var/log/playnetmano_rm
    sudo mkdir -p /var/log/playnetmano_rm
    sudo chown `whoami` /var/log/playnetmano_rm
    sudo rm -rf /etc/playnetmano_rm
    sudo mkdir -p /etc/playnetmano_rm
    sudo chown `whoami` /etc/playnetmano_rm

Copy the sample configuration to the configuration folder /etc/playnetmano_rm:

.. code-block:: bash

    cp etc/playnetmano_rm/playnetmano_rm.conf.sample /etc/playnetmano_rm/playnetmano_rm.conf

Before editing the configuration file, prepare the database info for playnetmano_rm.

.. code-block:: bash

    mysql -uroot -e "CREATE DATABASE $kb_db CHARACTER SET utf8;"
    mysql -uroot -e "GRANT ALL PRIVILEGES ON $kb_db.* TO '$kb_db_user'@'%' IDENTIFIED BY '$kb_db_pwd';"

For example, the following command will create database "playnetmano_rm", and grant the
privilege for the db user "playnetmano_rm" with password "password":

.. code-block:: bash

    mysql -uroot -e "CREATE DATABASE playnetmano_rm CHARACTER SET utf8;"
    mysql -uroot -e "GRANT ALL PRIVILEGES ON playnetmano_rm.* TO 'playnetmano_rm'@'%' IDENTIFIED BY 'password';"

Create the service user in OpenStack:

.. code-block:: bash

    source openrc admin admin
    openstack user create --project=service --password=$kb_svc_pwd $kb_svc_user
    openstack role add --user=$kb_svc_user --project=service admin

For example, the following command will create service user "playnetmano_rm",
and grant the user "playnetmano_rm" with password "password" the role of admin
in service project:

.. code-block:: bash

    source openrc admin admin
    openstack user create --project=service --password=password playnetmano_rm
    openstack role add --user=playnetmano_rm --project=service admin



Then edit the configuration file for playnetmano_rm:

.. code-block:: bash

    vim /etc/playnetmano_rm/playnetmano_rm.conf

By default, the bind_host of playnetmano_rm-api is local_host(127.0.0.1), and the
port for the service is 8118, you can leave it as the default if no port
conflict happened.

To make the playnetmano_rm work normally, you have to edit these configuration
items. The [cache] section is used by playnetmano_rm engine to access the quota
information of Nova, Cinder, Neutron in each region, replace the
auth_uri to the keystone service in your environment,
especially if the keystone service is not located in the same node, and
also for the account to access the Nova, Cinder, Neutron in each region,
in the following configuration, user "admin" with password "password" of
the tenant "admin" is configured to access other Nova, Cinder, Neutron in
each region:

.. code-block:: bash

    [cache]
    auth_uri = http://127.0.0.1:5000/v3
    admin_tenant = admin
    admin_password = password
    admin_username = admin

Configure the database section with the service user "playnetmano_rm" and its
password, to access database "playnetmano_rm". For detailed database section
configuration, please refer to http://docs.openstack.org/developer/oslo.db/opts.html,
and change the following configuration accordingly based on your
environment.

.. code-block:: bash

    [database]
    connection = mysql+pymysql://$kb_db_user:$kb_db_pwd@127.0.0.1/$kb_db?charset=utf8

For example, if the database is "playnetmano_rm", and the db user "playnetmano_rm" with
password "password", then the configuration is as following:

.. code-block:: bash

    [database]
    connection = mysql+pymysql://playnetmano_rm:password@127.0.0.1/playnetmano_rm?charset=utf8

The [keystone_authtoken] section is used by keystonemiddleware for token
validation during the API request to the playnetmano_rm-api, please refer to
http://docs.openstack.org/developer/keystonemiddleware/middlewarearchitecture.html
on how to configure the keystone_authtoken section for the keystonemiddleware
in detail, and change the following configuration accordingly based on your
environment:

*please specify the region_name where you want the token will be validated if the
KeyStone is deployed in multiple regions*

.. code-block:: bash

    [keystone_authtoken]
    signing_dir = /var/cache/playnetmano_rm
    cafile = /opt/stack/data/ca-bundle.pem
    auth_uri = http://127.0.0.1:5000/v3
    project_domain_name = Default
    project_name = service
    user_domain_name = Default
    password = $kb_svc_pwd
    username = $kb_svc_user
    auth_url = http://127.0.0.1:35357/v3
    auth_type = password
    region_name = RegionOne

For example, if the service user is "playnetmano_rm, and the password for the user
is "password", then the configuration will look like this:

.. code-block:: bash

    [keystone_authtoken]
    signing_dir = /var/cache/playnetmano_rm
    cafile = /opt/stack/data/ca-bundle.pem
    auth_uri = http://127.0.0.1:5000/v3
    project_domain_name = Default
    project_name = service
    user_domain_name = Default
    password = password
    username = playnetmano_rm
    auth_url = http://127.0.0.1:35357/v3
    auth_type = password
    region_name = RegionOne


And also configure the message bus connection, you can refer to the message
bus configuration in Nova, Cinder, Neutron configuration file.

.. code-block:: bash

    [DEFAULT]
    rpc_backend = rabbit
    control_exchange = openstack
    transport_url = None

    [oslo_messaging_rabbit]
    rabbit_host = 127.0.0.1
    rabbit_port = 5671
    rabbit_userid = guest
    rabbit_password = guest
    rabbit_virtual_host = /

After these basic configuration items configured, now the database schema of
"playnetmano_rm" should be created:

.. code-block:: bash

    python playnetmano_rm/cmd/manage.py --config-file=/etc/playnetmano_rm/playnetmano_rm.conf db_sync

And create the service and endpoint for playnetmano_rm, please change the endpoint url
according to your cloud planning:

.. code-block:: bash

    openstack service create --name=playnetmano_rm synchronization
    openstack endpoint create --region=RegionOne \
    --publicurl=http://127.0.0.1:8118/v1.0 \
    --adminurl=http://127.0.0.1:8118/v1.0 \
    --internalurl=http://127.0.0.1:8118/v1.0 playnetmano_rm

Now it's ready to run playnetmano_rm-api and playnetmano_rm-engine:

.. code-block:: bash

    nohup python playnetmano_rm/cmd/api.py --config-file=/etc/playnetmano_rm/playnetmano_rm.conf &
    nohup python playnetmano_rm/cmd/engine.py --config-file=/etc/playnetmano_rm/playnetmano_rm.conf &

Run the following command to check whether playnetmano_rm-api and playnetmano_rm-engine
are running:

.. code-block:: bash

    ps aux|grep python


Post-installation activities
----------------------------

Run the following commands to check whether playnetmano_rm-api is serving, please
replace $token to the token you get from "openstack token issue":

.. code-block:: bash

    openstack token issue
    curl  -H "Content-Type: application/json"  -H "X-Auth-Token: $token" \
    http://127.0.0.1:8118/

If the response looks like following: {"versions": [{"status": "CURRENT",
"updated": "2016-03-07", "id": "v1.0", "links": [{"href":
"http://127.0.0.1:8118/v1.0/", "rel": "self"}]}]},
then that means the playnetmano_rm-api is working normally.

Run the following commands to check whether playnetmano_rm-engine is serving, please
replace $token to the token you get from "openstack token issue", and the
$admin_project_id to the admin project id in your environment:

.. code-block:: bash

    curl  -H "Content-Type: application/json"  -H "X-Auth-Token: $token" \
    -H  "X_ROLE: admin"  -X PUT \
    http://127.0.0.1:8118/v1.0/$admin_project_id/os-quota-sets/$admin_project_id/sync

If the response looks like following: "triggered quota sync for
0320065092b14f388af54c5bd18ab5da", then that means the playnetmano_rm-engine
is working normally.
