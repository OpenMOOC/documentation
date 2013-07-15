Installation via RPM
====================

.. warning:: The RPM installation is still in development.

Installing
----------

Adding the Yaco repository
,,,,,,,,,,,,,,,,,,,,,,,,,,

To install the OpenMOOC platform you will need to add the Yaco repository to your
system, which contains all the necessary packages for the installation.

To add it put these command in your terminal::

    # commandtobeshown


Installing the virtual package
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

The is a virtual package called "openmooc" that should install everything
without any problem for you.

.. note:: The OpenMOOC package will eliminate any Askbot instances you have on
          your system.
::

    # yum install openmooc

After that, you can continue to 'Configuration'. If for any reason you're unable to
install the platform via the virtual package, follow these step-by-step instructions.

Dependencies
,,,,,,,,,,,,

After you have added the Yaco repository and updated you package database it's time
to install all the OpenMOOC dependencies, this is the complete list of dependencies.
**Please be aware that OpenMOOC needs a fixed version of the packages, if you have
any package on your system with a different version it will be replaced**

django-admin-sortable   1.4.9
django-celery   3.0.17
django-countries    1.0.5
django-followit 0.0.3
django-grappelli    2.4.5
django-keyedcache   1.4.1
django-mathjax  0.0.2
django-recaptcha-works  0.3.4
django-robots   0.8.1
Django-south    0.7.5
django-threaded-multihost   1.4.0
Django14    1.4.5
ffmpeg  20120806
memcached   1.4.4
mongo-10gen-server  2.4.5
mysql-server    5.1.69
nginx   1.0.15
openmooc-askbot 0.7.44
openmooc-askbot-customs 0.7.44
openmooc-engine 0.1.0
openmooc-tastypie   0.9.11
postfix 2.6.6
postgresql-server   8.4.13
pymongo 2.4.2
pystache    0.3.1
python-akismet  0.2.0
python-anyjson  0.3.3
python-beautifulsoup4   4.1.3
python-billiard 2.7.3.28
python-boto 2.8.0
python-celery   3.0.20
python-coffin   0.3.5
python-django-compressor    1.2
python-django-longerusername    0.4
python-django-tinymce   1.5.1b4
python-djangosaml2  0.10.0
python-gunicorn 0.14.6
python-html5lib 0.9
python-imaging (PIL)    1.1.6
python-jinja2   2.2.1
python-kombu    2.5.12
python-lamson   1.1
python-markdown2    1.4.2
python-memcached    1.48
python-oauth2   1.5.170
python-openid   2.2.5
python-psycopg2 2.4.2
python-pysaml2  0.4.3
python-requests 1.2.0
pytz    2010h
rabbitmq-server 2.6.1
supervisor  2.1
unidecode   0.04.7

To install everything put this command in your command line::

# yum install django-admin-sortable django-celery django-countries django-followit django-grappelli django-keyedcache django-mathjax django-recaptcha-works django-robots Django-south django-threaded-multihost Django14 ffmpeg memcached mongo-10gen-server mysql-server nginx postfix postgresql-server pymongo pystache python-akismet python-anyjson python-beautifulsoup4 python-billiard python-boto python-celery python-coffin python-django-compressor python-django-longerusername python-django-tinymce python-djangosaml2 python-gunicorn python-html5lib python-imaging python-jinja2 python-kombu python-lamson python-markdown2 python-memcached python-oauth2 python-openid python-psycopg2 python-pysaml2 python-requests pytz rabbitmq-server supervisor unidecode

Databases
,,,,,,,,,

OpenMOOC uses two different databases to store the contents, one is MongoDB (for student activity) and the other is PostgreSQL (for course data)

MongoDB
.......

PostgreSQL
..........

MOOCng
,,,,,,

MOOCng is the core of the OpenMOOC platform. It contains all the necessary to
create and participate in courses but the debating tool (askbot)

IDP
,,,

Askbot
,,,,,,

Configuration
-------------

Nginx
,,,,,

Apache
,,,,,,

Supervisor
,,,,,,,,,,

MOOCng
,,,,,,

Askbot
,,,,,,
