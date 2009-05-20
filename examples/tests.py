import pyfactory
import models
from django.test import TestCase

class UserFactory(pyfactory.FactoryObject):
    class Meta:
        klass = 'models.User'
        name  = 'user'
    class Elements:
        name    = 'User1'
        url     = 'http://twitter.com/user1'
        network = 'twitter'

class UserTests(TestCase):
    def setUp(self):
        self.user = pyfactory.Factory.build('user')

    def test_should_have_a_name(self):
        self.assert_(self.user.name != None)
        self.assert_(isinstance(self.user.name, str))

    def test_should_have_a_url(self):
        self.assert_(self.user.url != None)
        self.assert_(isinstance(self.user.url, str))

    def test_should_have_a_network(self):
        self.assert_(self.user.network != None)
        self.assert_(isinstance(self.user.network, str))

    def test_should_save(self):
        self.user.save()
        self.assert_(self.user.id != None)
