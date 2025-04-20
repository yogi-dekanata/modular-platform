from unittest import TestCase
from unittest.mock import patch, MagicMock
from apps.product_management.repositories.product_repository import ProductRepository

class TestBaseRepository(TestCase):
    @patch('apps.product_management.repositories.product_repository.connection')
    def test_list(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        # FIX: Kolom name harus string beneran
        mock_connection.introspection.get_table_description.return_value = [
            type('col', (object,), {'name': 'id'})(),
            type('col', (object,), {'name': 'name'})(),
        ]

        mock_cursor.description = [('id',), ('name',)]
        mock_cursor.fetchall.return_value = [
            (1, 'Product A'),
            (2, 'Product B')
        ]

        rows, columns = ProductRepository.list()

        self.assertEqual(columns, ['id', 'name'])
        self.assertEqual(rows, [
            {'id': 1, 'name': 'Product A'},
            {'id': 2, 'name': 'Product B'}
        ])

    @patch('apps.product_management.repositories.product_repository.connection')
    def test_list_exclude_fields(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_connection.introspection.get_table_description.return_value = [
            type('col', (object,), {'name': 'id'})(),
            type('col', (object,), {'name': 'name'})(),
            type('col', (object,), {'name': 'barcode'})(),
        ]

        mock_cursor.description = [('id',), ('name',)]
        mock_cursor.fetchall.return_value = [
            (1, 'Product A'),
        ]

        rows, columns = ProductRepository.list(exclude_fields=['barcode'])

        self.assertEqual(columns, ['id', 'name'])
        self.assertEqual(rows, [{'id': 1, 'name': 'Product A'}])

    @patch('apps.product_management.repositories.product_repository.connection')
    def test_get_by_id_found(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.description = [('id',), ('name',)]
        mock_cursor.fetchone.return_value = (1, 'Product A')

        result = ProductRepository.get_by_id(1)

        self.assertEqual(result, {'id': 1, 'name': 'Product A'})

    @patch('apps.product_management.repositories.product_repository.connection')
    def test_get_by_id_not_found(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = ProductRepository.get_by_id(1)

        self.assertIsNone(result)

    @patch('apps.product_management.repositories.product_repository.connection')
    def test_create(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [123]

        result = ProductRepository.create(name='Product A', barcode='123456', price=10.0, stock=100)

        self.assertEqual(result, 123)

    @patch('apps.product_management.repositories.product_repository.connection')
    def test_update(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        ProductRepository.update(1, name='Updated Name')

        mock_cursor.execute.assert_called()

    @patch('apps.product_management.repositories.product_repository.connection')
    def test_soft_delete(self, mock_connection):
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        ProductRepository.soft_delete(1)

        mock_cursor.execute.assert_called()
