import environ

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from users.models import User
from products.models import Category, Product

env = environ.Env()

TEST_ON_CHROME = True if env('TEST_ON_CHROME') == 'on' else False
TEST_ON_FIREFOX = True if env('TEST_ON_FIREFOX') == 'on' else False

class ProductsTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.selenium = None
        if TEST_ON_CHROME:
            cls.selenium = webdriver.Chrome(executable_path = env('CHROMEDRIVER_PATH'))
        elif TEST_ON_FIREFOX:
            cls.selenium = webdriver.Firefox(executable_path = env('FIREFOXDRIVER_PATH'))

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
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
            is_admin = True
        ) if not user else user

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(user.email)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys('1234')
        driver.find_element_by_xpath('//input[@value="Entrar"]').click()
        assert 'email ou senha estão incorretos' not in driver.page_source

    def test_register_product_with_all_data_filled_in(self):
        producer_rodrigo = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
            is_seller = True,
        )
        self.test_login(producer_rodrigo)

        fruit_category = Category.objects.create(name="Fruit")

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/product/products/list"))
        driver.find_element_by_xpath("//a[@href=\"/product/create\"]").click()
        driver.find_element_by_xpath(f"//select[@name='category']/option[text()='{fruit_category.name}']").click()
        name = driver.find_element_by_name("name")
        name.send_keys('Apple')
        variety = driver.find_element_by_name("variety")
        variety.send_keys('Normal')
        expiration_days = driver.find_element_by_name('expiration_days')
        expiration_days.send_keys('7')
        price = driver.find_element_by_name('price')
        price.send_keys('1')
        stock_amount =  driver.find_element_by_name('stock_amount')
        stock_amount.send_keys('50')
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        assert 'Apple' in driver.page_source

    def test_register_product_without_some_data(self):
        producer_rodrigo = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
            is_seller = True,
        )
        self.test_login(producer_rodrigo)

        fruit_category = Category.objects.create(name="Fruit")

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, "/product/products/list"))
        driver.find_element_by_xpath("//a[@href=\"/product/create\"]").click()
        driver.find_element_by_xpath(f"//select[@name='category']/option[text()='{fruit_category.name}']").click()
        variety = driver.find_element_by_name("variety")
        variety.send_keys('Normal')
        expiration_days = driver.find_element_by_name('expiration_days')
        expiration_days.send_keys('7')
        price = driver.find_element_by_name('price')
        price.send_keys('1')
        stock_amount =  driver.find_element_by_name('stock_amount')
        stock_amount.send_keys('50')
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        assert 'Cadastre seu produto' in driver.page_source

    def test_visualize_existent_product(self):
        producer_rodrigo = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
            is_seller = True,
        )
        self.test_login(producer_rodrigo)

        fruit_category = Category.objects.create(name="Fruit")
        product = Product.objects.create(user=producer_rodrigo,name="Abacate",expiration_days=2,price=10,category=fruit_category)
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/product/products/view/{product.id}"))
        assert product.name in driver.page_source
    
    def test_visualize_inexistent_product(self):
       
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/product/products/view/{-1}"))
        assert 'teste' not in driver.page_source
