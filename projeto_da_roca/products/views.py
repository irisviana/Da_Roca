from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product
from users.models import User
from .forms import ProductForm

# Create your views here.

class ProductView:
    @classmethod
    def list_products(cls, request):
        if request.user.is_authenticated:
            user = request.user
            if user.id:
                products = Product.objects.filter(user=user.id)
            else:
                products = Product.objects.all()

            return render(request, 'product/home.html', {
                "products": products,
            })
        return redirect('login')

    @classmethod
    def create_product(cls, request):
        form = ProductForm()
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'POST':
                form = ProductForm(request.POST or None)
                if form.is_valid():
                    product = form.save(commit=False)
                    product.user = user
                    product.save()

                    return redirect('list_products')

            return render(request, 'product/create.html', {
                'form': form
            })
        return redirect('login')

    @classmethod
    def update_product(cls, request, product_id):
        product = get_object_or_404(Product, id = product_id)
        if request.user.is_authenticated:
            form = ProductForm(instance=product)
            user = request.user
            if request.method == 'POST':
                form = ProductForm(request.POST,instance=product)
                if form.is_valid():
                    product = form.save(commit = False)
                    product.user = user
                    product.save()

                    return redirect('list_products')

            return render(request, 'product/update.html', {
                'form': form,
                'post': product,
                'products': product
            })
        return redirect('login')

    @classmethod
    def delete_product(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                product_id = request.POST['product_id']
                product = get_object_or_404(Product, id=product_id)
                product.delete()
                return redirect('list_products')
        return redirect('login')

