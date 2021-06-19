from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .models import CartProduct
from users.models import User
from products.models import Product

# Create your views here.
class CartProductView():

    @classmethod
    def list(cls, request):
        if request.user.is_authenticated:
            user = request.user
            cart = CartProduct.objects.filter(user_id=user.id).order_by('-id')
            return render(request, 'cart/home.html', {
                "cart": cart,
            })
        return redirect('login')

    @classmethod
    def create(cls, request):
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'POST':
                product_id = request.POST['product_id']
                quantity = request.POST['quantity']
                try:
                    cart_product = CartProduct.objects.get(
                        user_id=user.id, product_id=product_id)
                    cart_product.quantity += quantity
                    cart_product.save()

                except CartProduct.DoesNotExist:
                    cart_product = CartProduct(
                        quantity=quantity,
                        product=Product.objects.get(pk=product_id),
                        user=User.objects.get(pk=user.id))
                    cart_product.save()
        return redirect('login')

    @classmethod
    def update(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                cart_product_id = request.POST['cart_product_id']
                quantity = request.POST.get('quantity', None) # Increment if no quantity is provided
                cart_product = get_object_or_404(CartProduct, id=cart_product_id)
                if quantity:
                    if int(quantity) <= 0:
                        messages.error(request, 'Quantidade não pode ser negativa.')
                    elif int(quantity) <= cart_product.product.stock_amount:
                        cart_product.quantity = quantity
                    else:
                        messages.error(request, 'Quantidade de estoque excedida.')
                elif (cart_product.quantity + 1) <= cart_product.product.stock_amount:
                    cart_product.quantity += 1

                cart_product.save()
            return redirect('cart')
        return redirect('login')
