from django.test import TestCase
from users import models

# Create your tests here.

class UsersTest(TestCase):
    """ Test module for User model """

    def setUp(self):
        self.user_rodrigo = models.User.objects.create(
            first_name = "Rodrigo", email = "rodrigo@gmail.com", 
            cpf="70550481419", password="teste")

        self.user_thais = models.User.objects.create(
            first_name = "Thais", email = "thais@gmail.com", 
            cpf="66668592007", password="teste")

    def test_create_client_successfully(self):
        user_iris = models.User.objects.create(
            first_name = "Íris", email = "iris@gmail.com", 
            cpf="82441895095", password="teste")
        self.assertEqual(
             user_iris.cpf,"82441895095")

    def test_create_client_without_cpf(self):
        user_iris=None
        try:
            user_iris = models.User.objects.create(
                first_name = "Íris", email = "iris@gmail.com", 
                cpf=None, password="teste")

        except Exception :
            self.assertIsNone(user_iris)

    def test_update_client_valid_email(self):
        old_email = self.user_thais.email
        self.user_thais.email = "thais@hotmail.com"
        self.user_thais.save()
        self.assertNotEqual(old_email, self.user_thais.email)

    def test_add_admin_permission(self):
        #user inst admin
        self.assertEqual(self.user_rodrigo.is_admin,1)
        self.user_rodrigo.is_admin=0
        self.user_rodrigo.save()
        #user is admin
        self.assertEqual(self.user_rodrigo.is_admin,0)

    def test_add_seller_permission(self):
        #user inst seller
        self.assertEqual(self.user_rodrigo.is_seller,1)
        self.user_rodrigo.is_seller=0
        self.user_rodrigo.save()
        #user is seller
        self.assertEqual(self.user_rodrigo.is_seller,0)
'''
    def test_delete_existent_client(self):
        user_vini = models.User.objects.create(
            first_name = "Vini", email = "vini@gmail.com", 
            cpf="44145114027", password="teste")
        user_vini.delete()
        try:
            user_vini = models.User.objects.get(cpf = "44145114027")
        except Exception :
            self.assertFalse(user_vini)

'''

