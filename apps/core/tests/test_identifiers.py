from unittest import TestCase
from apps.core.identifiers import get_pk

class TestGetPk(TestCase):
    def test_get_pk_from_dict(self):
        data = {'id': 123}
        result = get_pk(data)
        self.assertEqual(result, 123)

    def test_get_pk_from_integer(self):
        data = 456
        result = get_pk(data)
        self.assertEqual(result, 456)

    def test_get_pk_from_dict_without_id(self):
        data = {'name': 'Product'}
        result = get_pk(data)
        self.assertIsNone(result)

    def test_get_pk_from_none(self):
        data = None
        result = get_pk(data)
        self.assertIsNone(result)
