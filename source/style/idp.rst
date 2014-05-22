OpenMOOC Style Guide - IdP
==========================

In simpleSAMLphp a theme is a module. The openmooc theme is at the modules folder: sspopenmooc

This module has a configuration file module_sspopenmooc.php where are allocated style info:

.. code-block:: none

    'cssfile' => '',              // css file
    'bootstrapfile' => '',        // bootstrap file  
    'imgfile' => '.',             // logo 
    'title' => '',                // Is the html title
    'slogan' => '',               // Title under the logo (subtitle in MoocNG)


If you don't set a value/filename, then the default values will be used. 

At www/openmooc/ you can find:

  * css
      * bootstrap.css A bootstrap v2 css file. (bootstrapfile)
      * default.css  Some extra css that extends the bootstrap.css file. (cssfile)
  * img
      * logo.png The logo of the OpenMOOC entity.  (imgfile)

For more info about themes check: https://simplesamlphp.org/docs/stable/simplesamlphp-theming
