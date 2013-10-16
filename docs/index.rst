.. toctree::
   :maxdepth: 2

.. _Flask: http://flask.pocoo.org/
.. _FormEncode: http://www.formencode.org/
.. _FormEncode Documentation: http://www.formencode.org/en/latest

.. _flask_formencode:

****************
Flask-FormEncode
****************

.. module:: flask_formencode

Flask-FormEncode is a `Flask`_ extension for `FormEncode`_, a validation and
form generation package.

.. seealso:: `FormEncode Documentation`_

Installation
============

.. code-block:: bash

    $ pip install Flask-FormEncode

.. _example:

Example
=======

.. code-block:: python

    from flask import Flask, redirect, flash, abort
    from formencode import Invalid, Schema
    from formencode.validators import UnicodeString

    app = Flask(__name__)

    class LoginSchema(Schema):
        username = UnicodeString(strip=True, not_empty=True)

    @app.route('/')
    def index():
        return 'Hello'

    @app.route('/login', methods=['POST'])
    def login():
        try:
            form = Form(LoginSchema)
        except Invalid as e:
            flash(e.unpack_errors())
            abort(400)
        else:
            flash('Welcome {0}'.format(form['username']))
        return redirect(url_for('index'))



.. _api:

API
===

.. _form:

Form
====

.. autoclass:: flask_formencode.Form
    :inherited-members:
