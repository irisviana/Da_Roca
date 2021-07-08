from django.contrib import messages
from users.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import Product, Category, Favorite
from .forms import ProductForm, CategoryForm
from django.db.models import Q

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
            print(request.FILES)
            if request.method == 'POST':
                form = ProductForm(request.POST or None,request.FILES)
                if form.is_valid():
                    product = form.save(commit=False)
                    product.user = user
                    product.stock_amount_prev = product.stock_amount
                    product.save()

                    return redirect('list_products')

            return render(request, 'product/create.html', {
                'form': form
            })
        return redirect('login')

    @classmethod
    def update_product(cls, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            form = ProductForm(instance=product)
            user = request.user
            if request.method == 'POST':
                form = ProductForm(request.POST,request.FILES, instance=product)
                if form.is_valid():
                   
                    product = form.save(commit=False)
                   
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
                product = get_object_or_404(
                Product, id=product_id)
                product.delete()
                return redirect('list_products')
        return redirect('login')

    @classmethod
    def delete_product(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                product_id = request.POST['product_id']
                product = get_object_or_404(
                    Product, id=product_id)
                product.delete()
                return redirect('list_products')
        return redirect('login')

    @classmethod
    def delete_product_admin(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                product_id = request.POST['product_id']
                product = get_object_or_404(
                    Product, id=product_id)
                product.delete()
                return render(request, 'product/manage_products.html')
        return redirect('login')
    
    @classmethod
    def view_product(cls, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'GET':
                favorite = Favorite.objects.filter(user=user, product=product)
                return render(request, 'product/view_product.html', {
                    'product': product,
                    'favorites': favorite
                })
        else:
            if request.method == 'GET':
                favorite = None
                return render(request, 'product/view_product.html', {
                    'product': product,
                    'favorites': favorite
                })

    @classmethod
    def search_product(cls, request):
        if request.user.is_authenticated:
            if request.method == 'GET':

                search_string = request.GET.get('search',None)
                if search_string:
                    products = Product.objects.filter(Q(name__icontains=search_string) | Q(variety__icontains=search_string))
                else:
                    products = Product.objects.all()
                return render(
                    request,
                    '../templates/users_profile/search_seller_product.html',
                    {
                        'products': products,
                        'filter': 'Produto'
                    }
                )
        products = Product.objects.all()
        return render(
                    request,
                    '../templates/users_profile/search_seller_product.html',
                    {
                        'products': products,
                        'filter': 'Produto'
                    }
                )

    @classmethod
    def filter_product_category(cls, request):
        if request.user.is_authenticated:
            if request.method == 'GET':
                category_id = request.GET.get('category_id')
                products = []
                if category_id:
                    products = Product.objects.filter(category_id=category_id)
                return render(
                    request,
                    '../templates/users_profile/search_seller_product.html',
                    {
                        'products': products,
                        'filter': 'Produto'
                    }
                )

        return redirect('login')

    @classmethod
    def search_product_to_admin(cls, request):
        if request.user.is_authenticated:
            if request.method == 'GET':
                search_string = request.GET.get('table-search')

                sellers = User.objects.filter(
                    Q(first_name__icontains=search_string) | Q(last_name__icontains=search_string))

                products = Product.objects.filter(
                    Q(name__icontains=search_string) | Q(variety__icontains=search_string) | Q(user__in=sellers))

                return render(request, 'product/manage_products.html', {'products': products})

        return redirect('login')

    @classmethod
    def see_products(cls, request):
        if request.user.is_authenticated:
            return render(request, 'product/manage_products.html', )
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
                product = Product.objects.filter(category=category)
                if len(product) > 0:
                    messages.error(request, 'Não é possível excluir categorias com produtos.')
                else:
                    category.delete()
                    messages.success(request, 'Categoria removida com sucesso.')
                return redirect('list_categories')
        return redirect('login')

def get_categories(request):
    categories = Category.objects.all()
    return {"categories": categories}

class FavoriteView:
    @classmethod
    def list_favorites(cls, request):
        if request.user.is_authenticated:
            user = request.user
            favorites = Favorite.objects.filter(user_id=user.id)

            return render(request, 'favorite/home.html', {
                "favorites": favorites 
            })
        return redirect('login')

    @classmethod
    def create_favorite(cls, request):
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'POST':
                product_id = request.POST['product_id']
                product = Product.objects.get(id=product_id)

                try:
                    favorite = Favorite.objects.get(user=user, product=product)
                    favorite.delete()
                except Favorite.DoesNotExist:
                    favorite = Favorite(user=user, product=product)
                    favorite.save()

            return redirect('view_product', product_id=product.id)
        return redirect('login')
    
    @classmethod
    def delete_favorite(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                favorite_id = request.POST['favorite_id']
                favorite = get_object_or_404(Favorite, id=favorite_id)
                favorite.delete()

            return redirect('list_favorites')
        return redirect('login')