===================
Installing OpenMOOC
===================

Requirements
============

* RPM based system (recommended Centos 6)
* Python >= 2.6 (we do not support python 3 yet)

Adding OpenMOOC package repository
==================================

You will have to add the OpenMOOC package repository to have access to the OpenMOOC
RPMs.

Update your package index and system packages:

.. code-block:: bash

    # yum update

.. note:: This information cannot be finished until we have the Yaco repository
          working.


OpenMOOC virtual package
========================

There is a virtual package that should help you to install the complete OpenMOOC
platform without any trouble.

.. warning:: Some packages are specific for OpenMOOC and can overwrite your current
             installed versions. Please make sure that you do a backup before starting.

Run this command in the command line:

.. code-block:: bash

    # yum install openmooc

If the installation was successful, please follow to :doc:`Configuration <../configure/idp>`
If you had any trouble please check the :doc:`FAQ <installfaq>`
