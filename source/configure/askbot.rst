======
Askbot
======

.. note:: This section is in development


Create the PostgreSQL database
------------------------------

Initialize PostgreSQL (only in new installations):

.. code-block:: none

    # service postgresql initdb
    # service postgresql start

Configure the moocng database:

.. code-block:: none

    # su - postgres
    $ createuser askbot --no-createrole --no-createdb --no-superuser -P
    Enter password for new role: *****
    Enter it again: *****
    $ createdb -E UTF8 --owner=askbot askbot

Add the new user to the allowed users for that database. For that we need to
edit **/var/lib/pgsql/data/pg_hba.conf** and add this line in the first place,
before anything:

.. code-block:: none

    # TYPE        DATABASE       USER               CIDR-ADDRESS        METHOD
    host          all            askbot             127.0.0.1/32        md5
    host          all            askbot             ::1/128             md5

Please note: The pg_hba.conf location depends on your distribution, in Ubuntu
for example, it is **/etc/postgresql/8.1/main/pg_hba.conf**


Settings
========

OpenMOOC askbot has multiple configuration files located in **/etc/openmooc/askbot** like

- local_settings.py
- instances_creator_conf.py

local_settings
--------------

The first file sets the local environment variables. You can fin there the SAML2 settings,
theme settings, etc.


instances_creator_conf
----------------------

This file establishes the general settings for all the instances of openmooc-askbot.

INSTANCE_NAME
    Name of the instance to create, this should not be editable by the user.

INSTANCE_DB_NAME
    Database name of the instance. Not editable by the user

REMOTE_HOST
    If the askbot instances are located behing a farm proxym set this to the proxy IP.

DB_HOST
    Main server of the databases, tends to be 'localhost' by  default, but you can
    change it if the database server if located in another machine.

DB_USER
    Main database user for creating the databases. OpenMOOC-Askbot usually works
    with an askbot DB superuser, you should set the username.

DB_PASSWORD
    Superuser password

DEFAULT_INSTANCE_DIR
    Set the default instance directory where the instances will be stored. It defaults
    to '/etc/openmooc/askbot/instances' but you can change it anytime.

DEFAULT_DISABLED_INSTANCES_DIR
    Default disabled instances dir. It defaults to '/etc/openmooc/askbot/instances.disabled'
    but you can change it anytime.

SKEL_DIR
    Directory with the instances file skeleton. It defaults to '/usr/lib/python2.6/site-packages/askbotopenmooc/skel_instances'
    but you can change it if you create a new skel.

GUNICORN_START_PORT
    Port where Gunicorn will start to operate. Every instance will be created to work
    from that por on. Default: 10000


Instance creator
================

OpenMOOC askbot works under the premise that you will use an askbot farm. For that
purpose we developed a set of scripts and an application wrapper so askbot could
be easily extended and had identity federation.

The command to create new askbot instances is: openmooc-askbot-instancetool:

--create, -c (name, database)
    Creates a new askbot instance and puts it to work. It also syncs and migrates
    the database. **After that you'll only have to create a superuser**

--destroy, -k (name)
    Destroys an askbot instance, deleting all the files and the database.

--disable, -d (name)
    Disables an askbot instance, it moves the instance files to the disabled folder and
    it doesn't touch the database.

