Translations
============

Generate django.po files
------------------------

Severals django.po files will be placed in this folder when running:

.. code-block:: python

    django-admin makemessages --all --ignore=.venv

Generate django.mo files
------------------------

After the Translations are complete, severals django.mo files will be generated with translations when running:

.. code-block:: python

    django-admin compilemessages --ignore=.venv
