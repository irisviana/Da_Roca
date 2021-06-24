from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

from products.models import Product
from users.models import User, Address
from .models import CartProduct


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
                    if int(quantity) < 0:
                        messages.error(request, 'Quantidade não pode ser negativa.')
                    elif int(quantity) == 0:
                        cart_product.delete()
                        messages.success(request, 'Item removido com sucesso.')
                        return redirect('cart')
                    elif int(quantity) <= cart_product.product.stock_amount:
                        cart_product.quantity = quantity
                    else:
                        messages.error(request, 'Quantidade de estoque excedida.')
                elif (cart_product.quantity + 1) <= cart_product.product.stock_amount:
                    cart_product.quantity += 1

                cart_product.save()
            return redirect('cart')
        return redirect('login')

    @classmethod
    def delete(cls, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                cart_product_id = request.POST['cart_product_id']
                decrement = request.POST.get('decrement', 0)
                cart_product = get_object_or_404(CartProduct, id=cart_product_id)
                if int(decrement) == cart_product.quantity or int(decrement) == 0:
                    cart_product.delete()
                    messages.success(request, 'Item removido com sucesso.')
                else:
                    cart_product.quantity -= 1
                    cart_product.save()
            return redirect('cart')
        return redirect('login')


class ConfirmOrderView:
    @classmethod
    def list(cls, request):
        user = get_object_or_404(User, id=request.user.id)
        error_message = []
        if request.user.is_authenticated:
            cart = CartProduct.objects.filter(user_id=user.id).order_by('-id')
            if len(cart) > 0:
                if request.method == "POST":
                    payment_method = request.POST.get('payment_method')
                    address_id = request.POST.get('address')
                    if not payment_method:
                        error_message.append('Selecione um método de pagamento')
                    if not address_id:
                        error_message.append('Selecione um endereço de entrega')
                    if address_id:
                        address = Address.objects.filter(id=address_id, user=user)
                        if not address:
                            error_message.append('O endereço selecionado não existe')



                    ## redirect pra onde quiser

                addresses = Address.objects.filter(user=user)
                cart = CartProduct.objects.filter(user_id=user.id).order_by('-id')
                return render(request, 'cart/confirm_order.html', {
                    "cart": cart,
                    "addresses": addresses,
                    "error_message": error_message
                })

            return render('cart')
        return redirect('login')