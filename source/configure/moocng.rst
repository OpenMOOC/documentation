moocng
======

These are the configuration steps required for the moocng installation to work.

Create the PostgreSQL database
------------------------------

.. code-block:: bash

    $ su - postgres
    $ createuser moocng --no-createrole --no-createdb --no-superuser -P
    Enter password for new role: *****
    Enter it again: *****
    $ createdb -E UTF8 --owner=moocng moocng

Add the new user to the allowed users for that database. For that we need to edit **/var/lib/pgsql/data/pg_hba.conf** and add this line in the first place, before anything:

.. code-block:: ini

    # TYPE        DATABASE       USER               CIDR-ADDRESS        METHOD
    local         moocng         moocng                                 md5

Please note: The pg_hba.conf location depends on your distribution, in Ubuntu for example, it is **/etc/postgresql/8.1/main/pg_hba.conf**

Configure rabbitMQ
------------------

RabbitMQ is used in OpenMOOC engine to perform some tasks like sending emails and creating the last frames of the videos. First of all you need to install it:

.. code-block:: bash

    # yum install erlang rabbitmq-server

First, you need to create a user, a password, and a virtual host. You can do it with these commands:

.. code-block:: bash

    $ service rabbitmq-server start
    $ rabbitmqctl add_user rabbitusername rabbitpassword
    $ rabbitmqctl add_vhost yourvirtualhost
    $ rabbitmqctl set_permissions -p username virtualhost ".*" ".*" ".*"

*Example*:

.. code-block:: bash

    $ service rabbitmq-server start
    $ rabbitmqctl add_user moocng moocngpassword
    $ rabbitmqctl add_vhost moocng
    $ rabbitmqctl set_permissions -p moocng moocng ".*" ".*" ".*"

You should not need anything else but putting the address of your rabbitMQ server in the settings. Edit your **/etc/openmooc/moocng/moocngsettings/local.py** file and add a connection line to your rabbitMQ server:

.. code-block:: ini

    BROKER_URL = 'amqp://myuser:mypassword@rabbitServerAdress:5672/moocng'

*Example*:

.. code-block:: ini

    BROKER_URL = 'amqp://moocng:moocngpassword@localhost:5672/moocng'

Configuring your moocng instance
--------------------------------

The configuration files for moocng are located in **/etc/openmooc/moocng/moocngsettings/**. Open your *local.py* file and add this:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'moocng',
            'USER': 'moocng',
            'PASSWORD': 'yourmoocngpassword',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

Generate the SECRET_KEY
.......................

The secret key is a random string that Django uses in several places like the CSRF attack protection. It is considered a security problem if you don't change this value and leave it as the moocng default. You can generate a random value with the following command:

.. code-block:: bash

    $ tr -c -d '0123456789abcdefghijklmnopqrstuvwxyz' </dev/urandom | dd bs=32 count=1 2>/dev/null;echo

Copy the returning value in your **/etc/openmooc/moocng/moocngsettings/local.py** file, like this:

.. code-block:: python

    SECRET_KEY = "uzy3hc2mtevod229yrsywldgh945cmiu"

Copy the static files
.....................

If you will be using the default static and media folders, please skip until the copy part of this section. If you plan to use your own folders follow the full instructions.

The default moocng static and media directories are located in:

.. code-block:: bash

    /var/lib/openmooc/moocng/static
    /var/lib/openmooc/moocng/media

To change the default directories you must edit your **/etc/openmooc/moocng/moocngsettings/local.py** and add these two settings:

.. code-block:: bash

    MEDIA_ROOT = “path/to/your/media/files/”
    STATIC_ROOT = “path/to/your/static/files/”

To copy the static files we are going to use the command **moocngadmin**:

.. code-block:: bash

    # moocngadmin collectstatic

Change the permissions in **/var/lib/openmooc/moocng** so nginx can read the files, and the wsgi can read/write them.

Sync the database and make the migrations

.. code-block:: bash

    # moocngadmin syncdb --migrate

You’re done! You should be able to run a test instance and visit it with this command:

.. code-block:: bash

    $ moocngadmin runserver 0.0.0.0:8000
