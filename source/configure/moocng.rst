moocng
======

These are the configuration steps required for the moocng installation to work.


Create the PostgreSQL database
------------------------------

Initialize PostgreSQL (only in new installations):

.. code-block:: none

    # service postgresql initdb
    # service postgresql start

Configure the moocng database:

.. code-block:: none

    # su - postgres
    $ createuser moocng --no-createrole --no-createdb --no-superuser -P
    Enter password for new role: *****
    Enter it again: *****
    $ createdb -E UTF8 --owner=moocng moocng

Add the new user to the allowed users for that database. For that we need to
edit **/var/lib/pgsql/data/pg_hba.conf** and add this line in the first place,
before anything:

.. code-block:: none

    # TYPE        DATABASE       USER               CIDR-ADDRESS        METHOD
    local         moocng         moocng                                 md5

Please note: The pg_hba.conf location depends on your distribution, in Ubuntu
for example, it is **/etc/postgresql/8.1/main/pg_hba.conf**

Configure rabbitMQ
------------------

RabbitMQ is used in OpenMOOC engine to perform some tasks like sending emails
and creating the last frames of the videos. First of all you need to install it:

.. code-block:: none

    # yum install erlang rabbitmq-server
    # service rabbitmq-server start

First, you need to create a user, a password, and a virtual host. You can do it
with these commands:

.. code-block:: none

    # rabbitmqctl add_user rabbitusername rabbitpassword
    # rabbitmqctl add_vhost yourvirtualhost
    # rabbitmqctl set_permissions -p username yourvirtualhost ".*" ".*" ".*"

*Example*:

.. code-block:: none

    # rabbitmqctl add_user moocng moocngpassword
    # rabbitmqctl add_vhost moocng
    # rabbitmqctl set_permissions -p moocng moocng ".*" ".*" ".*"

You should not need anything else but putting the address of your rabbitMQ server
in the settings. Open your **/etc/openmooc/moocng/moocngsettings/common.py** file
and edit the connection line to your rabbitMQ server:

.. code-block:: python

    BROKER_URL = 'amqp://rabbitusername:rabbitpassword@rabbitServerAdress:5672/yourvirtualhost'

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

Supervisor is a process control system that allows you to monitor the different
instances of programs you have. It is installed by default with moocng, and a default configuration should be here:

.. code-block:: none

    /etc/supervisord.d/openmooc-moocng-supervisord.conf

By default, this configuration should be enough to have two instances of moocng
running with Gunicorn.

.. code-block:: none
    # sevice supervisord start

Configure nginx
---------------

By default, moocng is configured to work with nginx, and it comes with a default
configuration that should run out of the box (remember to edit **server_name**),
It's located here:

.. code-block:: none

    /etc/nginx/conf.d/moocng.conf

nginx requires a certificate. You can create your own self-signed certificates.
For other purposes buy them. To create your own self-signed certificates, please
follow this steps:

.. code-block :: none

    # mkdir /etc/pki/openmooc-moocng
    # cd /etc/pki/openmooc-moocng
    # openssl genrsa -des3 -out server.key 2048
    # openssl req -new -key server.key -out server.csr
    # mv server.key server.key.orig
    # openssl rsa -in server.key.orig -out server.key
    # openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

.. code-block:: none
    # sevice nginx start

Configuring your moocng instance
--------------------------------

