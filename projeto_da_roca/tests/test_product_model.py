
from django.test import TestCase
from django.db.utils import IntegrityError
from users.models import User
# Create your tests here.


class ProductTest(TestCase):
    """ Test module for Product model """

    def setUp(self):
        self.producer_rodrigo = User.objects.create(
            first_name="Rodrigo", email="rodrigo@gmail.com",
            cpf="70550481419", password="teste", is_seller=True)

        self.fruit_category = Category.objects.create(
            name="Fruit")
        self.orange = Product.objects.create(user=self.producer_rodrigo,
                                             name="orange", variety="test",
                                             expiration_days=10, price=2.0,
                                             stock_amount=50,
                                             category=self.fruit_category)

    def test_register_product_with_all_data_filled_in(self):
        apple = Product.objects.create(user=self.producer_rodrigo,
                                       name="apple", variety="test",
                                       expiration_days=10, price=2.0,
                                       stock_amount=50,
                                       category=self.fruit_category)

        self.assertEqual(apple.name, "apple")

    def test_register_product_with_empty_fields(self):
        self.jack_fruit = None
        try:
            self.orange = Product.objects.create(user=self.producer_rodrigo,
                                                 name=None, variety=None,
                                                 expiration_days=None,
                                                 price=None,
                                                 stock_amount=None,
                                                 category=None)
        except IntegrityError:
            self.assertEqual(self.jack_fruit, None)

    def test_successfully_edit_product(self):
        self.orange.stock_amount = 100
        self.orange.save()
        self.assertEqual(self.orange.stock_amount, 100)

    def test_edit_product_with_empty_fields(self):
        try:
            self.orange = Product.objects.filter(pk=self.orange.id).update(user=self.producer_rodrigo,
                                                                           name=None, variety=None,
                                                                           expiration_days=None,
                                                                           price=None,
                                                                           stock_amount=None,
                                                                           category=None)

        except IntegrityError:
            self.assertEqual(self.orange.name, "orange")

    def test_edit_with_incomplete_data(self):
        try:
            self.orange.id = Product.objects.filter(
                pk=self.orange.id).update(name=None)

        except IntegrityError:
            self.assertEqual(self.orange.name, "orange")

    def test_edit_product_and_dont_save(self):
        self.orange.price = 4.0
        product_orange = Product.objects.get(pk=self.orange.id)
        self.assertNotEqual(product_orange.price, 4.0)

    def test_delete_product(self):
        try:
            self.orange = self.orange.delete()

        except IntegrityError:
            self.assertEqual(self.orange.name, "orange")
