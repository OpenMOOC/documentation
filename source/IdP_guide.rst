=============================================================
Install and configure an IdP (Identity Provider) for OpenMOOC
=============================================================

This documentation explain how to install and configure the IdP instance on a CentOS (require root account).

For the rest of the explanation we will consider that our service will be displayed at **idp.example.com**


SELinux and firewall
====================

In a development enviroment you can disable both:

.. code-block:: bashe

   lokkit --selinux=disabled
   lokkit --disabled

In a production enviroment contact a sysadmin to configure correctly SELinux.


Deploy OpenLDAP
===============

Here is a generic guide about `How to deploy OpenLDAP <http://www.centos.org/docs/5/html/Deployment_Guide-en-US/s1-ldap-quickstart.html>`_ if you need more info.  Following are the steps to deploy OpenLDAP that we use at OpenMOOC deployment:

Edit the hosts file and add the host of your LDAP: (in our case we add 'idp.example.com' at the 127.0.0.1 and the IP entry)::

  # vim /etc/hosts

  Something similar to

  127.0.0.1       localhost.localdomain   localhost idp.example.com
  ::1             localhost6.localdomain6 localhost6 idp.example.com
  XXX.XXX.XXX.XXX localhost.localdomain localhost idp.example.com


Install the packages:

.. code-block:: bash

   yum install openldap openldap-clients openldap-servers

Copy the CONFIG_BASE file:

.. code-block:: bash

   cp /usr/share/openldap-servers-xxxx/DB_CONFIG.example /var/lib/ldap/DB_CONFIG

Edit the ldap config file ``/etc/openldap/ldap.conf``: ::

  URI ldap://XXX.XXX.XXX.XXX/    # put the correct IP
  BASE dc=example,dc=com

Create the root password:

.. code-block:: bash

   slappasswd

Create the config file (``/etc/openldap/slapd.conf``): ::

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


As you can see we use new schemas that not exists in the basic LDAP installation.
You may copy them and store them with the following names on the schemes directory (``/etc/openldap/schema``)

* `eduperson.schema <https://spaces.internet2.edu/display/macedir/OpenLDAP+eduPerson>`_
* `iris.schema <http://www.rediris.es/ldap/esquemas/iris.schema>`_
* `schac.schema <http://www.terena.org/activities/tf-emc2/docs/schac/schac-20061212-1.3.0.schema.txt>`_

Delete the old slap.d directory to avoid conflicts with our new configuration:

.. code-block:: bash

   rm -rf /etc/openldap/slapd.d


Start and stop the LDAP server:

.. code-block:: bash

   service slapd start
   service  slapd stop

Create the root-path file (``/etc/openldap/root.ldif``): ::

  dn: dc=example,dc=com
  dc: example
  description: LDAP Admin
  objectClass: dcObject
  objectClass: organizationalUnit
  ou: rootobject

Create the people-path file (``/etc/openldap/people.ldif``): ::

  dn: ou=People,dc=idp,dc=example,dc=com
  ou: People
  description: Users
  objectClass: organizationalUnit

Create a testuser file to be imported: (``/etc/openldap/testuser.ldif``): ::

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

.. code-block:: bash

   slapadd -l /etc/openldap/root.ldif -f slapd.conf -d 10
   slapadd -l /etc/openldap/people.ldif -f slapd.conf -d 10
   slapadd -l /etc/openldap/testuser.ldif -f slapd.conf -d 10

Start the server:

.. code-block:: bash

   service slapd start


If restarting the server, warnings appear, change the permissions on the LDAP directory and restart LDAP to check that warnings disssapear:

.. code-block:: bash

   chown -R ldap:ldap /var/lib/ldap/
   service slapd restart

Add the service to the system boot:

.. code-block:: bash

   chkconfig slapd on


We can create a backup script and insert it in our crontab:


For example, this will create a backup of the LDAP at the /var/backups/ folder

.. code-block:: bash

slapcat | /usr/bin/bzip2 > /var/backups/ldap_`/bin/date +%Y-%m-%d-%H-%M-%S`.ldif.bz2

We can save this script as backup_ldap.sh in the simplesamlphp folder or wherever we want, give this file execution permission and add it to the cron. 
(`/etc/cron.d/backup_ldap`)::

  00 3 * * *      <path-to-the-folder-that-contain-the-script>/backup_ldap.sh

