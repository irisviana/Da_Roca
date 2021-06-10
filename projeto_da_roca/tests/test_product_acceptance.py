import environ

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from users.models import User
from products.models import Product, Category

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
        self.fruit_category = Category.objects.create(
            name="Fruit")
        apple = Product.objects.create(user=self.producer_rodrigo,
                                       name="apple", variety="test",
                                       expiration_days=10, price=2.0,
                                       stock_amount=50,
                                       category=self.fruit_category)

        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/product/products/list/{apple.id}"))
        driver.find_element_by_xpath(f"//a[@href=\"/product/create/{apple.id}\"]").click()
        driver.find_element_by_xpath("//select[@name='category']/option[text()='Fruit']").click()
        name = driver.find_element_by_name("apple")
        name.send_keys(apple.name)
        variety = driver.find_element_by_name("teste")
        variety.send_keys(apple.variety)
        expiration_days = driver.find_element_by_name(10)
        expiration_days.send_keys(apple.expiration_days)
        price = driver.find_element_by_name(2.0)
        price.send_keys(apple.price)
        stock_amount =  driver.find_element_by_name(10)
        stock_amount.send_keys(apple.stock_amount)
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        assert 'apple' in driver.page_source 

        