OpenMooc
========

OpenMooc is an open source platform (Apache license 2.0) that implements a fully open MOOC solution. If you do not know what a MOOC is, check this `Massive Online Open course <http://en.wikipedia.org/wiki/Massive_open_online_course>`_.


How it works
============

* **Vídeo+Internet**. Combined use of Video and intelligent discussion forums. Available at internet from a desktop, tablet or a smartphone.
* **Progressive**. The courses consist of units built by a set of knowledge pills. Pills are short videos that can be associated with supplementary material (documents, links, exercises) and questions with their respective answers. Pills are clasified in normal, homeworks and exams. The diference between them are the time to study them and the posibility or not to see the answers before the deadtime of the pill.
* **Participative**. Each course has associate a intelligent discusion forum where students and teachers  discuss and collaborate about an unit/knowledge pill.


Architecture
============

OpenMooc is a platform based on several components:

* **Identity provider**. This component is responsible on the identity of the users. This includes: user registration, user management data, Single Sign On. Is based on SimpleSAMLphp and require new modules like the userregistration and a custom template.
* **MoocNG**. This is the engine of the platform. This module lets the teachers create, manage and publicate courses and let the students to study them. Is writen in Python/Django.
* **Askbot**. This component is an Questions & Answers platform. At present is the main way of comunication between teachers and stuedents.


Main features
=============

* 100% open source solution
* Video integration with documents and teacher’s remarks
* Extremely simple course creation interface
* Self assessment progress
* Social discussion forum
* Follow up own/others questions
* No need to stream videos (use youtube)
* Wyswyg interface for creation of questions
* Medals (badges) for assessing your social behaviour in the forum
* Federation of identities based on standard (SAML2)


Installation
============

We are sorry to inform that the documentation of howto install the platform and configure it is still under development.


Contribute
==========

Get involved:
* **Coding**. OpenMooc source is hosted on `GitHub <https://github.com/OpenMOOC>`_. You are welcome to contribute patches, create a fork of the project on GitHub and submit a pull request.
* **Giving feedback**. Your opinion is important for us. Participate (for example in our `mailing list <https://groups.google.com/d/forum/openmooc>`_) and help us improve our system.
* **Broadcasting**. Tell a friend about us,  follow `@openmooc <https://twitter.com/openmooc>`_ on twitter.
* **Reporting bugs**.  


Keep yourself updated of the projec
===================================

* **Mailing list**: https://groups.google.com/forum/#!forum/openmooc
* **Github**: https://github.com/OpenMOOC
* **News**: http://openmooc.org/blog/
* **Sandbox**: http://openmooc.org/sandbox/
* **Twitter**: `@openmooc <https://twitter.com/openmooc>`_


Who is using it?
================

* `UNED <http://unedcoma.es>`_. Free access.


License
=======

OpenMooc is licensed under `Apache 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_

OpenMooc is an open source platform that integrated some others open source components:
* SimpleSAMLphp  is licensed under the `CC-GNU LGPL version 2.1 <http://creativecommons.org/licenses/LGPL/2.1/>`_.
* userregistration (based on selfregister) is licensed under `Apache 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_.
* Askbot is licensed under `GPL <http://www.gnu.org/copyleft/gpl.html>`_.
* And others: Apache, Postgres, Mysql, MongoDB, Rabitmq, Django, Jquery, Boootstrap, Backbone.js

Some images used on OpenMooc were provided by `Ana Isabel Rey Botello <https://github.com/anarey>`_
