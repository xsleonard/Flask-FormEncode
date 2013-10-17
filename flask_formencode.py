from flask import request
from formencode.variabledecode import variable_decode
from formencode.validators import (
    FieldStorageUploadConverter as _FieldStorageUploadConverter
)
from werkzeug.datastructures import FileStorage


class Form(object):
    """ Wrapper around :class:`formencode.schema.Schema`.

    :param schema: The :class:`formencode.schema.Schema` to wrap.
    :param params: If provided, it will be decoded with
        :func:`formencode.variabledecode.variable_decode` and used in the call
        to :meth:`to_python`. Defaults to ``None``.
    """

    def __init__(self, schema, params=None):
        self.schema = schema
        self.params = self.get_params(params=params)

    def to_python(self, *args, **kwargs):
        """ Wrapper around :func:`formencode.schema.Schema.to_python`.

        If validation fails, :class:`formencode.Invalid` is raised. See:
        http://www.formencode.org/en/latest/Validator.html#invalid-exceptions
        """
        return self.schema(*args, **kwargs).to_python(self.params)

    @staticmethod
    def get_params(params=None):
        """ Returns the request's form parameters.

        If params is not ``None``, it is decoded and returned. Else if
        ``request.json`` is available, that is returned unmodified.
        Otherwise, if ``request.method`` is POST or PUT, ``request.form`` and
        ``request.files`` are decoded, combined and returned.  If
        ``request.method`` is neither POST nor PUT,
        ``request.args`` is decoded and returned.

        Note that this will hide potential multivalued keys in
        :class:`werkzeug.datastructures.MultiDict`, used for
        ``request.args``, ``request.form`` and ``request.files``.
        That is, if the client sends two values for the key 'name', only the
        first will be used. Additionally, if there is a key present in both
        ``request.form`` and ``request.files``, the key from
        ``request.files`` will be used.

        For the way to submit multivalued fields to formencode, see:
        http://www.formencode.org/en/latest/Validator.html#http-html-form-input

        :param params: If provided, this object will be passed through
            :func:`variable_decode` and returned. Defaults to ``None``.
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


class FieldStorageUploadConverter(_FieldStorageUploadConverter):
    """ Same as :class:`formencode.validators.FieldStorageUploadConverter`, but
    supporting :class:`werkzeug.datastructures.FileStorage`.

    .. seealso:: http://www.formencode.org/en/latest/modules/validators.html#formencode.validators.FieldStorageUploadConverter

    .. automethod:: _to_python
    .. automethod:: is_empty
    """

    def _to_python(self, value, state=None):
        """ Returns the same value if it is a :class:`FileStorage`, otherwise
        letting :class:`formencode.validators.FieldStorageUploadConverter`
        decide.

        :param value: Value to convert
        :param state: User-defined state object to pass through validation.
            Defaults to ``None``.
        """
        if isinstance(value, FileStorage):
            return value
        spr = super(FieldStorageUploadConverter, self)
        return spr._to_python(value, state=state)

    def is_empty(self, value):
        """ Returns ``True`` if the filename of the :class`FileStorage` is not set,
        otherwise letting
        :class:`formencode.validators.FieldStorageUploadConverter` decide.

        :param value: Value to check if empty
        """
        if isinstance(value, FileStorage):
            return not value.filename
        return super(FieldStorageUploadConverter, self).is_empty(value)