Restart the crond service:

.. code-block:: bash

   service crond restart



Deploy and configure phpldapadmin (not mandatory)
=================================================

`phpldapadmin <http://phpldapadmin.sourceforge.net/wiki/index.php/Main_Page>`_ is a tool that let us manage our ldap using a web.

We need an apache server for the phpldapadmin so if it is not already at the system, we install and start it:

.. code-block:: bash

   yum install httpd
   service httpd start
   chkconfig httpd on

Now we install phpldapadmin:

.. code-block:: bash

 i386 --> yum install http://dl.fedoraproject.org/pub/epel/6/i386/phpldapadmin-1.2.2-3.gitbbedf1.el6.noarch.rpm 
 x86_64   --> yum install http://dl.fedoraproject.org/pub/epel/6/x86_64/phpldapadmin-1.2.2-3.gitbbedf1.el6.noarch.rpm 

`If the file does not exist, search the phpldapadmin rpm on the `epel directory <http://dl.fedoraproject.org/pub/epel/6/>`_

Then we edit the config file (``/etc/phpldapadmin/config.php``) and we set those values: ::

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

To allow global access to our phpldapadmin we config its apache file (``/etc/httpd/conf.d/phpldapadmin.conf``): ::

 Alias /phpldapadmin /usr/share/phpldapadmin/htdocs
 Alias /ldapadmin /usr/share/phpldapadmin/htdocs

 <Directory /usr/share/phpldapadmin/htdocs>
   Order Deny,Allow
   Allow from all
 </Directory>

Restart the apache server:

.. code-block:: bash

   service httpd restart

Now the phpldapadmin is accessible at http://idp.example.com/phpldapadmin, you can access it using your root user, so on username set
``cn=admin,dc=example,dc=com`` and the password is the one you have configured before.

You can use this tool to manage the data that users registered on the IdP.


IdP Core
========

The IdP Core is based on `simpleSAMLphp <http://simplesamlphp.org/>`_ and its modules. SimpleSAMLphp is an implementation of the SAML2 standar.
In order to use simpleSAMLphp in a secure way is required a SSL connection between each system. That mean that you will need a SSL cert per domain, or a wildcard cert for the global domain.

In development enviroments you can use self-signed certificates, for production we recommend to use certificates from recognized organizations to avoid that browsers sent to the users the "warnings notification about certs" for each domain, which can be very annoying.


How to create a self-signed cert
--------------------------------

SimpleSAMLphp requires a cert to work. If you haven't got one, you can create a self-signed cert and use it.

In order to generate a self-signed cert you need openssl:

.. code-block:: bash

   yum install openssl

Using OpenSSL we will generate a self-signed certificate in 3 steps.

* Generate private key:

.. code-block:: bash

   openssl genrsa -out server.pem 1024

* Generate CSR: (In the "Common Name" set the domain of your instance)

.. code-block:: bash

   openssl req -new -key server.pem -out server.csr

* Generate Self Signed Cert:

.. code-block:: bash

   openssl x509 -req -days 365 -in server.csr -signkey server.pem -out server.crt

At the end of the process you will get server.csr (certificate signing request), server.pem (private key) and server.crt (self signed cert)


Install and config SimpleSAMLphp
--------------------------------

First of all we install some simpleSAMLphp dependences and the subversion in roder to checkout the simpleSAMLphp:

.. code-block:: bash

   yum install subversion php-ldap php-mbstring php-xml mod_ssl

`We also need php-mcrypt that could be found at the epel repository (if those files dont't exist search them at the` `epel directory <http://dl.fedoraproject.org/pub/epel/6/>`_ `)`

.. code-block:: bash

 i386 --> yum install http://dl.fedoraproject.org/pub/epel/6/i386/libmcrypt-2.5.8-9.el6.i686.rpm
          yum install http://dl.fedoraproject.org/pub/epel/6/i386/mcrypt-2.6.8-9.el6.i686.rpm
 x86_64 --> yum install http://dl.fedoraproject.org/pub/epel/6/x86_64/libmcrypt-2.5.8-9.el6.x86_64.rpm
            yum install http://dl.fedoraproject.org/pub/epel/6/x86_64/php-mcrypt-5.3.3-1.el6.x86_64.rpm 

