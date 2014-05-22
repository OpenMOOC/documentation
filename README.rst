OpenMOOC
========

OpenMOOC is an open source platform (Apache license 2.0) that implements a
fully open MOOC solution. If you do not know what a MOOC is,
`check it out on Wikipedia <http://en.wikipedia.org/wiki/Massive_open_online_course>`_.


How it works
============

* **Video+Internet**. Combined use of video and intelligent discussion forums.
  The content is available online from a desktop, tablet or smartphone.
* **Progressive**. The courses consist of units built by a set of knowledge
  pills. Pills are short videos that can be associated with supplementary material
  (documents, links, exercises) and questions with their respective answers. Pills
  are classified in normal, homework and exams. The difference between them is the
  time to study them and the possibility or not to see the answers before the
  deadline of the pill.
* **Participative**. Each course has associated an intelligent discuission forum
  where students and teachers can discuss and collaborate on a unit/knowledge
  pill.


Architecture
============

OpenMOOC is a platform based on several components:

* **Identity provider**. This component is responsible on the identity of the
  users. This includes: user registration, user management data and Single Sign On
  (SSO). It's based on SimpleSAMLphp and modules for it like the userregistration
  and a custom template.
* **Moocng**. This is the platform's engine. This module allows teachers to
  create, manage and release courses and students to apply and follow them. It's
  written in Python/Django.
* **Askbot**. This component is a Q&A platform written in Python/Django. At
  present time it's the main way of communication between teachers and students.


Main features
=============

* 100% open source solution
* Video integration with documents and teacher’s remarks
* Extremely simple course creation interface
* Self assessment progress
* Social discussion forum
* Follow up own/others' questions
* No need to stream videos from a local platform (uses YouTube)
* WYSIWYG interface for content creation
* Medals (badges) for assessing your social behavior in the forum
* Federation of identities based on standard (SAML2)


First contact through an appliance
==================================

There is one virtual appliance published, very useful to get the system
running quickly or to run a demo in your own machine.

For more information go to the
`demo documentation <source/manual/demostrator.rst>`_.


Installation
============

The deployment can be done using RPM packages. For details and information
about the installation and configuration of each component, look at this
guides:

* `Setting up the repositories <source/install/repositories.rst>`_
* Identity Provider (IdP) for OpenMOOC:

  * `Installation <source/install/idp.rst>`_
  * `Configuration <source/configure/idp.rst>`_

* MOOC Engine (MoocNG):

  * `Installation <source/install/moocng.rst>`_
  * `Configuration <source/configure/moocng.rst>`_

* Askbot:

  * `Installation <source/install/askbot.rst>`_
  * `Configuration <source/configure/askbot.rst>`_

* `Settings reference <source/configure/settingsref.rst>`_
* Frequently asked questions (FAQ):

  * `About installation <source/install/faq.rst>`_
  * `About configuration <source/configure/faq.rst>`_

If you want to learn how change style and images review the `style guide <source/style/openmooc.rst>`_

Contribute
==========

Get involved!

* **Coding**. OpenMOOC source is hosted on `GitHub <https://github.com/OpenMOOC>`_.
  You are welcome to contribute patches, create a fork of the project on GitHub
  and submit a pull request.
* **Giving feedback**. Your opinion is important for us. Participate (for
  example in our `mailing list <https://groups.google.com/d/forum/openmooc>`_)
  and help us improve our system.
* **Broadcasting**. Tell a friend about us, follow
  `@openmooc <https://twitter.com/openmooc>`_ on Twitter.
* **Reporting bugs**. Please file as many issues as you can!  Our bug tracking
  system lives in GitHub (see above).  Select the project to report on, and send
  us your bug reports.


Development
-----------

There are alternatives to the installation through rpm, that are more suited
for a development environment. You can find them here:

* IdP `installation <source/development/IdP_guide.rst>`_.
* MoocNG `installation <https://github.com/OpenMOOC/moocng/blob/master/docs/source/install.rst>`_
  and `configuration <https://github.com/OpenMOOC/moocng/blob/master/docs/source/configuration.rst>`_.
* Askbot `deployment <https://github.com/OpenMOOC/askbot-openmooc/blob/master/docs/source/old_docs/deployment/centos-multipleinstance.rst>`_
  and `more (utils) <https://github.com/OpenMOOC/askbot-openmooc/tree/master/docs/source/old_docs>`_.


Keep yourself updated of the project
====================================

* **Mailing list**: https://groups.google.com/forum/#!forum/openmooc
* **Github**: https://github.com/OpenMOOC
* **News**: http://openmooc.org/blog/
* **Sandbox**: http://openmooc.org/sandbox/
* **Twitter**: `@openmooc <https://twitter.com/openmooc>`_


Who is using it?
================

* `UNED <http://unedcoma.es>`_.The National Distance Education University. Free
  access.


License
=======

OpenMOOC is licensed under the terms of
`Apache 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_

The main header image used on OpenMOOC platform and blog was created by
`Ana Isabel Rey Botello <https://github.com/anarey>`_
