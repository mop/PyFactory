import unittest
import pyfactory
import mock

class Tester(object):
    """This class represents the model class"""
    def __init__(self, **kwargs):
        self.saved   = False
        self.has_put = False
        for key, val in kwargs.items():
            setattr(self, key, val)

    def save(self):
        self.saved = True

    def put(self):
        self.has_put = True

class TestFactory(pyfactory.FactoryObject):
    class Meta:
        name = 'test_object'
        klass = 'tests.test_factory.Tester'

    class Elements:
        first_name = 'the first name'
        last_name  = 'the last name'

def generate_first_name(i):
    return "first name %d" % i

class TestFactoryGenerator(pyfactory.FactoryObject):
    class Meta:
        name = 'test_object_generator'
        klass = 'tests.test_factory.Tester'

    class Elements:
        first_name = pyfactory.Generator(generate_first_name)
        last_name  = 'the last name'

class TestForeignGenerator(pyfactory.FactoryObject):
    class Meta:
        name  = 'test_object_foreign'
        klass = 'tests.test_factory.Tester'
    class Elements:
        first_name = pyfactory.Foreign('test_object')
        last_name  = 'the last name'
    

class FactoryBuildTest(unittest.TestCase):
    def setUp(self):
        self.object = pyfactory.Factory.build('test_object')

    def test_should_set_testers_first_name(self):
        self.assertEqual(self.object.first_name, 'the first name')

    def test_should_set_testers_last_name(self):
        self.assertEqual(self.object.last_name, 'the last name')

    def test_should_not_call_save(self):
        self.assertEqual(self.object.saved, False)

class FactoryAttributeTest(unittest.TestCase):
    def setUp(self):
        self.attributes = pyfactory.Factory.attributes_for('test_object')

    def test_should_return_first_name(self):
        self.assertEqual(self.attributes['first_name'], 'the first name')

    def test_should_return_last_name(self):
        self.assertEqual(self.attributes['last_name'], 'the last name')

class FactoryCreateTest(unittest.TestCase):
    def setUp(self):
        self.object = pyfactory.Factory.create('test_object')

    def test_should_set_testers_first_name(self):
        self.assertEqual(self.object.first_name, 'the first name')

    def test_should_set_testers_last_name(self):
        self.assertEqual(self.object.last_name, 'the last name')

    def test_should_call_save(self):
        self.assertEqual(self.object.saved, True)
        
class FactoryGeneratorAttributeTest(unittest.TestCase):
    def setUp(self):
        self.object1 = pyfactory.Factory.build('test_object_generator')
        self.object2 = pyfactory.Factory.build('test_object_generator')

    def test_should_set_testers_first_name_uniquely(self):
        self.assertNotEqual(self.object1.first_name, self.object2.first_name)

class FactoryGeneratorForeignAttributeTest(unittest.TestCase):
    def setUp(self):
        self.object = pyfactory.Factory.build('test_object_foreign')
        
    def test_should_generate_another_factory_object(self):
        self.assert_(isinstance(self.object.first_name, Tester))

    def test_should_initialize_the_other_factory_correctly(self):
        self.assertEqual(self.object.first_name.first_name, 'the first name')

    def test_should_not_save_the_created_factory(self):
        self.assertEqual(self.object.first_name.saved, False)

class FactoryGeneratorForeignAttributeTypesTest(unittest.TestCase):
    def test_should_save_the_created_object_when_calling_create(self):
        self.object = pyfactory.Factory.create('test_object_foreign')
        self.assertEqual(self.object.first_name.saved, True)

    def test_should_create_attributes_for_object_when_calling_create(self):
        self.object = pyfactory.Factory.attributes_for('test_object_foreign')
        self.assertEqual(
            self.object['first_name']['first_name'], 
            'the first name'
        )

class FactoryOverridingAttributesTest(unittest.TestCase):
    def test_should_override_the_given_attributes_on_build(self):
        self.object = pyfactory.Factory.build(
            'test_object',
            first_name='overridden'
        )
        self.assertEqual(self.object.first_name, 'overridden')

    def test_should_override_the_given_attributes_on_create(self):
        self.object = pyfactory.Factory.create(
            'test_object',
            first_name='overridden'
        )
        self.assertEqual(self.object.first_name, 'overridden')

    def test_should_override_the_given_attributes_on_attributes_for(self):
        self.object = pyfactory.Factory.attributes_for(
            'test_object',
            first_name='overridden'
        )
        self.assertEqual(self.object['first_name'], 'overridden')

class GoogleAppEngineTests(unittest.TestCase):
    def setUp(self):
        pyfactory.type = 'appengine'
        self.result = pyfactory.Factory.create('test_object')

    def test_should_call_put_instead_of_save_on_create(self):
        self.assertFalse(self.result.saved)
        self.assertTrue(self.result.has_put)

if __name__ == '__main__':
    unittest.main()
