modoboa-radicale
================

|gha| |codecov|

The `Radicale <http://radicale.org/>`_ frontend of Modoboa.

Installation
------------

Install this extension system-wide or inside a virtual environment by
running the following commands::

  $ pip install https://github.com/modoboa/caldav/tarball/master#egg=caldav
  $ pip install modoboa-radicale

Edit the settings.py file of your modoboa instance and apply the following modifications:

- add ``modoboa_radicale`` inside the ``MODOBOA_APPS`` variable like this::

    MODOBOA_APPS = (
      'modoboa',
      'modoboa.core',
      'modoboa.lib',
      'modoboa.admin',
      'modoboa.transport',
      'modoboa.relaydomains',
      'modoboa.limits',
      'modoboa.parameters',
      # Extensions here
      # ...
      'modoboa_radicale',
    )

- Add the following at the end of the file::

    from modoboa_radicale import settings as modoboa_radicale_settings
    modoboa_radicale_settings.apply(globals())

Run the following commands to setup the database tables::

  $ cd <modoboa_instance_dir>
  $ python manage.py migrate
  $ python manage.py load_initial_data
  $ python manage.py collectstatic
    
Finally, restart the python process running modoboa (uwsgi, gunicorn,
apache, whatever).

For developpers
---------------

The frontend part of this plugin is developed with `VueJS 2 <https://vuejs.org/>`_ and
requires `nodejs <https://nodejs.org/en/>`_ and `webpack <https://webpack.js.org/>`_.

Once nodejs is installed on your system, run the following commands::

  $ cd frontend
  $ npm install
  $ npm run serve

To update dist files (the ones that will be distributed with the plugin), run::

  $ npm run build

.. |gha| image:: https://github.com/modoboa/modoboa-radicale/actions/workflows/plugin.yml/badge.svg
   :target: https://github.com/modoboa/modoboa-radicale/actions/workflows/plugin.yml
.. |codecov| image:: http://codecov.io/github/modoboa/modoboa-radicale/coverage.svg?branch=master
   :target: http://codecov.io/github/modoboa/modoboa-radicale?branch=master
