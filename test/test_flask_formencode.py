from unittest import TestCase
from mock import patch, call
from flask import Flask
from formencode.schema import Schema
from formencode.validators import UnicodeString
from werkzeug.datastructures import FileStorage
from flask_formencode import Form, FieldStorageUploadConverter


class DummySchema(Schema):
    name = UnicodeString(strip=True, not_empty=True)


class BaseFlaskTest(TestCase):

    def setUp(self):
        super(BaseFlaskTest, self).setUp()
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        super(BaseFlaskTest, self).tearDown()
        if self._ctx is not None:
            self._ctx.pop()


class FormTest(TestCase):

    @patch.object(Form, 'get_params')
    def test_create(self, mock_get_params):
        f = Form(DummySchema)
        self.assertEqual(f.schema, DummySchema)
        mock_get_params.assert_called_once_with(params=None)

    @patch.object(Form, 'get_params')
    def test_create_with_params(self, mock_get_params):
        params = dict(name='dog')
        f = Form(DummySchema, params=params)
        self.assertEqual(f.schema, DummySchema)
        mock_get_params.assert_called_once_with(params=params)


class FormParamsTest(BaseFlaskTest):

    def setUp(self):
        super(FormParamsTest, self).setUp()
        self.params = dict(name='dog')
        self.files = dict(image='dog.jpg')

    @patch('flask_formencode.variable_decode')
    def test_get_params_with_given_params(self, mock_decode):
        mock_decode.return_value = self.params
        p = Form.get_params(params=self.params)
        self.assertEqual(p, self.params)
        mock_decode.assert_called_once_with(self.params)

    @patch('flask_formencode.request')
    def test_get_params_with_json(self, mock_request):
        mock_request.json = self.params
        p = Form.get_params()
        self.assertEqual(p, self.params)

    @patch('flask_formencode.variable_decode')
    @patch('flask_formencode.request')
    def test_get_params_when_post_put(self, mock_request, mock_decode):
        for method in ('POST', 'PUT'):
            mock_request.json = None
            mock_request.method = method
            mock_request.form = dict(**self.params)
            mock_request.files = dict(**self.files)
            expected = dict(**self.params)
            expected.update(self.files)
            mock_decode.return_value = expected
            p = Form.get_params()
            self.assertEqual(p, expected)
            calls = [call(self.params), call(self.files)]
            mock_decode.assert_has_calls(calls)

    @patch('flask_formencode.variable_decode')
    @patch('flask_formencode.request')
    def test_get_params_when_get(self, mock_request, mock_decode):
        mock_request.json = None
        mock_request.method = 'GET'
        mock_request.args = self.params
        mock_decode.return_value = self.params
        p = Form.get_params()
        self.assertEqual(p, self.params)
        mock_decode.assert_called_once_with(self.params)


class FormToPythonTest(TestCase):

    @patch.object(Form, 'get_params')
    @patch.object(DummySchema, 'to_python')
    def test_to_python(self, mock_to_python, mock_params):
        mock_to_python.return_value = 'xxx'
        params = dict(name='dog')
        mock_params.return_value = params
        f = Form(DummySchema, params=params)
        r = f.to_python()
        self.assertEqual(r, 'xxx')
        mock_to_python.assert_called_once_with(params)

    @patch.object(Form, 'get_params')
    @patch.object(DummySchema, '__init__')
    @patch.object(DummySchema, 'to_python')
    def test_to_python_varargs(self, mock_to_python, mock_init, mock_params):
        mock_init.return_value = None
        f = Form(DummySchema, params={})
        mock_params.return_value = {}
        f.to_python(1, something='x')
        mock_init.assert_called_with(1, something='x')


class FieldStorageUploadConverterTest(TestCase):

    def test_convert_to_python(self):
        v = FileStorage(filename='xxx.jpg')
        c = FieldStorageUploadConverter()
        self.assertEqual(c._to_python(v), v)

    @patch('flask_formencode._FieldStorageUploadConverter._to_python')
    def test_convert_to_python_is_not_filestorage(self, mock_convert):
        c = FieldStorageUploadConverter()
        v = 88
        mock_convert.return_value = 7
        self.assertEqual(c._to_python(v, state='xxx'), 7)
        mock_convert.assert_called_once_with(v, state='xxx')

    def test_is_empty(self):
        c = FieldStorageUploadConverter()
        v = FileStorage(filename='xxx.jpg')
        self.assertFalse(c.is_empty(v))
        self.assertTrue(c.is_empty(FileStorage(filename='')))

    @patch('flask_formencode._FieldStorageUploadConverter.is_empty')
    def test_is_empty_is_not_filestorage(self, mock_is_empty):
        c = FieldStorageUploadConverter()
        v = 'xxx'
        mock_is_empty.return_value = True
        self.assertTrue(c.is_empty(v))
        mock_is_empty.assert_called_once_with(v)


def test_flask_ext_import():
    try:
        import flask.ext.formencode as _
    except ImportError:
        msg = 'flask_formencode extension is not importing via flask.ext'
        assert False, msg
    _
