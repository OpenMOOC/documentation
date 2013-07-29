============================
Generating the OpenMOOC RPMs
============================

OpenMOOC installation is based on RPM packages, and we will show you how you
can generate them from the spec files.

Prerequisites
=============

* RPM-based distribution (preferably Centos 6)

Preparing the environment
=========================

* Install rpm-build in your system

.. code-block:: bash

    # yum install rpm-build redhat-rpm-config

* Create a new regular user, for example: thebuilder and login with it.
* Create the directory structure for RPM building

.. code-block:: bash

    $ mkdir -p ~/rpmbuild
    $ mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
    $ echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros

Explanation:
    The SPECS directory is where you need to copy the spec files to generate
    The SOURCES directory is where you need to copy the required source files for generating determined RPMs.
