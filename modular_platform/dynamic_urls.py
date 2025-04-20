from django.urls import path, include
from apps.modular_engine.models.module import Module


def get_dynamic_module_urls():
    dynamic_urls = []

    installed_modules = Module.objects.filter(status='installed')

    for module in installed_modules:
        if module.slug == 'product_management':
            dynamic_urls.append(
                path('product/', include('apps.product_management.urls'))
            )
        # Nanti bisa tambah module lain di sini

    return dynamic_urls
