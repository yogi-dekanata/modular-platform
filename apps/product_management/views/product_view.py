from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from apps.core.utils import has_role
from apps.modular_engine.models.module import Module
from apps.product_management.services.product_service import ProductService


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
class ProductListView(View):
    def get(self, request):
        # Cek module product_management status
        try:
            module = Module.objects.get(slug='product_management')
            if module.status != 'installed':
                return render(request, 'errors/module_not_installed.html', status=404)

        except Module.DoesNotExist:
            return render(request, 'errors/module_not_found.html', status=404)

        products, columns = ProductService.list_products()

        can_create = can_update = can_delete = False

        if request.user.is_authenticated:
            if request.user.has_perm('product_management.add_product'):
                can_create = True
            if request.user.has_perm('product_management.change_product'):
                can_update = True
            if request.user.has_perm('product_management.delete_product'):
                can_delete = True

        return render(request, 'product_management/product_list.html', {
            'products': products,
            'columns': columns,
            'can_create': can_create,
            'can_update': can_update,
            'can_delete': can_delete,
        })


@method_decorator([login_required(login_url='/accounts/login/'), permission_required('product_management.add_product', raise_exception=True)], name='dispatch')
class ProductCreateView(View):
    def post(self, request):
        if not has_role(request.user, ['Manager', 'User']):
            raise PermissionDenied

        ProductService.create_product(request.POST)
        return redirect('product_list')


@method_decorator([login_required(login_url='/accounts/login/'), permission_required('product_management.change_product', raise_exception=True)], name='dispatch')
class ProductUpdateView(View):
    def post(self, request, pk):
        if not has_role(request.user, ['Manager', 'User']):
            raise PermissionDenied

        product = ProductService.get_product(pk)
        ProductService.update_product(product, request.POST)
        return redirect('product_list')


@method_decorator([login_required(login_url='/accounts/login/'), permission_required('product_management.delete_product', raise_exception=True)], name='dispatch')
class ProductDeleteView(View):
    def post(self, request, pk):
        if not has_role(request.user, ['Manager']):
            raise PermissionDenied

        ProductService.delete_product(pk)
        return redirect('product_list')
