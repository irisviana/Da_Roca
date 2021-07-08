from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from products.models import Product
from users.models import User, Address
from .models import CartProduct, Order, OrderProduct, Payment, Rating


class CartProductView:
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
                product = Product.objects.get(pk=product_id)
                if product.stock_amount < int(quantity):
                    messages.error(request,
                        'Estoque do produto excedido, tente comprar de outro produtor.')
                    return redirect('view_product', product_id=product_id)
                try:
                    cart_product = CartProduct.objects.get(
                        user_id=user.id, product_id=product_id)
                    cart_product.quantity += int(quantity)
                    cart_product.save()

                except CartProduct.DoesNotExist:
                    cart_products = CartProduct.objects.filter(
                        user_id=user.id)

                    if (len(cart_products) > 0 and \
                        cart_products[0].product.user.id == product.user.id) or \
                        (len(cart_products) == 0):
                        cart_product = CartProduct(
                            quantity=quantity,
                            product=product,
                            user=User.objects.get(pk=user.id))
                        cart_product.save()
                    else:
                        messages.error(request,
                            'Você possui produtos de outro produtor no carrinho, remova-os ou finalize a compra para poder comprar esse produto')
                        return redirect('view_product', product_id=product.id)

                return redirect('cart')
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


class OrderView:
    @classmethod
    def list(cls, request):
        user = get_object_or_404(User, id=request.user.id)
        if request.user.is_authenticated:
            cart = CartProduct.objects.filter(user_id=user.id).order_by('-id')
            if len(cart) > 0:
                if request.method == "POST":
                    payment_method = request.POST.get('payment_method')
                    address_id = request.POST.get('address')
                    change = request.POST.get('change', None)
                    change = change.replace(',', '.')
                    address = None
                    if not payment_method:
                        messages.error(request, 'Selecione um método de pagamento.')
                        return redirect('confirm_order')
                    if not address_id:
                        messages.error(request, 'Selecione um endereço de entrega.')
                        return redirect('confirm_order')
                    if not change and payment_method == 'C':
                        messages.error(request, 'Defina o valor do troco se for pagar em dinheiro.')
                        return redirect('confirm_order')
                    try:
                        address = Address.objects.get(id=address_id, user=user)
                        if not address:
                            messages.error(request, 'O endereço selecionado não existe.')
                    except Address.DoesNotExist:
                        messages.error(request, 'Endereço inválido, tente novamente.')
                        return redirect('confirm_order')

                    total_price = OrderView.get_total_price(cart)
                    payment = Payment(type=payment_method, status=0, change=change if change else 0)
                    payment.save()
                    order = Order(
                        status=0, address=address, user=user, payment=payment, total_price=total_price)
                    order.save()

                    for c in cart:
                        c.product.stock_amount -= c.quantity
                        c.product.save()

                        orderProduct = OrderProduct(
                            quantity=c.quantity, product=c.product, order=order)
                        orderProduct.save()

                        c.delete()

                    messages.success(request, 'Pedido feito com sucesso.')
                    return redirect('list_user_orders')

                addresses = Address.objects.filter(user=user)
                cart = CartProduct.objects.filter(user_id=user.id).order_by('-id')
                return render(request, 'cart/confirm_order.html', {
                    "cart": cart,
                    "addresses": addresses,
                })

            return redirect('cart')
        return redirect('login')

    @classmethod
    def list_order(cls, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            orders = Order.objects.filter(user=user).order_by('-id')

            return render(
                request,
                'orders/list_user_orders.html',
                {'orders': orders}
            )
        return redirect('login')

    @classmethod
    def view_order(cls, request, order_id):
        if request.user.is_authenticated:
            order = get_object_or_404(Order, pk=order_id)
            order_items = OrderProduct.objects.filter(order_id=order.id)
            try:
                rating = Rating.objects.get(order_id=order.id)
            except Rating.DoesNotExist:
                rating = None

            return render(
                request,
                'orders/view_order.html',
                {
                    'order': order,
                    'order_products': order_items,
                    'rating': rating,
                }
            )
        return redirect('login')

    @staticmethod
    def get_total_price(cart):
        total = 0

        if len(cart):
            for c in cart:
                total += c.product.price * c.quantity

        return total

    @classmethod
    def cancel_order(cls, request):
        if request.user.is_authenticated:
            if request.method == "POST":
                order_id = request.POST.get("order_id")
                order = get_object_or_404(Order, id=order_id)
                order.status = 4
                order.save()

                order_products = OrderProduct.objects.filter(order_id=order.id)
                for order_product in order_products:
                    product = order_product.product
                    product.stock_amount += order_product.quantity
                    product.save()

            if request.user.is_admin:
                return redirect("list_all_orders")
            else:
                return redirect("list_user_orders")
        return redirect('login')

    @classmethod
    def list_all_orders(cls, request):
        if request.user.is_authenticated:
            orders = Order.objects.all().order_by('-id')
            return render(request, '../templates/orders/list_seller_orders.html', {'orders': orders})
        return redirect('login')


class SellerOrderView:
    @classmethod
    def list(cls, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            orders = Order.objects.filter(orderproduct__product__user=user).order_by('-id')

            return render(request, '../templates/orders/list_seller_orders.html', {'orders': orders})

        return redirect('login')

    @classmethod
    def index(cls, request):
        order_id = request.GET.get('order_id', None)
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            order = Order.objects.get(id=order_id, orderproduct__product__user=user)
            order_products = OrderProduct.objects.filter(order=order)

            return render(request, '../templates/orders/details_seller_order.html', {
                'order': order,
                'order_products': order_products
            })

        return redirect('login')

    @classmethod
    def cancel(cls, request, order_id):
        order = get_object_or_404(Order, pk=order_id, orderproduct__product__user=request.user)
        if request.user.is_authenticated:
            order.status = 4
            order.save()
            return redirect(reverse('seller_order_detail') + '?order_id={}'.format(order_id))

        return redirect('login')

    @classmethod
    def update(cls, request, order_id):
        status_value = request.POST.get('status_value', None)

        order = get_object_or_404(Order, pk=order_id, orderproduct__product__user=request.user)
        if request.user.is_authenticated:
            order.status = status_value
            order.save()
            return redirect(reverse('seller_order_detail') + '?order_id={}'.format(order_id))

        return redirect('login')
class RatingView:

    @classmethod
    def create(cls, request):
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'POST':
                is_anonimous = request.POST.get('is_anonimous', True)
                order_id = request.POST['order_id']
                rate = request.POST['rate']
                rate_message = request.POST.get('rate_message', None)

                order = Order.objects.get(pk=order_id)
                ratings = Rating.objects.filter(order_id=order.id)
                if len(ratings):
                    messages.error(request, 'Esse pedido já foi avaliado.')
                    return redirect('list_user_orders')
                rating = Rating(
                    order=order,
                    rate=rate,
                    rate_message=rate_message,
                    user=(user if not is_anonimous else None))
                rating.save()
                messages.success(request, 'Avaliação publicada com sucesso.')
            return redirect('list_user_orders')
        return redirect('login')
