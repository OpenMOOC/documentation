=============================================================
Install and configure an IdP (Identity Provider) for OpenMooc
=============================================================

This documentation explain how to install and configure the IdP instance on a CentOS (require root account).

For the rest of the explanation we will consider that our service will be displayed at **idp.openmooc.org**


Selinux and Firewall
====================

In a development enviroment you can disable both: ::

  # lokkit --selinux=disabled
  # lokkit --disabled

In a production enviroment contact a sysadmin to configure correctly Selinux.


Deploy OpenLDAP
===============

Here is a generic guide about `howto deploy OpenLDAP <http://www.centos.org/docs/5/html/Deployment_Guide-en-US/s1-ldap-quickstart.html>`_ if you need more info.  Following are the steps to deploy OpenLDAP that we use at OpenMooc deployment:

We edit the host file and add the host of our ldap: (in our case we add 'openmooc.org' at the 127.0.0.1 and the IP entry)::

  # vim /etc/hosts

  Something similar to

  127.0.0.1       localhost.localdomain   localhost openmooc.org
  ::1             localhost6.localdomain6 localhost6 openmooc.org
  XXX.XXX.XXX.XXX localhost.localdomain localhost openmooc.org


We install the packages: ::

  # yum install openldap openldap-clients openldap-servers

We copy the CONFIG_BASE file: ::

  # cp /usr/share/openldap-servers-xxxx/DB_CONFIG.example /var/lib/ldap/DB_CONFIG

We edit the ldap config file ``/etc/openldap/ldap.conf``: ::

  URI ldap://XXX.XXX.XXX.XXX/    # put the correct IP
  BASE dc=openmooc,dc=org

We create the root password: ::

  # slappasswd

We edit the config file (``/etc/openldap/slapd.conf``): ::

  include         /etc/openldap/schema/core.schema
  include         /etc/openldap/schema/cosine.schema
  include         /etc/openldap/schema/inetorgperson.schema
  include         /etc/openldap/schema/nis.schema
  include     /etc/openldap/schema/eduperson.schema
  include     /etc/openldap/schema/schac.schema
  include     /etc/openldap/schema/iris.schema

  allow bind_v2

  TLSCACertificateFile /etc/pki/tls/certs/ca-bundle.crt
  TLSCertificateFile /etc/pki/tls/certs/slapd.pem
  TLSCertificateKeyFile /etc/pki/tls/certs/slapd.pem
  pidfile     /var/run/openldap/slapd.pid
  argsfile    /var/run/openldap/slapd.args

  database    bdb
  suffix      "dc=openmooc,dc=org"
  rootdn      "cn=admin,dc=openmooc,dc=org"
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

Remember to remplace the <secretpassword> by the ldap root password.


As you can see we use new schemas that not exists in the basic ldap installation.
You may copy them and store them with the following names on the schemes directory (``/etc/openldap/schemes``)

* `eduperson.schema <https://spaces.internet2.edu/display/macedir/OpenLDAP+eduPerson>`_
* `iris.schema <http://www.rediris.es/ldap/esquemas/iris.schema>`_
* `schac.schema <http://www.terena.org/activities/tf-emc2/docs/schac/schac-20061212-1.3.0.schema.txt>`_

We delete the old slap.d directory to avoid conflicts with our new configuration: ::

  # rm -rf /etc/openldap/slapd.d


We start and stop the ldap server: ::

  # service slapd start
  # service  slapd stop

We create the root-path file (``/etc/openldap/root.ldif``): ::

  dn: dc=openmooc,dc=org
  dc: openmooc
  description: LDAP Admin
  objectClass: dcObject
  objectClass: organizationalUnit
  ou: rootobject

We create the people-path file (``/etc/openldap/people.lidf``): ::

  dn: ou=People,dc=openmooc,dc=org
  ou: People
  description: Users
  objectClass: organizationalUnit

