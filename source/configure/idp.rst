============================
IdP (SAML Identity Provider)
============================

This documentation explain how to configure the IdP instance on a CentOS to work
with nginx after installing the rpm openmooc-idp-nginx.

For the rest of the explanation we will consider that our service will
be displayed at idp.example.com


SELinux and firewall
--------------------

In a development enviroment you can disable both:

.. code-block:: none

	# lokkit --selinux=disabled
	# lokkit --disabled

In a production enviroment you may configure a secure environment. The nginx
publish the IdP under 80 and 443 port. The idP uses also some internal services
that runs in default port, like ldap (port 389), mongodb (port 27017).


Configure OpenLDAP
------------------

Edit the hosts file and add the host of your LDAP: (in our case we add 'idp.example.com' at the 127.0.0.1 and the IP entry):

.. code-block:: none

	# vim /etc/hosts


Something similar to ::

	127.0.0.1       localhost.localdomain   localhost idp.example.com
	::1             localhost6.localdomain6 localhost6 idp.example.com


.. code-block:: none

   # cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG

Edit the ldap config file **/etc/openldap/ldap.conf**: ::

  URI ldap://XXX.XXX.XXX.XXX/    # put the correct IP
  BASE dc=example,dc=com

dc=example,dc=com will be the base root of our example environment, change this
with your desired base root (note that all the ldap configuration is based on 
that base root) 


Create the LDAP root password:

.. code-block:: none

	$ slappasswd

Create the config file **/etc/openldap/slapd.conf**: ::

	include         /etc/openldap/schema/core.schema
	include         /etc/openldap/schema/cosine.schema
	include         /etc/openldap/schema/inetorgperson.schema
	include         /etc/openldap/schema/nis.schema
	include     /etc/openldap/schema/eduperson.schema
	include     /etc/openldap/schema/schac.schema
	include     /etc/openldap/schema/iris.schema

	allow bind_v2

	pidfile     /var/run/openldap/slapd.pid
	argsfile    /var/run/openldap/slapd.args

	database    bdb
	suffix      "dc=example,dc=com"
	rootdn      "cn=admin,dc=example,dc=com"
	rootpw      <secretpassword>

	# The database directory MUST exist prior to running slapd AND
	# should only be accessible by the slapd and slap tools.
	# Mode 700 recommended.
	directory   /var/lib/ldap

	# Indices to maintain for this database
	index objectClass                       eq,pres
	index ou,cn,mail,surname,givenname      eq,pres,sub
	index uidNumber,gidNumber,loginShell    eq,pres
	index uid,memberUid                     eq,pres,sub
	index nisMapName,nisMapEntry            eq,pres,sub

Remember to replace the <secretpassword> by the LDAP root password.

Delete the **/etc/openldap/slap.d** directory to avoid conflicts with our new configuration:

.. code-block:: none

	# rm -rf /etc/openldap/slap.d

Start and stop the LDAP server:

.. code-block:: none

   # service slapd start
   # service slapd stop


Create the root-path file **/etc/openldap/root.ldif**: ::

	dn: dc=example,dc=com
	dc: example
	description: LDAP Admin
	objectClass: dcObject
	objectClass: organizationalUnit
	ou: rootobject

Create the people-path file **/etc/openldap/people.ldif**: ::

	dn: ou=People,dc=example,dc=com
	ou: People
	description: Users
	objectClass: organizationalUnit

Create a testuser file to be imported: **/etc/openldap/testuser.ldif**: ::

	# Entry 1: mail=testuser@example.com,ou=People,dc=example,dc=com
	dn: mail=testuser@example.com,ou=People,dc=example,dc=com
	cn: Test_cn
	edupersonaffiliation: student
	mail: testuser@example.com
	objectclass: inetOrgPerson
	objectclass: person
	objectclass: top
	objectclass: eduPerson
	sn: Test_sn
	userpassword: testuser


Add the entries to the LDAP:

.. code-block:: none

   # slapadd -l /etc/openldap/root.ldif -f /etc/openldap/slapd.conf -d 10
   # slapadd -l /etc/openldap/people.ldif -f /etc/openldap/slapd.conf -d 10
   # slapadd -l /etc/openldap/testuser.ldif -f /etc/openldap/slapd.conf -d 10

