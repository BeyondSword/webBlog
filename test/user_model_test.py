"""authetication module unit test"""
import unittest
from app.alchemy_model import User

class UserModelTest(unittest.TestCase):
    """some test about password"""
    def password_setter_test(self):
        """test password setter"""
        user = User(password="cat")
        self.assertTrue(user.password_hash is not None)

    def password_getter_test(self):
        """test password access"""
        user = User(password="dog")
        with self.assertRaises(AttributeError):
            user.password

    def password_verification_test(self):
        """test password auth"""
        user = User(password="dog")
        self.assertTrue(user.verify_password("dog"))
        self.assertFalse(user.verify_password("cat"))

    def password_salts_are_random_test(self):
        """test if same password generated diffrent hash_value"""
        user1 = User(password='dog')
        user2 = User(password='dog')
        self.assertFalse(user1.password_hash, user2.password_hash)
