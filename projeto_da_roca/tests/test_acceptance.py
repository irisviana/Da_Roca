'''
import environ

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from users.models import User, DeliveryTime, ServiceAddress

env = environ.Env()

TEST_ON_CHROME = True if env('TEST_ON_CHROME') == 'on' else False
TEST_ON_FIREFOX = True if env('TEST_ON_FIREFOX') == 'on' else False

class UsersTest(StaticLiveServerTestCase):

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

    def test_admin_search_user_with_cpf(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
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
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
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
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
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
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
        )

        driver = self.selenium
        self.test_login(user)
        driver = self.selenium
        driver.get('%s%s' % (self.live_server_url, f"/user/{user.username}/update"))
        driver.find_element_by_xpath("//button[@class=\"btn btn-danger\"]").click()
        driver.find_element_by_xpath("//a[@class=\"btn btn-danger btn-confirm\"]").click()
        assert 'Acesso' not in driver.page_source

class DeliveryTimeTest(StaticLiveServerTestCase):

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

    def test_create_delivery_time(self):
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
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
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
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
        
        assert 'Novo horário de entrega' == driver.title

    def test_update_delivery_time(self):
        # Use already created delivery time
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
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
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
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

        # Click edit button to start editing delivery time
        driver.find_element_by_xpath(f"//a[@href=\"/user/delivery_time/update/{delivery_time.id}\"]").click()
        
        # Update fields
        time_input = driver.find_element_by_name("time")
        time_input.send_keys('')
        driver.find_element_by_xpath("//select[@name='day']/option[text()='Sexta-feira']").click()
        driver.find_element_by_xpath("//input[@type=\"submit\"]").click()
        
        assert 'Novo horário de entrega' == driver.title

    def test_delete_delivery_time(self):
        # Use already created delivery time
        user = User.objects.create(
            first_name = 'Iris Viana',
            email = 'iris@gmail.com',
            cpf = '22222222222',
            password = 'pbkdf2_sha256$260000$Sp6bL4xpZQ9iXLHVbpGNHe$QsVBRhxviJntcy4dZuzT0PhiotJ41gCKGTR1yKOJR1s=',
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

'''