moocng
======

These are the configuration steps required for the moocng installation to work.

Create the PostgreSQL database
------------------------------

.. code-block:: none

    # su - postgres
    $ createuser moocng --no-createrole --no-createdb --no-superuser -P
    Enter password for new role: *****
    Enter it again: *****
    $ createdb -E UTF8 --owner=moocng moocng

Add the new user to the allowed users for that database. For that we need to edit **/var/lib/pgsql/data/pg_hba.conf** and add this line in the first place, before anything:

.. code-block:: none

    # TYPE        DATABASE       USER               CIDR-ADDRESS        METHOD
    local         moocng         moocng                                 md5

Please note: The pg_hba.conf location depends on your distribution, in Ubuntu for example, it is **/etc/postgresql/8.1/main/pg_hba.conf**

Configure rabbitMQ
------------------

RabbitMQ is used in OpenMOOC engine to perform some tasks like sending emails and creating the last frames of the videos. First of all you need to install it:

.. code-block:: none

    # yum install erlang rabbitmq-server

First, you need to create a user, a password, and a virtual host. You can do it with these commands:

.. code-block:: none

    # service rabbitmq-server start
    # rabbitmqctl add_user rabbitusername rabbitpassword
    # rabbitmqctl add_vhost yourvirtualhost
    # rabbitmqctl set_permissions -p username virtualhost ".*" ".*" ".*"

*Example*:

.. code-block:: none

    # service rabbitmq-server start
    # rabbitmqctl add_user moocng moocngpassword
    # rabbitmqctl add_vhost moocng
    # rabbitmqctl set_permissions -p moocng moocng ".*" ".*" ".*"

You should not need anything else but putting the address of your rabbitMQ server in the settings. Edit your **/etc/openmooc/moocng/moocngsettings/local.py** file and add a connection line to your rabbitMQ server:

.. code-block:: python

    BROKER_URL = 'amqp://myuser:mypassword@rabbitServerAdress:5672/moocng'

*Example*:

.. code-block:: python

    BROKER_URL = 'amqp://moocng:moocngpassword@localhost:5672/moocng'

Configure supervisor
--------------------

Supervisor is a process control system that allows you to monitor the different instances of programs you have. It is installed by default with moocng, and a default configuration should be here:

.. code-block:: none

    /etc/openmooc/moocng/supervisord.conf

By default, this configuration should be enough to have two instances of moocng running with Gunicorn.

Configure nginx
---------------

By default, moocng is configured to work with nginx, and it comes with a default configuration that should run out of the box, It's located here:

.. code-block:: none

    /etc/nginx/conf.d/moocng.conf

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

.. code-block:: none

    $ tr -c -d '0123456789abcdefghijklmnopqrstuvwxyz' </dev/urandom | dd bs=32 count=1 2>/dev/null;echo

Copy the returning value in your **/etc/openmooc/moocng/moocngsettings/local.py** file, like this:

.. code-block:: python

    SECRET_KEY = "uzy3hc2mtevod229yrsywldgh945cmiu"

Copy the static files
.....................

If you will be using the default static and media folders, please skip until the copy part of this section. If you plan to use your own folders follow the full instructions.

The default moocng static and media directories are located in:

.. code-block:: none

    /var/lib/openmooc/moocng/static
    /var/lib/openmooc/moocng/media

To change the default directories you must edit your **/etc/openmooc/moocng/moocngsettings/local.py** and add these two settings:

.. code-block:: python

    MEDIA_ROOT = "path/to/your/media/files/"
    STATIC_ROOT = "path/to/your/static/files/"

To copy the static files we are going to use the command **moocngadmin**:

.. code-block:: none

    # moocngadmin collectstatic

Change the permissions in **/var/lib/openmooc/moocng** so nginx can read the files, and the wsgi can read/write them.

Sync the database and make the migrations

.. code-block:: none

    # moocngadmin syncdb --migrate

Google Analytics support
........................

This setting is optional and allows you to integrate your moocng with Google Analytics so you can track who, when and how uses your site.

Just set the Google Analytics Code in the *local.py* settings file:

.. code-block:: python

    GOOGLE_ANALYTICS_CODE = 'XX-XXXX'

User registration
.................

Moocng doesn't handle by default the user registration. There is a setting called *AUTH_HANDLER* that will allow you to change
the default registration handler. Default: *"moocng.auth_handlers.handlers.SAML2"*

.. code-block:: python

    AUTH_HANDLER = "moocng.auth_handlers.handlers.SAML2"

Other options: "moocng.auth_handlers.handlers.dbauth"

If you're using SAML2, you must set two extra variables that allow you to redirect the user to the registration page and his profile.

.. code-block:: python

    REGISTRY_URL = 'https://idp.example.com/simplesaml/module.php/userregistration/newUser.php'
    PROFILE_URL = 'https://idp.example.com/simplesaml/module.php/userregistration/reviewUser.php'

Settings reference
..................

There are a lot of different settings available in OpenMOOC, please :doc:`take a look to the list <settingsref>`
Testing your installation
.........................

Before testing if the nginx and gunicorn processes work, you can check if moocng works by typing this command:

.. code-block:: none

    $ moocngadmin runserver 0.0.0.0:8000

Now you can open your web browser and go to this location:

    http://localhost:8000
