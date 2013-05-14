OpenMOOC Demo Appliance
=======================


The OpenMOOC Demo Appliance is the fastest and easiest way to get
running a Open MOOC System.

To run this system, your virtual machine host need a CPU and BIOS with Virtual
Extensions enabled, like VT in Intel processors or AMD-V or SMV in AMD
processors, 2 GB of ram and 10GB of free disk space.

This appliance has been tested in VMWare Player 5, VirtualBox 4.1, and with the
correct settings modification can be executed in a libvirt environment.


Network details
---------------

The default setted network is Bridge on eth0, you can change this to any where
the virtual machine is accessible from your host.

The Appliance is configured by default to reconfigure all components affected
by an IP change at boot process.

To allow this, every app use an alternative port:

* Moocng: 80
* Askbot: 8080
* IDP: 8081

You can set the apache servername of virtualhost by editing the file
`/etc/default/openmooc`, explained below.


Internal Configuration details
------------------------------

The file `/etc/default/openmooc` handle the configuration of configuration
process at boot.

.. code::

   # Force reconfig on every boot
   FORCE_RECONFIG=True


   # Complete this values if you want to use public domains
   # Remember to execute
   #
   # HOSTNAME_ASKBOT="questions.example.com"
   # HOSTNAME_MOOCNG="mooc.example.com"
   # HOSTNAME_IDP="idp.example.com


If you set the variable `FORCE_RECONFIG` to false or leave empty, the
reconfiguration process only run at the first boot, if you already boot up the
system, then the system never will be reconfigured.

If you want to change from IP and port to a more pretty values with a domain
and without ports, you must uncomment `HOSNTAME_*` variables and execute the
reconfing command. Remember set `FORCE_RECONFIG` to false

.. code:: bash

   service openmooc-config reconfig


First steps in OpenMOOC
-----------------------

A url to your OpenMOOC instance is given when the system has booted up.

There are different users with different roles registered in your system. Note
that all users in OpenMOOC use an email as username.

A generic password has been assigned to all users: openmooc

* Students:

  * student1@example.com

  * student2@example.com

  * student3@example.com

* Teachers:

  * teacher1@example.com

  * teacher2@example.com

* Platform manager:

  * admin@example.com

As example content, there are 10 courses created.

The first course is for demo. It has demo content.

The follows courses are empty courses with a pre-created forum.

The courses and forums are linked by theirs urls. So, remember that you can't
change the "slug" of one course if you want to conserve the link integrity
between its forum.


Courses and forums creation or rename
-------------------------------------

Remember that if you rename a course by changing its slug, you must login in
the system, change to askbot user and rename the directory course. You can do
this using the command `askbot_rename.sh`.


.. code::

   askbot_rename.sh source_slug target_slug


This script don't rename the database, so be careful if you create a forum with
the same database name.


If you have created one extra course, you must create the forum manually by run
this in a ssh root session in the system:


.. code::

   askbot_create.sh new_course_slug database_name


Remember that `database_name` only can have letters and numbers.

Remember that `new_course_slug` must be exactly the course slug.


External API Keys
-----------------

OpenMOOC uses external services that need a API key to run like Google
Analytics or Amazon S3. Another services like Youtube or Vimeo don't need a API
key to run.

For moocng, courses application, the important file to this is:

`/home/moocng/moocng/moocng/local_settings.py`


Amazon S3 Configuration
***********************

You need to append this properties:

.. code::

   # Amazon credentials
   AWS_ACCESS_KEY_ID = ""
   AWS_SECRET_ACCESS_KEY = ""
   AWS_STORAGE_BUCKET_NAME = ""
   AWS_S3_UPLOAD_EXPIRE_TIME = (60 * 5) # 5 minutes


Google Analytics
****************

You need to append this property:

.. code::

   OOGLE_ANALYTICS_CODE = ''


Production Details
------------------

This system is proposed for demo environment only. This system with this
deployment isn't prepared to support a true MOOC course with millions of
users, but is very usable for until 20 or 30 concurrent users.
