import environ
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from orders.models import CartProduct
from products.models import Category, Product
from users.models import User, Address
import os 
env = environ.Env()

if os.getenv('BUILD_ON_TRAVIS', None):
    TEST_ON_FIREFOX='on'
    FIREFOXDRIVER_PATH="geckodriver-v0.29.1-linux64/geckodriver"
else:
    TEST_ON_CHROME = True if env('TEST_ON_CHROME') == 'on' else False
    TEST_ON_FIREFOX = True if env('TEST_ON_FIREFOX') == 'on' else False


class OrderTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = None

        if TEST_ON_CHROME:
            cls.selenium = webdriver.Chrome(executable_path=env('CHROMEDRIVER_PATH'))
        elif TEST_ON_FIREFOX:
            cls.selenium = webdriver.Firefox(executable_path=env('FIREFOXDRIVER_PATH'))

        cls.selenium.get('http://127.0.0.1:8000')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self, user=False):
        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        ) if not user else user

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user.email)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys('abcde123456')
        driver.find_element_by_xpath('//input[@value="Entrar"]').click()
        assert 'email ou senha estão incorretos' not in driver.page_source

    def test_create_order(self):
        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )
        Address.objects.create(
            user=user,
            address_type='user',
            zip_code='55370000',
            state='PE',
            city='Garanhuns',
            district='Boa Vista',
            street='Rua rua rua rua',
            house_number=123,
        )
        driver = self.selenium
        self.test_login(user)

        fruit_category = Category.objects.create(name="Fruit")
        maca_product = Product.objects.create(
            name='Maça',
            variety='Comum',
            expiration_days=7,
            price=1.5,
            stock_amount=50,
            category=fruit_category,
            user=user
        )
        CartProduct.objects.create(
            user=user,
            product=maca_product,
            quantity=20
        )
        driver.get('%s%s' % (self.live_server_url, "/order/cart/"))
        driver.find_element_by_xpath("//a[@title=\"Prosseguir compra\"]").click()
        driver.find_element_by_class_name("address").click()
        driver.find_element_by_id("C").click()
        driver.find_element_by_xpath("//button[@title=\"Finalizar compra\"]").click()
        assert 'Pedido feito com sucesso.' in driver.page_source

    def test_list_seller_orders(self):
        driver = self.selenium
        self.test_create_order()

        driver.get('%s%s' % (self.live_server_url, "/order/seller/"))
        driver.find_element_by_class_name('order-cell')
        assert True

    def test_cancel_seller_orders(self):
        driver = self.selenium
        self.test_create_order()

        driver.get('%s%s' % (self.live_server_url, "/order/seller/"))
        driver.find_element_by_xpath('//a[@title=\"Ver pedido\"]').click()
        driver.find_element_by_id('update-status-button').click()
        driver.find_element_by_id('update-status-modal-button').click()
        select_option = Select(driver.find_element_by_id('status-value')).first_selected_option.get_attribute(
            "value")

        assert select_option == '4'

    def test_delivery_order(self):
        driver = self.selenium
        self.test_create_order()

        driver.get('%s%s' % (self.live_server_url, "/order/seller/"))
        driver.find_element_by_xpath('//a[@title=\"Ver pedido\"]').click()
        driver.find_element_by_xpath("//select[@name='status_value']/option[text()='Em rota de entrega']").click()
        select_option = Select(driver.find_element_by_id('status-value')).first_selected_option.get_attribute(
            "value")

        assert select_option == '2'

    def test_delivered_order(self):
        driver = self.selenium
        self.test_create_order()

        driver.get('%s%s' % (self.live_server_url, "/order/seller/"))
        driver.find_element_by_xpath('//a[@title=\"Ver pedido\"]').click()
        driver.find_element_by_xpath("//select[@name='status_value']/option[text()='Concluído']").click()
        select_option = Select(driver.find_element_by_id('status-value')).first_selected_option.get_attribute(
            "value")

        assert select_option == '3'
