from flask import request
from formencode.variabledecode import variable_decode


class Form(object):
    """ Wrapper around `formencode.schema.Schema`.

    :param schema: The :class:`formencode.schema.Schema` to wrap.
    :param params: If provided, it will be decoded with
        :func:`formencode.variabledecode.variable_decode` and used in the call
        to :meth:`to_python`. Defaults to `None`.
    """

    def __init__(self, schema, params=None):
        self.schema = schema
        self.params = self.get_params(params=params)

    def get_params(self, params=None):
        """ Returns the request's form parameters.

        If params is not `None`, it is decoded and returned. Else if
        `request.json` is available, that is returned unmodified.
        Otherwise, if `request.method` is POST or PUT, `request.form` and
        `request.files` are decoded, combined and returned.  If
        `request.method` is neither POST nor PUT,
        `request.args` is decoded and returned.

        Note that this will hide potential multivalued keys from
        `werkzeug.datastructures.MultiDict`, used for
        `request.args`, `request.form` and `request.files`.
        That is, if the client sends two values for the key 'name', only the
        first will be used. Additionally, if there is a key present in both
        `request.form` and `request.files`, the key from
        `request.files` will be used.

        For the way to submit multivalued fields to formencode, see:
        http://www.formencode.org/en/latest/Validator.html#http-html-form-input

        :param params: Default `None`. If provided, this object will be
            passed through `variable_decode` and returned.
        """
        if params is not None:
            return variable_decode(params)
        if request.json is not None:
            return request.json
        if request.method in ('POST', 'PUT'):
            params = variable_decode(request.form)
            files = variable_decode(request.files)
            params.update(files)
            return params
        else:
            return variable_decode(request.args)

    def to_python(self, *args, **kwargs):
        """ Wrapper around `formencode.schema.Schema.to_python`.

        If validation fails, `formencode.Invalid` is raised. See:
        http://www.formencode.org/en/latest/Validator.html#invalid-exceptions
        """
        return self.schema(*args, **kwargs).to_python(self.params)
