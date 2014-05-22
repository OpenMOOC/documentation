OpenMOOC Style Guide - Askbot
=============================

OpenMOOC uses a farm of Askbots. Each Askbot instance share code and style.
Askbot is a django application, you can search at the settings.py file where are allocated style info:

STATIC_URL
STATIC_ROOT
ASKBOT_EXTRA_SKINS_DIR

STATIC_URL is served by Apache/Nginx server, so take a look what are the target path related to this urls, may match the STATIC_ROOT value.

ASKBOT_EXTRA_SKINS_DIR defines extra template folders. By default we use it to store openmooc images/css, the askbot-openmooc-themes folder that is located at the PROJECT_ROOT (askbot-openmooc/askbotopenmooc).

In that folder there are:

  * mooc/media/style
    * extra.css Extra css rules for askbot
    * custom.css Customize rules  
  * mooc/media/images
    * logo.png The logo of the OpenMOOC entity.

After change/update any static file you will need to execute python manage.py collectstatic
(it will copy static files from askbot folder to STATIC_ROOT path)