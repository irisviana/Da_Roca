import environ
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from orders.models import CartProduct, Order, OrderProduct, Payment
from products.models import Category, Product
from users.models import User, DeliveryTime, ServiceAddress, Address
from users.utils import check_has_class
import os

chrome_options = Options()
env = environ.Env()


TEST_ON_CHROME = True if os.getenv('TEST_ON_CHROME') == 'on' else False
TEST_ON_FIREFOX = True if os.getenv('TEST_ON_FIREFOX') == 'on' else False


class UsersTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = None
        if TEST_ON_CHROME:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            cls.selenium = webdriver.Chrome(executable_path=os.getenv('CHROMEDRIVER_PATH'),options=chrome_options)
        elif TEST_ON_FIREFOX:
            cls.selenium = webdriver.Firefox(executable_path=os.getenv('FIREFOXDRIVER_PATH'))

        #Choose your url to visit
        cls.selenium.get('http://127.0.0.1:8000')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self, user=False):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
        ) if not user else user

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user.email)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys('abcde123456')
        driver.find_element_by_xpath('//input[@value="Entrar"]').click()
        assert 'email ou senha estão incorretos' not in driver.page_source

    def test_admin_search_user_with_cpf(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
        )

        driver = self.selenium
        self.test_login()
        driver.get('%s%s' % (self.live_server_url, '/user/admin/users/all'))
        search_input = driver.find_element_by_id('custom_table-search')
        search_input.send_keys(user.cpf)
        assert user.cpf in driver.page_source

    def test_admin_search_user_with_name(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
        )

        driver = self.selenium
        self.test_login()
        driver.get('%s%s' % (self.live_server_url, '/user/admin/users/all'))
        search_input = driver.find_element_by_id('custom_table-search')
        search_input.send_keys(user.first_name)
        assert user.first_name in driver.page_source

    def test_admin_search_user_with_error(self):
        driver = self.selenium
        self.test_login()
        driver.get('%s%s' % (self.live_server_url, '/user/admin/users/all'))
        search_input = driver.find_element_by_id('custom_table-search')
        search_input.send_keys('Luana')
        assert 'Luana' not in driver.page_source

    def test_admin_remove_user(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
        )

        driver = self.selenium
        self.test_login()
        driver.get('%s%s' % (self.live_server_url, '/user/admin/users/all'))
        driver.find_element_by_xpath(f"//button[@data-query=\"user_id={user.id},user_type=all\"]").click()
        driver.find_element_by_xpath("//button[@class=\"btn btn-danger btn-confirm\"]").click()
        assert user.first_name not in driver.page_source

    def test_admin_self_remove(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
        )

        driver = self.selenium
        self.test_login(user)
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/update"))
        driver.find_element_by_xpath("//button[@class=\"btn btn-danger\"]").click()
        driver.find_element_by_xpath("//button[@class=\"btn btn-danger btn-confirm\"]").click()
        assert 'Acesso' not in driver.page_source

    def test_user_self_edit(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
        )
        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/update"))
        first_name_input = driver.find_element_by_name("first_name")
        first_name_input.send_keys('Iris')
        last_name_input = driver.find_element_by_name("last_name")
        last_name_input.send_keys('Viana')
        driver.find_element_by_xpath("//input[@name=\"save\"]").click()
        assert 'Atualizado com sucesso.' in driver.page_source

    def test_update_store_status(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller=True
        )

        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/seller/"))
        status_old = driver.find_element_by_name("status").get_attribute('value')
        driver.find_element_by_xpath("//a[@href=\"/user/seller/updateStoreStatus\"]").click()

        assert status_old not in driver.page_source

    def test_user_self_edit_without_name(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
        )

        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/update"))
        first_name_input = driver.find_element_by_name("first_name")
        first_name_input.clear()
        last_name_input = driver.find_element_by_name("last_name")
        last_name_input.send_keys('Viana')
        driver.find_element_by_xpath("//input[@name=\"save\"]").click()
        assert 'Atualizado com sucesso.' not in driver.page_source

    def test_request_reset_password(self):
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/reset_password"))
        email_input = driver.find_element_by_id("id_email")
        email_input.send_keys('email@dominio.com')
        driver.find_element_by_xpath("//input[@value=\"Recuperar\"]").click()
        assert 'Confirmação de redefinição de senha' in driver.page_source

    def test_update_exists_user_email(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
        )
        User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )
        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/update"))
        driver.find_element_by_id('update-email-button').click()
        new_email_input = driver.find_element_by_id("id_email")
        new_email_input.send_keys('user@gmail.com')
        confirm_new_email_input = driver.find_element_by_id("id_confirm_email")
        confirm_new_email_input.send_keys('user@gmail.com')
        password_confirm_input = driver.find_element_by_id("id_confirm_password")
        password_confirm_input.send_keys('abcde123456')
        driver.find_element_by_id("update-email-modal-button").click()

        assert 'O e-mail já está sendo usado' in driver.page_source

    def test_update_user_password(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
        )
        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/update"))
        driver.find_element_by_id('update-password-button').click()
        old_password_input = driver.find_element_by_id("id_old_password")
        old_password_input.send_keys('abcde123456')
        new_password_input = driver.find_element_by_id("id_new_password")
        new_password_input.send_keys('123456abcde')
        password_confirm_input = driver.find_element_by_id("id_confirm_new_password")
        password_confirm_input.send_keys('123456abcde')
        driver.find_element_by_id("update-password-modal-button").click()

        assert 'Entrar' in driver.page_source

    def test_update_user_incorrect_confirm_password(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
        )
        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/update"))
        driver.find_element_by_id('update-password-button').click()
        old_password_input = driver.find_element_by_id("id_old_password")
        old_password_input.send_keys('abcde123456')
        new_password_input = driver.find_element_by_id("id_new_password")
        new_password_input.send_keys('123456abcde574')
        password_confirm_input = driver.find_element_by_id("id_confirm_new_password")
        password_confirm_input.send_keys('123456abcde')
        driver.find_element_by_id("update-password-modal-button").click()

        assert 'As senhas precisam ser iguais' in driver.page_source

    def test_admin_remove_admin_permissions(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )

        user_to_remove = User.objects.create(
            first_name='Vinicius',
            email='vinicius@gmail.com',
            cpf='33333333333',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )
        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/admin/users/admin"))
        driver.find_element_by_xpath(f"//button[@data-query=\"admin_id={user_to_remove.id},user_type=admin\"]").click()
        driver.find_element_by_xpath("//*[text()='Remover administrador']").click()
        assert user_to_remove.first_name not in driver.page_source

    def test_admin_cancel_remove_admin_permissions(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )

        user_to_remove = User.objects.create(
            first_name='Vinicius',
            email='vinicius@gmail.com',
            cpf='33333333333',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )
        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/admin/users/admin"))
        driver.find_element_by_xpath(f"//button[@data-query=\"admin_id={user_to_remove.id},user_type=admin\"]").click()
        driver.find_element_by_xpath("//div[@id=\"includedModalRemoveAdmin\"]/div/div/div/button[@class=\"btn btn-primary w-50\"]").click()
        assert user_to_remove.first_name in driver.page_source

    def test_admin_remove_producer_permissions(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True,
            is_seller=True
        )

        user_to_remove = User.objects.create(
            first_name='Vinicius',
            email='vinicius@gmail.com',
            cpf='33333333333',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller=True
        )
        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/admin/users/producer"))
        driver.find_element_by_xpath(f"//button[@title=\"Tirar privilégios de produtor\" and @data-query=\"user_id={user_to_remove.id},user_type=producer\"]").click()
        driver.find_element_by_xpath("//*[text()='Remover produtor']").click()
        assert user_to_remove.first_name not in driver.page_source

    def test_admin_cancel_remove_producer_permissions(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True,
            is_seller=True
        )

        user_to_remove = User.objects.create(
            first_name='Vinicius',
            email='vinicius@gmail.com',
            cpf='33333333333',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller=True
        )
        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/admin/users/producer"))
        driver.find_element_by_xpath(f"//button[@title=\"Tirar privilégios de produtor\" and @data-query=\"user_id={user_to_remove.id},user_type=producer\"]").click()
        driver.find_element_by_xpath("//div[@id=\"includedModalRemoveProducer\"]/div/div/div/button[@class=\"btn btn-primary w-50\"]").click()
        assert user_to_remove.first_name in driver.page_source

    def test_visualize_existent_producer(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )
        self.test_login(user)
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/user/seller/view/{user.id}"))
        assert user.first_name in driver.page_source

    def test_visualize_inexistent_producer(self):
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/user/seller/view/view/{-1}"))
        assert 'teste' not in driver.page_source

    def test_seller_search_with_name(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller=True,
        )

        driver = self.selenium
        self.test_login()
        driver.get('%s%s' % (self.live_server_url, f"/user/customer_home"))
        search_input = driver.find_element_by_id("search_")
        search_input.send_keys(user.first_name)
        driver.find_element_by_id("filterSearchDropdown").click()
        driver.find_element_by_xpath("//input[@value=\"option1\"]").click()
        driver.find_element_by_id("button-addon3").click()
        assert user.first_name in driver.page_source

    def test_seller_search_with_name_error(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller=False,
        )

        driver = self.selenium
        self.test_login()
        driver.get('%s%s' % (self.live_server_url, f"/user/customer_home"))
        search_input = driver.find_element_by_id("search_")
        driver.find_element_by_id("filterSearchDropdown").click()
        driver.find_element_by_xpath("//input[@value=\"option1\"]").click()
        search_input.send_keys(user.first_name)
        assert user.first_name not in driver.page_source

    def test_update_delivery_price(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller=True,
            delivery_price=5
        )

        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/user/seller/"))
        price_old = driver.find_element_by_name("price").get_attribute('value')
        search_input = driver.find_element_by_name("price")
        search_input.clear()
        search_input.send_keys("1")
        driver.find_element_by_id("save").click()

        assert price_old != driver.find_element_by_name("price").get_attribute('value')

    def test_delete_product_by_admin(self):
        user = User.objects.create(
            first_name='Iris Viana',
            email='iris@gmail.com',
            cpf='22222222222',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller=True,
            is_admin=True
        )

        category = Category.objects.create(
            name='Verdura'
        )

        product = Product.objects.create(
            user=user,
            name='Alface',
            variety='Americano',
            expiration_days=7,
            price=2,
            category=category,
        )

        driver = self.selenium
        self.test_login(user)
        driver.get('%s%s' % (self.live_server_url, "/product/products/see"))
        search_input = driver.find_element_by_id("custom_table-search")
        search_input.send_keys(product.name)
        driver.find_element_by_id("button-search").click()
        driver.find_element_by_id("button-delete").click()
        driver.find_element_by_xpath("//*[text()='Remover permanentemente']").click()

        assert product.name not in driver.page_source


class DeliveryTimeTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = None
        if TEST_ON_CHROME:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            cls.selenium = webdriver.Chrome(executable_path=os.getenv('CHROMEDRIVER_PATH'))#,options=chrome_options)
        elif TEST_ON_FIREFOX:
            cls.selenium = webdriver.Firefox(executable_path=os.getenv('FIREFOXDRIVER_PATH'))

        #Choose your url to visit
        cls.selenium.get('http://127.0.0.1:8000')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self, user=False):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
        ) if not user else user

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user.email)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys('abcde123456')
        driver.find_element_by_xpath('//input[@value="Entrar"]').click()
        assert 'email ou senha estão incorretos' not in driver.page_source

    def test_create_delivery_time(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)

        service_address = ServiceAddress.objects.create(
            user = user,
            city = 'Garanhuns',
            state = 'PE'
        )

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/user/delivery_time/list/{service_address.id}"))
        driver.find_element_by_xpath(f"//a[@href=\"/user/delivery_time/create/{service_address.id}\"]").click()
        time_input = driver.find_element_by_name("time")
        time_input.send_keys('13:00')
        driver.find_element_by_xpath("//select[@name='day']/option[text()='Quinta-feira']").click()
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        search_input = driver.find_element_by_id('custom_table-search')
        search_input.send_keys('quinta')
        assert '13:00' in driver.page_source and 'Quinta-feira' in driver.page_source

    def test_create_delivery_time_with_error(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)

        service_address = ServiceAddress.objects.create(
            user = user,
            city = 'Garanhuns',
            state = 'PE'
        )

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/user/delivery_time/list/{service_address.id}"))
        driver.find_element_by_xpath(f"//a[@href=\"/user/delivery_time/create/{service_address.id}\"]").click()
        driver.find_element_by_xpath("//select[@name='day']/option[text()='Quinta-feira']").click()
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()

        assert 'Quando você irá atender?' == driver.title

    def test_update_delivery_time(self):
        # Use already created delivery time
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)

        service_address = ServiceAddress.objects.create(
            user = user,
            city = 'Garanhuns',
            state = 'PE'
        )

        delivery_time = DeliveryTime.objects.create(
            service_address=service_address,
            time='13:00',
            day='thursday'
        )

        # Find created delivery time
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/user/delivery_time/list/{service_address.id}"))
        search_input = driver.find_element_by_id('custom_table-search')
        search_input.send_keys('quinta')

        # Click edit button to start editing delivery time
        driver.find_element_by_xpath(f"//a[@href=\"/user/delivery_time/update/{delivery_time.id}\"]").click()

        # Update fields
        driver.find_element_by_xpath("//select[@name='day']/option[text()='Sexta-feira']").click()
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()

        assert '13:00' in driver.page_source and 'Sexta-feira' in driver.page_source

    def test_update_delivery_time_with_error(self):
        # Use already created delivery time
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)

        service_address = ServiceAddress.objects.create(
            user = user,
            city = 'Garanhuns',
            state = 'PE'
        )

        delivery_time = DeliveryTime.objects.create(
            service_address=service_address,
            time='13:00',
            day='thursday'
        )

        # Find created delivery time
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/user/delivery_time/list/{service_address.id}"))
        search_input = driver.find_element_by_id('custom_table-search')
        search_input.send_keys('quinta')

        # Click edit button to start editing delivery time
        driver.find_element_by_xpath(f"//a[@href=\"/user/delivery_time/update/{delivery_time.id}\"]").click()

        # Update fields
        time_input = driver.find_element_by_name("time")
        time_input.clear()
        driver.find_element_by_xpath("//select[@name='day']/option[text()='Sexta-feira']").click()
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()

        validation = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='time']")))
        assert validation.get_attribute("validationMessage")

    def test_delete_delivery_time(self):
        # Use already created delivery time
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)

        service_address = ServiceAddress.objects.create(
            user = user,
            city = 'Garanhuns',
            state = 'PE'
        )

        delivery_time = DeliveryTime.objects.create(
            service_address = service_address,
            time='13:00',
            day='thursday'
        )

        # Find created delivery time
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/user/delivery_time/list/{service_address.id}"))
        search_input = driver.find_element_by_id('custom_table-search')
        search_input.send_keys('quinta')

        driver.find_element_by_xpath(f"//button[@data-query=\"delivery_time_id={delivery_time.id}\"]").click()
        driver.find_element_by_xpath("//button[@class=\"btn btn-danger btn-confirm\"]").click()

        search_input = driver.find_element_by_id('custom_table-search')
        search_input.send_keys('quinta')
        assert '13:00' not in driver.page_source and 'Quinta-feira' not in driver.page_source


class CategoryTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = None

        if TEST_ON_CHROME:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            cls.selenium = webdriver.Chrome(executable_path=os.getenv('CHROMEDRIVER_PATH'),options=chrome_options)
        elif TEST_ON_FIREFOX:
            cls.selenium = webdriver.Firefox(executable_path = os.getenv('FIREFOXDRIVER_PATH'))

        cls.selenium.get('http://127.0.0.1:8000')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self, user=False):
        user = User.objects.create(
            first_name = 'Usuario',
            email = 'usuario@gmail.com',
            cpf = '44455544455',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
        ) if not user else user

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user.email)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys('abcde123456')
        driver.find_element_by_xpath('//input[@value="Entrar"]').click()
        assert 'email ou senha estão incorretos' not in driver.page_source

    def test_create_category(self):
        user = User.objects.create(
            first_name = 'Raquel Vieira',
            email = 'raquel@gmail.com',
            cpf = '99999999999',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/admin"))
        driver.find_element_by_xpath("//a[@href=\"/product/categories/create\"]").click()
        search_input = driver.find_element_by_name('name')
        search_input.send_keys('Frutas')
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        assert 'Frutas' in driver.page_source

    def test_create_category_with_error_name(self):
        user = User.objects.create(
            first_name = 'Raquel Vieira',
            email = 'raquel@gmail.com',
            cpf = '99999999999',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/admin"))
        driver.find_element_by_xpath("//a[@href=\"/product/categories/create\"]").click()
        search_input = driver.find_element_by_name('name')
        search_input.send_keys('Frutas')
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        assert 'Frutas' in driver.page_source
        driver.find_element_by_xpath("//a[@href=\"/product/categories/create\"]").click()
        search_input = driver.find_element_by_name('name')
        search_input.send_keys('Frutas')
        assert 'Cadastre sua categoria' in driver.page_source

    def test_create_category_empty(self):
        user = User.objects.create(
            first_name = 'Raquel Vieira',
            email = 'raquel@gmail.com',
            cpf = '99999999999',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/admin"))
        driver.find_element_by_xpath("//a[@href=\"/product/categories/create\"]").click()
        search_input = driver.find_element_by_name('name')
        search_input.send_keys('')
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        assert 'Cadastre sua categoria' in driver.page_source

    def test_delete_category(self):
        user = User.objects.create(
            first_name = 'Raquel Vieira',
            email = 'raquel@gmail.com',
            cpf = '99999999999',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)
        category = Category.objects.create(
            name='Verdura'
        )

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/admin"))
        driver.find_element_by_xpath("//a[@href=\"/product/categories/list\"]").click()

        driver.find_element_by_xpath(f"//button[@data-query=\"category_id={category.id}\"]").click()
        driver.find_element_by_xpath("//button[@class=\"btn btn-danger btn-confirm\"]").click()

        assert 'Verdura' not in driver.page_source

    def test_delete_category_with_product(self):
        user = User.objects.create(
            first_name = 'Raquel Vieira',
            email = 'raquel@gmail.com',
            cpf = '99999999999',
            password = 'pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_seller = True
        )
        self.test_login(user)
        category = Category.objects.create(
            name='Verdura'
        )

        Product.objects.create(
            user=user,
            name='Alface',
            variety='Americano',
            expiration_days=7,
            price=2,
            category=category,
        )

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/admin"))
        driver.find_element_by_xpath("//a[@href=\"/product/categories/list\"]").click()

        driver.find_element_by_xpath(f"//button[@data-query=\"category_id={category.id}\"]").click()
        driver.find_element_by_xpath("//button[@class=\"btn btn-danger btn-confirm\"]").click()

        assert 'Não é possível excluir categorias com produtos.' in driver.page_source


class CartProductTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = None

        if TEST_ON_CHROME:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            cls.selenium = webdriver.Chrome(executable_path=os.getenv('CHROMEDRIVER_PATH'),options=chrome_options)
        elif TEST_ON_FIREFOX:
            cls.selenium = webdriver.Firefox(executable_path = os.getenv('FIREFOXDRIVER_PATH'))

        cls.selenium.get('http://127.0.0.1:8000')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self, user=False):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
        ) if not user else user

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user.email)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys('abcde123456')
        driver.find_element_by_xpath('//input[@value="Entrar"]').click()
        assert 'email ou senha estão incorretos' not in driver.page_source

    def test_create_cart_product(self):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
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

        driver.get('%s%s' % (self.live_server_url, f"/product/products/view/{maca_product.id}"))
        driver.find_element_by_xpath("//button[@title=\"Comprar agora\"]").click()
        assert maca_product.name in driver.page_source and 'Cesta de compras' in driver.page_source

    def test_increment_cart_product(self):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
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
            quantity=1
        )
        driver.get('%s%s' % (self.live_server_url, "/order/cart/"))
        driver.find_element_by_xpath("//button[@title=\"Adicionar um item\"]").click()
        quantity = driver.find_element_by_name("quantity")
        assert '2' == quantity.get_attribute('value')

    def test_decrement_cart_product(self):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
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
            quantity=10
        )
        driver.get('%s%s' % (self.live_server_url, "/order/cart/"))
        driver.find_element_by_xpath("//button[@title=\"Remover um item\"]").click()
        quantity = driver.find_element_by_name("quantity")
        assert '9' == quantity.get_attribute('value')

    def test_update_cart_product(self):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
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
            quantity=1
        )
        driver.get('%s%s' % (self.live_server_url, "/order/cart/"))
        quantity_type = driver.find_element_by_name("quantity")
        quantity_type.send_keys(Keys.DELETE + '30' + Keys.TAB)
        quantity_assert = driver.find_element_by_name("quantity")
        assert '30' == quantity_assert.get_attribute('value')

    def test_remove_cart_product(self):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
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
            quantity=1
        )
        driver.get('%s%s' % (self.live_server_url, "/order/cart/"))
        driver.find_element_by_xpath("//button[@title=\"Remover produto da cesta\"]").click()
        assert maca_product.name not in driver.page_source

    def test_update_cart_product_exceed_stock(self):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
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
        quantity = driver.find_element_by_name("quantity")
        quantity.send_keys('1' + Keys.TAB)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class=\"alert cart-item message error\"]")))
        assert 'Quantidade de estoque excedida.' in driver.page_source

    def test_create_order(self):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
        )
        address = Address.objects.create(
            user = user,
            address_type = 'user',
            zip_code = '55370000',
            state = 'PE',
            city = 'Garanhuns',
            district = 'Boa Vista',
            street = 'Rua rua rua rua',
            house_number = 123,
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
        driver.get('%s%s' % (self.live_server_url, f"/order/cart/"))
        driver.find_element_by_xpath("//a[@title=\"Prosseguir compra\"]").click()
        address_element = driver.find_element_by_id(address.id)
        address_element.click()
        driver.find_element_by_class_name("address").click()
        driver.find_element_by_id("CC").click()
        driver.find_element_by_xpath("//button[@title=\"Finalizar compra\"]").click()
        assert 'Pedido feito com sucesso.' in driver.page_source

    def test_create_order_back_to_cart(self):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
        )
        Address.objects.create(
            user = user,
            address_type = 'user',
            zip_code = '55370000',
            state = 'PE',
            city = 'Garanhuns',
            district = 'Boa Vista',
            street = 'Rua rua rua rua',
            house_number = 123,
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
        driver.get('%s%s' % (self.live_server_url, f"/order/cart/"))
        driver.find_element_by_xpath("//a[@title=\"Prosseguir compra\"]").click()
        driver.find_element_by_xpath("//a[@title=\"Voltar para o carrinho\"]").click()
        assert 'Cesta de compras' in driver.page_source

    def test_select_order_address(self):
        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )
        address = Address.objects.create(
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
        driver.get('%s%s' % (self.live_server_url, f"/order/cart/"))
        driver.find_element_by_xpath("//a[@title=\"Prosseguir compra\"]").click()
        address_element = driver.find_element_by_id(address.id)
        address_element.click()
        driver.find_element_by_id(address.id)
        assert check_has_class(address_element.get_attribute("class"), "active")

    def test_select_order_not_exist_address(self):
        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
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
        driver.get('%s%s' % (self.live_server_url, f"/order/cart/"))
        driver.find_element_by_xpath("//a[@title=\"Prosseguir compra\"]").click()
        try:
            driver.find_element_by_class_name("address")
            assert False
        except Exception as error:
            assert True

    def test_select_order_address(self):
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
        address2 = Address.objects.create(
            user=user,
            address_type='user',
            zip_code='55555555',
            state='AL',
            city='MACEIO',
            district='Boa Vista',
            street='Rua rua rua rua',
            house_number=322,
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
        driver.get('%s%s' % (self.live_server_url, f"/order/cart/"))
        driver.find_element_by_xpath("//a[@title=\"Prosseguir compra\"]").click()
        address_element = driver.find_element_by_id(address2.id)
        address_element.click()
        driver.find_element_by_id(address2.id)
        assert check_has_class(address_element.get_attribute("class"), "active")

    def test_select_order_payment_method(self):
        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
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
        driver.get('%s%s' % (self.live_server_url, f"/order/cart/"))
        driver.find_element_by_xpath("//a[@title=\"Prosseguir compra\"]").click()
        payment_element = driver.find_element_by_id('CC')
        payment_element.click()
        assert check_has_class(payment_element.get_attribute("class"), "active")

    def test_cash_payment_change(self):
        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )
        address = Address.objects.create(
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
        driver.get('%s%s' % (self.live_server_url, f"/order/cart/"))
        driver.find_element_by_xpath("//a[@title=\"Prosseguir compra\"]").click()
        address_element = driver.find_element_by_id(address.id)
        address_element.click()
        payment_element = driver.find_element_by_id('C')
        payment_element.click()
        change_input = driver.find_element_by_id('change')
        change_input.send_keys(20)
        driver.find_element_by_xpath("//button[@title=\"Finalizar compra\"]").click()
        assert 'Pedido feito com sucesso.' in driver.page_source

    def test_cash_payment_no_change(self):
        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )
        address = Address.objects.create(
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
        driver.get('%s%s' % (self.live_server_url, f"/order/cart/"))
        driver.find_element_by_xpath("//a[@title=\"Prosseguir compra\"]").click()
        address_element = driver.find_element_by_id(address.id)
        address_element.click()
        payment_element = driver.find_element_by_id('C')
        payment_element.click()
        driver.find_element_by_xpath("//button[@title=\"Finalizar compra\"]").click()
        assert 'Defina o valor do troco se for pagar em dinheiro.' in driver.page_source

class OrderTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = None

        if TEST_ON_CHROME:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            cls.selenium = webdriver.Chrome(executable_path=os.getenv('CHROMEDRIVER_PATH'),options=chrome_options)
        elif TEST_ON_FIREFOX:
            cls.selenium = webdriver.Firefox(executable_path = os.getenv('FIREFOXDRIVER_PATH'))

        cls.selenium.get('http://127.0.0.1:8000')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self, user=False):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
        ) if not user else user

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user.email)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys('abcde123456')
        driver.find_element_by_xpath('//input[@value="Entrar"]').click()
        assert 'email ou senha estão incorretos' not in driver.page_source

    def test_view_order(self):
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

        address = Address.objects.create(
            user=user,
            address_type='user',
            zip_code='55370000',
            state='PE',
            city='Garanhuns',
            district='Boa Vista',
            street='Rua rua rua rua',
            house_number=123,
        )

        category = Category.objects.create(
            user=user,
            name='Frutas'
        )

        banana = Product.objects.create(
            user=user,
            name='Banana',
            variety='Prata',
            expiration_days=7,
            stock_amount=50,
            category=category,
        )

        payment = Payment.objects.create(
            type='C', status=0
        )
        order = Order.objects.create(
            status=3, address=address, user=user, payment=payment, total_price=6
        )
        OrderProduct.objects.create(
            quantity=2, product=banana, order=order
        )

        driver = self.selenium
        self.test_login(user)

        driver.get('%s%s' % (self.live_server_url, "/order/order/list"))
        driver.find_element_by_xpath(f"//a[@href=\"/order/order/{order.id}\"]").click()
        assert banana.name in driver.page_source

    def cancel_order(self):
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

        address = Address.objects.create(
            user=user,
            address_type='user',
            zip_code='55370000',
            state='PE',
            city='Garanhuns',
            district='Boa Vista',
            street='Rua rua rua rua',
            house_number=123,
        )

        category = Category.objects.create(
            user=user,
            name='Frutas'
        )

        banana = Product.objects.create(
            user=user,
            name='Banana',
            variety='Prata',
            expiration_days=7,
            stock_amount=50,
            category=category,
        )

        payment = Payment.objects.create(
            type='C', status=0
        )
        order = Order.objects.create(
            status=3, address=address, user=user, payment=payment, total_price=6
        )
        OrderProduct.objects.create(
            quantity=2, product=banana, order=order
        )

        driver = self.selenium
        self.test_login(user)

        driver.get('%s%s' % (self.live_server_url, "/order/list_all_orders/"))
        driver.find_element_by_xpath(f"//button[@data-query=\"order_id={order.id}\"]").click()
        driver.find_element_by_xpath("//button[@class=\"btn btn-danger btn-confirm\"]").click()

        assert 'Cancelado' in driver.page_source


class RatingTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = None

        if TEST_ON_CHROME:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            cls.selenium = webdriver.Chrome(executable_path=os.getenv('CHROMEDRIVER_PATH'),options=chrome_options)
        elif TEST_ON_FIREFOX:
            cls.selenium = webdriver.Firefox(executable_path = os.getenv('FIREFOXDRIVER_PATH'))

        cls.selenium.get('http://127.0.0.1:8000')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self, user=False):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
        ) if not user else user

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user.email)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys('abcde123456')
        driver.find_element_by_xpath('//input[@value="Entrar"]').click()
        assert 'email ou senha estão incorretos' not in driver.page_source

    def test_rate_an_order_with_comment(self):
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

        address = Address.objects.create(
            user=user,
            address_type='user',
            zip_code='55370000',
            state='PE',
            city='Garanhuns',
            district='Boa Vista',
            street='Rua rua rua rua',
            house_number=123,
        )

        category = Category.objects.create(
            user=user,
            name='Frutas'
        )

        banana = Product.objects.create(
            user=user,
            name='Banana',
            variety='Prata',
            expiration_days=7,
            stock_amount=50,
            category=category,
        )

        payment = Payment.objects.create(
            type='C', status=0
        )
        order = Order.objects.create(
            status=3, address=address, user=user, payment=payment, total_price=6
        )
        OrderProduct.objects.create(
            quantity=2, product=banana, order=order
        )

        driver = self.selenium
        self.test_login(user)

        driver.get('%s%s' % (self.live_server_url, "/order/order/list"))
        driver.find_element_by_xpath(f"//a[@href=\"/order/order/{order.id}\"]").click()
        comment_element = driver.find_element_by_xpath("//textarea[@name=\"rate_message\"]")
        comment_element.send_keys('Muito bom!')
        driver.find_element_by_xpath("//input[@id=\"rate-5\"]").click()
        driver.find_element_by_xpath("//button[@title=\"Avaliar\"]").click()
        assert 'Avaliação publicada com sucesso.' in driver.page_source

    def test_rate_an_order_without_comment(self):
        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )
        address = Address.objects.create(
            user=user,
            address_type='user',
            zip_code='55370000',
            state='PE',
            city='Garanhuns',
            district='Boa Vista',
            street='Rua rua rua rua',
            house_number=123,
        )

        category = Category.objects.create(
            user=user,
            name='Frutas'
        )

        banana = Product.objects.create(
            user=user,
            name='Banana',
            variety='Prata',
            expiration_days=7,
            stock_amount=50,
            category=category,
        )

        payment = Payment.objects.create(
            type='C', status=0
        )
        order = Order.objects.create(
            status=3, address=address, user=user, payment=payment, total_price=6
        )
        OrderProduct.objects.create(
            quantity=2, product=banana, order=order
        )

        driver = self.selenium
        self.test_login(user)

        driver.get('%s%s' % (self.live_server_url, "/order/order/list"))
        driver.find_element_by_xpath(f"//a[@href=\"/order/order/{order.id}\"]").click()
        driver.find_element_by_xpath("//input[@id=\"rate-5\"]").click()
        driver.find_element_by_xpath("//button[@title=\"Avaliar\"]").click()
        assert 'Avaliação publicada com sucesso.' in driver.page_source


class AddressTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = None

        if TEST_ON_CHROME:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            cls.selenium = webdriver.Chrome(executable_path=os.getenv('CHROMEDRIVER_PATH'),options=chrome_options)
        elif TEST_ON_FIREFOX:
            cls.selenium = webdriver.Firefox(executable_path = os.getenv('FIREFOXDRIVER_PATH'))

        cls.selenium.get('http://127.0.0.1:8000')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self, user=False):
        user = User.objects.create(
            first_name = 'User',
            email = 'user@gmail.com',
            cpf = '11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin = True
        ) if not user else user

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user.email)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys('abcde123456')
        driver.find_element_by_xpath('//input[@value="Entrar"]').click()
        assert 'email ou senha estão incorretos' not in driver.page_source

    def test_add_address(self):

        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )

        self.test_login(user)

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/address/list"))
        driver.find_element_by_id("add_button").click()

        zip_code = driver.find_element_by_id("id_zip_code")
        zip_code.send_keys('56.640-000')
        driver.find_element_by_xpath("//select[@id='id_state']/option[text()='Pernambuco']").click()
        city = driver.find_element_by_id("id_city")
        city.send_keys('Custódia')
        district = driver.find_element_by_id("id_district")
        district.send_keys('Centro')
        street = driver.find_element_by_id("id_street")
        street.send_keys('Ten Moura')
        house_number = driver.find_element_by_id("id_house_number")
        house_number.send_keys(610)

        driver.find_element_by_id('submit-id-save').click()

        assert '56.640-000' in driver.page_source and '610' in driver.page_source

    def test_add_address_error(self):

        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )

        self.test_login(user)

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/address/list"))
        driver.find_element_by_id("add_button").click()

        zip_code = driver.find_element_by_id("id_zip_code")
        zip_code.send_keys('56.640-000')
        driver.find_element_by_xpath("//select[@id='id_state']/option[text()='Pernambuco']").click()
        city = driver.find_element_by_id("id_city")
        city.send_keys('Custódia')
        district = driver.find_element_by_id("id_district")
        district.send_keys('Centro')
        street = driver.find_element_by_id("id_street")
        street.send_keys('Ten Moura')

        driver.find_element_by_id('submit-id-save').click()

        assert '56.640-000' not in driver.page_source and '610' not in driver.page_source

    def test_remove_address(self):

        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )

        address = Address.objects.create(
            user=user,
            address_type='user',
            zip_code='56640000',
            state='PE',
            city='Custódia',
            district='Centro',
            street='Ten Moura',
            house_number=610,
        )

        self.test_login(user)

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/address/list"))
        driver.find_element_by_id("btn_delete").click()
        driver.find_element_by_xpath("//*[text()='Sim']").click()

        assert '56.640-000' not in driver.page_source and '610' not in driver.page_source

    def test_edit_address(self):

        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )

        address = Address.objects.create(
            user=user,
            address_type='user',
            zip_code='56640000',
            state='PE',
            city='Custódia',
            district='Centro',
            street='Ten Moura',
            house_number=610,
        )

        self.test_login(user)

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/address/list"))
        driver.find_element_by_id("btn_edit").click()

        zip_code = driver.find_element_by_id("id_zip_code")
        zip_code.clear()
        zip_code.send_keys('56.641-000')
        house_number = driver.find_element_by_id("id_house_number")
        house_number.clear()
        house_number.send_keys(611)

        driver.find_element_by_id('submit-id-save').click()

        assert '56.641-000' in driver.page_source and '611' in driver.page_source

    def test_edit_address_error(self):

        user = User.objects.create(
            first_name='User',
            email='user@gmail.com',
            cpf='11111111111',
            password='pbkdf2_sha256$260000$TuHWxP0N32cFSfqCkGVVvl$33dSJ0TKPHQev0weDFHu97mPz8oIPAAdphqDLvo1A3U=',
            is_admin=True
        )

        address = Address.objects.create(
            user=user,
            address_type='user',
            zip_code='56640000',
            state='PE',
            city='Custódia',
            district='Centro',
            street='Ten Moura',
            house_number=610,
        )

        self.test_login(user)

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/user/address/list"))
        driver.find_element_by_id("btn_edit").click()

        zip_code = driver.find_element_by_id("id_zip_code")
        zip_code.clear()
        zip_code.send_keys('56.641-000')
        house_number = driver.find_element_by_id("id_house_number")
        house_number.clear()
        house_number.send_keys(611)

        driver.find_element_by_id('submit-id-save').click()

        assert '56.640-000' not in driver.page_source and '610' not in driver.page_source

