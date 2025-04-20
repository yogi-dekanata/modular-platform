from unittest import TestCase
from apps.product_management.templatetags.custom_tags import get_item

class TestGetItemFilter(TestCase):
    pass
    def test_get_item(self):
        dummy_dict = {
            'a': 1,
            'b': 2,
            'c': 3
        }

        self.assertEqual(get_item(dummy_dict, 'a'), 1)
        self.assertEqual(get_item(dummy_dict, 'b'), 2)
        self.assertEqual(get_item(dummy_dict, 'c'), 3)
        self.assertIsNone(get_item(dummy_dict, 'd'))