We will create in our apache server path a directory called ``idp`` where the simplesamlphp code will be placed:

.. code-block:: bash

   mkdir /var/www/idp

Get simpleSAMLphp code at the idp folder:

.. code-block:: bash
 
   svn co http://simplesamlphp.googlecode.com/svn/tags/simplesamlphp-1.9.0 simplesamlphp

Copy the default config file from the template directory:

.. code-block:: bash

   cp /var/www/idp/simplesamlphp/config-templates/config.php /var/www/idp/simplesamlphp/config/config.php

And configure some values: ::

   'auth.adminpassword' => 'secret'	 # Set a new password for admin web interface

   'enable.saml20-idp' => true,          # Enable ssp as IdP

   'secretsalt' => 'secret',		 # Set a Salt, in the config file there is documentation to generate it

   'technicalcontact_name' => 'Admin name',          # Set admin data
   'technicalcontact_email' => 'xxxx@example.com',

   'session.cookie.domain' => '.example.com',	     # Set the global domain, to share cookie with the rest of componnets 

   'language.available' => array('en', 'es'),     # Set the languages we will support for the platform (atm en and es)
   'language.rtl'          => array(),

In production environment set also those values: ::

   'admin.protectindexpage'        => true,    # To protect the index page of simpleSAMLphp
   'debug' 		   => 	   FALSE,
   'showerrors'            =>      FALSE,      # To hide error-trace

Change again permission for some directories, execute the following command at the simpleSAMLphp folder:

.. code-block:: bash

   chown -R apache:apache cert log data metadata

Add the following apache configuration: (``/etc/httpd/conf.d/idp.conf``)::

 <VirtualHost *:80>
     ServerName idp.example.com
     DocumentRoot /var/www/idp/simplesamlphp/www
     SSLProxyEngine On
     ProxyPreserveHost On
     Alias /simplesaml /var/www/idp/simplesamlphp/www
 </VirtualHost>

 <VirtualHost *:443>
     ServerName idp.example.com
     DocumentRoot /var/www/idp/simplesamlphp/www
     Alias /simplesaml /var/www/idp/simplesamlphp/www
     SSLEngine on
     SSLCertificateFile /var/www/idp/simplesamlphp/cert/server.crt
     SSLCertificateKeyFile /var/www/idp/simplesamlphp/cert/server.pem
 </VirtualHost>

Restart the apache server:

.. code-block:: bash

   service httpd restart

Open a browser, access ``https://idp.example.com/simplesaml`` and check that simplesamlphp works.

Use the LDAP as our auth source backend, so we must configure it in the simplesamlphp authsource config file ``/var/www/idp/simplesamlphp/config/authsources.php``:

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
                'enable_tls' => FALSE,             # We don't use TLS, for production enviroment you can config the LDAP Server with TLS and 						          # enable this param

                'debug' => FALSE,
                'timeout' => 0,

                'attributes' => NULL,		   # To retrieve all atributes from the LDAP

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

Save your SSL cert files at the cert folder (rename file names to server.crt and server.pem, overriding the existing files)


Now configure the metadata of the IdP. This is made at `/var/www/idp/simplesamlphp/metadata/saml20-idp-hosted.php`:

.. code-block:: php

  <?php

  $metadata['https://idp.example.com/simplesaml/saml2/idp/metadata.php'] = array(

    'host' => 'idp.example.com',

    'OrganizationName' => array(
        'en' => 'OpenMOOC',
    ),
    'OrganizationURL' => array(
        'en' => 'http://example.com',
    ),

    'certificate' => 'server.crt',
    'privatekey' => 'server.pem',

     // The authentication source for this IdP. Must be one
     // from config/authsources.php.
    'auth' => 'ldap',

    // Logout requests and logout responses sent from this IdP should be signed
    'redirect.sign' => TRUE,
    // All communications are encrypted
    'assertion.encryption' => TRUE,

    // This filter eliminate the userPassword from the metadata that will be sent to the diferents components
    'authproc' => array(
            100 => array(
                'class' => 'core:PHP',
                'code' => '
                        if (isset($attributes["userPassword"])) {
                                unset($attributes["userPassword"]);
                        }
                ',
            ),
    ),
  );

  ?>


Configure the cron and metarefresh module
-----------------------------------------