We create a testuser file to be imported: (``/etc/openldap/testuser.lidf``)::
  # Entry 1: mail=testuser@openmooc.org,ou=People,dc=openmooc,dc=org
  dn: mail=testuser@openmooc.org,ou=People,dc=openmooc,dc=org
  cn: Test_cn
  edupersonaffiliation: student
  mail: testuser@openmooc.org
  objectclass: inetOrgPerson
  objectclass: person
  objectclass: top
  objectclass: eduPerson
  sn: Test_sn
  userpassword: testuser


We add the entries to the ldap: ::

 # slapadd -l /etc/openldap/root.ldif -f slapd.conf -d 10
 # slapadd -l /etc/openldap/people.ldif -f slapd.conf -d 10
 # slapadd -l /etc/openldap/testuser.ldif -f slapd.conf -d 10

We start the server: ::

 # service slapd start


If restarting the server, warnings appear, change the permissions on the ldap directory and restart ldap to check that warnings disssapear: ::

 # chown -R ldap:ldap /var/lib/ldap/
 # service slapd restart

Add the service to the system boot: ::

 # chkconfig slapd on


Deploy and configure phpldapadmin (not mandatory)
=================================================

`phpldapadmin <http://phpldapadmin.sourceforge.net/wiki/index.php/Main_Page>`_ is a tool that let us manage our ldap using a web.

We need an apache server for the phpldapadmin so if it is not already at the system, we install and start it: ::

 # yum install httpd
 # service httpd start
 # chkconfig httpd on

Now we install phpldapadmin: ::

 # yum install http://dl.fedoraproject.org/pub/epel/6/x86_64/phpldapadmin-1.2.2-1.el6.noarch.rpm

Then we edit the config file (``/etc/phpldapadmin/config.php``) and we set those values: ::

 $servers = new Datastore();
 $servers->newServer('ldap_pla');
 $servers->setValue('server','name','Mooc LDAP Server');
 $servers->setValue('server','host','127.0.0.1');
 $servers->setValue('server','port',389);
 $servers->setValue('server','base',array('dc=openmooc,dc=org'));
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

Restart the apache server: ::

 # service httpd restart

Now the phpldapadmin is accessible at http://openmooc.org/phpldapadmin, you can access it using your root user, so on username set
``cn=admin,dc=openmooc,dc`` and the password is the one you have configured before.

You can use this tool to manage the data that users registered on the IdP.


IdP Core
========

The IdP Core is based on `simpleSAMLphp <http://simplesamlphp.org/>`_ and its modules. SimpleSAMLphp is an implementation of the SAML2 standar.
In order to use simpleSAMLphp in a secure way is required a SSL connection between each system. That mean that you will need a SSL cert per domain, or a wildcard cert for the global domain.

In development enviroments you can use self-signed certificates, for production we recommend to use certificates from recognized organizations to avoid that browsers sent to the users the "warnings notification about certs" for each domain, which can be very annoying.


How to create a self-signed cert
--------------------------------

In order to generate a self-signed cert you need openssl: ::

 # yum install openssl

Using OpenSSL we will generate a self-signed certificate in 3 steps.

* Generate private key: ::

  # openssl genrsa -out cert.key 1024

* Generate CSR: (In the "Common Name" set the domain of your instance)::

  # openssl req -new -key cert.key -out cert.csr

* Generate Self Signed Key: ::

  # openssl x509 -req -days 365 -in cert.csr -signkey cert.key -out cert.crt


Install and config SimpleSAMLphp
================================

First of all we install some simpleSAMLphp dependences and the subversion in roder to checkout the simpleSAMLphp: ::

 # yum install subversion php-ldap php-mbstring php-xml mod_ssl


We will create in our apache server path a directory called ``idp`` where the simplesamlphp code will be placed: ::

 # mkdir /var/www/idp

We get simpleSAMLphp code at the idp folder: ::
 
 # svn co http://simplesamlphp.googlecode.com/svn/tags/simplesamlphp-1.9.0 simplesamlphp

