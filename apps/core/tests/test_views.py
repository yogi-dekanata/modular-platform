from unittest import TestCase
from unittest.mock import patch, MagicMock

from apps.core.views import custom_permission_denied_view

class TestCustomPermissionDeniedView(TestCase):
    @patch('apps.core.views.render')
    def test_custom_permission_denied_view_positive(self, mock_render):
        mock_response = MagicMock(status_code=403)
        mock_render.return_value = mock_response

        response = custom_permission_denied_view(MagicMock())
        self.assertEqual(response.status_code, 403)

    @patch('apps.core.views.render')
    def test_custom_permission_denied_view_negative(self, mock_render):
        mock_render.side_effect = Exception("Something went wrong")

        with self.assertRaises(Exception):
            custom_permission_denied_view(MagicMock())
