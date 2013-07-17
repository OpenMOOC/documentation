===============
OpenMOOC Askbot
===============

The Askbot component of OpenMOOC serves as a way to ask questions about a course.

To install it via the package repository you just need to do::

    # yum install openmooc-askbot openmooc-askbot-customs

If for some reason the package from the repository couldn't work, you still can
download the openmooc-askbot RPM and try to install it with the command::

    # yum --nogpgcheck localinstall openmooc-askbot-0.7.44_x86_64.rpm openmooc-askbot-customs-0.7.44_x86_64.rpm

.. note:: Put link here

You can now follow to OpenMOOC Askbot Configuration

CentOS
------

Deployment
..........

The installation instructions for askbot-openmooc are `here <https://github.com/OpenMOOC/askbot-openmooc/blob/master/README-centos.rst>`_

Deploying multiple instances
............................

The usual deployment mehtod of OpenMOOC requires multiple instancing of Askbots,
here are the `instructions <https://github.com/OpenMOOC/askbot-openmooc/blob/master/README-centos-multipleinstance.rst>`_

Ubuntu
------

Deployment
..........

`Instructions <https://github.com/OpenMOOC/askbot-openmooc/blob/master/README-ubuntu.rst>`_

Deploying multiple instances
............................

`Instructions <https://github.com/OpenMOOC/askbot-openmooc/blob/master/README-ubuntu-multipleinstance.rst>`_