We copy the default config file from the template directory: ::

 # cp /var/www/idp/simplesamlphp/config-templates/config.php /var/www/idp/simplesamlphp/config/config.php

And we configure some values: ::

   'auth.adminpassword' => 'secret'	 # We set a new password for admin web interface

   'enable.saml20-idp' => true,          # Enable ssp as IdP

   'secretsalt' => 'secret',		 # Set a Salt, in the config file there is documentation to generate it

   'technicalcontact_name' => 'Admin name',          # Set admin data
   'technicalcontact_email' => 'xxxx@openmooc.org',

   'session.cookie.domain' => '.openmooc.org',	     # We set the global domain, to share cookie with the rest of componnets 

   'language.available' => array('en', 'es'),     # We set the languages we will support for the platform (atm en and es)
   'language.rtl'          => array(),

We change again permission for some directories: ::

 # chown -R apache:apache cert log data metadata

We add the following apache configuration: (``/etc/httpd/conf.d/idp.conf``)::

 <VirtualHost *:80>
     ServerName idp.openmooc.org
     DocumentRoot /var/www/idp/simplesamlphp/www
     SSLProxyEngine On
     ProxyPreserveHost On
     Alias /simplesaml /var/www/idp/simplesamlphp/www
 </VirtualHost>

 <VirtualHost *:443>
     ServerName idp.openmooc.org
     DocumentRoot /var/www/idp/simplesamlphp/www
     Alias /simplesaml /var/www/idp/simplesamlphp/www
     SSLEngine on
     SSLCertificateFile /var/www/idp/simplesamlphp/cert/server.crt
     SSLCertificateKeyFile /var/www/idp/simplesamlphp/cert/server.pem
 </VirtualHost>

We restart the apache server: ::

 # service httpd restart

Open a browser, access ``https://idp.openmooc.org/simplesaml`` and check that simplesamlphp works.

