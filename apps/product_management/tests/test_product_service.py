from unittest import TestCase
from unittest.mock import patch, MagicMock
from apps.product_management.services.product_service import ProductService


class TestProductService(TestCase):
    @patch('apps.product_management.services.product_service.ProductRepository')
    def test_list_products(self, mock_repo):
        mock_repo.list.return_value = (['product1', 'product2'], ['id', 'name'])
        products, columns = ProductService.list_products()
        self.assertEqual(products, ['product1', 'product2'])
        self.assertEqual(columns, ['id', 'name'])

    @patch('apps.product_management.services.product_service.ProductRepository')
    def test_create_product(self, mock_repo):
        mock_repo.list.return_value = ([], ['id', 'name'])
        mock_repo.create.return_value = 'created_product'
        request_post = {'id': 1, 'name': 'Test Product'}
        result = ProductService.create_product(request_post)
        self.assertEqual(result, 'created_product')
        mock_repo.create.assert_called_with(id=1, name='Test Product')

    @patch('apps.product_management.services.product_service.get_pk')
    @patch('apps.product_management.services.product_service.ProductRepository')
    def test_update_product(self, mock_repo, mock_get_pk):
        mock_repo.list.return_value = ([], ['id', 'name'])
        mock_get_pk.return_value = 123
        mock_repo.update.return_value = 'updated_product'
        request_post = {'id': 1, 'name': 'Updated Product', 'details': {'nested': 'ignored'}}
        result = ProductService.update_product('some_pk', request_post)
        self.assertEqual(result, 'updated_product')
        mock_repo.update.assert_called_with(123, id=1, name='Updated Product')

    @patch('apps.product_management.services.product_service.ProductRepository')
    def test_delete_product(self, mock_repo):
        mock_repo.soft_delete.return_value = 'deleted_product'
        result = ProductService.delete_product(1)
        self.assertEqual(result, 'deleted_product')
        mock_repo.soft_delete.assert_called_with(1)

    @patch('apps.product_management.services.product_service.ProductRepository')
    def test_get_product(self, mock_repo):
        mock_repo.get_by_id.return_value = 'product_data'
        result = ProductService.get_product(1)
        self.assertEqual(result, 'product_data')
        mock_repo.get_by_id.assert_called_with(1)
