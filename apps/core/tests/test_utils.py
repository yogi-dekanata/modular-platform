from unittest import TestCase
from unittest.mock import MagicMock

from apps.core.utils import has_role

class TestHasRole(TestCase):
    def setUp(self):
        self.user = MagicMock()
        self.user.is_authenticated = True
        self.user.groups.filter.return_value.exists.return_value = False

    def test_user_has_role(self):
        self.user.groups.filter.return_value.exists.return_value = True
        roles = ['Manager', 'User']
        result = has_role(self.user, roles)
        self.assertTrue(result)

    def test_user_does_not_have_role(self):
        self.user.groups.filter.return_value.exists.return_value = False
        roles = ['Manager', 'User']
        result = has_role(self.user, roles)
        self.assertFalse(result)

    def test_unauthenticated_user(self):
        self.user.is_authenticated = False
        roles = ['Manager', 'User']
        result = has_role(self.user, roles)
        self.assertFalse(result)
