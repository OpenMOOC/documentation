Adding extra repositories
-------------------------

First of all, you should add the Mongo and OpenMOOC repositories.

Add the MongoDB repository:

To add the MongoDB repository, create the file **/etc/yum.repos.d/mongodb.repo**
and add this content:

.. code-block:: ini

    [mongodb]
    name=MongoDB Repository
    baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
    gpgcheck=0
    enabled=1

Add the OpenMOOC repository:

To add the OpenMOOC repository, create the file **/etc/yum.repos.d/openmooc.repo**
and add this content:

.. code-block:: ini

    [openmooc]
    name=Packages for OpenMOOC platform - x86_64
    baseurl=http://openmooc.org/openmooc-rpms/x86_64/
    enabled=1
    gpgcheck=0

    [openmooc-source]
    name=Source code for OpenMOOC platform
    baseurl=http://openmooc.org/openmooc-rpms/SRPMS/
    enabled=1
    gpgcheck=0

Before starting, please update your system with:

.. code-block:: none

    # sudo yum update
