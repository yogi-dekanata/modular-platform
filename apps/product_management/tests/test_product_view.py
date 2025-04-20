from unittest import TestCase
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from apps.product_management.views.product_view import ProductListView, ProductCreateView


class TestProductListView(TestCase):
    @patch('apps.product_management.views.product_view.ProductService')
    @patch('apps.product_management.views.product_view.Module')
    def test_get(self, mock_module, mock_service):
        factory = RequestFactory()
        request = factory.get('/products/')
        request.user = MagicMock(is_authenticated=True)
        request.user.has_perm.side_effect = lambda perm: True

        mock_module.objects.get.return_value.status = 'installed'
        mock_service.list_products.return_value = ([{'id': 1, 'name': 'Test Product'}], ['id', 'name'])

        response = ProductListView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestProductCreateView(TestCase):
    @patch('apps.product_management.views.product_view.has_role')
    @patch('apps.product_management.views.product_view.ProductService')
    def test_post(self, mock_service, mock_has_role):
        factory = RequestFactory()
        request = factory.post('/products/create/', data={'name': 'Test Product'})
        request.user = MagicMock(is_authenticated=True)

        mock_has_role.return_value = True
        mock_service.create_product.return_value = None

        response = ProductCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/product/')

