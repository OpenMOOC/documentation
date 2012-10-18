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