The configuration files for moocng are located in
**/etc/openmooc/moocng/moocngsettings/**. Open your *common.py* file and edit this:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'moocng',
            'USER': 'moocng',
            'PASSWORD': 'moocng',
            'HOST': '',
            'PORT': '',
        }
    }

SAML configuration
..................

SAML requires a certificate. You can use your own certificates from nginx.

Open your *saml_settings.py* file located in
**/etc/openmooc/moocng/moocngsettings/** and edit **SAML_CONFIG**:

.. code-block:: python

	SAML_CONFIG = {
	    # full path to the xmlsec1 binary programm
	    'xmlsec_binary': '/usr/bin/xmlsec1',

	    # your entity id, usually your subdomain plus the url to the metadata view
	    'entityid': 'https://moocng.example.com/auth/saml2/metadata/',

	    # directory with attribute mapping
	    'attribute_map_dir': os.path.join(BASEDIR, 'attributemaps'),

	    # this block states what services we provide
	    'service': {
		# we are just a lonely SP
		'sp': {
		    'name': 'Moocng SP',
		    'endpoints': {
			# url and binding to the assetion consumer service view
			# do not change the binding or service name
			'assertion_consumer_service': [
			    ('https://moocng.example.com/auth/saml2/acs/', saml2.BINDING_HTTP_POST),
			],
			# url and binding to the single logout service view
			# do not change the binding or service name
			'single_logout_service': [
			    ('https://moocng.example.com/auth/saml2/ls/', saml2.BINDING_HTTP_REDIRECT),
			],
		    },

		    # in this section the list of IdPs we talk to are defined
		    'idp': {
			# we do not need a WAYF service since there is
			# only an IdP defined here. This IdP should be
			# present in our metadata

			# the keys of this dictionary are entity ids
			'https://idp.example.com/simplesaml/saml2/idp/metadata.php': {
			    'single_sign_on_service': {
				saml2.BINDING_HTTP_REDIRECT: 'https://idp.example.com/simplesaml/saml2/idp/SSOService.php',
			    },
			    'single_logout_service': {
				saml2.BINDING_HTTP_REDIRECT: 'https://idp.example.com/simplesaml/saml2/idp/SingleLogoutService.php',
			    },
			},
		    },
		},
	    },

	    # where the remote metadata is stored
	    'metadata': {
		'local': ['/etc/openmooc/moocng/moocngsettings/remote_metadata.xml'],
	    },

	    # set to 1 to output debugging information
	    'debug': 0,

	    # certificate
	    'key_file': '/etc/pki/openmooc-moocng/server.key',   # private part
	    'cert_file': '/etc/pki/openmooc-moocng/server.crt',  # public part

	    # own metadata settings
	    'contact_person': [
		{'given_name': 'Sysadmin',
		'sur_name': '',
		'company': 'Example CO',
		'email_address': 'sysadmin@example.com',
		'contact_type': 'technical'},
		{'given_name': 'Boss',
		'sur_name': '',
		'company': 'Example CO',
		'email_address': 'admin@example.com',
		'contact_type': 'administrative'},
	    ],

	    # you can set multilanguage information here
	    'organization': {
		'name': [('Example CO', 'es'), ('Example CO', 'en')],
		'display_name': [('Example', 'es'), ('Example', 'en')],
		'url': [('http://example.com', 'es'), ('http://example.com', 'en')],
	    },
	}

Moocng also uses djangosaml2, to config it check the doc at *http://pypi.python.org/pypi/djangosaml2*

In order to connect openmooc with an IdP, you will need its metadata. Download
it (https://idp.example.com/simplesaml/saml2/idp/metadata.php) and save as
**remote_metadata.xml** (check the saml configuration to check that the path
and name match)

Now you need to add the SAML SP metadata to your IdP. First of all you need to
configure in the IdP the metarefresh issue. After that you can go to the idp and
call update entries, You can go to a url like this: *https://idp.example.com/simplesaml/module.php/metarefresh/fetch.php*

Generate the SECRET_KEY
.......................

The secret key is a random string that Django uses in several places like the
CSRF attack protection. It is considered a security problem if you don't change
this value and leave it as the moocng default. You can generate a random value
with the following command:

.. code-block:: none

    $ tr -c -d '0123456789abcdefghijklmnopqrstuvwxyz' </dev/urandom | dd bs=32 count=1 2>/dev/null;echo

Copy the returning value in your **/etc/openmooc/moocng/moocngsettings/local.py** file, like this:

.. code-block:: python

    SECRET_KEY = "uzy3hc2mtevod229yrsywldgh945cmiu"

Copy the static files
.....................

If you will be using the default static and media folders, please skip until the
copy part of this section. If you plan to use your own folders follow the full
instructions.

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

Change the permissions in **/var/lib/openmooc/moocng** so nginx can read the
files, and the wsgi can read/write them.

Sync the database and make the migrations

 Please, see the next issue before do a syncdb https://github.com/OpenMOOC/moocng/issues/65

.. code-block:: none

    # openmooc-moocng-admin syncdb
    # openmooc-moocng-admin migrate
    # openmooc-moocng-admin createsuperuser --username=root --email=admin@example.com

Google Analytics support
........................

This setting is optional and allows you to integrate your moocng with Google
Analytics so you can track who, when and how uses your site.

Just set the Google Analytics Code in the *local.py* settings file:

.. code-block:: python

    GOOGLE_ANALYTICS_CODE = 'XX-XXXX'

User registration
.................

Moocng doesn't handle by default the user registration. There is a setting
called *AUTH_HANDLER* that will allow you to change
the default registration handler. Default: *"moocng.auth_handlers.handlers.SAML2"*

.. code-block:: python

    AUTH_HANDLER = "moocng.auth_handlers.handlers.SAML2"

Other options: "moocng.auth_handlers.handlers.dbauth"

If you're using SAML2, you must set two extra variables that allow you to
redirect the user to the registration page and his profile.

.. code-block:: python

    REGISTRY_URL = 'https://idp.example.com/simplesaml/module.php/userregistration/newUser.php'
    PROFILE_URL = 'https://idp.example.com/simplesaml/module.php/userregistration/reviewUser.php'
    CHANGEPW_URL = 'https://idp.example.com/simplesaml/module.php/userregistration/changePassword.php'

Settings reference
..................

There are a lot of different settings available in OpenMOOC, please :doc:`take a look to the list <settingsref>`

Enabling all the services
.........................

To run all the services on boot once you installed and configured everythin, you
should type these commands:

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
    # chkconfig supervisord on

By default, moocng is configured to work with **nginx**, but you can use Apache **httpd**:

.. code-block:: none

    # chkconfig nginx off
    # chkconfig --add httpd
    # chkconfig httpd on

Testing your installation
.........................

Before testing if the nginx and gunicorn processes work, you can check if moocng
works by typing this command:

.. code-block:: none

    $ openmooc-moocng-admin runserver 0.0.0.0:8000

Now you can open your web browser and go to this location:

    http://localhost:8000