Start the server:

.. code-block:: none

   # service slapd start


If restarting the server, warnings appear, change the permissions on the LDAP directory and restart LDAP to check that warnings disssapear:

.. code-block:: none

   # chown -R ldap:ldap /var/lib/ldap/
   # service slapd restart

Add the service to the system boot:

.. code-block:: none

   # chkconfig slapd on


We can create a backup script and insert it in our crontab:

For example, this will create a backup of the LDAP at the */var/backups/* folder

.. code-block:: none

	# slapcat | /usr/bin/bzip2 > /var/backups/ldap_`/bin/date +%Y-%m-%d-%H-%M-%S`.ldif.bz2

We can save this script as backup_ldap.sh in the simplesamlphp folder or wherever we want, give this file execution permission and add it to the cron. (**/etc/cron.d/backup_ldap**) ::

  00 3 * * *      <path-to-the-folder-that-contain-the-script>/backup_ldap.sh

Restart the crond service:

.. code-block:: none

   # service crond restart


Configure phpldapadmin (not mandatory)
--------------------------------------

`phpldapadmin <http://phpldapadmin.sourceforge.net/wiki/index.php/Main_Page>`_ is a tool that let us manage our ldap using a web.

You can use this tool to manage the user directory of the OpenMOOC IdP.

The configuration file of phpldapadmin is located at **/etc/phpldapadmin/config.php**. We need to configure some params that will
be based in our ldap configuration:

.. code-block:: none

	$servers = new Datastore();
	$servers->newServer('ldap_pla');
	$servers->setValue('server','name','Mooc LDAP Server');
	$servers->setValue('server','host','127.0.0.1');
	$servers->setValue('server','port',389);
	$servers->setValue('server','base',array('dc=example,dc=com'));
	$servers->setValue('login','auth_type','session');
	$servers->setValue('server','tls',false);
	$servers->setValue('appearance','password_hash','');
	$servers->setValue('login','attr','dn');



Review the nginx configuration **/etc/nginx/conf.d/idp.conf**, you will be defined a location entry: /phpldapadmin 
One important thing is that we protect this location with auth-basic. The file where the auth-basic credentials are
stored at **/etc/nginx/htpasswd** In order to create 

.. code-block:: none

	# htpasswd /etc/nginx/htpasswd <username>


phpldapadmin must be accessible at http://idp.example.com/phpldapadmin (make sure that nginx and the php-fpm service are running), use the auth-basic credentials and after that you can log in using your root user of ldap, so on username set cn=admin,dc=example,dc=com and the password is the one you have configured before on the slapd.conf file.


IdP Core
--------

The IdP Core is based on `simpleSAMLphp <http://simplesamlphp.org>`_ and its modules. SimpleSAMLphp is an implementation of the SAML2 standar. In order to use simpleSAMLphp in a secure way is required a SSL connection between each system. That mean that you will need a SSL cert per domain, or a wildcard cert for the global domain.

In development enviroments you can use self-signed certificates, for production we recommend to use certificates from recognized organizations to avoid that browsers sent to the users the "warnings notification about certs" for each domain, which can be very annoying.

The certs must be stored at **/etc/pki/simplesamlphp/**. You can use the same certs in nginx to serve HTTPs.
The configuration documentation expect that the certs are named as **server.key** and **server.crt**.


How to create a self-signed cert
................................

SimpleSAMLphp requires a cert to work. If you haven't got one, you can create a self-signed cert and use it (require openssl).

Using OpenSSL we will generate a self-signed certificate in 3 steps.

* Generate private key:

.. code-block:: none

	$ openssl genrsa -out server.pem 1024

* Generate CSR: (In the "Common Name" set the domain of your instance)

.. code-block:: none

	$ openssl req -new -key server.pem -out server.csr

* Generate Self Signed Cert:

.. code-block:: none

	$ openssl x509 -req -days 365 -in server.csr -signkey server.pem -out server.crt

At the end of the process you will get server.csr (certificate signing request), server.pem (private key) and server.crt (self signed cert)


Configure SimpleSAMLphp
.......................

The simpleSAMLphp configuration files are in the folder **/etc/simplesamlphp/config/**.

First of all configure the followig parameters of the main file **/etc/simplesamlphp/config/config.php**

