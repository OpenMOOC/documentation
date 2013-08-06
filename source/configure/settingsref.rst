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

FREE_ENROLLMENT_CONSISTENT = False

SAML2
.....

These settings are specific for SAML2. If you set up the SAML2 authentication, then you
need to set up these settings too.

REGISTRY_URL *(string)*
    Registration URL for the user.

    Default: *https://idp.openmooc.org/simplesaml/module.php/userregistration/newUser.php*

PROFILE_URL *(string)*
    User profile URL.

    Default: *https://idp.openmooc.org/simplesaml/module.php/userregistration/reviewUser.php*

CHANGEPW_URL *(string)*
    Change user password URL

    Default: *https://idp.openmooc.org/simplesaml/module.php/userregistration/changePassword.php*

DBAuth
......

These settings are specific for DBAuth

# INSTALLED_APPS.append('moocng.auth_handlers.dbauth')
# INSTALLED_APPS.append('registration')
# ACCOUNT_ACTIVATION_DAYS = 15

Media related
-------------

FFMPEG *(string)*
    Determines where the FFMpeg binary is. Remember that OpenMOOC uses it's own
    ffmpeg binary, so be sure to point this variable to it.

    Default: */usr/libexec/openmooc/ffmpeg/*


# Amazon credentials
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_STORAGE_BUCKET_NAME = ""
AWS_S3_UPLOAD_EXPIRE_TIME = (60 * 5)  # 5 minutes

# Use custom formats
FORMAT_MODULE_PATH = 'moocng.formats'

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



ALLOW_PUBLIC_COURSE_CREATION = False

# Make this unique, and don't share it with anybody else than payment system
# Override this in local settings
USER_API_KEY = '123456789'

# A list with the slugs of the courses that use the old qualification system
# where the normal units counted
COURSES_USING_OLD_TRANSCRIPT = []

# Enrollment methods
ENROLLMENT_METHODS = (
    'moocng.enrollment.methods.FreeEnrollment',
)

BROKER_URL = 'amqp://moocng:moocngpassword@localhost:5672/moocng'

ASKBOT_URL_TEMPLATE = 'https://questions.example.com/%s/'

CERTIFICATE_URL = 'http://example.com/idcourse/%(courseid)s/email/%(email)s'  # Example, to be overwritten in local settings

MASSIVE_EMAIL_BATCH_SIZE = 30

PEER_REVIEW_TEXT_MAX_SIZE = 5000  # in chars
PEER_REVIEW_FILE_MAX_SIZE = 5  # in MB
PEER_REVIEW_ASSIGNATION_EXPIRE = 24  # in hours

ASSET_SLOT_GRANULARITY = 5  # Slot time of assets should be a multiple of this value (in minutes)


