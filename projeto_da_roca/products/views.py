from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm

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

class CategoryView:
    @classmethod
    def list_categories(cls, request):
        if request.user.is_authenticated:
            user = request.user
            if user.id:
                categories = Category.objects.filter()
            else:
                categories = Category.objects.all()

            return render(request, 'category/home.html', {
                "categories": categories,
            })
        return redirect('login')

    @classmethod
    def create_category(cls, request):
        form = CategoryForm()
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'POST':
                form = CategoryForm(request.POST or None)
                if form.is_valid():
                    category = form.save(commit=False)
                    category.user = user
                    category.save()

                    return redirect('list_categories')
            return render(request, 'category/create.html', {
                'form': form
            })
        return redirect('login')

    @classmethod
    def update_category(cls, request, category_id):
        category = get_object_or_404(Category, id = category_id)
        if request.user.is_authenticated:
            form = CategoryForm(instance=category)
            user = request.user
            if request.method == 'POST':
                form = CategoryForm(request.POST, instance=category)
                if form.is_valid():
                    category = form.save(commit=False)
                    category.user = user
                    category.save()

                    return redirect('list_categories')
            return render(request, 'category/update.html', {
                'form': form,
                'post': category,
                'category': category
            })
        return redirect('login')

    @classmethod
    def delete_category(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                category_id = request.POST['category_id']
                category = get_object_or_404(Category, id=category_id)
                category.delete()
                return redirect('list_categories')
        return redirect('login')

    
def get_categories(request):
    categories = Category.objects.all()
    return {"categories": categories}

