Flask-FormEncode
================

Flask extension for the form processing &amp; validation library [FormEncode](http://www.formencode.org/en/1.2-branch/)

[![PyPI version](https://badge.fury.io/py/Flask-FormEncode.png)](http://badge.fury.io/py/Flask-FormEncode)
[![Build Status](https://travis-ci.org/xsleonard/Flask-FormEncode.png)](https://travis-ci.org/xsleonard/Flask-FormEncode)
[![Coverage Status](https://coveralls.io/repos/xsleonard/Flask-FormEncode/badge.png?branch=master)](https://coveralls.io/r/xsleonard/Flask-FormEncode?branch=master)

[Read the complete docs](https://flask-formencode.readthedocs.org)

Flask-FormEncode supports python 2.6, 2.7 and pypy. Python 3 support will be added once FormEncode supports it (expected next release).

To run the tests, do `python setup.py test`.

Example:

```python
# app.py
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
```