.. code-block:: none

	'auth.adminpassword' => 'secret'      # Set a new password for admin web interface
	'secretsalt' => 'secret',             # Set a Salt, in the config file there is documentation to generate it

	'technicalcontact_name' => 'Admin name',          # Set admin data
	'technicalcontact_email' => 'xxxx@example.com',

	'session.cookie.domain' => '.example.com',        # Set the global domain, to share cookie with the rest of componnets

	'language.available' => array('en', 'es'),        # Set the languages that the IdP will support (atm en and es)
	'language.rtl'          => array(),

In production environment set also those values:

.. code-block:: none

	'admin.protectindexpage'        => true,    # To protect the index page of simpleSAMLphp
	'debug'                 =>      FALSE,
	'showerrors'            =>      FALSE,      # To hide error-trace

Review the nginx configuration **/etc/nginx/conf.d/idp.conf**, you will see that simplesamlphp will be available at
https://idp.example.com/simplesaml (make sure that nginx and the php-fpm service are running)

Configure the authentication backend of the IdP. In this case we use admin and ldap as authentication backend. 
We must configure the simplesamlphp authsource config file **/etc/simplesamlphp/config/authsources.php**

.. code-block:: php

	<?php

	$config = array(

		  // This is a authentication source which handles admin authentication.
		  'admin' => array(
		          'core:AdminPassword',
		  ),

		  'ldap' => array(
		          'ldap:LDAP',

		          'hostname' => 'idp.example.com',
		          'enable_tls' => FALSE,             # We don't use TLS, for production enviroment you can config the LDAP Server 
													 # with TLS and enable this param
		          'debug' => FALSE,
		          'timeout' => 0,

		          'attributes' => NULL,              # To retrieve all atributes from the LDAP

		          'dnpattern' => 'mail=%username%,ou=People,dc=example,dc=com',
		          'search.enable' => FALSE,
		          'search.base' => 'ou=People,dc=example,dc=com',

		          // The attribute(s) the username should match against.
		          // This is an array with one or more attribute names. Any of the attributes in
		          // the array may match the value the username.
		          'search.attributes' => array('mail'),

		          // The username & password the simpleSAMLphp should bind to before searching. If
		          // this is left as NULL, no bind will be performed before searching.
		          'search.username' => NULL,
		          'search.password' => NULL,

		          'priv.read' => FALSE,
		          'priv.username' => NULL,
		          'priv.password' => NULL,
		  ),
	);

	?>


The metadata of the IdP is configured at **/var/lib/simplesamlphp/metadata/saml20-idp-hosted.php**, no need any change, thee host and the entityID is automaticaly generated.

.. code-block:: php

	$metadata['__DYNAMIC:1__'] = array(
		/*
		 * The hostname of the server (VHOST) that will use this SAML entity.
		 *
		 * Can be '__DEFAULT__', to use this entry by default.
		 */
		'host' => '__DEFAULT__',

		/* X.509 key and certificate. Relative to the cert directory. */
		'privatekey' => 'server.pem',
		'certificate' => 'server.crt',

		/*
		 * Authentication source to use. Must be one that is configured in
		 * 'config/authsources.php'.
		 */
		'auth' => 'ldap',

		/* Uncomment the following to use the uri NameFormat on attributes. */
		/*
		'attributes.NameFormat' => 'urn:oasis:names:tc:SAML:2.0:attrname-format:uri',
		*/

		// This filter eliminate the userPassword from the metadata that will be sent to the diferents components
		'authproc' => array(
			10 => array(
				'class' => 'core:PHP',
				'code' => '
			                  if (isset($attributes["userPassword"])) {
			                          unset($attributes["userPassword"]);
			                  }
				',
			),
		),
	);

Now we can access to https://idp.example.com/simplesaml/module.php/core/authenticate.php?as=ldap and test the LDAP source (use the credentials of the testuser that we created on ldap previously (review the "section: configure ldap").


Configure the cron module and add a crontab
...........................................

In SAML Identity Federations the IdP must know the metadata of the components (SPs) connected with it. In order to get this metadata in dynamic way we use the metarefresh module. This module will get the metadata of the differents componets that build the OpenMOOC platform.

