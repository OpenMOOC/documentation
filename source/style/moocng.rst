OpenMOOC Style Guide - MoocNG
=============================

MoocNG is a django application, you can search at the settings.py file where are allocated style info:

Review the values of:

* STATIC_URL
* STATIC_ROOT
* STATICFILES_DIRS

STATIC_URL is served by Apache/Nginx server, so take a look what are the target path related to this urls, may match the STATIC_ROOT value.

There are some values from the MoocNG theme that can be changed:

```python
MOOCNG_THEME = {
    'logo': u'',
    'subtitle': u'',  #  The OpenMOOC title under the logo.
    'top_banner': u'',
    'right_banner1': u'',
    'right_banner2': u'',
    'bootstrap_css': u'',
    'moocng_css': u'',
    'cert_banner': u'',
}
```

If you don't set a value/filename, then the default values will be used. Inside the MoocNG app you will found a folder named 'static', where you can find:

* css. That contains the css that will be used.
  * bootstrap.css  A bootstrap v2 css file. (MOOGNG_THEME.bootstrap_css)
  * moocng.css Some extra css that extends the bootstrap.css file (MOOGNG_THEME.moocng_css)
* img. A folder that contains images of the MoocNG theme.
  * logo.png The logo of the OpenMOOC entity. (MOOGNG_THEME.logo)
  * top_banner.jpg The top banner showed in the main page (MOOCNG_THEME.top_banner)
  * right_banner1.jpg and right_banner1.jpg Images showed in the main page, at the right side
    of the course list. (MOOGNG_THEME.right_banner1.jpg and MOOGNG_THEME.right_banner2.jpg)
  * cert_banner.png Default certificate banner MOOGNG_THEME.cert_banner)

If you want your own images/css override the previous files, or include the new files at the css/img folder and set the filename at the MOOCNG_THEME.

After change/update any static file you will need to execute python manage.py collectstatic
(it will copy static files from askbot folder to STATIC_ROOT path)