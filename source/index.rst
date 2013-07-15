.. OpenMOOC documentation master file, created by
   sphinx-quickstart on Tue Jun 11 09:42:28 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OpenMOOC's documentation!
====================================

OpenMOOC is an open source Massive Open Online Course system built ton top of the django framework.

.. note:: This documentation is still in heavy development. Feel free to send an email to the mailing list in openmooc@googlegroups.com if you have any questions.


Installation
------------
.. toctree::
   :maxdepth: 3

   rpm/install
   demostrator
   moocng
   askbot
   sentry_guide
   IdP_guide

.. note:: For moocng and askbot installation details please refer to the docs/ directory in their respective repositories

.. warning:: Currently moocng does not have an egg in Pypi, if you try to install it that way it will fail.

Manuals
-------
.. toctree::
   :maxdepth: 3

   teacher_manual
   students_manual

Reference
---------
.. toctree::
   :maxdepth: 2

   mongo_structure



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