The file to configure the cron module is **/etc/simplesamlphp/config/module_cron.php**, you must edit that file and
set a secure value for the **key** parameter

Then create a crontab for execute the metarefresh task.

Create the file **/etc/cron.d/metarefresh** with the following content:

.. code-block:: php

	01 * * * * root curl --silent "https://idp.example.com/simplesaml/module.php/cron/cron.php?key=<secret>&tag=metarefresh" > /dev/null 2>&1

Replace the **<secret>** with the value that you previously set on the cron module configuration's file.



Configure the metarefresh module
................................


This module is required in order import and keep update the metadata of the SPs connected to this IdP. Lets add the metadata of several componets (MoocNG, Askbot, MoinMoin, etc), each dynamic metadata will be stored in differents folders, at the parent folder
**/var/lib/simplesamlphp/metadata/**.

Lets explain how add a MoocNG and Askbot metadata. First of all we need the directories with writable permission for nginx
(nginx should be in simplesamlphp group):

.. code-block:: none

	mkdir /var/lib/simplesamlphp/metadata/askbots/
	mkdir /var/lib/simplesamlphp/metadata/moocng/
	chown -R root:simplesamlphp /var/lib/simplesamlphp/metadata


We based the metarefresh module config file **/etc/simplesamlphp/config/config-metarefresh.php** on **/etc/simplesamlphp/config/openmooc_components.php**, so we only need to edit that last file and add there the component name and the url where is its metadata.
(For complex metarefresh configurations, create your own metarefresh configuration file based on **/usr/lib64/simplesamlphp/modules/metarefresh/config-templates/**, documentation is available `here <http://simplesamlphp.org/docs/stable/simplesamlphp-automated_metadata#section_5>`_)

In the example, our openmooc_components.php file look like:

.. code-block:: php

	<?php

	$components =  array (
		array ('moocng' => 'https://example.com/auth/saml2/metadata/') ,
		array ('askbot' => 'https://askbots.example.com/m/group-metadata.xml') ,
	);

You can learn more about how to configure a simpleSAMLphp IdP at `this documentation <http://simplesamlphp.org/docs/stable/simplesamlphp-idp>`_


Userregistration
----------------

This is a simpleSAMLphp module that let you register and manage users.

The config file of this module is **/etc/simplesamlphp/config/module_userregistration.php** that should be similar to:

.. code-block:: php

	<?php
	/**
	 * The configuration of userregistration module
	 */

	$config = array (

		/* The authentication source that should be used. */
		'auth' => 'ldap',

		/* The authentication source for admin views. */
		'admin.auth' => 'admin',

		// Realm for eduPersonPrincipalName
		'user.realm' => 'example.com',

		// Usen in mail and on pages
		'system.name' => 'OpenMOOC User registration',

		// Mail options
		'mail' => array(
		    'token.lifetime' => (3600*24*6),
		    'from'     => 'OpenMOOC <no-reply@example.com>',
		    'replyto'  => 'OpenMOOC <no-reply@example.com>',
		    'subject'  => 'OpenMOOC - verification',
		    'admin_create_subject'  => 'OpenMOOC - user account created',
		    'admin_modify_subject'  => 'OpenMOOC - user account modified',
		),

		// URL of the Terms of Service
		'tos' => 'https://idp.example.com/simplesaml/module.php/userregistration/TOS.txt',

		// To enable/disable navigation links in the module block
		'custom.navigation' => TRUE,

		// User storage backend selector
		'storage.backend' => 'LdapMod',

		// LDAP backend configuration
		// This is configured in authsources.php
		// FIXME: The name of this arrays shoud be the same as storage.backend value
		'ldap' => array(
		    'admin.dn' => 'cn=admin,dc=example,dc=com',
		    'admin.pw' => '<ldaprootpw>',

		    // Storage User Id indicate which of the attributes
		    // that is the key in the storage
		    // This relates to the attributs mapping
		    'user.id.param' => 'mail',

		    // Password encryption
		    // plain, md5, sha1
		    'psw.encrypt' => 'sha1',

		    // Field user to save the registration email of the user
		    'user.register.email.param' => 'mail',

		    // Fields that contain a valid email to recover the password
		    // (Sometimes is needed to be able to send recover password mail to a different email than the register email,
		    //  For example if the Mail-System of the registered mail is protected by the IdP)
		    'recover.pw.email.params' => array('mail'),

		    // Password policy
		    'password.policy' => array(
		        'min.length' => 5,
		        'require.lowercaseUppercase' => false,
		        'require.digits' => true,
		        // Require that password contains a non alphanumeric letter.
		        'require.any.non.alphanumerics' => false,
		        // Check if password contains the user values of the params of the array. Empty array to don't check
		        'no.contains' => array(),
		        // Dictionay filenames inside hooks folder. Empty array to don't check
		        'check.dicctionaries' => array(),
		    ),

		    // LDAP objectClass'es
		    'objectClass' => array(
		        'inetOrgPerson',
		        'organizationalPerson',
		        'person',
		        'top',
		        'eduPerson',
		        'irisPerson',
		        'norEduPerson'
		    ),

		    // Multivalued attributes we want to retrieve as arrays
		    'multivalued.attributes' => array(
		        'eduPersonAffiliation',
		        'irisMailAlternateAddress',
		    ),
		), // end Ldap config

		// AWS SimpleDB configuration

		// SQL backend configuration

		// Password policy enforcer
		// Inspiration and backgroud
		// http://www.hq.nasa.gov/office/ospp/securityguide/V1comput/Password.htm



		/*
		 * Mapping from the Storage backend field names to web frontend field names
		 */

		'attributes'  => array(
		    'sn' => 'sn',
		    'cn' => 'cn',
		    'mail' => 'mail',
		    'oldmail' => 'irisMailAlternateAddress',
		    // Set from password validataion and encryption
		    'userPassword' => 'userPassword',
		),

		/*
		 * Search options
		 */
		'search' => array(
		    'min_length' => 3, // Minimum string length allowed
		    'filter' => '*%STRING%*',
		    // Searchable attributes
		    // Use same names from recognized attributes (case sensitive)
		    'searchable' => array(
		        'cn',
		        'sn',
		        'mail',
		    ),
		    'pagination' => true,
		    'elems_per_page' => 20,
		),

		/*
		 * Configuration for the field in the web frontend
		 * This controlls the order of the fields
		 *
		 * Valid values for 'show', 'read_only' and 'optional' settings
		 *
		 * 'new_user': user tries to register by himself
		 * 'edit_user': user tries to update his account details
		 * 'admin_new_user': admin user creation form
		 * 'admin_edit_user': admin account modification form
		 * 'first_password': user is setting his own password after registering
		 * 'change_password': user is changing his password
		 * 'change_mail': user is changing his mail
		 */
		'formFields' => array(

		    // Surname (ldap: sn)
		    'sn' => array(
		        'validate' => FILTER_DEFAULT,
		        'layout' => array(
		            'control_type' => 'text',
		            'show' => array(
		                'new_user',
		                'edit_user',
		                'admin_new_user',
		                'admin_edit_user',
		            ),
		            'read_only' => array(
		                ),
		            ),
		        ), // end ename

		    // Common name: read only
		    'cn' => array(
		        'validate' => FILTER_DEFAULT,
		        'layout' => array(
		            'control_type' => 'text',
		            'size' => '35',
		            'show' => array(
		                'new_user',
		                'edit_user',
		                'admin_new_user',
		                'admin_edit_user',
		            ),
		            'read_only' => array(
		            ),
		        ),
		    ), // end cn

		    'mail' => array(
		        'validate' => FILTER_VALIDATE_EMAIL,
		        'layout' => array(
		            'control_type' => 'text',
		            'show' => array(
		                'new_user',
		                'edit_user',
		                'admin_new_user',
		                'admin_edit_user',
		            ),
		            'read_only' => array(
		                'edit_user',
		            ),
		        ),
		    ), // end mail

		    'eduPersonAffiliation' => array(
		        'validate' => array(
		            'filter' => FILTER_DEFAULT,
		            'flags' => FILTER_REQUIRE_ARRAY,
		        ),
		        'layout' => array(
		            'control_type' => 'multivalued',
		            'show' => array(
		                'admin_new_user',
		                'admin_edit_user',
		            ),
		            'read_only' => array(
		            ),
		        ),
		    ), // end eduPersonAffiliation

		    'userPassword' => array(
		        'validate' => FILTER_DEFAULT,
		        'layout' => array(
		            'control_type' => 'password',
		            'show' => array(
		                'first_password',
		                'change_password',
		                'admin_new_user',
		                'admin_edit_user',
		            ),
		            'read_only' => array(
		            ),
		            'optional' => array(
		                'admin_edit_user',
		            ),
		        ),
		    ),

		    'pw1' => array(
		        'validate' => FILTER_DEFAULT,
		        'layout' => array(
		            'control_type' => 'password',
		            'show' => array(
		                'change_password',
		                'admin_new_user',
		                'admin_edit_user',
		            ),
		            'read_only' => array(
		            ),
		            'optional' => array(
		                'admin_edit_user',
		            ),
		        ),
		    ),

		    'pw2' => array(
		        'validate' => FILTER_DEFAULT,
		        'layout' => array(
		            'control_type' => 'password',
		            'show' => array(
		                'change_password',
		                'admin_new_user',
		                'admin_edit_user',
		            ),
		            'read_only' => array(
		            ),
		            'optional' => array(
		                'admin_edit_user',
		            ),
		        ),
		    ),
		    'oldpw' => array(
		        'validate' => FILTER_DEFAULT,
		        'layout' => array(
		            'control_type' => 'password',
		            'show' => array(
		                'change_password',
		            ),
		            'read_only' => array(
		            ),
		        ),
		    ),
		    'newmail' => array(
		        'validate' => FILTER_VALIDATE_EMAIL,
		        'layout' => array(
		            'control_type' => 'text',
		            'show' => array(
		                'change_mail',
		            ),
		            'read_only' => array(
		            ),
		        ),
		    ), 
		),

		// Known mail services
		// Used to show a direct link to the inbox after registering a new account
		'known.email.providers' => array(
			array(
				'name' => 'GMail',
				'regexp' => '/g(oogle)?mail.com/',
				'url' => 'http://www.gmail.com',
				'image' => 'gmail.png',
			),

			array(
				'name' => 'Outlook',
				'regexp' => '/(hotmail|outlook).com/',
				'url' => 'http://www.outlook.com',
				'image' => 'outlook.png',
			),
		),

		// Extra storage. Use redis, mongodb
		'extraStorage.backend' => 'mongodb',
		// Redis connection
		'redis' => array(
			'scheme' => 'tcp',
			'host'   => '127.0.0.1',
			'port'   => 6379,
		),
		'mongodb' => array(
			'scheme' => 'mongodb',
			'host'   => '127.0.0.1',
			'port'   => 27017,
			'database' => 'idp',
		),
	);

In OpenMOOC we use mongodb so you must change the 'extraStorage.backend' and set mongodb
(review that the mongodb service is running [service mongod start])

The attributes used on the userregistration module are registered at the value 'attributes'.
The forms, that the module displays, depends on the 'formFields' array.  Configure it conveniently

Configure the 'ldap' params: ldap credentials ('admin.dn', 'admin.pw'), the fieldname used to identify the
entity ('user.id.param', OpenMOOC uses the 'mail')

There is an extense documentation about `how configure the userregistration module <https://github.com/OpenMOOC/userregistration/blob/master/doc/configuration.md>`_


In case that you require that 3rd party elements interact with the userregistration module you will need to configure the API config file
**/etc/simplesamlphp/config/module_userregistration-api.php** setting a 'api.key' and enabling the actions that you require.


SSPOpenMOOC
-----------

This is a simpleSAMLphp module theme for OpenMOOC.

Edit the configuration file of sspopenmooc **/etc/simplesamlphp/config/module_sspopenmooc.php**
where you can personalize your OpenMOOC environment: Define the urls, style and some texts.

.. code-block:: php

	<?php

	// Domain of our MoocNG component
	$mooc_domain = 'mooc.example.com';

	// Domain of the IdP
	$idp_domain = 'idp.example.com';

	$config = array(

		  'urls' => array (
		          'site' => 'https://'.$mooc_domain,
		          'login' => "https://$mooc_domain/saml2/login/",
		          'logout' => "https://$mooc_domain/saml2/logout/",
		          'register' => "https://$idp_domain/simplesaml/module.php/userregistration/newUser.php",
		          'forgotpassword' => "https://$idp_domain/simplesaml/module.php/userregistration/lostPassword.php",
		          'changepassword' => "https://$idp_domain/simplesaml/module.php/userregistration/changePassword.php",
		          'profile' => "https://$idp_domain/simplesaml/module.php/userregistration/reviewUser.php",
		          'legal' => "https://$mooc_domain/legal",
		          'tos' => "https://$mooc_domain/legal/#tos",
		          'copyright' => "#",
		  ),

		  // Internal file (Ex.  default.css)  or external (Ex. //example.com/css/default.css)
		  // (Notice that // will respect the http/https protocol,
		  //  load elements with different protocol than main page produce warnings on some browser)
		  'cssfile' => 'default.css',
		  'bootstrapfile' => 'bootstrap.css',
		  'imgfile' => 'logo.png',
		  'title' => 'OpenMOOC',
		  'slogan' => 'Knowledge for the masses',
	);
	?>


How to config SMTP Server
-------------------------

The OpenMOOC platform require a SMTP server and we can deploy our own SMTP server on the IdP.

We use postfix, configure it at  **/etc/postfix/main.cf**:

.. code-block:: none

	inet_interfaces = all
	inet_protocols = all
	mynetworks = 127.0.0.1, XXX.XXX.XXX.XXX    # our IP

Then start the service and add it to the boot:

.. code-block:: none

	$ service postfix start
	$ chkconfig postfix on


We can test if postfix works sending a main to our mailbox:

.. code-block:: none

	mail <test_mail>

Note: If the mail command not exists install mailx   [yum install mailx]


If we deploy OpenMOOC componnents in diferents machines we can use the SMTP server of the IdP
for them. But don't forguet to enable the access on the SMTP server, adding the IPs
of the machines at the 'mynetworks' param.

Notice that instead deploy our own SMTP server we can use gmail as relay server. Check `this guide <http://charlesa.net/tutorials/centos/centosgmail.php>`_


Sync clock
----------

To get Saml2 run correctly we need have sure that all machine's clock are synced.

We propose configure idp as central clock and allow other systems clocks sync through idp.

Install ntp package over all systems (idp, questions, moocng, ...)

We go to configure idp as central clock:


Idp ntp clock server
....................

Edit **/etc/ntp.conf** and change the follow properties according to this values. We use ntp server for UK because linode datacenter is in UK.

.. code-block:: none

	rescrict 0.0.0.0

	server 0.uk.pool.ntp.org
	server 1.uk.pool.ntp.org
	server 2.uk.pool.ntp.org
	server 3.uk.pool.ntp.org

Enable ntp service and run it.

.. code-block:: none

	$ chkconfig ntpd on
	$ service ntpd start

If you have iptables fully configured you need allow ntpd (tcp/udp 123) access in iptables firewall. The follow block is a iptable file format example, set correct IP values for IP_IDP, IP_ASKBOTS, IP_MOOCNG:

.. code-block:: none

	-A INPUT -m state --state NEW -m tcp -p tcp -s IP_IDP --dport 123 -j ACCEPT
	-A INPUT -m state --state NEW -m udp -p udp -s IP_IDP --dport 123 -j ACCEPT
	-A INPUT -m state --state NEW -m tcp -p tcp -s IP_ASKBOTS --dport 123 -j ACCEPT
	-A INPUT -m state --state NEW -m udp -p udp -s IP_ASKBOTS --dport 123 -j ACCEPT
	-A INPUT -m state --state NEW -m tcp -p tcp -s IP_MOOCNG --dport 123 -j ACCEPT
	-A INPUT -m state --state NEW -m udp -p udp -s IP_MOOCNG --dport 123 -j ACCEPT

Reload iptables service to apply changes:

.. code-block:: none

	$service iptables reload


Sync others clocks systems with IDP clock
.........................................

Install ntpd package, configure ntp through the file **/etc/ntp.conf**

Change servers and set it according to our configuration (set idp.example.com name according to your idp ns name).

.. code-block:: none

	server idp.example.com
	server 0.uk.pool.ntp.org
	server 1.uk.pool.ntp.org
	server 2.uk.pool.ntp.org
	server 3.uk.pool.ntp.org

Enable service ntpd and start it