In SAML Identity Federations the IdP must know the metadata of the components (SPs) connected with it. In order to get this
metadata in dynamic way we use the metarefresh module. This module will get the metadata of the differents componets
that build the OpenMOOC platform.

Enable the metarefresh module and its dependences:

.. code-block:: bash
   touch /var/www/idp/simplesamlphp/modules/cron/enable
   touch /var/www/idp/simplesamlphp/modules/metarefresh/enable

Copy the sanitycheck config file:

.. code-block:: bash

   cp /var/www/idp/simplesamlphp/modules/sanitycheck/config-templates/config-sanitycheck.php /var/www/idp/simplesamlphp/config/config-sanitycheck.php


Configure the cron:

Create the cron config file (`/var/www/idp/simplesamlphp/config/module_cron.php`):

.. code-block:: php

 <?php

  $config = array (

  	'key' => 'secret',	# Set a password that will be used at the crontab call
  	'allowed_tags' => array('daily', 'hourly', 'frequent','metarefresh'),
  	'debug_message' => TRUE,
        'sendemail' => FALSE,
  );

 ?>


Add a crontab. Create ``/etc/cron.d/metarefresh``: ::

  01 * * * * root curl --silent "https://idp.example.com/simplesaml/module.php/cron/cron.php?key=secret&tag=metarefresh" > /dev/null 2>&1

You may replace the 'secret' with the one you configured at ``module_cron.php``

Set the crond at the boot and restart the crond: 

.. code-block:: bash

   chkconfig crond on
   service crond restart


Configure the metarefresh
-------------------------

This module is required in order import and keep update the metadata of the SPs connected to this IdP.
Lets add the metadata of 2 componets (Askbot and MoocNG), each dynamic metadata will be stored
in differents folders. Create `/var/www/idp/simplesamlphp/config/config-metarefresh.php`

.. code-block:: php

  <?php

  $config = array(

  	'sets' => array(

        	'askbots' => array(
                	'cron'          => array('metarefresh'),
                        'sources'       => array(
                                array(
                                        'src' => 'https://questions.example.com/m/group-metadata.xml',
                                ),
                        ),
                        'expireAfter'   => 60*60*24*4, // Maximum 4 day cache time.
                        'outputDir'     => 'metadata/askbots/',
                        'outputFormat' => 'flatfile',
                ),
                'moocng' => array(
                        'cron'          => array('metarefresh'),
                        'sources'       => array(
                                array(
                                        'src' => 'https://moocng.example.com/saml2/metadata/',
                                ),
                        ),
                        'expireAfter'   => 60*60*24*4, // Maximum 4 day cache time.
                        'outputDir'     => 'metadata/moocng/',
                        'outputFormat' => 'flatfile',
                ),
        ),
  );

  ?> 

Now create the folders where metadata will be stored:

.. code-block:: bash

   mkdir /var/www/idp/simplesamlphp/metadata/askbots/
   mkdir /var/www/idp/simplesamlphp/metadata/moocng/


Change permission for metadata folder:

.. code-block:: bash

   chown -R apache:apache  metadata

Now we need that simpleSAMLphp read those imported metadata, we edit the ssp config file (``/var/www/idp/simplesamlphp/config/config.php``): ::

  'metadata.sources' => array(
  	array('type' => 'flatfile'),
        array('type' => 'flatfile', 'directory' => 'metadata/askbots'),
        array('type' => 'flatfile', 'directory' => 'metadata/moocng'),
  ),


Restart the apache server:

.. code-block:: bash

   service httpd restart


Now we can access to `https://idp.example.com/simplesaml/module.php/core/authenticate.php?as=ldap <https://idp.example.com/simplesaml/module.php/core/authenticate.php?as=ldap>`_ and test the LDAP source (use the credentials of the testuser).


You can learn more about how to configure a simpleSAMLphp IdP at `http://simplesamlphp.org/docs/stable/simplesamlphp-idp <http://simplesamlphp.org/docs/stable/simplesamlphp-idp>`_


Userregistration
================

This is a simpleSAMLphp module that let you register and manage users. 

Put it at the modules folder:

.. code-block:: bash

   cd /var/www/idp/simplesamlphp/modules
   git clone https://github.com/OpenMOOC/userregistration.git

`If you dont have git, install it with  # yum install git`