We will use the ldap as our auth source backend, so we must configure it in the simplesamlphp authsource config file ``/var/www/idp/simplesamlphp/config/authsources.php``: ::

  <?php

  $config = array(

        // This is a authentication source which handles admin authentication.
        'admin' => array(
                'core:AdminPassword',
        ),

        'ldap' => array(
                'ldap:LDAP',

                'hostname' => 'openmooc.org',
                'enable_tls' => FALSE,             # We don't use TLS, for production enviroment you can config the LDAP Server with TLS and 						          # enable this param

                'debug' => FALSE,
                'timeout' => 0,

                'attributes' => NULL,		   # To retrieve all atributes from the LDAP

                'dnpattern' => 'mail=%username%,ou=People,dc=openmooc,dc=org',
                'search.enable' => FALSE,
                'search.base' => 'ou=People,dc=openmooc,dc=org',

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

Save your SSL cert files at the cert folder (rename file names to server.crt and server.key, overriding the existing files)


Now configure the metadata of the IdP. This is made at `/var/www/idp/simplesamlphp/metadata/saml20-idp-hosted.php`: ::

  <?php

  $metadata['https://idp.openmooc.org/simplesaml/saml2/idp/metadata.php'] = array(

    'host' => 'idp.openmooc.org',

    'OrganizationName' => array(
        'en' => 'OpenMooc',
        'es' => 'OpenMooc',
    ),
    'OrganizationURL' => array(
        'en' => 'http://openmooc.org',
        'es' => 'http://openmooc.org',
    ),

    'certificate' => 'server.crt',
    'privatekey' => 'server.key',

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


In SAML Identity Federations the IdP must know the metadata of the components (SPs) connected with it. In order to get this
metadata in dynamic way we use the metarefresh module. This module will get the metadata of the differents componets 
that build the OpenMooc platform.

Enable the metarefresh module and its dependences: ::

 # touch /var/www/idp/simplesamlphp/modules/cron/enable
 # touch /var/www/idp/simplesamlphp/modules/metarefresh/enable

Copy the sanitycheck config file: ::

 # cp /var/www/idp/simplesamlphp/modules/sanitycheck/config-templates/config-sanitycheck.php /var/www/idp/simplesamlphp/config/config-sanitycheck.php

Configure the cron: ::

 <?php

  $config = array (

  	'key' => 'secret',	# Set a password that will be used at the crontab call
  	'allowed_tags' => array('daily', 'hourly', 'frequent','metarefresh'),
  	'debug_message' => TRUE,
        'sendemail' => FALSE,
  );

 ?>


Configure the metarefresh, we add the metadata of 2 componnets (Askbot and MoocNG), each dynamic metadatas will be stored
in differents folders: ::
  <?php

  $config = array(

  	'sets' => array(

        	'askbots' => array(
                	'cron'          => array('metarefresh'),
                        'sources'       => array(
                                array(
                                        'src' => 'https://questions.openmooc.org/m/group-metadata.xml',
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
                                        'src' => 'https://demo.openmooc.org/saml2/metadata/',
                                ),
                        ),
                        'expireAfter'   => 60*60*24*4, // Maximum 4 day cache time.
                        'outputDir'     => 'metadata/moocng/',
                        'outputFormat' => 'flatfile',
                ),
        ),
  );

  ?> 

Now create the folders where metadata will be stored: ::

  # mkdir /var/www/idp/simplesamlphp/metadata/askbots/
  # mkdir /var/www/idp/simplesamlphp/metadata/moocng/


Change permission for metadata folder: ::

 # chown -R apache:apache  metadata

Now we need that simpleSAMLphp read those imported metadata, we edit the ssp config file (``/var/www/idp/simplesamlphp/config/config.php``): ::

  'metadata.sources' => array(
  	array('type' => 'flatfile'),
        array('type' => 'flatfile', 'directory' => 'metadata/askbots'),
        array('type' => 'flatfile', 'directory' => 'metadata/moocng'),
  ),


Restart the apache server: ::

 # service httpd restart


Now we can access to `https://idp.openmooc.org/simplesaml/module.php/core/authenticate.php?as=ldap <https://idp.openmooc.org/simplesaml/module.php/core/authenticate.php?as=ldap>`_ and test the ldap source (use the credentials of the testuser).


You can learn more about how to configure a simpleSAMLphp IdP at `http://simplesamlphp.org/docs/stable/simplesamlphp-idp <http://simplesamlphp.org/docs/stable/simplesamlphp-idp>`_


How to config SMTP Server
-------------------------

The OpenMooc platform require a SMTP server.

We can deploy our own SMTP server on the IdP.

 * Install postfix: ::

    # yum install postfix

 * Config postfix (``/etc/postfix/main.cf``): ::

    inet_interfaces = all
    inet_protocols = all
    mynetworks = 127.0.0.1, XXX.XXX.XXX.XXX    # our IP

 * Start the service and add it to the boot: ::

    # service postfix start
    # chkconfig postfix on



If we deploy OpenMooc componnents in diferents machines we can use form them the SMTP server deployed at the IdP.

But don't forguet to enable the access on the SMTP server, adding the IPs of the machines at the 'mynetworks' param.


Notice that instead deploy our own SMTP server we can use gmail as relay server. Check `this guide <http://charlesa.net/tutorials/centos/centosgmail.php>`_


We can test if postfix works sending a main to our mailbox: ::

 # mail <my_mail>



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

Edit */etc/ntp.conf* and change the follow properties according to this values.
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

Configure ntp through the file */etc/ntp.conf*

Change servers and set it according to our configuration (set idp.example.com
name according to your idp ns name).

.. code-block:: bash

   server idp.example.com
   server 0.uk.pool.ntp.org
   server 1.uk.pool.ntp.org
   server 2.uk.pool.ntp.org
   server 3.uk.pool.ntp.org


Enable service ntpd and start it
