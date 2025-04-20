from django.utils import timezone

from django.db import connection

class BaseRepository:

    @staticmethod
    def get_table_name():
        raise NotImplementedError("Child class must implement get_table_name()")

    @classmethod
    def list(cls, exclude_fields=None):
        table_name = cls.get_table_name()
        with connection.cursor() as cursor:
            real_columns = [
                col.name for col in connection.introspection.get_table_description(cursor, table_name)
            ]

            if exclude_fields:
                real_columns = [col for col in real_columns if col not in exclude_fields]

            query = f"SELECT {', '.join(real_columns)} FROM {table_name} WHERE is_deleted = FALSE"
            cursor.execute(query)

            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return rows, real_columns

    @classmethod
    def get_by_id(cls, pk):
        table_name = cls.get_table_name()
        with connection.cursor() as cursor:
            query = f"SELECT * FROM {table_name} WHERE id = %s AND is_deleted = FALSE"
            cursor.execute(query, [pk])
            row = cursor.fetchone()
            if not row:
                return None
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))

    @classmethod
    def create(cls, **kwargs):
        if not kwargs:
            raise ValueError("Cannot create with empty data.")

        table_name = cls.get_table_name()
        if 'is_deleted' not in kwargs:
            kwargs['is_deleted'] = False
        if 'created_at' not in kwargs:
            kwargs['created_at'] = timezone.now()
        if 'updated_at' not in kwargs:
            kwargs['updated_at'] = timezone.now()
        fields = ', '.join(kwargs.keys())
        placeholders = ', '.join(['%s'] * len(kwargs))
        values = list(kwargs.values())

        with connection.cursor() as cursor:
            query = f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders}) RETURNING id"
            cursor.execute(query, values)
            return cursor.fetchone()[0]

    @classmethod
    def update(cls, pk, **kwargs):
        table_name = cls.get_table_name()
        set_clause = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        values = list(kwargs.values())
        values.append(pk)  # <- pk append terakhir

        with connection.cursor() as cursor:
            query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"
            cursor.execute(query, values)

    @classmethod
    def soft_delete(cls, pk):
        table_name = cls.get_table_name()
        with connection.cursor() as cursor:
            query = f"UPDATE {table_name} SET is_deleted = TRUE WHERE id = %s"
            cursor.execute(query, [pk])


class ProductRepository(BaseRepository):

    @staticmethod
    def get_table_name():
        return 'product_management_product'