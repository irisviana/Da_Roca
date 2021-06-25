from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

from products.models import Product
from users.models import User, Address
from .models import CartProduct, Order, OrderProduct, Payment

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
                    quantity = int(quantity)
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
                return render(request, 'cart/home.html', {
                    "cart": cart_product,
                    })
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
        if request.user.is_authenticated:
            cart = CartProduct.objects.filter(user_id=user.id).order_by('-id')
            if len(cart) > 0:
                if request.method == "POST":
                    payment_method = request.POST.get('payment_method')
                    address_id = request.POST.get('address')
                    address = None
                    if not payment_method:
                        messages.error(request, 'Selecione um método de pagamento')
                        return redirect('confirm-order')
                    if not address_id:
                        messages.error(request, 'Selecione um endereço de entrega')
                        return redirect('confirm-order')
                    try:
                        address = Address.objects.get(id=address_id, user=user)
                        if not address:
                            messages.error(request, 'O endereço selecionado não existe')
                    except Address.DoesNotExist:
                        messages.error(request, 'Endereço inválido, tente novamente')
                        return redirect('confirm-order')

                    total_price = ConfirmOrderView.get_total_price(cart)
                    payment = Payment(type=payment_method, status=0)
                    payment.save()
                    order = Order(
                        status=0, address=address, user=user, payment=payment, total_price=total_price)
                    order.save()

                    for c in cart:
                        orderProduct = OrderProduct(
                            quantity=c.quantity, product=c.product, order=order)
                        orderProduct.save()

                        c.delete()

                    messages.success(request, 'Pedido feito com sucesso.')
                    return redirect('cart')

                addresses = Address.objects.filter(user=user)
                cart = CartProduct.objects.filter(user_id=user.id).order_by('-id')
                return render(request, 'cart/confirm_order.html', {
                    "cart": cart,
                    "addresses": addresses,
                })

            return redirect('cart')
        return redirect('login')

    @staticmethod
    def get_total_price(cart):
        total = 0

        if len(cart):
            for c in cart:
                total += c.product.price * c.quantity

        return total
