from apps.product_management.repositories.product_repository import ProductRepository
from apps.core.identifiers import get_pk


class ProductService:
    EXCLUDED_FIELDS = {'created_at', 'updated_at', 'is_deleted'}

    @staticmethod
    def list_products():
        products, real_columns = ProductRepository.list(exclude_fields=ProductService.EXCLUDED_FIELDS)
        return products, real_columns

    @staticmethod
    def create_product(request_post):
        _, real_columns = ProductRepository.list(exclude_fields=ProductService.EXCLUDED_FIELDS)
        data = {
            field: request_post.get(field)
            for field in real_columns
            if request_post.get(field) is not None
        }
        return ProductRepository.create(**data)

    @staticmethod
    def update_product(pk, request_post):
        _, real_columns = ProductRepository.list(exclude_fields=ProductService.EXCLUDED_FIELDS)

        # Fix: build hanya primitive field
        data = {}
        for field in real_columns:
            value = request_post.get(field)
            if value is not None:
                if isinstance(value, (dict, list)):
                    continue  # Abaikan kalau value dict atau list
                data[field] = value

        return ProductRepository.update(get_pk(pk), **data)

    @staticmethod
    def delete_product(pk):
        return ProductRepository.soft_delete(pk)

    @staticmethod
    def get_product(pk):
        return ProductRepository.get_by_id(pk)
