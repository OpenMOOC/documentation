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

We add the entries to the ldap: ::

 # slapadd -l /etc/openldap/root.ldif -f slapd.conf -d 10
 #  slapadd -l /etc/openldap/people.ldif -f slapd.conf -d 10


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

Now the phpldapadmin is accessible at http://XXX.XXX.XXX.XXX/phpldapadmin, you can access it using your root user, so on username set
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

TODO
