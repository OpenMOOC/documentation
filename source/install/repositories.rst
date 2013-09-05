Adding extra repositories
-------------------------

First of all, you should add the OpenMOOC, EPEL and Mongo repositories and some
minor tools.

.. code-block:: none

    # yum install wget

Add the EPEL for Centos 6 repository:

.. code-block:: none

    # wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
    # sudo rpm -Uvh epel-release-6*.rpm

Add the MongoDB repository:

To add the MongoDB repository, create the file **/etc/yum.repos.d/10gen.repo**
and add this content:

.. code-block:: ini

    [10gen]
    name=10gen Repository
    baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
    gpgcheck=0
    enabled=1

Add the OpenMOOC repository:

.. code-block:: none

    # <commands here>

Before starting, please update your system with:

.. code-block:: none

    # yum update
