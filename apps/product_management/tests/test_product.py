from unittest import TestCase
from unittest.mock import patch, MagicMock
from apps.product_management.models.product import Product

class TestProduct(TestCase):
    @patch('apps.product_management.models.product.Product.save')
    def test_soft_delete(self, mock_save):
        # Arrange
        product = Product(name="Dummy", barcode="12345", price=10.0, stock=5)

        # Act
        product.delete()

        # Assert
        self.assertTrue(product.is_deleted)
        mock_save.assert_called_once()

    def test_str_representation(self):
        product = Product(name="Dummy Product")
        self.assertEqual(str(product), "Dummy Product")