import unittest
import factory
import mock

class Tester(object):
    """This class represents the model class"""
    def __init__(self, **kwargs):
        self.saved = False
        for key, val in kwargs.items():
            setattr(self, key, val)

    def save(self):
        self.saved = True

class TestFactory(factory.FactoryObject):
    class Meta:
        name = 'test_object'
        klass = 'tests.Tester'

    class Elements:
        first_name = 'the first name'
        last_name  = 'the last name'

def generate_first_name(i):
    return "first name {num}".format(num=i)

class TestFactoryGenerator(factory.FactoryObject):
    class Meta:
        name = 'test_object_generator'
        klass = 'tests.Tester'

    class Elements:
        first_name = factory.Generator(generate_first_name)
        last_name  = 'the last name'

class TestForeignGenerator(factory.FactoryObject):
    class Meta:
        name  = 'test_object_foreign'
        klass = 'tests.Tester'
    class Elements:
        first_name = factory.Foreign('test_object')
        last_name  = 'the last name'
    

class FactoryBuildTest(unittest.TestCase):
    def setUp(self):
        self.object = factory.Factory.build('test_object')

    def test_should_set_testers_first_name(self):
        self.assertEqual(self.object.first_name, 'the first name')

    def test_should_set_testers_last_name(self):
        self.assertEqual(self.object.last_name, 'the last name')

    def test_should_not_call_save(self):
        self.assertEqual(self.object.saved, False)

class FactoryAttributeTest(unittest.TestCase):
    def setUp(self):
        self.attributes = factory.Factory.attributes_for('test_object')

    def test_should_return_first_name(self):
        self.assertEqual(self.attributes['first_name'], 'the first name')

    def test_should_return_last_name(self):
        self.assertEqual(self.attributes['last_name'], 'the last name')

class FactoryCreateTest(unittest.TestCase):
    def setUp(self):
        self.object = factory.Factory.create('test_object')

    def test_should_set_testers_first_name(self):
        self.assertEqual(self.object.first_name, 'the first name')

    def test_should_set_testers_last_name(self):
        self.assertEqual(self.object.last_name, 'the last name')

    def test_should_call_save(self):
        self.assertEqual(self.object.saved, True)
        
class FactoryGeneratorAttributeTest(unittest.TestCase):
    def setUp(self):
        self.object1 = factory.Factory.build('test_object_generator')
        self.object2 = factory.Factory.build('test_object_generator')

    def test_should_set_testers_first_name_uniquely(self):
        self.assertEqual(self.object1.first_name, 'first name 1')
        self.assertEqual(self.object2.first_name, 'first name 2')

class FactoryGeneratorForeignAttributeTest(unittest.TestCase):
    def setUp(self):
        self.object = factory.Factory.build('test_object_foreign')
        
    def test_should_generate_another_factory_object(self):
        self.assert_(isinstance(self.object.first_name, Tester))

    def test_should_initialize_the_other_factory_correctly(self):
        self.assertEqual(self.object.first_name.first_name, 'the first name')

    def test_should_not_save_the_created_factory(self):
        self.assertEqual(self.object.first_name.saved, False)

if __name__ == '__main__':
    unittest.main()
