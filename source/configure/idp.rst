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

	$ lokkit --selinux=disabled
	$ lokkit --disabled

In a production enviroment you may configure a secure environment. The nginx
publish the IdP under 80 and 443 port. The idP uses also some internal services
that runs in default port, like ldap (port 389), mongodb (port 27017).


Configure OpenLDAP
------------------

Edit the hosts file and add the host of your LDAP: (in our case we add 'idp.example.com' at the 127.0.0.1 and the IP entry):

.. code-block:: none

	$ vim /etc/hosts


Something similar to ::

	127.0.0.1       localhost.localdomain   localhost idp.example.com
	::1             localhost6.localdomain6 localhost6 idp.example.com


.. code-block:: bash

   $ cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG

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

	$ rm -rf /etc/openldap/slap.d

tart and stop the LDAP server:

.. code-block:: none

   $ service slapd start
   $ service  slapd stop


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

   $ slapadd -l /etc/openldap/root.ldif -f slapd.conf -d 10
   $ slapadd -l /etc/openldap/people.ldif -f slapd.conf -d 10
   $ slapadd -l /etc/openldap/testuser.ldif -f slapd.conf -d 10

Start the server:

.. code-block:: none

   $ service slapd start


If restarting the server, warnings appear, change the permissions on the LDAP directory and restart LDAP to check that warnings disssapear:

.. code-block:: none

   $ chown -R ldap:ldap /var/lib/ldap/
   $ service slapd restart

Add the service to the system boot:

.. code-block:: none

   $ chkconfig slapd on


We can create a backup script and insert it in our crontab:

For example, this will create a backup of the LDAP at the */var/backups/* folder

.. code-block:: none

	$ slapcat | /usr/bin/bzip2 > /var/backups/ldap_`/bin/date +%Y-%m-%d-%H-%M-%S`.ldif.bz2

We can save this script as backup_ldap.sh in the simplesamlphp folder or wherever we want, give this file execution permission and add it to the cron. (**/etc/cron.d/backup_ldap**) ::

  00 3 * * *      <path-to-the-folder-that-contain-the-script>/backup_ldap.sh

Restart the crond service:

.. code-block:: none

   $ service crond restart
