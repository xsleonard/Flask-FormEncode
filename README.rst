.. _Flask: http://flask.pocoo.org/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _FormEncode: http://www.formencode.org/en/1.2-branch/
.. _FormEncode Documentation: http://www.formencode.org/en/1.2-branch/
.. _FormEncode Schema: http://www.formencode.org/en/1.2-branch/modules/schema.html
.. _FormEncode validators: http://www.formencode.org/en/1.2-branch/Validator.html
.. _CsrfProtect: https://flask-wtf.readthedocs.org/en/latest/csrf.html
.. _Flask-WTF: https://flask-wtf.readthedocs.org/en/latest/
.. _Flask-SeaSurf: http://pythonhosted.org/Flask-SeaSurf/
.. _Complete Flask-FormEncode Documentation: http://pythonhosted.org/Flask-FormEncode/

.. _flask_formencode:

****************
Flask-FormEncode
****************

.. module:: flask_formencode

Flask-FormEncode is a `Flask`_ extension for `FormEncode`_, a validation and
form generation package.

Flask and `Werkzeug`_ specific support is added for loading ``request`` data in
a `FormEncode Schema`_ automatically, and for `FormEncode validators`_ that handle file
uploading.

CSRF protection is not offered by this extension, see `Flask-SeaSurf`_ or
`Flask-WTF`_'s `CsrfProtect`_ for that.

.. seealso:: `Complete Flask-FormEncode Documentation`_

.. seealso:: `FormEncode Documentation`_


Example
=======

.. code-block:: python

    from flask import Flask, redirect, flash, abort
    from flask.ext.formencode import Form
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
