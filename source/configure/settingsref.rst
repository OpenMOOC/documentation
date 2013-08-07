Settings reference
==================

.. warning:: This section is under construction

This is a comprehensive list of all the possible settings in OpenMOOC Moocng and their description.

Databases
---------

MONGODB_URI *(string)*
    This is the MongoDB connection string.

    Default: *mongodb://localhost:27017/moocng*


Authentication
--------------

SESSION_EXPIRE_AT_BROWSER_CLOSE *(boolean)*
    Expire the user session as soon as the user closes the browser.

    Default: *True*

AUTH_HANDLER *(string)*
    Authentication handler, here you can set your preferred authentication system.

    Default: *moocng.auth_handlers.handlers.SAML2*

    Other settings: *moocng.auth_handlers.handlers.dbauth*

LOGIN_REDIRECT_URL | LOGOUT_REDIRECT_URL *(string)*
    URLs for after the login and logout actions.

    Default: */*

FREE_ENROLLMENT_CONSISTENT *(boolean)*
    If this variable is set, the enrollments of the user are registered in the IdP and the moocng database. If
    it is False, the enrollments are registered only in the moocng database.

    Default: *False*

SAML2
.....

These settings are specific for SAML2. If you set up the SAML2 authentication, then you
need to set up these settings too.

REGISTRY_URL *(url)*
    Registration URL for the user.

    Default: *https://idp.openmooc.org/simplesaml/module.php/userregistration/newUser.php*

PROFILE_URL *(url)*
    User profile URL.

    Default: *https://idp.openmooc.org/simplesaml/module.php/userregistration/reviewUser.php*

CHANGEPW_URL *(url)*
    Change user password URL

    Default: *https://idp.openmooc.org/simplesaml/module.php/userregistration/changePassword.php*

DBAuth
......

These settings are specific for DBAuth

.. code-block:: python

    INSTALLED_APPS.append('moocng.auth_handlers.dbauth')
    INSTALLED_APPS.append('registration')
    ACCOUNT_ACTIVATION_DAYS = 15

Media related
-------------

FFMPEG *(string)*
    Determines where the FFMpeg binary is. Remember that OpenMOOC uses it's own
    ffmpeg binary, so be sure to point this variable to it.

    Default: */usr/libexec/openmooc/ffmpeg/*

Amazon S3 and peer review
-------------------------

Amazon credentials

.. code-block:: python

    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""
    AWS_STORAGE_BUCKET_NAME = ""
    AWS_S3_UPLOAD_EXPIRE_TIME = (60 * 5)  # 5 minutes

PEER_REVIEW_TEXT_MAX_SIZE *(int [characters])*
    Maximum size for the text submitted for the peer review. Users won't be able to send solutions bigger than that.

    Default: *5000*

PEER_REVIEW_FILE_MAX_SIZE *(int [MB])*
    Maximum size for the uploaded files for peer review.

    Default: *5*

PEER_REVIEW_ASSIGNATION_EXPIRE *(int [hours])*
    When a user is reviewing another user task, this evaluation will be locked down until it is reviewed or the time specified
    in this variable expires.

    Default: *24*

Courses
-------

ALLOW_PUBLIC_COURSE_CREATION *(boolean)*
    Allow creation of courses by everyone (True), or allow course creation only to platform administrators (False)

    Default: *False*

FORMAT_MODULE_PATH *(module)*
    Model defining the date and other data formats.

    Default: *'moocng.formats'*

COURSES_USING_OLD_TRANSCRIPT *(list)*
    A list with the slugs of the courses that use the old qualification system where the normal units counted.

ENROLLMENT_METHODS *(tuple)*
    Select the enrollment method of the courses. Currently only free enrollments are allowed, but you can integrate new
    enrollment methods (for example paid enrollment) without problem

    Default: *('moocng.enrollment.methods.FreeEnrollment',)*

ASSET_SLOT_GRANULARITY *(int [minutes])*
    Slot duration time of assets should always be multiple of the asset slot granularity. That slot granularity is set to
    five minutes by default. To use another value, simply specify a different value (in minutes) in the ASSET_SLOT_GRANULARITY
    property of the settings file.

    Default: *5*

ASKBOT_URL_TEMPLATE *(url)*
    URL pointing to the askbot instance of the course.

    Default: *'https://questions.example.com/%s/'*

CERTIFICATE_URL *(url)*
    URL for the certification bad= 'http://example.com/idcourse/%(courseid)s/email/%(email)s'  # Example, to be overwritten in local settings

Platform
--------

.. code-block:: python

    COMPRESS_CSS_FILTERS = [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter',
    ]

    COMPRESS_OFFLINE = False

    GOOGLE_ANALYTICS_CODE = ''

    GRAVATAR_URL_PREFIX = '//www.gravatar.com/'

    MOOCNG_THEME = {
        # 'cert_banner': u'',
    }

    ENABLED_COMUNICATIONS = (
        'feedback',
        'incidence',
        'rights',
        'unsubscribe',
        'others'
    )

    #SHOW_TOS = True

    # Make this unique, and don't share it with anybody else than payment system
    # Override this in local settings
    USER_API_KEY = '123456789'

BROKER_URL *(amqp connection string)*
    Defines the connection string for RabbitMQ.

    Default: *'amqp://moocng:moocngpassword@localhost:5672/moocng'*

MASSIVE_EMAIL_BATCH_SIZE *(int)*
    When a teacher or administrator sends a massive mail it will be split into batches. This will specify the number of emails
    per batch.

    Default: *30*




