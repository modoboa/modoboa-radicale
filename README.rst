modoboa-radicale
================

|travis| |codecov| |landscape|

The `Radicale <http://radicale.org/>`_ frontend of Modoboa.

Installation
------------

Install this extension system-wide or inside a virtual environment by
running the following command::

  $ pip install modoboa-radicale

Edit the settings.py file of your modoboa instance and add
``modoboa_radicale`` inside the ``MODOBOA_APPS`` variable like this::

    MODOBOA_APPS = (
      'modoboa',
      'modoboa.core',
      'modoboa.lib',
      'modoboa.admin',
      'modoboa.relaydomains',
      'modoboa.limits',
      # Extensions here
      # ...
      'modoboa_radicale',
    )

Run the following commands to setup the database tables::

  $ cd <modoboa_instance_dir>
  $ python manage.py migrate
  $ python manage.py load_initial_data
  $ python manage.py collectstatic
    
Finally, restart the python process running modoboa (uwsgi, gunicorn,
apache, whatever).

.. |landscape| image:: https://landscape.io/github/modoboa/modoboa-radicale/master/landscape.svg?style=flat
   :target: https://landscape.io/github/modoboa/modoboa-radicale/master
   :alt: Code Health
.. |travis| image:: https://travis-ci.org/modoboa/modoboa-radicale.png?branch=master
   :target: https://travis-ci.org/modoboa/modoboa-radicale
.. |codecov| image:: http://codecov.io/github/modoboa/modoboa-radicale/coverage.svg?branch=master
   :target: http://codecov.io/github/modoboa/modoboa-radicale?branch=master