Create the userregistration configuration file ``/var/www/idp/simplesamlphp/config/module_userregistration.php``: 

.. code-block:: php

  <?php

  $config = array (

        'auth' => 'ldap',
        'user.realm' => 'idp.example.com',
        'system.name' => 'OpenMOOC',

        // Mailtoken valid for 5 days
        'mailtoken.lifetime' => (3600*24*6),
        'mail.from'     => 'OpenMOOC <no-reply@example.com>',
        'mail.replyto'  => 'OpenMOOC <no-reply@example.com>',
        'mail.subject'  => 'OpenMOOC - verification',

        // URL of the Terms of Service
        'tos' => 'https://idp.example.com/simplesaml/module.php/userregistration/TOS.txt',

        'custom.navigation' => TRUE,   // Let it as TRUE

        'storage.backend' => 'LdapMod',

        // LDAP backend configuration
        // This is configured in authsources.php
        // FIXME: The name of this arrays shoud be the same as storage.backend value
        'ldap' => array(
                'admin.dn' => 'cn=admin,dc=example,dc=com',
                'admin.pw' => 'secret_ldap_adminpassword',   // Set the correct ldap admin password

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
                        'person',
                        'top',
                        'eduPerson',
                ),
        ), // end Ldap config

        // AWS SimpleDB configuration

        // SQL backend configuration

        // Password policy enforcer
        // Inspiration and backgroud
        // http://www.hq.nasa.gov/office/ospp/securityguide/V1comput/Password.htm

        // Mapping from the Storage backend field names to web frontend field names
        // This also indicate which user attributes that will be saved
        'attributes'  => array(
                'cn' => 'cn',
                'sn' => 'sn',
                'mail' => 'mail',
        ),

        // Configuration for the field in the web frontend
        // This controlls the order of the fields
        'formFields' => array(
                'cn' => array(
                    'validate' => FILTER_DEFAULT,
                    'layout' => array(
                        'control_type' => 'text',
                        'show' => true,
                        'read_only' => false,
                        'size' => '35',
                    ),
                ),
                'sn' => array(
                        'validate' => FILTER_DEFAULT,
                        'layout' => array(
                                'control_type' => 'text',
                                'show' => true,
                                'read_only' => false,
                        ),
                ),
                'mail' => array(
                        'validate' => FILTER_VALIDATE_EMAIL,
                        'layout' => array(
                                'control_type' => 'text',
                                'show' => false,
                                'read_only' => true,
                        ),
                ),
                'eduPersonAffiliation' => array(
                    'validate' => FILTER_DEFAULT,
                    'layout' => array(
                        'control_type' => 'text',
                        'show' => false,
                        'read_only' => true,
                    ),
                ),
                'userPassword' => array(
                        'validate' => FILTER_DEFAULT,
                        'layout' => array(
                                'control_type' => 'password',
                        ),
                ),
                'pw1' => array(
                        'validate' => FILTER_DEFAULT,
                        'layout' => array(
                                'control_type' => 'password',
                        ),
                ),
                'pw2' => array(
                        'validate' => FILTER_DEFAULT,
                        'layout' => array(
                                'control_type' => 'password',
                        ),
                ),
                'oldpw' => array(
                        'validate' => FILTER_DEFAULT,
                        'layout' => array(
                                'control_type' => 'password',
                        ),
                ),
        ),

  );

`There is a template of this file at /var/www/idp/simplesamlphp/modules/userregistration/config-templates/module_userregistration.php`


Enable de module:

.. code-block:: bash

   touch /var/www/idp/simplesamlphp/modules/userregistration/enable


SSPOpenMOOC
===========

This is a simpleSAMLphp module theme for OpenMOOC. 

Put it at the modules folder: 

.. code-block:: bash

   cd /var/www/idp/simplesamlphp/modules
   git clone https://github.com/OpenMOOC/sspopenmooc.git


Create the config file of sspopenmooc ``/var/www/idp/simplesamlphp/config/module_sspopenmooc.php``:

.. code-block:: php

  <?php

  // Domain of our MoocNG component
  $mooc_domain = 'demo.example.com';

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

`There is a template of that file at /var/www/idp/simplesamlphp/modules/sspopenmooc/config-templates/module_sspopenmooc.php`


