Adding Yaco repository
======================

To add the Yaco repository...

Update your package index and system packages:

.. code-block:: bash

    # yum update

.. note:: This information cannot be finished until we have the Yaco repository
          working.

Prerequisites
=============

The minimum version of Python needed to run OpenMOOC is 2.6. We do not support Python 3.x yet.

In the process of installing moocng, both in the standard installation and
the development installation, it is necessary that some libraries already
exist on your system. It is also needed the baseic compiler chaintool and
the development version of those libraries since the installation process
compiles a couple of Python modules.

.. code-block:: bash

  # CentOS/Fedora example:
  $ yum install python-devel postgresql-devel libjpeg-turbo-devel libpng-devel
  $ yum groupinstall "Development Tools"

  # Debian/Ubuntu example:
  $ apt-get install build-essential python-dev libpq-dev libjpeg-turbo8-dev libpng12-dev

Installing the web server
=========================

The packages needed for installing Apache and wsgi support are:

.. code-block:: bash

  # Fedora example:
  $ yum install httpd mod_wsgi

  # Debian/Ubuntu example:
  $ apt-get install apache2 libapache2-mod-wsgi

.. note:: If you use someting different from Apache, please check the documentation
          of your web server about how to integrate it with a WSGI application.

OpenMOOC virtual package
========================

There is a virtual package that should help you to install the complete OpenMOOC
platform without any trouble.

.. warning:: Some packages are specific for OpenMOOC and can overwrite your current
             installed versions. Please make sure that you do a backup before starting.

Run this command in the command line:

.. code-block:: bash

    # yum install openmooc

.. note:: Put link to configuration of moocng here

After it's installed, please follow to :doc:`Configuration <../configure/idp>`
