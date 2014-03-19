moocng
======

These are the configuration steps required for the moocng installation to work.

Create the moocng settings local.py
-----------------------------------

Copy and check our **/etc/openmooc/moocng/moocngsettings/local.py.example**:

.. code-block:: none

    # cp /etc/openmooc/moocng/moocngsettings/local.py.example /etc/openmooc/moocng/moocngsettings/local.py


Create the PostgreSQL database
------------------------------

Initialize PostgreSQL (only in new installations):

.. code-block:: none

    # service postgresql initdb
    # service postgresql start

Configure the MOOCNG database:

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
    # service rabbitmq-server start

First, you need to create a user, a password, and a virtual host. You can do it with these commands:

.. code-block:: none

    # rabbitmqctl add_user rabbitusername rabbitpassword
    # rabbitmqctl add_vhost yourvirtualhost
    # rabbitmqctl set_permissions -p username virtualhost ".*" ".*" ".*"

*Example*:

.. code-block:: none

    # rabbitmqctl add_user moocng moocngpassword
    # rabbitmqctl add_vhost moocng
    # rabbitmqctl set_permissions -p moocng moocng ".*" ".*" ".*"

You should not need anything else but putting the address of your rabbitMQ server in the settings. Edit your **/etc/openmooc/moocng/moocngsettings/local.py** file and add a connection line to your rabbitMQ server:

.. code-block:: python

    BROKER_URL = 'amqp://myuser:mypassword@rabbitServerAdress:5672/moocng'

*Example*:

.. code-block:: python

    BROKER_URL = 'amqp://moocng:moocngpassword@localhost:5672/moocng'

Amazon S3 configuration
-----------------------

moocng use S3 to storage users uploaded files. You need an Amazon AWS account
and create a bucket to store the files.

The bucket must be configured with the next CORS configuration:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
        <CORSRule>
            <AllowedOrigin>*</AllowedOrigin>
            <AllowedMethod>PUT</AllowedMethod>
            <MaxAgeSeconds>3000</MaxAgeSeconds>
            <AllowedHeader>Content-Type</AllowedHeader>
            <AllowedHeader>x-amz-acl</AllowedHeader>
            <AllowedHeader>origin</AllowedHeader>
            <AllowedHeader>Accept</AllowedHeader>
            <AllowedHeader>Accept-Charset</AllowedHeader>
            <AllowedHeader>Accept-Encoding</AllowedHeader>
            <AllowedHeader>Accept-Language</AllowedHeader>
            <AllowedHeader>Access-Control-Request-Headers</AllowedHeader>
            <AllowedHeader>Access-Control-Request-Method</AllowedHeader>
            <AllowedHeader>Connection</AllowedHeader>
            <AllowedHeader>Host</AllowedHeader>
            <AllowedHeader>Origin</AllowedHeader>
            <AllowedHeader>Referer</AllowedHeader>
            <AllowedHeader>User-Agent</AllowedHeader>
        </CORSRule>
    </CORSConfiguration>

To improve the security in production environments you can define a more strict
AllowedOrigin setting in your CORS configuration.

And your settings must define your account data, your bucket and the expire
time of upload permissions.

.. code-block:: python

      AWS_ACCESS_KEY_ID = "your-access-key-id"
    AWS_SECRET_ACCESS_KEY = "your-secret-key-id"
    AWS_STORAGE_BUCKET_NAME = "your-bucket-name"
    AWS_S3_UPLOAD_EXPIRE_TIME = (60 * 5) # 5 minutes

Configure supervisor
--------------------

Supervisor is a process control system that allows you to monitor the different instances of programs you have. It is installed by default with moocng, and a default configuration should be here:

.. code-block:: none

    /etc/openmooc/moocng/supervisord.conf

By default, this configuration should be enough to have two instances of moocng running with Gunicorn.

.. code-block:: none
    # sevice supervisord start

Configure nginx
---------------

By default, moocng is configured to work with nginx, and it comes with a default configuration that should run out of the box, It's located here:

.. code-block:: none

    /etc/nginx/conf.d/moocng.conf

Remember to edit **server_name**.

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
            'HOST': '',
            'PORT': '',
        }
    }

SAML configuration
..................

SAML requires a certificate. You can create your own self-signed certificates. For other purposes buy them. To configure SAML2 in moocng please follow this steps:

 * Follow the first five steps of this guide: http://www.akadia.com/services/ssh_test_certificate.html
 * Create a directory called "saml2" at you moong folder
 * Create inside it a certs directory
 * Copy the 'attributemaps' of moocng inside the saml2
 * Copy server.key and server.crt to saml2/certs

.. code-block :: none

    $ openssl genrsa -des3 -out server.key 2048
    $ openssl req -new -key server.key -out server.csr
    $ cp server.key server.key.org
    $ openssl rsa -in server.key.org -out server.key
    $ openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

In **/etc/openmooc/moocng/moocngsettings/common.py** there is a SAML_CONFIG var. You must copy this variable in your local.py file and configure the parameters based in your environment. Moocng also uses djangosaml2, to config it check the doc at *http://pypi.python.org/pypi/djangosaml2*

In order to connect openmooc with an IdP, you will need its metadata. Download it and save as **remote_metadata.xml** (check the saml configuration to check that the path and name match)

Now you need to add the SAML SP metadata to your IdP. First of all you need to configure in the IdP the metarefresh issue. After that you can go to the idp and call update entries, You can go to a url like this: *https://idp.example.com/simplesaml/module.php/metarefresh/fetch.php*

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

To copy the static files we are going to use the command **openmooc-moocng-admin**:

.. code-block:: none

    # openmooc-moocng-admin collectstatic

Change the permissions in **/var/lib/openmooc/moocng** so nginx can read the files, and the wsgi can read/write them.

Sync the database and make the migrations

.. code-block:: none

    # openmooc-moocng-admin syncdb
    # openmooc-moocng-admin migrate

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

Enabling all the services
.........................

To run all the services on boot once you installed and configured everythin, you should type these commands:

.. code-block:: none

    # chkconfig --add nginx
    # chkconfig --add rabbitmq-server
    # chkconfig --add postgresql
    # chkconfig --add mongod
    # chkconfig --add celeryd
    # chkconfig --add supervisord
    # chkconfig postgresql on
    # chkconfig nginx on
    # chkconfig rabbitmq-server on
    # chkconfig mongod on
    # chkconfig celeryd on
    # chkconfig supervisord

By default, moocng is configured to work with **nginx**, but you can use Apache **httpd**:

.. code-block:: none

    # chkconfig nginx off
    # chkconfig --add httpd
    # chkconfig httpd on

Testing your installation
.........................

Before testing if the nginx and gunicorn processes work, you can check if moocng works by typing this command:

.. code-block:: none

    $ openmooc-moocng-admin runserver 0.0.0.0:8000

Now you can open your web browser and go to this location:

    http://localhost:8000