simpleSAMLphp themes must be activated at the main config file. In order activate this theme, edit `/var/www/idp/simplesamlphp/config/config.php`: ::

  'theme.use' => 'sspopenmooc:openmooc',


Cookie Integration
------------------

At the base folder of sspopenmooc exists a patch that must be applied to simplesamlphp. This patch make that simpleSAMLphp
write the language information in the global cookie.

Copy the patch to simpleSAMLphp folder and apply it:

.. code-block:: bash

   cp /var/www/idp/simplesamlphp/modules/sspopenmooc/session_logged_patch.diff /var/www/idp/simplesamlphp/session_logged_patch.diff
   cd /var/www/idp/simplesamlphp/
   patch -p0 < session_logged_patch.diff

`If you don't have the patch library, install it  #  yum install patch`

Notice that this patch applies only to the tag of simpleSAMLphp 1.9  and only works for the .openmooc.org domain.

After apply this patch you will need to edit the ``lib/SimpleSAML/XHTML/Template.php`` and search ".openmooc.org" and replace it with the domain you will use. In this example ".example.com"


How to config SMTP Server
=========================

The OpenMOOC platform require a SMTP server.

We can deploy our own SMTP server on the IdP.

* Install postfix:

.. code-block:: bash

   yum install postfix

* Config postfix (``/etc/postfix/main.cf``):

.. code-block:: bash

  inet_interfaces = all
  inet_protocols = all
  mynetworks = 127.0.0.1, XXX.XXX.XXX.XXX    # our IP

* Start the service and add it to the boot:

.. code-block:: bash

   service postfix start
   chkconfig postfix on


If we deploy OpenMOOC componnents in diferents machines we can use the SMTP server of the IdP for them.
But don't forguet to enable the access on the SMTP server, adding the IPs of the machines at the 'mynetworks' param.


Notice that instead deploy our own SMTP server we can use gmail as relay server. Check `this guide <http://charlesa.net/tutorials/centos/centosgmail.php>`_


We can test if postfix works sending a main to our mailbox:

.. code-block:: bash

   mail <test_mail>



Sync clock settings
===================

To get Saml2 run correctly we need have sure that all machine's clock are
synced.

We propose configure idp as central clock and allow other systems clocks sync
through idp.

Install ntp package over all systems (idp, questions, moocng, ...)

We go to configure idp as central clock:


Idp ntp clock server
--------------------

Edit ``/etc/ntp.conf`` and change the follow properties according to this values.
We use ntp server for UK because linode datacenter is in UK.

.. code-block:: bash

   rescrict 0.0.0.0

   server 0.uk.pool.ntp.org
   server 1.uk.pool.ntp.org
   server 2.uk.pool.ntp.org
   server 3.uk.pool.ntp.org


Enable ntp service and run it.

.. code-block:: bash

    chkconfig ntpd on
    service ntpd start


If you have iptables fully configured you need allow ntpd (tcp/udp 123) access
in iptables firewall. The follow block is a iptable file format example, set
correct IP values for IP_IDP, IP_ASKBOTS, IP_MOOCNG:

.. code-block:: bash

   -A INPUT -m state --state NEW -m tcp -p tcp -s IP_IDP --dport 123 -j ACCEPT
   -A INPUT -m state --state NEW -m udp -p udp -s IP_IDP --dport 123 -j ACCEPT
   -A INPUT -m state --state NEW -m tcp -p tcp -s IP_ASKBOTS --dport 123 -j ACCEPT
   -A INPUT -m state --state NEW -m udp -p udp -s IP_ASKBOTS --dport 123 -j ACCEPT
   -A INPUT -m state --state NEW -m tcp -p tcp -s IP_MOOCNG --dport 123 -j ACCEPT
   -A INPUT -m state --state NEW -m udp -p udp -s IP_MOOCNG --dport 123 -j ACCEPT


Reload iptables service to apply changes:

.. code-block:: bash

   service iptables reload


Sync others clocks systems with IDP clock
----------------------------------------

Install ntpd package

Configure ntp through the file ``/etc/ntp.conf``

Change servers and set it according to our configuration (set idp.example.com
name according to your idp ns name).

.. code-block:: bash

   server idp.example.com
   server 0.uk.pool.ntp.org
   server 1.uk.pool.ntp.org
   server 2.uk.pool.ntp.org
   server 3.uk.pool.ntp.org


Enable service ntpd and start it
