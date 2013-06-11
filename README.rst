OpenMOOC
========

OpenMOOC is an open source platform (Apache license 2.0) that implements a fully open MOOC solution. If you do not know what a MOOC is, `check it out on Wikipedia <http://en.wikipedia.org/wiki/Massive_open_online_course>`_.


How it works
============

* **Video+Internet**. Combined use of video and intelligent discussion forums. The content is available online from a desktop, tablet or smartphone.
* **Progressive**. The courses consist of units built by a set of knowledge pills. Pills are short videos that can be associated with supplementary material (documents, links, exercises) and questions with their respective answers. Pills are classified in normal, homework and exams. The difference between them is the time to study them and the possibility or not to see the answers before the deadline of the pill.
* **Participative**. Each course has associated an intelligent discuission forum where students and teachers can discuss and collaborate on a unit/knowledge pill.


Architecture
============

OpenMOOC is a platform based on several components:

* **Identity provider**. This component is responsible on the identity of the users. This includes: user registration, user management data and Single Sign On (SSO). It's based on SimpleSAMLphp and modules for it like the userregistration and a custom template.
* **Moocng**. This is the platform's engine. This module allows teachers to create, manage and release courses and students to apply and follow them. It's written in Python/Django.
* **Askbot**. This component is a Q&A platform written in Python/Django. At present time it's the main way of communication between teachers and students.


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


Installation using an appliance
===============================

 There is one virtual appliance published, very useful to get the system
 running or to run a demo in your own machine.

 For more info go to the `Demo doc
 <https://github.com/OpenMOOC/documentation/blob/master/demostrator.rst>`_

Installation
============

The documentation of how to install the platform and configure it is still under development.

Meanwhile you can take a look at these documents (beta):

* `Install and configure an IdP (Identity Provider) for OpenMooc <https://github.com/OpenMOOC/documentation/blob/master/IdP_guide.rst>`_
* `Install MoocNG <https://raw.github.com/OpenMOOC/moocng/master/docs/source/install.rst>`_
* `Configure MoocNG <https://github.com/OpenMOOC/moocng/blob/master/docs/source/configuration.rst>`_
* `Install and configure Askbot (multiple-instance) <https://github.com/OpenMOOC/askbot-openmooc/blob/master/README-centos-multipleinstance.rst>`_


Contribute
==========

Get involved!

* **Coding**. OpenMOOC source is hosted on `GitHub <https://github.com/OpenMOOC>`_. You are welcome to contribute patches, create a fork of the project on GitHub and submit a pull request.
* **Giving feedback**. Your opinion is important for us. Participate (for example in our `mailing list <https://groups.google.com/d/forum/openmooc>`_) and help us improve our system.
* **Broadcasting**. Tell a friend about us, follow `@openmooc <https://twitter.com/openmooc>`_ on Twitter.
* **Reporting bugs**. Please file as many issues as you can!  Our bug tracking system lives in GitHub (see above).  Select the project to report on, and send us your bug reports.


Keep yourself updated of the project
====================================

* **Mailing list**: https://groups.google.com/forum/#!forum/openmooc
* **Github**: https://github.com/OpenMOOC
* **News**: http://openmooc.org/blog/
* **Sandbox**: http://openmooc.org/sandbox/
* **Twitter**: `@openmooc <https://twitter.com/openmooc>`_


Who is using it?
================

* `UNED <http://unedcoma.es>`_.The National Distance Education University. Free access.


License
=======

OpenMOOC is licensed under the terms of `Apache 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_

The main header image used on OpenMOOC platform and blog was created by `Ana Isabel Rey Botello <https://github.com/anarey>`_
