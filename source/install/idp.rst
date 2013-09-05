IdP
===

IdP is the SAML Identity Provider of OpenMOOC based on  simpleSAMLphp,
it takes care of the user registration/authentication process.

Before install the rpm, configure your hostname (the rpm creates a nginx file
configuration based on it).

.. code-block:: none

    # yum install openmooc-idp-nginx

This will install a simpleSAMLphp instance and all the required dependencies
for OpenMOOC, including the userregistration module, a ldap, a theme
a working nginx, etc.




