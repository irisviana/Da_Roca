from django.db.utils import DataError, IntegrityError
from django.test import TestCase

from products.models import Category, Product
from orders.models import CartProduct, Payment, OrderProduct, Order, Rating
from users.models import User, ServiceAddress, DeliveryTime, Address


# Create your tests here.

class UsersTest(TestCase):
    """ Test module for User model """

    def setUp(self):
        self.user_rodrigo = User.objects.create(
            first_name="Rodrigo", email="rodrigo@gmail.com",
            cpf="70550481419", password="teste")

        self.user_thais = User.objects.create(
            first_name="Thais", email="thais@gmail.com",
            cpf="66668592007", password="teste")

        self.user_amanda = User.objects.create(
            first_name="Amanda", email="amanda@gmail.com",
            cpf="29963571085", password="teste")

        self.user_admin = User.objects.create(
            first_name='Admin',
            email='admin@gmail.com',
            cpf='11111111111',
            password='123456',
        )

    def test_create_client_successfully(self):
        user_iris = User.objects.create(
            first_name = "Íris", email = "iris@gmail.com",
            cpf="82441895095", password="teste")
        self.assertEqual(
             user_iris.cpf,"82441895095")

    def test_create_client_without_cpf(self):
        user_iris=None
        try:
            user_iris = User.objects.create(
                first_name = "Íris", email = "iris@gmail.com",
                cpf=None, password="teste")

        except Exception :
            self.assertIsNone(user_iris)

    def test_update_client_valid_email(self):
        old_email = self.user_thais.email
        self.user_thais.email = "thais@hotmail.com"
        self.user_thais.save()
        self.assertNotEqual(old_email, self.user_thais.email)

    def test_create_user_existing_email(self):
        user_raquel = None
        try:
            user_raquel = User.objects.create(
                first_name = 'Raquel',
                email = 'thais@gmail.com',
                cpf = '22222222222',
                password = '123456'
            )
        except IntegrityError:
            self.assertFalse(user_raquel)

    def test_update_user_existing_email(self):
        try:
            self.user_rodrigo.email = 'thais@gmail.com'
            self.user_rodrigo.save()
        except IntegrityError:
            assert True

    def test_update_user_password(self):
        try:
            self.user_rodrigo.password = 'abcde123456'
            self.user_rodrigo.save()
            assert True
        except IntegrityError:
            assert False

    def test_login_user(self):
        user = User.objects.get(email=self.user_admin.email, password=self.user_admin.password)
        self.assertEqual(user.email, self.user_admin.email)

    def test_login_user_does_not_exist(self):
        user = None
        try:
            user = User.objects.get(email='paula@email.com', password='123456')
        except User.DoesNotExist:
            self.assertFalse(user)

    def test_login_user_invalid_credentials(self):
        user = None
        try:
            user = User.objects.get(email=self.user_admin.email, password='12345678')
        except User.DoesNotExist:
            self.assertFalse(user)

    def test_add_admin_permission(self):
        #user inst admin
        self.assertEqual(self.user_rodrigo.is_admin,False)
        self.user_rodrigo.is_admin=True
        self.user_rodrigo.save()
        #user is admin
        self.assertEqual(self.user_rodrigo.is_admin,True)

    def test_add_seller_permission(self):
        #user inst seller
        self.assertEqual(self.user_rodrigo.is_seller,False)
        self.user_rodrigo.is_seller=True
        self.user_rodrigo.save()
        #user is seller
        self.assertEqual(self.user_rodrigo.is_seller,True)

    def test_remove_user_access(self):
        user = User.objects.get(pk=self.user_admin.pk, is_active=True)
        user.is_active = False
        user.save()
        self.assertEqual(user.is_active, False)

    def test_search_user_with_email(self):
        user = User.objects.get(email=self.user_admin.email)
        self.assertEqual(self.user_admin.email, user.email)

    def test_search_user_with_name(self):
        user = User.objects.get(first_name=self.user_admin.first_name)
        self.assertEqual(self.user_admin.first_name, user.first_name)

    def test_search_user_with_nothing(self):
        user = None
        try:
            user = User.objects.filter()
        except DataError:
            self.assertFalse(user)

    def test_search_user_does_not_exist(self):
        user = None
        try:
            user = User.objects.get(email='paloma@email.com')
        except User.DoesNotExist:
            self.assertFalse(user)

    def test_update_store_status_to_open(self):
        old_status = self.user_amanda.store_status
        self.user_amanda.store_status = "Aberto"
        self.user_amanda.save()
        self.assertNotEqual(old_status, self.user_amanda.store_status)

    def test_update_store_status_to_closed(self):
        self.user_amanda.store_status = "Fechado"
        self.user_amanda.save()
        self.assertNotEqual("Aberto", self.user_amanda.store_status)


class DeliveryTimeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name="Rodrigo", email="rodrigo@gmail.com",
            cpf="70550481419", password="teste"
        )
        self.service_address = ServiceAddress.objects.create(
            user=self.user,
            city = 'Garanhuns',
            state = 'PE'
        )
        self.delivery_time = DeliveryTime.objects.create(
            service_address = self.service_address,
            day = 'monday',
            time = '14:00'
        )

    def test_create_delivery_time_successfully(self):
        delivery_time = DeliveryTime.objects.create(
            service_address = self.service_address,
            day = 'monday',
            time = '14:00'
        )

        self.assertTrue(delivery_time)

    def test_create_delivery_time_with_error(self):
        delivery_time = None
        try:
            delivery_time = DeliveryTime.objects.create(
                service_address = self.service_address,
                time = '14:00'
            )

        except DataError:
            self.assertFalse(delivery_time)

    def test_update_delivery_time_successfully(self):
        old_delivery_time_day = self.delivery_time.day
        self.delivery_time.day = 'tuesday'
        self.delivery_time.save()
        self.assertNotEqual(old_delivery_time_day, self.delivery_time.day)

    def test_update_delivery_time_with_error(self):
        old_delivery_time_day = self.delivery_time.day
        try:
            DeliveryTime.objects.filter(pk=self.delivery_time.pk).update(day=None)
        except IntegrityError:
            self.assertEqual(old_delivery_time_day, self.delivery_time.day)

    def test_delete_delivery_time(self):
        old_id = self.delivery_time.pk
        self.delivery_time.delete()

        search_delivery_time = None
        try:
            search_delivery_time = DeliveryTime.objects.get(pk=old_id)
        except DeliveryTime.DoesNotExist:
            self.assertFalse(search_delivery_time)


class CategoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Raquel", email="raquel@gmail.com",
            cpf="70550481419", password="teste"
        )

        self.category = Category.objects.create(
            name='Frutas'
        )

    def test_create_category_successfully(self):
        category = Category.objects.create(
            name='Verduras'
        )

        self.assertTrue(category)

    def test_create_category_with_error_name(self):
        name = 'Frutas'
        category = None
        try:
            category = Category.objects.create(
                name=name
            )
        except IntegrityError:
            self.assertFalse(category)

    def test_create_category_with_error_empty(self):
        category = None
        try:
            category = Category.objects.create(
                name=""
            )
        except IntegrityError:
            self.assertFalse(category)

    def test_delete_category(self):
        old_id = self.category.pk
        self.category.delete()
        search_category = None
        try:
            search_category = Category.objects.get(pk=old_id)
        except Category.DoesNotExist:
            self.assertFalse(search_category)


class AddressTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name="Rodrigo", email="rodrigo@gmail.com",
            cpf="70550481419", password="teste"
        )
        self.address = Address.objects.create(
            user=self.user, zip_code="56.640-000",
            state="PE", city="Custódia",
            district="centro", street="Rua 1",
            house_number=1
        )

    def test_create_address_successfully(self):
        address = Address.objects.create(
            user=self.user, zip_code="56.640-000",
            state="PE", city="Custódia",
            district="centro", street="Rua 1",
            house_number=1
        )

        self.assertTrue(address)

    def test_create_address_with_error(self):
        address = None
        try:
            address = Address.objects.create(
                user=self.user,
                state="PE", city="Custódia",
                district="centro", street="Rua 1",
                house_number=1
            )

        except DataError:
            self.assertFalse(address)

    def test_update_address_successfully(self):
        old_address_house_number = self.address.house_number
        self.address.house_number = 2
        self.address.save()
        self.assertNotEqual(old_address_house_number, self.address.house_number)

    def test_update_address_with_error(self):
        old_address_zip_code = self.address.zip_code
        try:
            Address.objects.filter(pk=self.address.pk).update(zip_code=None)
        except IntegrityError:
            self.assertEqual(old_address_zip_code, self.address.zip_code)

class CartProductTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name="Rodrigo",
            email="rodrigo@gmail.com",
            cpf="70550481419",
            password="teste",
        )

        self.address = Address.objects.create(
            user = self.user,
            address_type = 'user',
            zip_code = '55370000',
            state = 'PE',
            city = 'Garanhuns',
            district = 'Boa Vista',
            street = 'Rua rua rua rua',
            house_number = 123,
        )

        self.category = Category.objects.create(
            user=self.user,
            name='Frutas'
        )

        self.maca = Product.objects.create(
            user=self.user,
            name='Maça',
            variety='Comum',
            expiration_days=7,
            stock_amount=50,
            category=self.category,
        )

        self.banana = Product.objects.create(
            user=self.user,
            name='Banana',
            variety='Prata',
            expiration_days=7,
            stock_amount=50,
            category=self.category,
            price=3
        )

        self.cart_product = CartProduct.objects.create(
            quantity=10,
            product=self.maca,
            user=self.user,
        )

    def test_add_cart_product(self):
        cart_product = CartProduct.objects.create(
            quantity=10,
            product=self.maca,
            user=self.user,
        )

        self.assertTrue(cart_product)

    def test_remove_cart_product(self):
        old_id = self.cart_product.pk
        self.cart_product.delete()

        search_cart_product = None
        try:
            search_cart_product = CartProduct.objects.get(
                pk=old_id)
        except CartProduct.DoesNotExist:
            self.assertFalse(search_cart_product)

    def test_increment_cart_product(self):
        old_cart_product_quantity = self.cart_product.quantity
        self.cart_product.quantity += 1
        self.cart_product.save()
        self.assertNotEqual(self.cart_product.quantity, old_cart_product_quantity)

    def test_decrement_cart_product(self):
        old_cart_product_quantity = self.cart_product.quantity
        self.cart_product.quantity -= 1
        self.cart_product.save()
        self.assertNotEqual(self.cart_product.quantity, old_cart_product_quantity)

    def test_create_order(self):
        payment = Payment.objects.create(
            type='C', status=0
        )
        order = Order.objects.create(
            status=0, address=self.address, user=self.user, payment=payment, total_price=6
        )
        OrderProduct.objects.create(
            quantity=2, product=self.banana, order=order
        )
        self.assertTrue(order)

    def test_create_order_incomplete(self):
        order = None
        try:
            order = Order.objects.create(
                status=0, user=self.user
            )
            OrderProduct.objects.create(
                quantity=2, product=self.banana, order=order
            )
        except IntegrityError:
            self.assertFalse(order)

class RatingTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name="Rodrigo",
            email="rodrigo@gmail.com",
            cpf="70550481419",
            password="teste",
        )

        self.address = Address.objects.create(
            user = self.user,
            address_type = 'user',
            zip_code = '55370000',
            state = 'PE',
            city = 'Garanhuns',
            district = 'Boa Vista',
            street = 'Rua rua rua rua',
            house_number = 123,
        )

        self.category = Category.objects.create(
            user=self.user,
            name='Frutas'
        )

        self.maca = Product.objects.create(
            user=self.user,
            name='Maça',
            variety='Comum',
            expiration_days=7,
            stock_amount=50,
            category=self.category,
        )

        self.banana = Product.objects.create(
            user=self.user,
            name='Banana',
            variety='Prata',
            expiration_days=7,
            stock_amount=50,
            category=self.category,
            price=3
        )

        self.payment = Payment.objects.create(
            type='C', status=0
        )
        self.order = Order.objects.create(
            status=3, address=self.address, user=self.user, payment=self.payment, total_price=6
        )
        OrderProduct.objects.create(
            quantity=2, product=self.banana, order=self.order
        )

    def test_create_rating(self):
        rate = Rating.objects.create(
            rate=5,
            rate_message='Muito bom!',
            user=self.user,
            order=self.order,
        )

        self.assertTrue(rate)

    def test_create_rating_without_comment(self):
        rate = Rating.objects.create(
            rate=5,
            user=self.user,
            order=self.order,
        )

        self.assertTrue(rate)

    def test_create_rating_without_rate(self):
        rate = None
        try:
            rate = Rating.objects.create(
                rate_message='Muito bom!',
                user=self.user,
                order=self.order,
            )
        except IntegrityError:
            self.assertFalse(rate)